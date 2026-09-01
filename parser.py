#!/usr/bin/env python3
"""Parse a SaaS pricing-page HTML in a Solari sandbox and emit CSV/JSON.

The input HTML path and CSS-style class selectors are passed via environment
variables so the same parser can be reused across different pricing pages.
"""

import csv
import json
import os
import re
from html.parser import HTMLParser
from typing import Any

VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}

PRICE_RE = re.compile(
    r"(\$\s*\d[\d,\.]*(?:\.\d+)?\s*(?:/\s*(?:month|year|user\s*/\s*month|member\s*/\s*month|mo))?|Custom(?:\s*pricing)?)\b",
    re.IGNORECASE,
)


class Tag:
    """Tiny DOM node for local HTML parsing."""

    def __init__(self, name: str | None, attrs: dict[str, str | None]) -> None:
        self.name = name
        self.attrs = {k: (v or "") for k, v in attrs.items()}
        self.classes = set((self.attrs.get("class") or "").split())
        self.children: list[Any] = []
        self.parent: "Tag | None" = None

    def find(self, *, name: str | None = None, class_: str | None = None) -> "Tag | None":
        if self._matches(name, class_):
            return self
        for child in self.children:
            if isinstance(child, Tag):
                found = child.find(name=name, class_=class_)
                if found is not None:
                    return found
        return None

    def find_all(self, *, name: str | None = None, class_: str | None = None) -> list["Tag"]:
        results: list[Tag] = []
        if self._matches(name, class_):
            results.append(self)
        for child in self.children:
            if isinstance(child, Tag):
                results.extend(child.find_all(name=name, class_=class_))
        return results

    def _matches(self, name: str | None, class_: str | None) -> bool:
        name_ok = name is None or self.name == name
        class_ok = class_ is None or class_ in self.classes
        return name_ok and class_ok

    def get_text(self, sep: str = " ") -> str:
        parts = []
        for child in self.children:
            if isinstance(child, str):
                parts.append(child)
            elif isinstance(child, Tag) and child.name not in ("script", "style"):
                parts.append(child.get_text(sep))
        text = sep.join(parts)
        text = re.sub(r"\s+", " ", text)
        return text.strip()


class SimpleSoup(HTMLParser):
    """Builds a lightweight tree from raw HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.root = Tag(None, {})
        self._stack: list[Tag] = [self.root]

    def handle_starttag(self, name: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = {k: v for k, v in attrs}
        node = Tag(name, attrs_map)
        node.parent = self._stack[-1]
        self._stack[-1].children.append(node)
        if name not in VOID_TAGS:
            self._stack.append(node)

    def handle_endtag(self, name: str) -> None:
        if len(self._stack) > 1 and self._stack[-1].name == name:
            self._stack.pop()

    def handle_data(self, data: str) -> None:
        if self._stack[-1].name in ("script", "style"):
            return
        self._stack[-1].children.append(data)


def _text(node: Tag | None) -> str:
    if node is None:
        return ""
    return node.get_text()


def _normalize(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip()


def _extract_price(container: Tag, exclude: str = "") -> str:
    """Find the first price-looking string in a card, ignoring list items."""
    for tag in container.find_all():
        if tag.name in ("li", "ul", "ol") or tag.name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            continue
        text = tag.get_text()
        if text == exclude:
            continue
        m = PRICE_RE.search(text)
        if m:
            return _normalize(m.group(1))
    return ""


def _extract_features(container: Tag) -> list[str]:
    features: list[str] = []
    for ul in container.find_all(name="ul"):
        for li in ul.find_all(name="li"):
            text = _text(li)
            if text:
                features.append(text)
    if not features:
        for li in container.find_all(name="li"):
            text = _text(li)
            if text:
                features.append(text)
    return features


def _extract_description(container: Tag, plan: str, price: str) -> str:
    """Return the first short paragraph that is not the plan name or price."""
    for tag in container.find_all():
        if tag.name not in ("p", "div"):
            continue
        text = _text(tag)
        if text == plan or text == price:
            continue
        if len(text) > 200:
            continue
        if PRICE_RE.search(text):
            continue
        if text:
            return text
    return ""


def parse_card(html: str, config: dict[str, str], site: str = "") -> list[dict[str, Any]]:
    soup = SimpleSoup()
    soup.feed(html)
    root = soup.root

    cards = root.find_all(class_=config["card"])
    plans: list[dict[str, Any]] = []

    for card in cards:
        name = _text(card.find(class_=config["name"]))
        price = _text(card.find(class_=config["price"]))
        suffix = _text(card.find(class_=config["suffix"]))
        description = _text(card.find(class_=config["description"]))

        full_price = f"{price} {suffix}".strip()

        features = [
            _text(f)
            for f in card.find_all(class_=config["features"])
        ]
        if not features:
            features = [_text(li) for li in card.find_all(name="li")]

        if not name:
            continue

        plans.append(
            {
                "site": site,
                "plan": name,
                "price": full_price,
                "description": description,
                "features": features,
            }
        )

    return plans


def parse_heading(html: str, config: dict[str, str], site: str) -> list[dict[str, Any]]:
    """Generic card extraction using h2/h3 headings and a price/features heuristic."""
    soup = SimpleSoup()
    soup.feed(html)
    root = soup.root

    heading_tags = [t.strip() for t in config.get("heading", "h2,h3").split(",")]
    headings: list[Tag] = []
    for tag in heading_tags:
        headings.extend(root.find_all(name=tag))

    seen: set[str] = set()
    plans: list[dict[str, Any]] = []

    for heading in headings:
        name = _normalize(heading.get_text())
        if not name or name in seen:
            continue

        card: Tag | None = heading.parent
        price = ""
        features: list[str] = []
        while card is not None and card.name not in ("body", "html", "main"):
            price = _extract_price(card, exclude=name)
            features = _extract_features(card)
            if card.name in ("div", "section", "article") and price and features:
                break
            card = card.parent

        if not card or not price or not features or len(features) > 20:
            continue

        description = _extract_description(card, name, price)

        seen.add(name)
        plans.append(
            {
                "site": site,
                "plan": name,
                "price": price,
                "description": description,
                "features": features,
            }
        )

    return plans


# Backwards-compatible alias used by tests.
parse = parse_card


def _load_config() -> dict[str, str]:
    mode = os.environ.get("PARSER_MODE", "card").lower()
    if mode == "heading":
        return {
            "mode": "heading",
            "heading": os.environ.get("HEADING_TAGS", "h2,h3"),
        }
    return {
        "mode": "card",
        "card": os.environ.get("CARD_CLASS", "solari-pricing-plan"),
        "name": os.environ.get("NAME_CLASS", "solari-pricing-plan-name"),
        "price": os.environ.get("PRICE_CLASS", "solari-pricing-price-value"),
        "suffix": os.environ.get("SUFFIX_CLASS", "solari-pricing-price-suffix"),
        "description": os.environ.get(
            "DESCRIPTION_CLASS", "solari-pricing-description"
        ),
        "features": os.environ.get("FEATURES_CLASS", "solari-pricing-feature"),
    }


def main() -> None:
    html_path = os.environ.get("PRICING_HTML_PATH", "/tmp/pricing.html")
    csv_path = os.environ.get("PRICING_CSV_PATH", "/tmp/pricing.csv")
    json_path = os.environ.get("PRICING_JSON_PATH", "/tmp/pricing.json")
    site = os.environ.get("SITE_NAME", "unknown")

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    config = _load_config()
    if config["mode"] == "heading":
        plans = parse_heading(html, config, site)
    else:
        plans = parse_card(html, config, site)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["site", "plan", "price", "description", "features"]
        )
        writer.writeheader()
        for plan in plans:
            row = dict(plan)
            row["features"] = " | ".join(plan["features"])
            writer.writerow(row)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"plans": plans, "site": site}, f, indent=2)

    print(f"WROTE {{'csv': '{csv_path}', 'json': '{json_path}', 'plans': {len(plans)}, 'site': '{site}'}}")


if __name__ == "__main__":
    main()

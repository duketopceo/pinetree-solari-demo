"""Pricing reporter — collect pricing pages from several SaaS sites in a
Solari browser, parse each one in a Solari sandbox, and write a combined
CSV and JSON on the host.
"""

import asyncio
import csv
import json
import os
import sys
from pathlib import Path
from typing import Any

from solari_browser import Solari
from solari_sandbox import SandboxClient

DEFAULT_BASE_URL = "https://api.getsolari.com"
PARSER_SCRIPT = Path(__file__).with_name("parser.py")
SITES_FILE = Path("sites.json")


def _load_sites() -> list[dict[str, Any]]:
    path = Path(os.environ.get("SITES_FILE", SITES_FILE))
    if not path.is_file():
        print(f"error: sites config not found: {path}", file=sys.stderr)
        sys.exit(1)
    raw = path.read_text(encoding="utf-8")
    try:
        sites = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"error: invalid sites JSON: {exc}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(sites, list) or not sites:
        print("error: sites.json must be a non-empty list", file=sys.stderr)
        sys.exit(1)
    return sites


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        print(f"error: {name} is required. See .env.example", file=sys.stderr)
        sys.exit(1)
    return value


def _env_for_site(site: dict[str, Any]) -> dict[str, str]:
    env = {
        "SITE_NAME": site["site"],
        "PARSER_MODE": site.get("mode", "card"),
        "PRICING_HTML_PATH": f"/tmp/{site['site']}.html",
        "PRICING_CSV_PATH": f"/tmp/{site['site']}.csv",
        "PRICING_JSON_PATH": f"/tmp/{site['site']}.json",
    }
    if env["PARSER_MODE"] == "heading":
        env["HEADING_TAGS"] = site.get("heading_tags", "h2,h3")
    else:
        for key in (
            "card_class",
            "name_class",
            "price_class",
            "suffix_class",
            "description_class",
            "features_class",
        ):
            env_key = key.upper()
            env[env_key] = site.get(key, os.environ.get(env_key, ""))
    return env


async def _process_site(
    page,
    sandbox,
    site: dict[str, Any],
) -> list[dict[str, Any]]:
    name = site["site"]
    url = site["url"]

    print(f"[{name}] loading {url}")
    await page.goto(url)
    await page.wait_for_load_state("networkidle")

    title = await page.title()
    print(f"[{name}] title: {title}")

    html = await page.content()
    html_path = f"/tmp/{name}.html"
    await sandbox.files.upload(html_path, html)

    parser_env = _env_for_site(site)
    await sandbox.env(parser_env)

    result = await sandbox.commands.run(
        "python3", args=["/tmp/parser.py"], timeout_ms=120_000
    )
    if result.exitCode != 0:
        print(f"[{name}] parser stderr: {result.stderr}", file=sys.stderr)
        raise RuntimeError(f"{name} parser failed with exit code {result.exitCode}")

    print(result.stdout.strip())

    json_bytes = await sandbox.files.download(f"/tmp/{name}.json")

    data = json.loads(json_bytes.decode("utf-8"))
    return data.get("plans", [])


def _write_combined(plans: list[dict[str, Any]]) -> None:
    output_csv = os.environ.get("OUTPUT_CSV", "pricing.csv")
    output_json = os.environ.get("OUTPUT_JSON", "pricing.json")

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump({"plans": plans}, f, indent=2)

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["site", "plan", "price", "description", "features"]
        )
        writer.writeheader()
        for plan in plans:
            row = dict(plan)
            row["features"] = " | ".join(plan["features"])
            writer.writerow(row)

    print(f"wrote {output_csv} and {output_json}")


async def main() -> None:
    api_key = _require_env("SOLARI_API_KEY")
    base_url = os.environ.get("SOLARI_BASE_URL", DEFAULT_BASE_URL)
    sites = _load_sites()

    if not PARSER_SCRIPT.is_file():
        print(f"error: parser script not found: {PARSER_SCRIPT}", file=sys.stderr)
        sys.exit(1)

    solari: Solari | None = None
    browser = None
    sandbox = None
    sb_client = SandboxClient(api_key=api_key, base_url=base_url)

    all_plans: list[dict[str, Any]] = []

    try:
        solari = Solari(api_key=api_key)
        browser = await solari.launch()
        sandbox = await sb_client.create(template="base")
        await sandbox.connect()

        parser_code = PARSER_SCRIPT.read_text(encoding="utf-8")
        await sandbox.files.upload("/tmp/parser.py", parser_code)

        page = await browser.new_page()

        for site in sites:
            try:
                plans = await _process_site(page, sandbox, site)
                all_plans.extend(plans)
            except Exception as exc:
                print(f"[{site['site']}] failed: {exc}", file=sys.stderr)

        _write_combined(all_plans)
    finally:
        if sandbox is not None:
            try:
                await sandbox.kill()
            except Exception:
                pass
            try:
                await sandbox.close()
            except Exception:
                pass
        if browser is not None:
            try:
                await browser.close()
            except Exception:
                pass
        if solari is not None:
            try:
                await solari.close()
            except Exception:
                pass
        await sb_client.aclose()


if __name__ == "__main__":
    asyncio.run(main())

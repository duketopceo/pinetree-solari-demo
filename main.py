"""Pricing reporter — collect a pricing page in a Solari browser,
parse it in a Solari sandbox, and write CSV/JSON on the host.

This demonstrates a real web-data-extraction pipeline across two Solari
primitives: cloud browser and headless sandbox.
"""

import asyncio
import os
import sys
from pathlib import Path

from solari_browser import Solari
from solari_sandbox import SandboxClient

DEFAULT_TARGET = "https://getsolari.com/pricing"
DEFAULT_BASE_URL = "https://api.getsolari.com"
PARSER_SCRIPT = Path(__file__).with_name("parser.py")


def _class_env(prefix: str, default: str) -> str:
    return os.environ.get(prefix, default)


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        print(f"error: {name} is required. See .env.example", file=sys.stderr)
        sys.exit(1)
    return value


async def main() -> None:
    api_key = _require_env("SOLARI_API_KEY")
    base_url = os.environ.get("SOLARI_BASE_URL", DEFAULT_BASE_URL)
    target_url = os.environ.get("TARGET_URL", DEFAULT_TARGET)
    output_csv = os.environ.get("OUTPUT_CSV", "pricing.csv")
    output_json = os.environ.get("OUTPUT_JSON", "pricing.json")

    card_class = _class_env("CARD_CLASS", "solari-pricing-plan")
    name_class = _class_env("NAME_CLASS", "solari-pricing-plan-name")
    price_class = _class_env("PRICE_CLASS", "solari-pricing-price-value")
    suffix_class = _class_env("SUFFIX_CLASS", "solari-pricing-price-suffix")
    description_class = _class_env("DESCRIPTION_CLASS", "solari-pricing-description")
    features_class = _class_env("FEATURES_CLASS", "solari-pricing-feature")

    if not PARSER_SCRIPT.is_file():
        print(f"error: parser script not found: {PARSER_SCRIPT}", file=sys.stderr)
        sys.exit(1)

    solari: Solari | None = None
    browser = None
    sandbox = None
    sb_client = SandboxClient(api_key=api_key, base_url=base_url)

    try:
        solari = Solari(api_key=api_key)
        browser = await solari.launch()
        page = await browser.new_page()
        await page.goto(target_url)
        await page.wait_for_load_state("networkidle")

        title = await page.title()
        print(f"loaded: {title}")

        html = await page.content()

        sandbox = await sb_client.create(template="base")
        await sandbox.connect()

        parser_code = PARSER_SCRIPT.read_text(encoding="utf-8")

        await sandbox.files.upload("/tmp/parser.py", parser_code)
        await sandbox.files.upload("/tmp/pricing.html", html)

        await sandbox.env(
            {
                "CARD_CLASS": card_class,
                "NAME_CLASS": name_class,
                "PRICE_CLASS": price_class,
                "SUFFIX_CLASS": suffix_class,
                "DESCRIPTION_CLASS": description_class,
                "FEATURES_CLASS": features_class,
                "PRICING_HTML_PATH": "/tmp/pricing.html",
                "PRICING_CSV_PATH": "/tmp/pricing.csv",
                "PRICING_JSON_PATH": "/tmp/pricing.json",
            }
        )

        result = await sandbox.commands.run(
            "python3", args=["/tmp/parser.py"], timeout_ms=120_000
        )
        if result.exitCode != 0:
            print("sandbox parser stderr:", result.stderr, file=sys.stderr)
            raise RuntimeError(f"sandbox parser failed with exit code {result.exitCode}")

        print(result.stdout.strip())

        csv_bytes = await sandbox.files.download("/tmp/pricing.csv")
        json_bytes = await sandbox.files.download("/tmp/pricing.json")

        Path(output_csv).write_bytes(csv_bytes)
        Path(output_json).write_bytes(json_bytes)

        print(f"wrote {output_csv} and {output_json}")
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

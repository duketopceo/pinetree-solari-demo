# Solari Browser + Sandbox Pricing Reporter

## Problem frame

`solari-cookbook` has separate browser and sandbox examples, but no end-to-end example of a real data pipeline that combines them. Solari's own use-case list explicitly includes **Web Data Extraction Pipeline**. A pricing reporter shows a complete browser → sandbox → structured output flow, which is the kind of product-shaped build Pinetree wants to see from a SWE intern candidate.

## Feature

A self-contained Python example that:

1. Uses `solari-browser` to load a SaaS pricing page and capture its rendered HTML.
2. Starts a `solari-sandbox`, uploads the HTML and a small parser script, and runs it.
3. The parser extracts plan names, prices, descriptions, and feature lists into JSON.
4. The host writes `pricing.csv` from the parsed JSON.

## Scope

**In scope**
- One browser session, one sandbox, one target URL.
- Local CSV output.
- README, `.env.example`, and a minimal parser unit test.

**Out of scope**
- Stealth, proxies, captcha, persistent profiles, desktop, LLM summarization, deployment, CI.

## Repo files

- `reporter.py` — main orchestration: browser → sandbox → CSV.
- `parser.py` — sandbox-side HTML parser.
- `requirements.txt` — `solari-browser`, `solari-sandbox`, `beautifulsoup4`.
- `.env.example` — `SOLARI_API_KEY`, `TARGET_URL`.
- `README.md` — setup, run, output, and how it maps to Solari's use cases.
- `tests/test_parser.py` — unit test the parser against a local HTML fixture.

## Acceptance criteria

- `reporter.py` runs end-to-end on a free-tier key without exceeding 1-hour session or sandbox limits.
- `pricing.csv` has columns: `plan`, `price`, `description`, `features`.
- README explains the pipeline and links to `docs.getsolari.com/use-cases`.
- No real API keys in git.

## Test scenarios

- Happy path: target `https://getsolari.com/pricing` returns one or more rows.
- Override: `PRICING_CARD_SELECTOR` env var changes the parsed HTML.
- Resilience: parser handles missing or empty fields without crashing.
- Resource: browser and sandbox are both closed so the free-tier limits are not exhausted.

## Risks / assumptions

- Assumes the target pricing page DOM is stable. Selectors can be overridden via env.
- Free plan allows only 1 sandbox and 3 concurrent browsers; the reporter must close sessions cleanly.
- `solari-sandbox` is available on PyPI and uses the same `slr_live_…` key.

## Upstream destination

This will be contributed to `solari-cookbook` as `examples/browser-sandbox-pricing-reporter-py/`.

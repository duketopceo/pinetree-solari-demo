# pinetree-solari-demo

A real Solari use case built for the Pinetree Research SWE intern application.

It shows a multi-URL browser-to-sandbox pipeline that collects live SaaS pricing
pages, parses each one in an isolated headless sandbox, and writes a combined
CSV and JSON on the host.

## What it demonstrates

1. **Cloud browser** — a single Solari browser loads each configured pricing
   page one after another.
2. **Headless sandbox** — each page's HTML and a shared parser are uploaded to
   a sandbox, which extracts tiered plans.
3. **Two parsing modes** — a class-based mode for modern React pricing cards and
   a heading-based heuristic mode for conventional pricing pages.
4. **Combined output** — the host merges all per-site `pricing.csv`/`pricing.json`
   files into a single `pricing.csv` and `pricing.json`.

## Live run output

A verified run collected Solari and Linear pricing on the Solari Free plan. The
combined result is in `OUTPUTS.md` and in this repository:

- `pricing.csv` — spreadsheet-ready, features joined with ` | `
- `pricing.json` — structured, features as arrays

![run output](assets/run-screenshot.png)

## Stack

- Python 3.11+
- `solari-browser`
- `solari-sandbox`
- Pure standard-library HTML parser (`html.parser`)

## Local setup

```bash
git clone https://github.com/duketopceo/pinetree-solari-demo
cd pinetree-solari-demo
pip install -r requirements.txt
cp .env.example .env
# fill in .env
python main.py
```

## Sites

Targets are configured in `sites.json`. Each entry can use either `"mode": "card"`
with CSS class selectors or `"mode": "heading"` for a generic `h2`/`h3` + price
+ list-item heuristic.

## Tests

The parser is tested locally against sample HTML, no Solari API key needed:

```bash
python -m unittest discover tests
```

## Cost

Designed for the Solari Free plan. One browser session and one sandbox are
started, used for all sites, then released before the script exits.

## Upstream contribution

The simpler single-site example is proposed to the official Solari cookbook:
https://github.com/solari-sdk/solari-cookbook/pull/3

## License

MIT

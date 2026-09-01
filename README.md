# pinetree-solari-demo

A real Solari use case built for the Pinetree Research SWE intern application.

It shows a browser-to-sandbox pipeline that collects a live SaaS pricing page,
parses the rendered HTML in an isolated headless sandbox, and exports the
extracted plans to CSV and JSON.

## What it demonstrates

1. **Cloud browser** — loads `https://getsolari.com/pricing`, waits for it to
   render, and captures the full HTML.
2. **Headless sandbox** — receives the HTML and a small parser, then runs the
   parser in an isolated Linux microVM.
3. **Clean output** — the host downloads `pricing.csv` and `pricing.json`.

The example intentionally uses two Solari primitives together to show how a
browser and sandbox can be chained in a real data-extraction workflow.

## Live run output

A verified run against `https://getsolari.com/pricing` extracted all 4 Solari
plans. The captured output is stored in `OUTPUTS.md` and in this repository:

- `pricing.csv` — spreadsheet-ready, features joined with ` | `
- `pricing.json` — structured, features as arrays

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

## Tests

The parser is tested locally against sample HTML, no Solari API key needed:

```bash
python -m unittest discover tests
```

## Cost

Designed for the Solari Free plan. Each run uses one browser session and one
sandbox; both are released before the script exits.

## Upstream contribution

The same example is proposed to the official Solari cookbook:
https://github.com/solari-sdk/solari-cookbook/pull/3

## License

MIT

# pinetree-solari-demo

> Pinetree SWE intern application: a real Solari use case that collects a SaaS pricing page with a cloud browser, parses it in a headless sandbox, and exports the results to CSV and JSON.

## What it does

`main.py` runs a two-stage pipeline:

1. **Browser** — launch a Solari cloud browser, navigate to the target pricing
   page, and collect the full rendered HTML.
2. **Sandbox** — upload the HTML and `parser.py` to a Solari sandbox, run the
   parser to extract tiered plan data, then download `pricing.csv` and
   `pricing.json` back to the host.

Both the browser and sandbox sessions are cleaned up in `finally` blocks so
free-tier concurrency is not left holding.

The target URL and class selectors are configurable via environment variables,
so the same script can be pointed at any SaaS pricing page.

## Stack

- Python 3.11+
- `solari-browser`
- `solari-sandbox`
- Pure-stdlib HTML parser (`html.parser`)

## Local Setup

```bash
# clone
git clone https://github.com/duketopceo/pinetree-solari-demo
cd pinetree-solari-demo

# install deps
pip install -r requirements.txt

# env vars
cp .env.example .env
# fill in .env

# run
python main.py
```

## Tests

The parser is exercised with a local sample HTML so the core extraction logic
is tested without needing a Solari API key:

```bash
python -m unittest discover tests
```

## Cost

Designed for the Solari **Free** plan. On that plan each run uses one browser
session and one sandbox, both of which are released before the script exits.

## Docs

- See `AGENTS.md` for agent context.

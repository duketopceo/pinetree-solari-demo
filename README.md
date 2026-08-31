# pinetree

> Pinetree SWE intern application: a real Solari use case that extracts a SaaS pricing page and exports the results to CSV.

## What it does

`main.py` launches a Solari cloud browser, navigates to the target pricing page,
waits for the plan cards to render, and extracts each tier's name, price,
description, and bullet features into `pricing.csv`.

The target URL and CSS selectors are configurable via environment variables, so
the same script can be pointed at any SaaS pricing page.

## Stack
- Python 3.11+
- Solari cloud browser SDK
- Playwright (via Solari)

## Local Setup
```bash
# clone
git clone https://github.com/duketopceo/pinetree
cd pinetree

# install deps
pip install -r requirements.txt

# env vars
cp .env.example .env
# fill in .env

# run
python main.py
```

## Deploy
Manual; run locally with a Solari API key.

## Docs
- See `AGENTS.md` for agent context.

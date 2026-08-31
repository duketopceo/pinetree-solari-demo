# pinetree

> Pinetree SWE intern application: a real Solari use case that extracts a SaaS pricing page and exports the results to CSV.

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

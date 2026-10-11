# AGENTS.md — pinetree-solari-demo

> This file is the agent entry point for this repo.
> Full agent context lives at: https://github.com/duketopceo/luke-agents

## What This Repo Does

A real use case built with Solari for the Pinetree SWE intern application: a cloud browser plus headless sandbox pipeline that visits every pricing page listed in `sites.json` (currently Solari and Linear), parses each one in an isolated sandbox using a card-class or heading-based parser, and merges the results into one `pricing.csv` and `pricing.json`.

## Key Files

- `main.py` — multi-URL pricing reporter entry point (one browser session, one sandbox)
- `parser.py` — in-sandbox HTML-to-CSV/JSON parser (`card` and `heading` modes)
- `sites.json` — target URLs and per-site parser mode
- `pricing.csv` / `pricing.json` / `OUTPUTS.md` — committed output from a verified live run
- `tests/test_parser.py` — local parser tests
- `requirements.txt` — Python dependencies
- `.env.example` — env var template

## Current Status

- [x] Shipped as a demo (verified live run on the Solari Free plan; outputs committed)
- [x] Parser tests run in CI (`python -m unittest discover -s tests`)
- [ ] Not a deployed service; it runs locally on demand

## Active Issues / Known State

Built as a demo for the Pinetree Research SWE intern application. The single-site example is proposed upstream in solari-sdk/solari-cookbook PR #3.

## Agent Instructions (repo-specific)

- Default: follow `duketopceo/luke-agents` for all standards.
- Do not commit `.env` or real API keys.


## Code graph index (optional accelerator)

This repo may be indexed by `codebase-memory-mcp` (CBM) on an agent's local
machine — `.codebase-memory/` is gitignored. If your harness exposes CBM
tools (`search_graph`, `trace_path`, `get_architecture`, `detect_changes`),
prefer them for structural questions — symbol lookup, caller/callee traces,
impact analysis — instead of grep/read loops. Reindex after large refactors
(`index_repository`); treat `.codebase-memory/graph.db.zst` as a local cache
artifact, never commit it.

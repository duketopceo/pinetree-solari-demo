# AGENTS.md — pinetree-solari-demo

> This file is the agent entry point for this repo.
> Full agent context lives at: https://github.com/duketopceo/luke-agents

## What This Repo Does

A real use case built with Solari for the Pinetree SWE intern application: a cloud browser plus headless sandbox pipeline that collects a SaaS pricing page, parses it in an isolated sandbox, and writes structured CSV/JSON.

## Key Files

- `main.py` — pricing reporter entry point
- `parser.py` — in-sandbox HTML-to-CSV/JSON parser
- `tests/test_parser.py` — local parser tests
- `requirements.txt` — Python dependencies
- `.env.example` — env var template

## Current Status

- [x] In development
- [ ] Deployed
- [ ] Production traffic

## Active Issues / Known State

Built as a demo for the Pinetree $300K SWE intern application.

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

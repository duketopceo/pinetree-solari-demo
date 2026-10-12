# Roadmap

Program plan, 2026-10-10. Scale: tiny demo repo. Status values: todo / done. Evidence is from the code in this repo.

## Now

### U1. Fix README claims and layout (done in this PR)
- Status: done. Evidence: README rewritten; every statement checked against `main.py`, `parser.py`, `sites.json`.
- Difficulty: easy. Docs only.
- Feasibility: no blockers.
- Simpler alternative: none; delete the duplicate "live output" description between README and `OUTPUTS.md` (done by linking).
- Verification: `python -m unittest discover -s tests` exits 0.

### U2. Non-zero exit when every site fails
- Status: todo. Evidence: `main.py` catches each site exception, logs it, then `_write_combined` still writes a header-only CSV and `{"plans": []}`, and the process exits 0.
- Difficulty: easy. A few lines in `main()` after the loop.
- Feasibility: none; no live API needed to unit-test if `_write_combined` logic is split out.
- Simpler alternative: only exit non-zero when `all_plans` is empty; skip any per-site retry logic.
- Verification: unit test on the combined-write path.

## Next

### U3. Strip the leading `+ ` from feature text
- Status: todo. Evidence: `pricing.csv` features read `+ Included credits ...`.
- Difficulty: easy. Likely in `_extract_features` in `parser.py` (needs a fixture to confirm whether the `+` comes from an icon element).
- Feasibility: depends on the live page markup, which may change.
- Simpler alternative: strip in the host when writing, in `_write_combined`, instead of touching the parser.
- Verification: add a parser test with a feature `<li>` that includes the glyph.

### U4. More parser tests (heading mode, empty page, Custom price)
- Status: todo. Evidence: `tests/test_parser.py` has 2 tests, both card mode.
- Difficulty: easy.
- Feasibility: none; stdlib unittest.
- Simpler alternative: one table-driven test over small fixtures.
- Verification: CI (`.github/workflows/ci.yml`) runs them on push and PR.

## Later

### U5. Run parser on the host with a `--local` flag
- Status: todo. Evidence: `parser.py` is stdlib-only and already unit-tested locally, so the sandbox hop is only needed for the demo.
- Difficulty: medium. Needs main.py to import `parser` and branch on a flag; env-var plumbing in `_env_for_site` / `parser._load_config` would be replaced by a dict.
- Feasibility: none, but it weakens the demo's purpose; keep sandbox as the default.
- Simpler alternative: leave as is and delete nothing; if pursued, remove `_env_for_site` env round trip by passing a config dict.
- Verification: output identical for a saved HTML fixture in both paths.

### U6. Output schema doc and `--sites` CLI arg
- Status: todo. Evidence: `SITES_FILE`, `OUTPUT_CSV`, `OUTPUT_JSON` are env-only and undocumented in `.env.example` and README.
- Difficulty: easy.
- Feasibility: none.
- Simpler alternative: document the env vars in README (done in this PR) and skip the CLI.
- Verification: README matches `os.environ.get` calls.

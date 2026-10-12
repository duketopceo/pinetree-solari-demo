# DESIGN

Direction: **Pine Ledger**. A plain-text, ledger-like look: monospace, flat green-on-paper colour, no decoration. It fits a small data tool whose real product is a CSV/JSON file.

## Surfaces

1. `README.md` (the main surface).
2. `pricing.csv` / `pricing.json` output files.
3. Console output of `python main.py` (lines of the form `[site] loading URL`).
4. `assets/demo-screenshot.html` / `social-screenshot.png` (a dark terminal-style card; existing, left unchanged).

There is no web UI or TUI.

## Reference lock and decisions

No live reference tool was used (Refero MCP not configured here; `refero-design` skipped, method applied by hand). References: GitHub's own README rendering (the constraint), and plain-text ledger/CLI conventions (e.g. `git` and `pytest` output: one prefixed line per event, no colour required).

| Decision | Choice | Why |
|---|---|---|
| Type | Monospace for mark and wordmark; README uses GitHub default | Data is tabular text; no custom fonts possible on GitHub |
| Glyph | Single pine mark with price-tag hole | Pinetree + price data |
| Motion | None | Static docs and CLI |
| Console | Keep `[site] message` prefix; errors to stderr, no ANSI | Pipe-safe |
| Data | Keep CSV column order `site,plan,price,description,features` | Stable for spreadsheets |

## Tokens (WCAG contrast measured against the background)

| Token | Light | Dark |
|---|---|---|
| background | `#F6F8F4` | `#0E1512` |
| ink | `#14231C` (15.27:1) | `#E4EEE7` (15.58:1) |
| accent | `#1F5A41` (7.57:1) | `#6FCF9A` (9.75:1) |
| muted | `#5B6B62` (5.28:1) | `#93A39A` (7.00:1) |

All pass AA for body text.

## Known audit findings (not fixed in this docs-only pass)

- CSV feature cells carry a leading `+ ` taken from the page markup (see `pricing.csv`); a cleanup belongs in `parser.py` (see ROADMAP U3).
- `assets/demo-screenshot.html` uses its own palette (`#38bdf8` accent) unrelated to this direction; left as is.

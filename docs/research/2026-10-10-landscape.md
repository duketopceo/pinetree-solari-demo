# Landscape: SaaS pricing-page extraction

Scope: this repo is a small demo (`main.py`, `parser.py`, `sites.json`) that loads pricing pages in a Solari cloud browser, parses them in a Solari sandbox with a stdlib `html.parser` tree, and writes `pricing.csv` / `pricing.json`. Research is deliberately short; one search was run, and vendor pages are marketing, so claims are limited to what they state.

## Comparable tools

| Tool | What it does | Source |
|---|---|---|
| changedetection.io | Open source, self-hostable page monitor; price-drop alerts using CSS, XPath and jq filters; managed plan listed at $8.99/month by a competitor's roundup | [ai-tldr](https://ai-tldr.dev/tools/changedetection-io/), [PageCrawl guide](https://pagecrawl.io/blog/complete-guide-website-monitoring-2026) |
| Firecrawl monitor | Scheduled scrapes, webhooks on change, a `changeTracking` structured diff | [firecrawl.dev/monitor](https://firecrawl.dev/monitor), [glossary](https://www.firecrawl.dev/glossary/web-scraping-apis/what-is-web-scraping-change-tracking) |
| Visualping, Apify, Bright Data, Browse AI | Hosted monitoring/scraping platforms | [roundup](https://superframeworks.com/articles/best-competitor-monitoring-tools) |

I found no source that covers extracting structured plan tables from SaaS pricing pages specifically; unverified claims were left out.

## What they do better

- Change tracking over time and alerting; this repo is a one-shot snapshot.
- Selector tooling and scheduling; here selectors are hand-written class names in `sites.json`.

## What they do worse / differ

- They are monitors or paid platforms; this repo is a 2-file pipeline whose output is a flat CSV/JSON of plans.

## What users expect

A stable schema, a documented way to add a site, and a reproducible local test; the repo has the first (columns `site,plan,price,description,features`) and a parser unit test, but adding a site needs trial and error.

## What is unique here

It demonstrates the Solari browser + sandbox combination end to end (per `docs/brainstorms/2026-08-31-solari-pricing-reporter-requirements.md`, built for an internship application and proposed to the Solari cookbook). Its value is as a readable example, not as a competing product.

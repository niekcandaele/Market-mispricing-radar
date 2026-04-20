# Local demo view

## Purpose

This document explains the lightweight local demo view for issue #19.

It exists to validate how the current app bundle actually reads in a judge-facing layout before the same structure is ported into Zerve Streamlit.

## Entry point

Generator script:
- `scripts/render_local_demo.py`

Default output:
- `artifacts/local-demo.html`

## What it renders

The demo page is intentionally simple.

It renders three core sections from the app bundle:
1. a refresh trust panel from `refresh_metadata`
2. a Radar table from `ranked_markets`
3. Market Detail cards from `market_explanations`

It also includes a short methodology section so the page loosely matches the planned judge-facing app flow.

## How to run it

From the repo root:

```bash
python3 scripts/render_local_demo.py
```

Useful options:

```bash
python3 scripts/render_local_demo.py --top 15
python3 scripts/render_local_demo.py --detail-count 5
python3 scripts/render_local_demo.py --output /tmp/market-demo.html
```

## Why this matters

The local prototype now produces:
- `ranked_markets`
- `market_explanations`
- `refresh_metadata`

This demo generator is the first lightweight consumer of that shape.

That makes it useful for checking:
- whether the Radar table reads cleanly
- whether the explanation fields feel judge-friendly
- whether the refresh metadata is sufficient for trust cues
- whether the current bundle shape is awkward anywhere before Zerve work resumes

## Bridge to Zerve

This is not the final app.

The intended migration path is:
1. keep refining the bundle shape locally until it feels coherent
2. port the same variable structure into Zerve once notebook execution becomes reliable again
3. recreate the same sections in Streamlit using the Zerve-side variables

## Constraint

This page is a validation artifact, not a substitute for the actual Zerve app.

# Local demo view

## Purpose

This document explains the lightweight local demo view for issue #19.

It exists to validate how the current app bundle actually reads in a presentation-ready layout before the same structure is ported into Zerve Streamlit.

## Entry point

Generator script:
- `scripts/render_local_demo.py`

Default output:
- `artifacts/local-demo.html`

## What it renders

The demo page is intentionally simple.

It renders four core sections from the app bundle:
1. a refresh trust panel from `refresh_metadata`
2. a category snapshot from `refresh_metadata.category_breakdown`
3. an interactive Radar table from `ranked_markets`
4. Market Detail cards from `market_explanations`

It also includes a short methodology section so the page loosely matches the planned Radar/Detail/Methodology app flow.

The current local demo now mirrors these planned Radar widgets and interactions:
- source filter
- category filter
- minimum score threshold
- result count selector
- sort control
- click-through market selection from the Radar table into the detail view
- reset-filters actions for empty states
- a small same-category peer comparison block in the selected detail view
- raw supporting-signal values in the selected detail view
- score-component cards with compact visual bars in the selected detail view

Those controls drive both the Radar table and the selected market detail view.

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
- whether category context is good enough to support later filtering
- whether the interactive controls feel coherent enough for the later Streamlit app
- whether row-driven detail selection feels natural
- whether same-category comparison helps the selected market feel more interpretable
- whether raw supporting-signal values make the score easier to trust
- whether the score breakdown reads like a real app section instead of a debug dump
- whether the explanation fields feel presentation-ready
- whether the refresh metadata is sufficient for trust cues
- whether the current bundle shape is awkward anywhere before Zerve work resumes

## Bridge to Zerve

This is not the final app.

The intended migration path is:
1. keep refining the bundle shape locally until it feels coherent
2. port the same variable structure into Zerve once notebook execution becomes reliable again
3. recreate the same sections in Streamlit using the Zerve-side variables

Current limit:
- category and topic labels in the local demo are heuristic, not source-authoritative
- this is still a single-page local validation artifact, not a full multi-screen deployed app

## Mirrored Streamlit bridge

The repo also carries a mirrored Streamlit app at `zerve/app/streamlit_app.py`.

For local iteration, prefer running it against a saved bundle artifact instead of forcing the app to import the heavier snippet fallback chain every time:

```bash
python3 scripts/export_streamlit_bundle.py --limit 200
MMR_APP_BUNDLE_PATH=artifacts/streamlit/app_bundle.json uv run --with streamlit streamlit run zerve/app/streamlit_app.py
```

That path is useful because it keeps the app focused on the deployment-layer handoff: loading the bundle shape, surfacing QA trust notes, and rendering the Radar/Detail/Methodology flow.

## Constraint

This page is a validation artifact, not a substitute for the actual Zerve app.

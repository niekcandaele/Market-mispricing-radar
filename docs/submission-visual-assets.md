# Submission Visual Assets

## Purpose

This doc maps the current local screenshot assets to likely slide and submission uses.

Use it when building the deck or assembling visual proof for the submission.

## Current screenshot set

Captured from the locked safe local default app using the refreshed local bundle.

Bundle basis:
- `artifacts/streamlit/app_bundle.json`
- refresh id: `refresh-20260424T120713Z`
- refreshed screenshot pass: `2026-04-24`

Screenshots:
- `artifacts/submission/local-radar-view.png`
- `artifacts/submission/local-market-detail-view.png`
- `artifacts/submission/local-methodology-view.png`

Slide-ready 16:9 crops:
- `artifacts/submission/slide-ready/local-radar-view-16x9.png`
- `artifacts/submission/slide-ready/local-market-detail-view-16x9.png`
- `artifacts/submission/slide-ready/local-methodology-view-16x9.png`

Google Workspace `Documents` copies:
- `Market Mispricing Radar - local-radar-view-16x9.png` — file id `1cJwxEV_aAVBadI1ZEbLNg1r7s38YISVl`
- `Market Mispricing Radar - local-market-detail-view-16x9.png` — file id `1heVTGPL-OH4q4IFHOIZbckXHssnkUZDv`
- `Market Mispricing Radar - local-methodology-view-16x9.png` — file id `1ABee8QF2x6RYPEZo43LEn9h0H4CI1Y4l`

## Recommended use by asset

### `artifacts/submission/local-radar-view.png`
Best for:
- raw proof capture
- backup visual if a taller crop is acceptable

### `artifacts/submission/slide-ready/local-radar-view-16x9.png`
Best for:
- title-adjacent product screenshot
- problem/solution slide
- live product proof slide

Why:
- shows the ranked Radar view clearly
- makes the product readable in one glance
- includes the overall framing and ranked-card experience

### `artifacts/submission/local-market-detail-view.png`
Best for:
- raw proof capture
- backup visual if a taller crop is acceptable

### `artifacts/submission/slide-ready/local-market-detail-view-16x9.png`
Best for:
- explainability slide
- credibility / why this is trustworthy slide
- product drilldown section

Why:
- shows the detail view, score context, and explanation framing
- makes it easy to talk about score drivers and caveats
- supports the claim that this is not just a black-box ranking

### `artifacts/submission/local-methodology-view.png`
Best for:
- raw proof capture
- backup visual if a taller crop is acceptable

### `artifacts/submission/slide-ready/local-methodology-view-16x9.png`
Best for:
- methodology / scope honesty slide
- caveats / MVP scope slide
- supporting screenshot for judging clarity

Why:
- reinforces that the product explains what it does and does not claim
- useful when the pitch needs to sound honest instead of overhyped

## Suggested slide mapping

- Slide 1 or 2: `local-radar-view-16x9.png`
- credibility / explainability slide: `local-market-detail-view-16x9.png`
- methodology / MVP honesty slide: `local-methodology-view-16x9.png`

## Notes

- these are safe local default screenshots, not live Zerve preview captures
- the 16:9 crops are the preferred slide assets, while the uncropped PNGs remain useful as raw proof captures
- matching Google Workspace copies in `Documents` were refreshed on 2026-04-24 to match this repo screenshot set, so the default office-layer visual store is back in sync with the current safe-local assets
- they are still useful because the safe local default path is verified and presentation-safe
- if a clean live preview screenshot pass becomes available later, it can replace or complement these assets

## If adding live screenshots later

Prefer replacing assets only when the live captures are:
- visually cleaner than the local ones
- clearly current
- not blocked by the live preview, because the current known preview behavior is now understood as short warm-up `503` lag rather than an unknown blocker

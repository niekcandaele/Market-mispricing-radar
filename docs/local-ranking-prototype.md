# Local ranking prototype

## Purpose

This document explains the local first-pass Polymarket ranking harness added for issue #15.

It exists because the current Zerve notebook path is blocked on run visibility, not because the project is moving away from Zerve.

The goal is to keep validating the scoring path and to keep portable logic in Git while the notebook execution path remains unreliable.

## What the prototype does

The prototype script lives at:
- `scripts/polymarket_ranker.py`

It does six things:
1. fetches live active Polymarket markets from the Gamma API
2. normalizes a core subset of fields from the raw payload
3. computes a first-pass fragility score inspired by `docs/scoring-model-v1.md`
4. assigns a readable primary reason code per market
5. derives explanation-ready fields from the score components
6. prints the top ranked rows for inspection

## Current implementation choices

The prototype is deliberately modest.

It uses:
- standard-library Python only
- a browser-like user agent for the Polymarket API request
- percentile-style normalization across the fetched live set
- a small number of interaction boosts for the combinations we already care about most

Current score components:
- staleness
- event horizon
- extremeness
- weak support / liquidity
- recent movement proxy via `oneMonthPriceChange`
- data quality penalty

## First tuning pass

A first review of the prototype output exposed a few obvious ranking pathologies:
- percentile-only freshness overreacted to tiny differences when almost every fetched market had been updated only minutes ago
- percentile-only event-horizon logic still rewarded far-future markets just because other fetched markets were even farther out
- ultra-longshot futures could dominate the top results even when they were neither stale nor close to resolution
- the first `--limit 200` slice was too order-biased and overrepresented one cluster of sports futures

The current prototype now compensates for that by:
- gating freshness with an absolute threshold, so sub-6-hour updates do not get fake stale credit
- using an absolute event-horizon signal that only meaningfully activates inside a roughly 30-day window
- adding extra penalties for overdue markets, very far-future markets, and ultra-extreme longshots that are neither stale nor near resolution
- raising the default fetch size to 500 markets to reduce API-order bias in the scored sample

These changes do not make the score "done", but they do make the first-pass output less obviously silly.

Current reason codes include:
- `stale_near_resolution`
- `extreme_price_low_support`
- `high_instability`
- `past_resolution_still_open`
- `weak_data_quality`
- plus simpler fallback reason labels for the strongest single component

Current explanation-oriented fields include:
- `headline_reason`
- `short_explanation`
- `detailed_explanation`
- `caveats`
- `supporting_signals`

The prototype also supports an app-ready bundle mode via `--app-json`.
That bundle currently emits:
- `ranked_markets`
- `market_explanations`
- `refresh_metadata`

These map directly onto the planned app flow:
- `ranked_markets` for the Radar screen list/table
- `headline_reason` inside `ranked_markets` for the Radar screen one-line reason
- `market_explanations` for the Market Detail explanation section
- `caveats` inside `market_explanations` for the detail-view caveat block
- `supporting_signals` and `score_components` inside `market_explanations` for the supporting-signals and score-breakdown sections
- `refresh_metadata` for the shared refresh trust panel

## Practical quirks already surfaced

Two useful implementation details showed up immediately:
- the Polymarket endpoint rejected a bare standard-library `urllib` request with HTTP 403, so the prototype now sends a browser-like user agent header
- some records can still appear open in the API while their end date is already in the past, so the prototype flags that case explicitly with `past_resolution_still_open`

## Why this is useful now

This prototype gives us a portable place to validate:
- field parsing assumptions from Polymarket
- score-shape sanity
- ranking plausibility
- explanation labels

That matters because issue #12 is blocked by notebook-side run visibility, not by the scoring concept itself.

## How to run it

From the repo root:

```bash
python3 scripts/polymarket_ranker.py
```

Default behavior now fetches 500 markets to reduce narrow-slice bias.

Useful options:

```bash
python3 scripts/polymarket_ranker.py --top 10
python3 scripts/polymarket_ranker.py --limit 300 --json
python3 scripts/polymarket_ranker.py --app-json
```

## How this should feed back into Zerve

Once the notebook execution path is reliable again, this prototype should be ported back in stages:

1. move the fetch logic into the first Polymarket ingestion block
2. preserve a raw snapshot output such as `polymarket_raw_markets`
3. move the normalization logic into a dedicated normalization block
4. move the score calculation into a scoring block
5. keep reason codes and score components explicit so the Streamlit layer can explain results cleanly
6. map `headline_reason`, `short_explanation`, `detailed_explanation`, `caveats`, and `supporting_signals` into the `market_explanations` output expected by the planned app flow in `docs/app-flow.md`

## Important constraint

This prototype is a validation harness, not the final runtime.

The target product is still:
- Zerve-native pipeline
- Zerve-hosted Streamlit app
- Git as the backup and control layer

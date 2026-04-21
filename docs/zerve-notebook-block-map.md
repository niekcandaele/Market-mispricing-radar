# Zerve notebook block map

This note turns the mirrored local snippets into an explicit notebook-side build order for Zerve.

It exists to reduce guesswork when copying the pipeline into the live Zerve notebook, especially for the deployed Streamlit handoff.

## Preferred block order

1. `configure_source`
2. `fetch_polymarket_data`
3. `normalize_markets`
4. `build_market_features`
5. `score_markets`
6. `build_market_explanations`
7. `build_app_bundle`
8. `build_qa_summary`

## Preferred block map

| Preferred Zerve block name | Mirrored local file | Primary outputs | Live notebook status |
| --- | --- | --- | --- |
| `configure_source` | inline notebook config or constants block | `source_config` | not yet created |
| `fetch_polymarket_data` | `zerve/snippets/polymarket_ingestion_block.py` | `source_config`, `polymarket_raw_markets`, `ingestion_metadata` | present |
| `normalize_markets` | `zerve/snippets/polymarket_normalization_block.py` | `normalized_markets`, `normalization_metadata` | present |
| `build_market_features` | `zerve/snippets/polymarket_feature_block.py` | `market_features`, `feature_metadata` | present |
| `score_markets` | `zerve/snippets/polymarket_scoring_block.py` | `ranked_markets`, `scoring_metadata` | present |
| `build_market_explanations` | `zerve/snippets/polymarket_explanations_block.py` | `market_explanations`, `explanation_metadata` | present |
| `build_app_bundle` | `zerve/snippets/polymarket_app_bundle_block.py` | `app_bundle`, `refresh_metadata` | present |
| `build_qa_summary` | `zerve/snippets/polymarket_qa_block.py` | `qa_summary` | present |

## Confirmed deployed Streamlit handoff

The deployed Zerve Streamlit runtime uses:
- `variable(block_name, variable_name)`

Preferred app-side lookups:
- `variable("build_app_bundle", "app_bundle")`
- `variable("build_qa_summary", "qa_summary")`

Current mirrored app support:
- defaults to those block names when `zerve.variable(...)` is available
- allows overrides with `MMR_ZERVE_APP_BUNDLE_BLOCK`
- allows overrides with `MMR_ZERVE_QA_BLOCK`
- falls back to local saved artifacts or snippet imports outside Zerve

## Practical notes

- A canvas-layout inspection on 2026-04-21 confirmed the live notebook initially contained only `fetch_polymarket_data` plus the Streamlit deployment surface.
- A follow-up live notebook pass on 2026-04-21 upgraded `fetch_polymarket_data` to the hardened ingestion code and then added working `normalize_markets`, `build_market_features`, `score_markets`, `build_market_explanations`, `build_app_bundle`, and `build_qa_summary` blocks.
- The live Zerve deploy proof used the internal notebook block name `fetch_polymarket_data` for `polymarket_raw_markets`.
- The ingestion block keeps browser-like request headers because the Zerve runtime returned `HTTP 403` without them.
- The current ingestion mirror fetches a wider upstream slice and emits a deterministic active-market output for downstream blocks.
- `build_app_bundle` and `build_qa_summary` are the names we should prefer going forward, even if temporary notebook experiments use rougher titles while iterating.

## Why this file exists

Without an explicit block map, notebook implementation work tends to depend on memory, UI labels, or ad hoc names.

This file makes the intended Zerve notebook contract visible in Git before every block is copied into the live canvas.

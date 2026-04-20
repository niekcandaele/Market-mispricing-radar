# Market Mispricing Radar

Support repository for the ZerveHack project.

Primary goals:
- keep plans, notes, and backups in Git
- keep project management sane
- mirror important Zerve artifacts locally

See `PROJECT_PLAN.md` for the initial project plan.

Project workflow and repo conventions live in `docs/repo-workflow.md`.
Judge-facing app flow notes live in `docs/app-flow.md`.
MVP source validation notes live in `docs/mvp-source-validation.md`.
Zerve hybrid execution/debug notes live in `docs/zerve-hybrid-execution.md`.
Local scoring prototype notes live in `docs/local-ranking-prototype.md`.
Local demo-view notes live in `docs/local-demo-view.md`.
The current local bridge artifacts also carry heuristic category/topic context for app shaping.

Prototype harness:
- `python3 scripts/polymarket_ranker.py`
- `python3 scripts/render_local_demo.py`

Zerve snippet mirror:
- `python3 zerve/snippets/polymarket_ingestion_block.py`
- `python3 zerve/snippets/polymarket_normalization_block.py`
- `python3 zerve/snippets/polymarket_feature_block.py`
- `python3 zerve/snippets/polymarket_scoring_block.py`
- `python3 zerve/snippets/polymarket_explanations_block.py`
- `python3 zerve/snippets/polymarket_app_bundle_block.py`
- `python3 zerve/snippets/polymarket_qa_block.py`

Zerve app scaffold mirror:
- `python3 -m py_compile zerve/app/streamlit_app.py`

Local Streamlit mirror run:
- `python3 scripts/export_streamlit_bundle.py --limit 200`
- `MMR_APP_BUNDLE_PATH=artifacts/streamlit/app_bundle.json uv run --with streamlit streamlit run zerve/app/streamlit_app.py`

Deployed Zerve Streamlit contract:
- confirmed runtime call shape is `variable(block_name, variable_name)`
- preferred notebook block names are `build_app_bundle` for `app_bundle` and `build_qa_summary` for `qa_summary`
- the mirrored app can override those with `MMR_ZERVE_APP_BUNDLE_BLOCK` and `MMR_ZERVE_QA_BLOCK`

The mirrored Streamlit scaffold now includes stateful Radar/Detail/Methodology navigation, a refresh-trust sidebar, a compact Radar-side QA warning summary for the active refresh, resettable Radar filters, a current-slice summary plus reason-code breakdown on Radar, multi-mode sort ordering for score/staleness/resolution views, app-like Radar result cards with detail-focus and source actions, honest handling when a focused market falls outside the current filters, filtered-slice context plus previous/next result stepping in Market Detail, fuller Market Detail header context, visual score cards, readable supporting-signal tables, same-category peer comparison, explicit unavailable-state messaging, missing-field notes for thin detail payloads, and a Methodology view that mixes judge-facing trust notes with live run context and QA warnings. The app now also prefers a saved local app-bundle artifact when `MMR_APP_BUNDLE_PATH` is set, and prefers real `zerve.variable(...)` loading when that runtime is available, which keeps local iteration light while preserving the real deployment handoff path.

The local demo now includes interactive Radar-style controls for filtering, sorting, click-through detail selection, filter reset states, a small same-category peer comparison block, raw supporting-signal values in the selected detail view, and compact score-breakdown cards for the selected market.

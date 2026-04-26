# Market Mispricing Radar

Support repository for the ZerveHack project.

Primary goals:
- keep plans, notes, and backups in Git
- keep project management sane
- mirror important Zerve artifacts locally

## Current submission handoff

Use these first during the final ZerveHack sprint:
- bundle index: `docs/submission-bundle.md`
- final sequence: `docs/final-submission-sequence.md`
- form map: `docs/submission-form-map.md`
- recording preflight: `docs/recording-preflight-checklist.md`
- final asset register: `docs/final-asset-register.md`
- final human handoff: `docs/final-human-handoff.md`

Current locked demo path:
- default: locked safe local default via `./scripts/check_safe_local_demo.sh` then `./scripts/run_local_demo.sh`
- drilldown: `Putin out as President of Russia by December 31, 2026?`
- retained proof: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/safe-local-demo-20260426T095005Z.json` (`refreshId`: `refresh-20260426T095005Z`)

Current deck handoff:
- source: `artifacts/submission/slides-generator-deck/slides.html`
- local PDF: `artifacts/submission/market-mispricing-radar-slides-generator-deck.pdf`
- local ZIP: `artifacts/submission/market-mispricing-radar-slides-generator-deck.zip`
- Drive PDF/HTML/ZIP links exist, but unauthenticated checks currently return `401 Unauthorized`; do not rely on Drive links for judges unless sharing is changed or the files are uploaded directly. Evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/drive-deck-unauth-open-check-20260426T0856Z.json`

Current public link:
- verified public Zerve notebook: `https://app.zerve.ai/notebook/1b13702d-5502-47d1-b1e0-6ba476250dc4`
- latest route gate: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-public-route-check-20260426T0503Z.json`
- `python3 scripts/check_zerve_public_share.py` now reports `summary.ready_for_share_post_link: true`

Immediate human actions:
1. record the final short demo on the locked safe local default
2. fill the submission form
3. publish the required public share post only after human platform/copy approval

Retained evidence manifest:
- `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/submission-evidence-manifest-20260425T1116Z.json`

See `PROJECT_PLAN.md` for the initial project plan.

Project workflow and repo conventions live in `docs/repo-workflow.md`.
Judge-facing app flow notes live in `docs/app-flow.md`.
Judge-facing demo script lives in `docs/judge-demo-script.md`.
Submission deck outline and speaker notes live in `docs/submission-deck-outline.md`.
Submission bundle index lives in `docs/submission-bundle.md`.
Submission copy draft lives in `docs/submission-copy-draft.md`.
Submission short variants live in `docs/submission-short-variants.md`.
Video recording run sheet lives in `docs/video-recording-run-sheet.md`.
Video voiceover script lives in `docs/video-voiceover-script.md`.
Recording preflight checklist lives in `docs/recording-preflight-checklist.md`.
Demo market shortlist lives in `docs/demo-market-shortlist.md`.
Submission form map lives in `docs/submission-form-map.md`.
Final submission sequence lives in `docs/final-submission-sequence.md`.
Presenter cheat sheet lives in `docs/presenter-cheat-sheet.md`.
Submission visual assets map lives in `docs/submission-visual-assets.md`.
Slide build kit lives in `docs/slide-build-kit.md`.
Slide copy pack lives in `docs/slide-copy-pack.md`.
Office-layer asset checklist lives in `docs/office-layer-asset-checklist.md`.
Final asset register lives in `docs/final-asset-register.md`.
Final readiness status lives in `docs/final-readiness-status.md`.
Submission verification checklist lives in `docs/submission-verification-checklist.md`.
MVP source validation notes live in `docs/mvp-source-validation.md`.
Zerve hybrid execution/debug notes live in `docs/zerve-hybrid-execution.md`.
Zerve notebook block-mapping notes live in `docs/zerve-notebook-block-map.md`.
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
- `./scripts/run_local_demo.sh`

Deployed Zerve Streamlit contract:
- confirmed runtime call shape is `variable(block_name, variable_name)`
- preferred notebook block names are `build_app_bundle` for `app_bundle` and `build_qa_summary` for `qa_summary`
- the mirrored app can override those with `MMR_ZERVE_APP_BUNDLE_BLOCK` and `MMR_ZERVE_QA_BLOCK`

The mirrored Streamlit scaffold now includes stateful Radar/Detail/Methodology navigation, a refresh-trust sidebar, a compact Radar-side QA warning summary for the active refresh, resettable Radar filters, a current-slice summary plus reason-code breakdown on Radar, multi-mode sort ordering for score/staleness/resolution views, app-like Radar result cards with detail-focus and source actions, honest handling when a focused market falls outside the current filters, filtered-slice context plus previous/next result stepping in Market Detail, fuller Market Detail header context, visual score cards, readable supporting-signal tables, same-category peer comparison, explicit unavailable-state messaging, missing-field notes for thin detail payloads, and a Methodology view that mixes product trust notes with live run context and QA warnings. The app now also prefers a saved local app-bundle artifact when `MMR_APP_BUNDLE_PATH` is set, and prefers real `zerve.variable(...)` loading when that runtime is available, which keeps local iteration light while preserving the real deployment handoff path.

The local demo now includes interactive Radar-style controls for filtering, sorting, click-through detail selection, filter reset states, a small same-category peer comparison block, raw supporting-signal values in the selected detail view, and compact score-breakdown cards for the selected market.

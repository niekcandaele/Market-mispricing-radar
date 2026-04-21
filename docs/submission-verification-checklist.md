# Submission Verification Checklist

## Purpose

This document is the final-mile verification layer for the submission bundle.

Use it before recording, presenting, or submitting so the project is checked intentionally instead of relying on memory.

## Current verification status

- repo-side narrative artifacts: present
- local fallback demo path: verified end to end
- live Zerve preview path: needs final pre-submission recheck and is currently auth-blocked in the available browser state
- Google Slides deck: not created yet and currently blocked on a browser Google accepts for login
- office-layer speaker notes doc: not created yet and currently blocked on the same office-layer browser/login constraint
- final submission form paste/check: not done yet

## Demo checks

### Preferred live demo
- [ ] open the current Zerve Streamlit preview from the deploy tab
- [ ] confirm the app loads without runtime error
- [ ] confirm sidebar shows live Zerve bundle context
- [ ] confirm Radar view renders ranked markets
- [ ] confirm one top market opens cleanly in Market Detail
- [ ] confirm Methodology view still matches current product framing

### Local fallback demo
- [x] run `python3 scripts/export_streamlit_bundle.py --limit 200`
- [x] run `MMR_APP_BUNDLE_PATH=artifacts/streamlit/app_bundle.json uv run --with streamlit streamlit run zerve/app/streamlit_app.py`
- [x] confirm the local app opens and renders the expected radar flow
- [x] confirm one market drilldown opens cleanly in Market Detail

## Artifact checks

### Repo docs
- [x] `docs/judge-demo-script.md`
- [x] `docs/submission-deck-outline.md`
- [x] `docs/submission-bundle.md`
- [x] `docs/submission-copy-draft.md`
- [x] `docs/submission-short-variants.md`
- [x] `docs/video-recording-run-sheet.md`
- [x] `docs/demo-market-shortlist.md`
- [x] `docs/submission-form-map.md`
- [x] `docs/final-submission-sequence.md`
- [x] `docs/presenter-cheat-sheet.md`
- [x] `docs/submission-visual-assets.md`
- [x] `docs/slide-build-kit.md`
- [x] `docs/slide-copy-pack.md`
- [x] `docs/office-layer-asset-checklist.md`
- [x] `docs/submission-verification-checklist.md`

### Office-layer artifacts
- [ ] Google Slides deck created
- [ ] Google Doc or deck speaker notes finalized
- [ ] assets stored cleanly in Google Workspace `Documents`
- [ ] browser path for Google Workspace creation is available and accepted by Google sign-in
- [x] repo-side office-layer handoff checklist exists

## Submission-form checks

- [ ] short description reflects the real MVP scope
- [ ] longer project summary matches the live product
- [ ] accomplishments section is specific and believable
- [ ] caveats stay honest about single-source MVP limits
- [ ] built-with / stack section matches the real implementation
- [ ] links pasted into the submission form actually open

## Recording checks

- [ ] use `docs/judge-demo-script.md` as the spoken baseline
- [ ] use `docs/video-recording-run-sheet.md` as the actual beat-by-beat recording order
- [ ] use `docs/demo-market-shortlist.md` to pre-pick a strong drilldown example
- [ ] keep the recording to one coherent story arc
- [ ] verify the chosen demo path before recording begins
- [ ] avoid relying on an old rotated preview URL without rechecking it

## Lightweight smoke-check notes

### 2026-04-21 local fallback export check
- command: `python3 scripts/export_streamlit_bundle.py --limit 200`
- goal: verify the repo can still generate the saved app bundle artifact used by the local fallback path
- expected result: refreshed `artifacts/streamlit/app_bundle.json` without failure
- observed result: passed, refreshed `artifacts/streamlit/app_bundle.json` with `refresh_id` `refresh-20260421T070336Z` and `ranked_market_count` `200`
- status: passed

### 2026-04-21 local fallback app render check
- command: `MMR_APP_BUNDLE_PATH=artifacts/streamlit/app_bundle.json uv run --with streamlit streamlit run zerve/app/streamlit_app.py --server.headless true --server.address 127.0.0.1 --server.port 8765`
- goal: verify the documented local fallback app actually opens and presents the expected product flow
- observed result: passed, the local app rendered the Radar view with live product framing, run status, QA warning summary, and ranked markets, then successfully opened a Market Detail drilldown for the top-ranked result
- notable observed values: `refresh_id` `refresh-20260421T070414Z`, `market_count` `200`, `open_markets` `200`, `score_version` `v1-prototype`
- status: passed

## Honest readiness call

The project is in a strong near-ready state, but it is not submission-complete yet.

What is already verified or present:
- deployed-product path exists
- local fallback path exists and now renders cleanly
- demo script exists
- deck source exists
- submission copy exists
- short submission variants exist
- video recording run sheet exists
- demo market shortlist exists
- submission form map exists
- final submission-day sequence exists
- presenter cheat sheet exists
- submission visual asset map exists
- slide build kit exists
- slide copy pack exists
- office-layer asset checklist exists
- bundle index exists

What still blocks a true done call:
- final live preview recheck right before submission
- Google Slides deck creation
- office-layer notes artifact creation
- a browser session that can complete the needed Zerve and Google office-layer checks without auth failure
- final link and form verification pass

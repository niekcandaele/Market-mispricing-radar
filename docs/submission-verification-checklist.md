# Submission Verification Checklist

## Purpose

This document is the final-mile verification layer for the submission bundle.

Use it before recording, presenting, or submitting so the project is checked intentionally instead of relying on memory.

## Current verification status

- repo-side narrative artifacts: present
- local fallback demo path: verified end to end
- live Zerve preview path: the new Browserless + Playwright path can sign into Zerve and reopen the project again, the real preview trigger has been re-confirmed, the valid deployed Streamlit script was directly recovered and patched back to the repo app, and the remaining live-check blocker is one clean verification pass on the newest repaired preview host once its DNS / reachability stabilizes
- Google Slides deck: compact deck now exists in Google Workspace `Documents`, and the latest pass tightened slide copy, improved hierarchy, added proof-structure elements, and synced embedded speaker notes to the safe demo-path plan; the remaining deck gap is mainly screenshot/layout polish
- office-layer speaker notes doc: presenter notes and deck speaker notes now both reflect the safe local-fallback default and align cleanly with the current compact deck order
- final submission form paste/check: not done yet

## Demo checks

### Preferred live demo
- [ ] open the current Zerve Streamlit preview from the deploy tab, using the in-editor preview control rather than the global header `Deploy` button if the UI bounces back to the generic chooser, or recover the same preview via the repaired direct script path if the tab UI is flaky again
- [ ] confirm the app loads without runtime error
- [ ] confirm sidebar shows live Zerve bundle context
- [ ] confirm Radar view renders ranked markets
- [ ] confirm one top market opens cleanly in Market Detail
- [ ] confirm Methodology view still matches current product framing
- [ ] if the newest host is still flaky, stop here and use the verified local fallback for recording/submission instead of chasing rotating preview DNS

### Local fallback demo
- [x] run `./scripts/run_local_demo.sh`
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
- [x] `docs/video-voiceover-script.md`
- [x] `docs/recording-preflight-checklist.md`
- [x] `docs/demo-market-shortlist.md`
- [x] `docs/submission-form-map.md`
- [x] `docs/final-submission-sequence.md`
- [x] `docs/presenter-cheat-sheet.md`
- [x] `docs/submission-visual-assets.md`
- [x] `docs/slide-build-kit.md`
- [x] `docs/slide-copy-pack.md`
- [x] `docs/office-layer-asset-checklist.md`
- [x] `docs/final-asset-register.md`
- [x] `docs/final-readiness-status.md`
- [x] `docs/submission-verification-checklist.md`

### Office-layer artifacts
- [x] Google Slides deck created
- [x] deck speaker notes updated and aligned with the safe demo-path plan
- [x] Google Doc presenter notes finalized
- [x] final submission copy reference created in Google Workspace `Documents`
- [x] demo link reference created in Google Workspace `Documents`
- [x] assets stored cleanly in Google Workspace `Documents`
- [x] authenticated `gws` CLI path for Google Workspace creation is available
- [x] repo-side office-layer handoff checklist exists
- [x] deck, notes, submission-copy, and demo-link artifacts can all be read back successfully through the Workspace APIs

## Submission-form checks

- [ ] short description reflects the real MVP scope
- [ ] longer project summary matches the live product
- [ ] accomplishments section is specific and believable
- [ ] caveats stay honest about single-source MVP limits
- [ ] built-with / stack section matches the real implementation
- [ ] links pasted into the submission form actually open

## Recording checks

- [ ] use `docs/judge-demo-script.md` as the spoken baseline
- [ ] use `docs/video-voiceover-script.md` if a more literal spoken script is helpful during recording
- [ ] use `docs/video-recording-run-sheet.md` as the actual beat-by-beat recording order
- [ ] run `docs/recording-preflight-checklist.md` before the real take
- [x] use `docs/demo-market-shortlist.md` to pre-pick a strong drilldown example (`Putin out as President of Russia by December 31, 2026?` locked as the current default unless the final live run clearly surfaces a cleaner option)
- [ ] keep the recording to one coherent story arc
- [ ] verify the chosen demo path before recording begins
- [ ] avoid relying on an old rotated preview URL without rechecking it
- [ ] if live preview is still unstable, explicitly choose the verified local fallback and record against that path

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

### 2026-04-21 refreshed local fallback export check
- command: `python3 scripts/export_streamlit_bundle.py --limit 200`
- goal: reconfirm the local fallback bundle can still be refreshed late in packaging without regressions
- observed result: passed, refreshed `artifacts/streamlit/app_bundle.json` with `refresh_id` `refresh-20260421T140836Z` and `ranked_market_count` `200`
- status: passed

### 2026-04-22 one-command local fallback launch check
- command: `./scripts/run_local_demo.sh`
- default runtime details:
  - refresh limit: `200`
  - address: `127.0.0.1`
  - port: `8768`
- goal: verify the documented one-command local fallback path refreshes the bundle and serves the app cleanly for recording and final verification
- observed result: passed, the helper refreshed the bundle and served the app cleanly on `http://127.0.0.1:8768`
- status: passed

### 2026-04-21 refreshed local fallback render check
- commands:
  - `./scripts/run_local_demo.sh`
  - local Playwright verification against `http://127.0.0.1:8768`
- goal: reconfirm the current local fallback still renders the full demo flow during late-stage submission polish
- observed result: passed, local Playwright confirmed visible `Market Mispricing Radar`, `Ranked Radar`, `Methodology`, and `Focus in detail`, then successfully navigated into Market Detail and Methodology
- notable observed values: `refresh_id` `refresh-20260421T140836Z`, `ranked_market_count` `200`
- status: passed

## Honest readiness call

The project is in a strong near-ready state, but it is not submission-complete yet.

What is already verified or present:
- deployed-product path exists
- local fallback path exists and now renders cleanly
- demo script exists
- compact Google Slides deck exists and has been read back successfully through the Workspace APIs
- presenter-notes doc exists and has been read back successfully through the Workspace APIs
- final submission-copy doc exists and has been read back successfully through the Workspace APIs
- demo-link reference doc exists and has been read back successfully through the Workspace APIs
- short submission variants exist
- video recording run sheet exists
- video voiceover script exists
- recording preflight checklist exists
- demo market shortlist exists
- submission form map exists
- final submission-day sequence exists
- presenter cheat sheet exists
- submission visual asset map exists
- slide build kit exists
- slide copy pack exists
- office-layer asset checklist exists
- final asset register exists
- final readiness status doc exists
- bundle index exists

What still blocks a true done call:
- final live preview recheck right before submission
- final visual polish on the compact deck
- actual recording execution against the aligned presenter notes / recording plan
- final link and form verification pass

### 2026-04-21 repaired live preview recheck
- browser/auth path: passed, Browserless + Playwright reopened the Zerve notebook successfully
- deploy repair seam: passed, recovered valid deployed Streamlit script `ecda0778-025a-4d74-898a-31ee7c3f709d` from canvas metadata and verified direct `PATCH /script/<deployment_script_id>` repair by replacing the stale probe content with the repo app
- preview trigger: passed, direct `POST /script/<deployment_script_id>/deploy_preview` returned success and emitted fresh preview metadata (`current_preview_id` `98be1ead-9c6b-45d3-8800-1c46e4b344a0`, `preview_deployment_id` `bdeef4a2-827c-4190-96e7-5dce68958d18`, DNS label `dc772abb-6f3a4e5a`)
- live host check: not yet final, because the fresh `dc772abb-6f3a4e5a.hub.zerve.cloud` host still showed inconsistent DNS / reachability during verification and should not be treated as the locked submission-day URL yet
- operator call: stop burning late-stage time on preview DNS roulette; use the verified local fallback as the safe default unless a final live check turns clean

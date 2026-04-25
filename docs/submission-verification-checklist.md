# Submission Verification Checklist

## Purpose

This document is the final-mile verification layer for the submission bundle.

Use it before recording, presenting, or submitting so the project is checked intentionally instead of relying on memory.

## Current verification status

- narrative artifacts: present
- safe local default demo path: verified end to end
- live Zerve preview path: verified as an optional upgrade path, with the latest 2026-04-22 recheck showing the known warm-up pattern before the real app renders
- submission deck: previous Google Slides deck was trashed, and a fresh 9-slide HTML deck rebuilt with the updated `slides-generator` skill now exists locally and in Google Drive
- office-layer speaker notes doc: presenter notes remain aligned to the safe local default and the rebuilt deck includes hidden per-slide notes
- final submission form paste/check: pending the final form-fill pass

## Demo checks

### Optional live demo upgrade
- [ ] open the current Zerve Streamlit preview from the deploy tab, using the in-editor preview control rather than the global header `Deploy` button if the UI bounces back to the generic chooser, or recover the same preview via direct bearer-auth `POST /script/<deployment_script_id>/deploy_preview`
- [ ] confirm the app loads without runtime error
- [ ] confirm sidebar shows live Zerve bundle context
- [ ] confirm Radar view renders ranked markets
- [ ] confirm one top market opens cleanly in Market Detail
- [ ] confirm Methodology view still matches current product framing
- [ ] if the newest host first returns ELB `503`, wait roughly 45 to 60 seconds and retry once before abandoning it
- [ ] if the newest host never emits preview metadata, never resolves, or never clears warm-up `503`, stop here and use the locked safe local default for recording/submission instead of chasing rotating preview URLs

### Safe local default demo
- [x] run `./scripts/run_local_demo.sh`
- [x] confirm the local app opens and renders the expected radar flow
- [x] confirm one market drilldown opens cleanly in Market Detail

## Artifact checks

### Repo docs
- [x] `docs/judge-demo-script.md`
- [x] `docs/submission-deck-outline.md`
- [x] `docs/submission-bundle.md`
- [x] `docs/final-human-handoff.md`
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
- [x] old Google Slides deck trashed per updated deck instruction
- [x] fresh slides-generator HTML deck created and aligned with the safe local default plan
- [x] rebuilt HTML deck passed local Playwright QA: 9 slides, 9 nav dots, all six images loaded with alt text, no overflowing slides at 1280x720
- [x] rebuilt deck ZIP verified as complete and uncorrupted
- [x] Drive deck HTML, ZIP, and PDF artifacts verified against local size/md5 checks
- [x] rebuilt deck exported to PDF, verified as 9 pages, and uploaded to Google Drive
- [x] Google Doc presenter notes refreshed to the rebuilt 9-slide deck and readback-verified
- [x] final submission copy reference created in Google Workspace `Documents/Hackathons/ZerveHack`
- [x] demo link reference created in Google Workspace `Documents/Hackathons/ZerveHack`
- [x] assets stored cleanly in Google Workspace `Documents/Hackathons/ZerveHack`
- [x] authenticated `gws` CLI path for Google Workspace creation is available
- [x] office-layer handoff checklist exists
- [x] deck, notes, submission-copy, and demo-link artifacts can all be read back successfully through the Workspace APIs; latest office-doc QA confirmed presenter notes, submission copy, and Demo Link Notes contain the required current story/proof markers

## Submission-form checks

- [ ] short description reflects the real MVP scope
- [ ] longer project summary matches the live product
- [ ] accomplishments section is specific and believable
- [ ] caveats stay honest about single-source MVP limits
- [ ] built-with / stack section matches the real implementation
- [ ] links pasted into the submission form actually open

## Public share-post checks

- [ ] confirm the hackathon still lists a public share post as required on the live Devpost page
- [ ] choose the posting platform explicitly, default LinkedIn unless the human prefers otherwise
- [ ] use draft wording from `docs/share-post-pack.md`
- [ ] confirm the exact Zerve tag on the chosen platform
- [ ] attach one clean screenshot and the final public project link
- [ ] if the latest public-status check still says the project is not public in Zerve, first use the Zerve share/privacy control to make it public
- [ ] after the privacy change, first verify the notebook share route `https://app.zerve.ai/notebook/1b13702d-5502-47d1-b1e0-6ba476250dc4`
- [ ] use `python3 scripts/check_zerve_public_share.py` as the canonical fast recheck helper
- [ ] let the checker auto-attempt its best-effort Chromium token extraction path if needed, but prefer a fresh `ZERVE_BEARER` or `--bearer` when available instead of relying on route-only output
- [ ] if you use the checker, require `summary.ready_for_share_post_link: true` instead of manually eyeballing a bare `200`
- [ ] do not treat a bare `200` on that route as success if it only returns the generic Zerve shell instead of the actual public project page
- [ ] if a different public route is used, confirm it was chosen deliberately and verified, not silently swapped in from the gallery/community path
- [ ] confirm the latest public-status check is no longer `canvas.is_public: false` before treating the share-post path as unblocked
- [ ] verify the post is actually published before treating the requirement as done

## Recording checks

- [ ] use `docs/judge-demo-script.md` as the spoken baseline
- [ ] use `docs/video-voiceover-script.md` if a more literal spoken script is helpful during recording
- [ ] use `docs/video-recording-run-sheet.md` as the actual beat-by-beat recording order
- [ ] run `docs/recording-preflight-checklist.md` before the real take
- [ ] on the safe local default path, run `./scripts/check_safe_local_demo.sh` right before the real take instead of trusting older evidence alone
- [x] use `docs/demo-market-shortlist.md` to pre-pick a strong drilldown example (`GTA VI released before June 2026?` locked as the current default for the safe local path unless the final live run clearly surfaces a cleaner option)
- [ ] keep the recording to one coherent story arc
- [ ] verify the chosen demo path before recording begins
- [ ] avoid relying on an old rotated preview URL without rechecking it
- [ ] if live preview is still unstable, explicitly choose the locked safe local default and record against that path

## Lightweight smoke-check notes

### 2026-04-21 safe local default export check
- command: `python3 scripts/export_streamlit_bundle.py --limit 200`
- goal: verify the repo can still generate the saved app bundle artifact used by the locked safe local default path
- expected result: refreshed `artifacts/streamlit/app_bundle.json` without failure
- observed result: passed, refreshed `artifacts/streamlit/app_bundle.json` with `refresh_id` `refresh-20260421T070336Z` and `ranked_market_count` `200`
- status: passed

### 2026-04-21 safe local default app render check
- command: `MMR_APP_BUNDLE_PATH=artifacts/streamlit/app_bundle.json uv run --with streamlit streamlit run zerve/app/streamlit_app.py --server.headless true --server.address 127.0.0.1 --server.port 8765`
- goal: verify the documented safe local default app actually opens and presents the expected product flow
- observed result: passed, the local app rendered the Radar view with live product framing, run status, QA warning summary, and ranked markets, then successfully opened a Market Detail drilldown for the top-ranked result
- notable observed values: `refresh_id` `refresh-20260421T070414Z`, `market_count` `200`, `open_markets` `200`, `score_version` `v1-prototype`
- status: passed

### 2026-04-21 refreshed safe local default export check
- command: `python3 scripts/export_streamlit_bundle.py --limit 200`
- goal: reconfirm the safe local default bundle can still be refreshed late in packaging without regressions
- observed result: passed, refreshed `artifacts/streamlit/app_bundle.json` with `refresh_id` `refresh-20260421T140836Z` and `ranked_market_count` `200`
- status: passed

### 2026-04-22 one-command safe local default launch check
- command: `./scripts/run_local_demo.sh`
- default runtime details:
  - refresh limit: `200`
  - address: `127.0.0.1`
  - port: `8768`
- goal: verify the documented one-command safe local default path refreshes the bundle and serves the app cleanly for recording and final verification
- observed result: passed, the helper refreshed the bundle and served the app cleanly on `http://127.0.0.1:8768`
- status: passed

### 2026-04-25 corrected safe local final sweep
- commands:
  - `./scripts/check_safe_local_demo.sh`
- goal: reconfirm shortly before submission work that the locked safe local default still passes the exact intended story arc without manual repair steps
- observed result: passed, the one-command sweep launched the app, verified Radar, confirmed the Methodology honesty beat, clicked the real `Focus in detail` control on the GTA card, and then verified true detail-only markers including `Primary signal`, `Why this market is flagged`, and `Observed market signals`
- notable observed values: `refresh_id` `refresh-20260425T130211Z`
- evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/safe-local-demo-20260425T130211Z.json`
- note: the `refresh_id` and evidence filename are UTC-stamped, while this verification entry is dated in local Europe/Brussels time; `./scripts/check_safe_local_demo.sh` now writes this retained JSON automatically and archives the previously active safe-local baseline on success
- status: passed

### 2026-04-22 safe local recording-flow check
- commands:
  - `./scripts/run_local_demo.sh`
  - local Playwright verification against `http://127.0.0.1:8768`
- goal: verify the current one-command local recording path still supports the exact intended story arc: Radar, Methodology honesty beat, and a clean GTA VI drilldown from the default Radar slice into Market Detail
- observed result: passed, local Playwright confirmed visible `Market Mispricing Radar`, `Ranked Radar`, and `Methodology`, confirmed the honest-scope beat on Methodology, and then reopened the Radar to drill cleanly into `GTA VI released before June 2026?` in Market Detail
- notable observed values: `refresh_id` `refresh-20260422T030359Z`, `ranked_market_count` `200`
- status: passed

### 2026-04-21 refreshed safe local default render check
- commands:
  - `./scripts/run_local_demo.sh`
  - local Playwright verification against `http://127.0.0.1:8768`
- goal: reconfirm the locked safe local default still renders the full demo flow during late-stage submission polish
- observed result: passed, local Playwright confirmed visible `Market Mispricing Radar`, `Ranked Radar`, `Methodology`, and `Focus in detail`, then successfully navigated into Market Detail and Methodology
- notable observed values: `refresh_id` `refresh-20260421T140836Z`, `ranked_market_count` `200`
- status: passed

## Honest readiness call

The project is in a strong near-ready state, but it is not submission-complete yet.

What is already verified or present:
- deployed-product path exists
- locked safe local default path exists and now renders cleanly
- demo script exists
- rebuilt 9-slide HTML deck exists locally and in Google Drive as both an HTML file and a ZIP bundle
- presenter-notes doc exists, was refreshed to the rebuilt 9-slide HTML/PDF deck, and has been read back successfully through the Workspace APIs
- final submission-copy doc exists, was refreshed to match the latest submission copy, and has been read back successfully through the Workspace APIs
- demo-link reference doc exists, was refreshed after the latest safe-local recheck, and has been read back successfully through the Workspace APIs
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
- actual recording execution against the aligned presenter notes / recording plan
- final public Zerve/share-post gate, form submission, and real final link capture
- final link and form verification pass

Optional, not blocking the safe-local submission path:
- final live preview recheck right before submission, only if considering a live upgrade
- low-risk visual polish on the rebuilt 9-slide HTML/PDF deck package, only if it is clearly beneficial

### 2026-04-21 repaired live preview recheck
- browser/auth path: passed, Browserless + Playwright reopened the Zerve notebook successfully
- deploy repair seam: passed, recovered valid deployed Streamlit script `ecda0778-025a-4d74-898a-31ee7c3f709d` from canvas metadata and verified direct `PATCH /script/<deployment_script_id>` repair by replacing the stale probe content with the repo app
- preview trigger: passed, direct `POST /script/<deployment_script_id>/deploy_preview` returned success and emitted fresh preview metadata (`current_preview_id` `98be1ead-9c6b-45d3-8800-1c46e4b344a0`, `preview_deployment_id` `bdeef4a2-827c-4190-96e7-5dce68958d18`, DNS label `dc772abb-6f3a4e5a`)
- live host check: incomplete at that moment, because the fresh `dc772abb-6f3a4e5a.hub.zerve.cloud` host still looked inconsistent during that pass

### 2026-04-22 recovered live preview warm-up check
- trigger path: passed, direct bearer-auth `POST https://canvas.api.zerve.ai/script/ecda0778-025a-4d74-898a-31ee7c3f709d/deploy_preview` returned `200`
- preview metadata: passed, fresh metadata appeared in `canvas_layout` for the same recovered script (`current_preview_id` `b0966b53-de68-43a2-9c8e-759bead27ab1`, `preview_deployment_id` `114fe023-2dfe-41ce-97c8-408d9a949602`, DNS label `1237c1f1-ee724b30`)
- DNS check: passed, `1237c1f1-ee724b30.hub.zerve.cloud` resolved immediately to `54.154.86.15` and `54.217.140.40`
- warm-up behavior: observed ELB `503`, then one timeout, then `200` within about 45 seconds
- rendered-app check: passed, the fresh preview rendered the real Market Mispricing Radar app, including sidebar views `Radar`, `Market Detail`, and `Methodology`, plus live app content such as `Ranked Radar` and `Processed 250`
- evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-preview-20260422T0534Z.json`
- conclusion: the live preview is recoverable and real, but it still should be treated as an optional upgrade because the safe local default remains simpler and safer for recording/submission

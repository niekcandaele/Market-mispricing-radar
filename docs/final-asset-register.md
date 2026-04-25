# Final Asset Register

## Purpose

This is the one place to record the actual final assets used on submission day.

Use it when the real last-mile artifacts start to exist, so the submission does not depend on memory, chat history, or stale breadcrumbs.

## Current status

This is now a real working register, not a blank template.

The main demo path, office artifacts, and submission materials are in place. The remaining unknowns are the final live checked links plus the actual submission-day execution items.

## Final demo path

### Primary demo path
- status: ready and locked as the safe local default
- chosen path: locked safe local default
- URL or launch source:
  - `./scripts/run_local_demo.sh`
- default runtime details:
  - refresh limit: `200`
  - address: `127.0.0.1`
  - port: `8768`
- verified on: `2026-04-24`
- verified by: `Jefke`
- notes: dedicated demo-link reference doc now exists in Google Workspace `Documents/Hackathons/ZerveHack` at `https://docs.google.com/document/d/1gA2LDL0E_2T-DfyQ8Fxxhw1DqvBjqPg2B5Fpl33c9UQ`; the one-command `./scripts/run_local_demo.sh` path was reverified on 2026-04-24, including Radar, Methodology, and Market Detail on the locked safe local default bundle, and should be used for recording and submission unless a final live preview check opens cleanly enough to justify switching

### Optional live upgrade path
- status: verified, but not chosen as the default path
- path: fresh live Zerve Streamlit preview reopened from the deploy tab
- URL or launch source: `https://1237c1f1-ee724b30.hub.zerve.cloud/` (fresh 2026-04-22 recovery) or a fresh equivalent reopened from the deploy tab
- verified on: `2026-04-22`
- verified by: `Jefke`
- notes: the latest concrete diagnosis is specific, not vague. Direct bearer-auth `POST /script/ecda0778-025a-4d74-898a-31ee7c3f709d/deploy_preview` returned `200`, emitted fresh preview metadata, the new host resolved immediately, then served ELB `503` during warm-up before converging to `200` and rendering the real Market Mispricing Radar app. Evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-preview-20260422T0534Z.json`

## Final drilldown example

- chosen market: `GTA VI released before June 2026?`
- why this one: currently rank `3` in the locked safe local default bundle, visible in the default Radar slice, broadly understandable, and easier to demo cleanly in one take from Radar into Market Detail
- source doc reference: `docs/demo-market-shortlist.md`
- locked on: `2026-04-24` (reconfirmed against the locked safe local default bundle unless the final live run clearly surfaces a cleaner example)

## Final presentation assets

### Google Slides deck
- status: created, compact 6-slide deck is fully built in Google Workspace with styling, embedded speaker notes, proof visuals, and current-state readback verification; acceptable for submission with only optional low-risk layout polish left
- final title: `Market Mispricing Radar - Submission Deck`
- deck shape used: `compact 6-slide`
- location: `https://docs.google.com/presentation/d/1MYzlPnXoFbulK9SopHM9Uh1rmAPNRVC8uzH_NurZxKA`
- alignment note: readback-verified so the body copy and embedded notes match the current compact deck and safe local GTA drilldown path.
- source docs:
  - `docs/submission-deck-outline.md`
  - `docs/slide-build-kit.md`
  - `docs/slide-copy-pack.md`

### Speaker notes / presenter notes
- status: created, structured presenter notes are aligned to the locked safe local default, readback-verified against the current recording path, and ready for recording use
- final title: `Market Mispricing Radar - Presenter Notes`
- location: `https://docs.google.com/document/d/17fNahknqysD206KM9VRocYRcOCOoQyrPDmsBVjQQhU4`
- alignment note: readback-verified so the presenter notes match the locked safe local default, the GTA drilldown default, and the compact deck order.
- source docs:
  - `docs/judge-demo-script.md`
  - `docs/video-voiceover-script.md`
  - `docs/video-recording-run-sheet.md`
  - `docs/presenter-cheat-sheet.md`

### Final submission copy reference
- status: created, paste-ready submission copy is in place in Google Workspace and reverified against the latest submission copy
- final title: `Market Mispricing Radar - Final Submission Copy`
- location: `https://docs.google.com/document/d/1Y6xAXczjmsoWiRsbQ_0HmR3EzNTBYxRkgFjK9-525sM`
- alignment note: reverified against the latest submission copy and kept aligned with the paste-ready submission baseline.

### Demo link reference
- status: created, aligned to the locked safe local default, and readback-verified again after the latest safe-local recheck
- final title: `Market Mispricing Radar - Demo Link Notes`
- location: `https://docs.google.com/document/d/1gA2LDL0E_2T-DfyQ8Fxxhw1DqvBjqPg2B5Fpl33c9UQ`
- alignment note: kept aligned to the locked safe local default, the one-command pre-take sweep, the auto-written retained proof flow, and the latest safe-local verification evidence.
- source docs:
  - `docs/submission-verification-checklist.md`
  - `docs/final-submission-sequence.md`
  - `docs/demo-market-shortlist.md`
  - `docs/video-recording-run-sheet.md`

## Final screenshot set used in slides or form

- product hero screenshot: `artifacts/submission/slide-ready/local-radar-view-16x9.png`
- explainability screenshot: `artifacts/submission/slide-ready/local-market-detail-view-16x9.png`
- methodology screenshot: `artifacts/submission/slide-ready/local-methodology-view-16x9.png`
- preferred repo assets today:
  - `artifacts/submission/slide-ready/local-radar-view-16x9.png`
  - `artifacts/submission/slide-ready/local-market-detail-view-16x9.png`
  - `artifacts/submission/slide-ready/local-methodology-view-16x9.png`
- repo screenshot basis: refreshed on `2026-04-24` against local bundle `refresh-20260424T120713Z`
- Google Workspace `Documents/Hackathons/ZerveHack` copies:
  - `Market Mispricing Radar - local-radar-view-16x9.png` — file id `1cJwxEV_aAVBadI1ZEbLNg1r7s38YISVl`
  - `Market Mispricing Radar - local-market-detail-view-16x9.png` — file id `1heVTGPL-OH4q4IFHOIZbckXHssnkUZDv`
  - `Market Mispricing Radar - local-methodology-view-16x9.png` — file id `1ABee8QF2x6RYPEZo43LEn9h0H4CI1Y4l`
- office-layer note: the `Documents/Hackathons/ZerveHack` screenshot copies were refreshed on `2026-04-24` from the current repo assets, and Drive md5 checks matched the local slide-ready PNGs after upload

Remaining unresolved values below are intentional submission-time fields, not packaging gaps.

## Final video asset

- status: not recorded yet; record the final demo and capture the real file path or upload URL
- title or filename: set after recording
- location or upload URL: set after recording or upload
- recorded on: set after the recording session
- notes: use `docs/video-recording-run-sheet.md`

## Final submission form

- status: not submitted yet; fill the real Devpost form with final links and submit
- Devpost submission URL: capture after the real form submission
- final project URL used in form: set at form-fill time
- video URL used in form: set after the final video file or upload URL exists
- screenshot/image URL used in form: set at form-fill time
- submitted on: set at the actual submission event

## Required public share post

- status: blocked until a verified public Zerve link exists and the human chooses and approves the final platform/post
- recommended platform: LinkedIn
- fallback platform: X
- draft pack: `docs/share-post-pack.md`
- screenshot default: `artifacts/submission/slide-ready/local-radar-view-16x9.png`
- project link to use: blocked until the notebook is made public in Zerve and `python3 scripts/check_zerve_public_share.py` reports `summary.ready_for_share_post_link: true`
- posted on: set after a verified public link exists and the human chooses and approves the final platform/post

## Last verification snapshot

- final demo link checked: yes, the safe local path was re-verified on 2026-04-24, and the live preview remains a separately verified optional upgrade
- demo evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/safe-local-demo-20260424T193220Z.json` (`refreshId`: `refresh-20260424T193220Z`)
- screenshot assets checked: yes, the local raw and slide-ready screenshot set was regenerated on 2026-04-24 against bundle `refresh-20260424T120713Z`, the repo-side crops now read cleanly without the earlier top-clipping, and the `Documents/Hackathons/ZerveHack` screenshot copies were refreshed to match
- deck link checked: yes, Slides API readback confirmed the compact 6-slide structure and updated speaker notes
- notes link checked: yes, Docs API readback confirmed the presenter notes and the Demo Link Notes doc, including the latest safe-local proof refresh
- office wording drift checked: yes, a 2026-04-24 readback pass confirmed the presenter notes doc, slide speaker notes, and visible slide body copy still match the latest repo wording, and the final submission-copy doc was refreshed and read back again later the same day to match the latest submission copy
- office folder checked: yes, `Documents/Hackathons/ZerveHack` was inspected directly on 2026-04-24 and contained exactly the expected seven MMR office artifacts without stray duplicates
- video link checked: not checked yet; this stays unresolved until a real video file or upload URL exists
- submission wording checked: yes, Docs API readback confirmed the final submission-copy reference content again after the latest submission-copy refresh
- public project status checked: yes, the latest retained authenticated metadata baseline still says `canvas.is_public: false`, so there is no verified public project/share URL yet; evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-public-status-20260423T055107Z.json`
- notebook public-route baseline checked: yes, latest retained route-check evidence still ends in the generic Zerve shell with `200`, while the same gate run still only reached auth `403`, so `summary.ready_for_share_post_link: false`; evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-public-route-check-20260424T194951Z.json`
- verified on: `2026-04-24`
- verified by: `Jefke`

## References

Use these during the final sprint:
- `docs/final-submission-sequence.md`
- `docs/submission-verification-checklist.md`
- `docs/office-layer-asset-checklist.md`
- `docs/submission-bundle.md`

## Done condition

This register is complete when all of these are filled in with real values:
- one confirmed primary demo path
- one chosen drilldown example
- deck location
- notes location
- final submission copy location
- final video location
- final submission URL and final public asset links
- last verification snapshot

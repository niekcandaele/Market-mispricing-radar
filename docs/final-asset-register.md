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
- verified on: `2026-04-25`
- verified by: `Jefke`
- notes: dedicated demo-link reference doc now exists in Google Workspace `Documents/Hackathons/ZerveHack` at `https://docs.google.com/document/d/1gA2LDL0E_2T-DfyQ8Fxxhw1DqvBjqPg2B5Fpl33c9UQ`; the one-command `./scripts/run_local_demo.sh` path was reverified on 2026-04-28, including Radar, Methodology, and Market Detail on the locked safe local default bundle, and should be used for recording and submission unless a final live preview check opens cleanly enough to justify switching

### Optional live upgrade path
- status: verified, but not chosen as the default path
- path: fresh live Zerve Streamlit preview reopened from the deploy tab
- URL or launch source: `https://1237c1f1-ee724b30.hub.zerve.cloud/` (fresh 2026-04-22 recovery) or a fresh equivalent reopened from the deploy tab
- verified on: `2026-04-22`
- verified by: `Jefke`
- notes: the latest concrete diagnosis is specific, not vague. Direct bearer-auth `POST /script/ecda0778-025a-4d74-898a-31ee7c3f709d/deploy_preview` returned `200`, emitted fresh preview metadata, the new host resolved immediately, then served ELB `503` during warm-up before converging to `200` and rendering the real Market Mispricing Radar app. Evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-preview-20260422T0534Z.json`

## Final drilldown example

- chosen market: `Putin out as President of Russia by December 31, 2026?`
- why this one: currently rank `1` in the refreshed locked safe local default bundle, visible in the default Radar slice, broadly understandable, and easier to demo cleanly in one take from Radar into Market Detail
- source doc reference: `docs/demo-market-shortlist.md`
- locked on: `2026-04-25`; reconfirmed against the retained safe-local proof unless the final live run clearly surfaces a cleaner example

## Final presentation assets

### Submission deck
- status: rebuilt from scratch with the updated `slides-generator` skill as a 9-slide HTML deck; the previous Google Slides deck was trashed per the updated deck instruction
- final title: `Market Mispricing Radar - Submission Deck (slides-generator HTML bundle)`
- deck shape used: `9-slide HTML deck`
- local HTML source: `artifacts/submission/slides-generator-deck/slides.html`
- local PDF to upload: `artifacts/submission/market-mispricing-radar-slides-generator-deck.pdf`
- local ZIP bundle to upload if the form accepts/supports it: `artifacts/submission/market-mispricing-radar-slides-generator-deck.zip`
- local upload manifest: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/local-submission-upload-manifest-20260426T0913Z.json`
- Drive HTML file: `https://drive.google.com/file/d/1Jdoz2KKe7Tgr602TwS8b-t69Aoj5YzHt/view`
- Drive bundle: `https://drive.google.com/file/d/1FFroHF0Gj-wie5AyykylTb08soQT79Bb/view`
- ZIP verification: local ZIP is non-empty, has no corrupt entries, and contains the deck root with `slides.html` plus all six required image assets; evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/deck-package-qa-20260426T0501Z.json`
- Drive deck-file verification: Drive HTML, ZIP, and PDF size/md5 checks match local artifacts; evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/drive-deck-files-qa-20260426T0501Z.json`
- Drive deck-link access: blocked for unauthenticated viewers right now (`401 Unauthorized` on PDF/HTML/ZIP view URLs); use local uploads or change Drive sharing before relying on those links for judges. Evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/drive-deck-unauth-open-check-20260426T0856Z.json`
- Drive PDF export: `https://drive.google.com/file/d/17smwphggaqZGOWXU5CNBgafynE4pAtKh/view`
- PDF verification: local PDF exists, is non-empty, and has 9 pages matching the rebuilt 9-slide deck
- alignment note: rebuilt around the locked safe local default, the Putin drilldown default, current proof screenshots, generated visual assets, and hidden per-slide speaker notes.
- QA note: local Playwright QA on 2026-04-25 confirmed 9 slides, 9 nav dots, all visible slide images loaded with alt text, no overflowing slides at 1280x720, and the vanilla `SlidePresentation` controller present; evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/html-deck-qa-20260426T0501Z.json`
- source docs:
  - `docs/submission-deck-outline.md`
  - `docs/slide-build-kit.md`
  - `docs/slide-copy-pack.md`

### Speaker notes / presenter notes
- status: created, refreshed on 2026-04-25 to match the rebuilt 9-slide HTML/PDF deck, aligned to the locked safe local default, readback-verified against the current recording path, and ready for recording use
- final title: `Market Mispricing Radar - Presenter Notes`
- location: `https://docs.google.com/document/d/17fNahknqysD206KM9VRocYRcOCOoQyrPDmsBVjQQhU4`
- alignment note: readback-verified so the presenter notes match the locked safe local default, the Putin drilldown default, the rebuilt 9-slide deck order, and the public-share blocker wording.
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

- status: link verified; still pending human platform/copy approval and actual post publication
- recommended platform: LinkedIn
- fallback platform: X
- draft pack: `docs/share-post-pack.md`
- screenshot default: `artifacts/submission/slide-ready/local-radar-view-16x9.png`
- project link to use: `https://app.zerve.ai/notebook/1b13702d-5502-47d1-b1e0-6ba476250dc4`; verified by `python3 scripts/check_zerve_public_share.py` with `summary.ready_for_share_post_link: true`
- posted on: set after the human chooses/approves the final platform and the public post is actually published

## Last verification snapshot

- retained evidence manifest: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/submission-evidence-manifest-20260425T1116Z.json` covers the current safe-local proof, deck QA, Drive deck checks, office-doc readbacks, live-preview recovery, repo-reference audit, and public-share link evidence; latest manifest self-check has no missing evidence paths and records the 2026-04-26T05:03Z public gate as share-ready
- final pre-submit sweep: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/final-pre-submit-sweep-20260428T1547Z.json` reports `all_green_before_human_gates: false`; remaining gates are final video recording, Devpost submission, human-approved public share post, and final URL capture
- final demo link checked: yes, the safe local path was re-verified on 2026-04-28, and the live preview remains a separately verified optional upgrade
- demo evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/safe-local-demo-20260428T050332Z.json` (`refreshId`: `refresh-20260428T050332Z`)
- screenshot assets checked: yes, the local raw and slide-ready screenshot set was regenerated on 2026-04-24 against bundle `refresh-20260424T120713Z`, the repo-side crops now read cleanly without the earlier top-clipping, and the `Documents/Hackathons/ZerveHack` screenshot copies were refreshed to match
- deck link checked: yes, local Playwright QA confirmed the rebuilt 9-slide HTML deck structure, navigation dots, image loading, alt text, hidden notes, and no 1280x720 slide overflow
- notes link checked: blocked for the 2026-04-28 safe-local refresh because `gws` auth now fails with `invalid_grant`; previous successful office-doc readback remains `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/office-docs-readback-qa-20260427T1223Z.json`
- office wording drift checked: last successful readback was 2026-04-27; 2026-04-28 refresh is blocked by expired/revoked Google Workspace auth (`gws invalid_grant`), so rerun `gws auth login` before treating Workspace docs as current
- office folder checked: yes, `Documents/Hackathons/ZerveHack` was inspected directly on 2026-04-25 after the deck rebuild and PDF export; the previous Google Slides deck is trashed, and the folder contains the expected HTML deck, deck ZIP bundle, PDF export, docs, and screenshot assets without duplicate presentation decks
- video link checked: not checked yet; this stays unresolved until a real video file or upload URL exists
- submission wording checked: yes, Docs API readback confirmed the final submission-copy reference content again after the latest submission-copy refresh
- repo reference audit checked: yes, `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/repo-reference-audit-20260425T1146Z.json` found no missing real proof/artifact paths; the only misses are intentional branch-name examples in `docs/repo-workflow.md`
- public project status checked: yes, the latest retained public-share checker confirms authenticated `canvas.is_public: true` and browser-rendered route verification; public URL: `https://app.zerve.ai/notebook/1b13702d-5502-47d1-b1e0-6ba476250dc4`; evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-public-route-check-20260426T0503Z.json`
- notebook public-route baseline checked: yes, latest retained route-check evidence uses browser-rendered verification and reports `summary.ready_for_share_post_link: true`; evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-public-route-check-20260426T0503Z.json`
- verified on: `2026-04-28`
- verified by: `Jefke`

## References

Use these during the final sprint:
- `docs/final-human-handoff.md`
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

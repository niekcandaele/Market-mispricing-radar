# Final Asset Register

## Purpose

This is the one place to record the actual final assets used on submission day.

Use it when the real last-mile artifacts start to exist, so the submission does not depend on memory, chat history, or stale breadcrumbs.

## Current status

This is no longer just a blank template.

The repo-side source material is strong, the Google Workspace office artifacts are real and aligned, and the remaining unknowns are the final live checked links plus the actual submission-day execution items.

## Final demo path

### Primary demo path
- status: ready, and currently the locked safe default
- chosen path: local fallback
- URL or launch source:
  - `./scripts/run_local_demo.sh`
- default runtime details:
  - refresh limit: `200`
  - address: `127.0.0.1`
  - port: `8768`
- verified on: `2026-04-22`
- verified by: `Jefke`
- notes: dedicated demo-link reference doc now exists in Google Workspace `Documents` at `https://docs.google.com/document/d/1gA2LDL0E_2T-DfyQ8Fxxhw1DqvBjqPg2B5Fpl33c9UQ`; the one-command `./scripts/run_local_demo.sh` path was reverified on 2026-04-22, including Radar, Methodology, and Market Detail on the current safe local bundle, and should be used for recording and submission unless a final live preview check opens cleanly enough to justify switching

### Optional live upgrade path
- status: verified, but not chosen as the safe default
- path: fresh live Zerve Streamlit preview reopened from the deploy tab
- URL or launch source: `https://1237c1f1-ee724b30.hub.zerve.cloud/` (fresh 2026-04-22 recovery) or a fresh equivalent reopened from the deploy tab
- verified on: `2026-04-22`
- verified by: `Jefke`
- notes: the latest concrete diagnosis is no longer a vague "flaky preview" label. Direct bearer-auth `POST /script/ecda0778-025a-4d74-898a-31ee7c3f709d/deploy_preview` returned `200`, emitted fresh preview metadata, the new host resolved immediately, then served ELB `503` during warm-up before converging to `200` and rendering the real Market Mispricing Radar app. Evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-preview-20260422T0534Z.json`

## Final drilldown example

- chosen market: `GTA VI released before June 2026?`
- why this one: currently rank `3` in the verified local fallback bundle, visible in the default Radar slice, broadly understandable, and easier to demo cleanly in one take from Radar into Market Detail
- source doc reference: `docs/demo-market-shortlist.md`
- locked on: `2026-04-22` (updated to match the current safe local bundle unless the final live run clearly surfaces a cleaner example)

## Final presentation assets

### Google Slides deck
- status: created, compact 6-slide structure tightened to the repo copy pack with embedded speaker notes, a visually coherent styling pass, a readability-tightening pass, small section-hierarchy kickers on the body slides, right-side visual proof cards on the core body slides, and an embedded safe demo-path note in the product-proof speaker notes; acceptable for submission with only optional low-risk layout polish left
- final title: `Market Mispricing Radar - Submission Deck`
- deck shape used: `compact 6-slide`
- location: `https://docs.google.com/presentation/d/1MYzlPnXoFbulK9SopHM9Uh1rmAPNRVC8uzH_NurZxKA`
- version note: initial CLI-created deck shell placed in `Documents` on 2026-04-21, then populated, tightened, styled, given embedded slide speaker notes, updated with soft coordinated slide backgrounds, and synced again on 2026-04-22 so the product-proof speaker notes point at the current safe local GTA drilldown and cleaner deployed-product wording
- source docs:
  - `docs/submission-deck-outline.md`
  - `docs/slide-build-kit.md`
  - `docs/slide-copy-pack.md`

### Speaker notes / presenter notes
- status: created, structured presenter notes populated, now includes default visual pairings for the compact deck, safe demo-path guidance, and corrected alignment to the actual compact slide order, and is ready for recording use
- final title: `Market Mispricing Radar - Presenter Notes`
- location: `https://docs.google.com/document/d/17fNahknqysD206KM9VRocYRcOCOoQyrPDmsBVjQQhU4`
- version note: initial CLI-created notes doc with starter content placed in `Documents` on 2026-04-21, then rewritten into slide-by-slide presenter notes, extended with default office-layer visual cues, aligned to the safe local-fallback demo plan, corrected to match the compact deck slide order, and updated on 2026-04-22 to use the GTA drilldown as the current safe local default
- source docs:
  - `docs/judge-demo-script.md`
  - `docs/video-voiceover-script.md`
  - `docs/video-recording-run-sheet.md`
  - `docs/presenter-cheat-sheet.md`

### Final submission copy reference
- status: created and tightened into a cleaner paste-ready baseline, may still get a last tiny wording trim before final form paste
- final title: `Market Mispricing Radar - Final Submission Copy`
- location: `https://docs.google.com/document/d/1Y6xAXczjmsoWiRsbQ_0HmR3EzNTBYxRkgFjK9-525sM`
- version note: initial CLI-created submission-copy reference doc placed in `Documents` on 2026-04-21, then tightened to remove repo-facing packaging language and sharpen the submission wording

### Demo link reference
- status: created
- final title: `Market Mispricing Radar - Demo Link Notes`
- location: `https://docs.google.com/document/d/1gA2LDL0E_2T-DfyQ8Fxxhw1DqvBjqPg2B5Fpl33c9UQ`
- version note: created in `Documents` on 2026-04-21 with preferred live path, verified local fallback, drilldown defaults, and explicit default visual pairings, then updated on 2026-04-22 to use `./scripts/run_local_demo.sh` and the GTA drilldown as the current safe local default
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
- Google Workspace `Documents` copies:
  - `Market Mispricing Radar - local-radar-view-16x9.png` — file id `1cJwxEV_aAVBadI1ZEbLNg1r7s38YISVl`
  - `Market Mispricing Radar - local-market-detail-view-16x9.png` — file id `1heVTGPL-OH4q4IFHOIZbckXHssnkUZDv`
  - `Market Mispricing Radar - local-methodology-view-16x9.png` — file id `1ABee8QF2x6RYPEZo43LEn9h0H4CI1Y4l`

Remaining `pending` values below are intentional submission-time fields, not packaging gaps.

## Final video asset

- status: not recorded yet
- title or filename: pending final recording output
- location or upload URL: pending video upload
- recorded on: pending recording session
- notes: use `docs/video-recording-run-sheet.md`

## Final submission form

- status: not submitted yet
- Devpost submission URL: pending real submission
- final project URL used in form: pending final form fill
- video URL used in form: pending final video upload
- screenshot/image URL used in form: pending final form fill
- submitted on: pending submission event

## Required public share post

- status: pending human platform choice and approval
- recommended platform: LinkedIn
- fallback platform: X
- draft pack: `docs/share-post-pack.md`
- screenshot default: `artifacts/submission/slide-ready/local-radar-view-16x9.png`
- project link to use: unresolved blocker, needs a clean verified public Zerve project/share URL before posting
- posted on: pending share action

## Last verification snapshot

- final demo link checked: local fallback path re-verified on 2026-04-22 through `./scripts/check_safe_local_demo.sh` with refreshed GTA detail-drilldown evidence at `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/safe-local-demo-20260422T231924Z.json`; optional live preview also verified on 2026-04-22 at `https://1237c1f1-ee724b30.hub.zerve.cloud/` after the expected warm-up window (`503` then `200`)
- deck link checked: yes, Slides API readback confirmed compact 6-slide structure and updated speaker notes
- notes link checked: yes, Docs API readback confirmed the rewritten slide-by-slide presenter notes and updated demo-link notes
- video link checked: pending final recording and upload
- submission wording checked: yes, Docs API readback confirmed the final submission-copy reference content
- verified on: `2026-04-22`
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

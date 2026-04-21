# Final Asset Register

## Purpose

This is the one place to record the actual final assets used on submission day.

Use it when the browser/auth blocker clears and the real last-mile artifacts start to exist, so the submission does not depend on memory, chat history, or stale breadcrumbs.

## Current status

Right now this is a template.

The repo-side source material is strong, but the actual final office-layer assets and live checked links are still blocked or not yet created.

## Final demo path

### Primary demo path
- status: pending final check
- chosen path: `TBD`
- URL or launch source: `TBD`
- verified on: `TBD`
- verified by: `TBD`
- notes: use the live Zerve preview if healthy, otherwise switch to the verified local fallback

### Backup demo path
- status: ready
- path: local fallback
- commands:
  - `python3 scripts/export_streamlit_bundle.py --limit 200`
  - `MMR_APP_BUNDLE_PATH=artifacts/streamlit/app_bundle.json uv run --with streamlit streamlit run zerve/app/streamlit_app.py`
- notes: this is the safe fallback if the live preview is flaky on submission day

## Final drilldown example

- chosen market: `TBD`
- why this one: `TBD`
- source doc reference: `docs/demo-market-shortlist.md`
- locked on: `TBD`

## Final presentation assets

### Google Slides deck
- status: not created yet
- final title: `Market Mispricing Radar - Submission Deck`
- deck shape used: `TBD` (`full 8-slide` or `compact 6-slide`)
- location: `TBD`
- version note: `TBD`
- source docs:
  - `docs/submission-deck-outline.md`
  - `docs/slide-build-kit.md`
  - `docs/slide-copy-pack.md`

### Speaker notes / presenter notes
- status: not created yet
- final title: `Market Mispricing Radar - Presenter Notes`
- location: `TBD`
- version note: `TBD`
- source docs:
  - `docs/judge-demo-script.md`
  - `docs/video-recording-run-sheet.md`
  - `docs/presenter-cheat-sheet.md`

### Final submission copy reference
- status: not created yet
- final title: `Market Mispricing Radar - Final Submission Copy`
- location: `TBD`
- version note: `TBD`
- source docs:
  - `docs/submission-form-map.md`
  - `docs/submission-copy-draft.md`
  - `docs/submission-short-variants.md`

## Final screenshot set used in slides or form

- product hero screenshot: `TBD`
- explainability screenshot: `TBD`
- methodology screenshot: `TBD`
- preferred repo assets today:
  - `artifacts/submission/slide-ready/local-radar-view-16x9.png`
  - `artifacts/submission/slide-ready/local-market-detail-view-16x9.png`
  - `artifacts/submission/slide-ready/local-methodology-view-16x9.png`

## Final video asset

- status: not recorded yet
- title or filename: `TBD`
- location or upload URL: `TBD`
- recorded on: `TBD`
- notes: use `docs/video-recording-run-sheet.md`

## Final submission form

- status: not submitted yet
- Devpost submission URL: `TBD`
- final project URL used in form: `TBD`
- video URL used in form: `TBD`
- screenshot/image URL used in form: `TBD`
- submitted on: `TBD`

## Last verification snapshot

- final demo link checked: `TBD`
- deck link checked: `TBD`
- notes link checked: `TBD`
- video link checked: `TBD`
- submission wording checked: `TBD`
- verified on: `TBD`
- verified by: `TBD`

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

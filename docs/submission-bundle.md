# Submission Bundle Index

## Purpose

This document is the single inspection point for submission-facing artifacts.

Use it to answer four questions quickly:
- what is the best demo entrypoint
- what should Niek/Cata say
- what presentation material already exists
- what is still missing before the hackathon submission is truly ready

## Current status snapshot

### Demo
- status: usable
- primary live entrypoint: current Zerve Streamlit preview from the deploy tab
- repo docs: `docs/judge-demo-script.md`, `docs/app-flow.md`
- local fallback: verified locally

### Slides
- status: not created yet
- repo source material: `docs/submission-deck-outline.md`
- required next artifact: polished Google Slides deck
- current blocker: Google login is not currently usable from the available managed browser path

### Video / talking track
- status: draft-ready
- repo source material: `docs/judge-demo-script.md`, `docs/submission-deck-outline.md`, `docs/video-recording-run-sheet.md`, `docs/demo-market-shortlist.md`
- required next artifact: final recording outline in Google Docs or deck speaker notes
- current blocker: office-layer note creation is tied to the same Google/browser constraint as the slide deck

### Submission copy
- status: draft-ready
- repo source material: `docs/submission-copy-draft.md`
- required next artifact: paste/adapt into the actual hackathon submission form

### Submission readiness
- status: not submission-complete yet
- reason: the project now has a strong app and strong narrative source docs, but the final office-style artifacts still need to be created and checked, and the current browser/auth state is still blocking that office-layer finish

## Demo entrypoints

### Preferred live demo
- open the current deployed Streamlit preview from the Zerve deploy tab
- preview URLs rotate, so the deploy tab is the reliable source of the latest live demo link

### Known recent working previews
- `https://0bd71592-a1a1481b.hub.zerve.cloud`
- `https://b1f7cd6e-7de84c75.hub.zerve.cloud`
- `https://f25e450d-8a72464f.hub.zerve.cloud`

These should be treated as useful breadcrumbs, not permanent URLs.

### Local fallback demo
```bash
python3 scripts/export_streamlit_bundle.py --limit 200
MMR_APP_BUNDLE_PATH=artifacts/streamlit/app_bundle.json uv run --with streamlit streamlit run zerve/app/streamlit_app.py
```

## Story / talking-track sources

### Judge-facing demo script
- `docs/judge-demo-script.md`
- best for the live walkthrough and short video narrative

### Submission deck outline and speaker notes
- `docs/submission-deck-outline.md`
- best for turning the repo story into slides and presenter notes

### Submission copy draft
- `docs/submission-copy-draft.md`
- best for the hackathon form fields, project summary, and one-minute written pitch

### Submission short variants
- `docs/submission-short-variants.md`
- best for cramped form fields, taglines, and short summaries under length pressure

### Video recording run sheet
- `docs/video-recording-run-sheet.md`
- best for the actual one-take recording order and beat-by-beat filming flow

### Demo market shortlist
- `docs/demo-market-shortlist.md`
- best for quickly choosing a strong drilldown example without improvising live

### Submission form map
- `docs/submission-form-map.md`
- best for turning the repo copy into actual form answers without hunting across docs

### Final submission sequence
- `docs/final-submission-sequence.md`
- best for the exact day-of-submission order once the browser/auth blocker is gone

### Presenter cheat sheet
- `docs/presenter-cheat-sheet.md`
- best for the live verbal pitch and likely judge follow-up questions

### Submission visual assets map
- `docs/submission-visual-assets.md`
- best for using the current screenshot set in slides or submission materials without guessing

### Slide build kit
- `docs/slide-build-kit.md`
- best for turning the outline plus screenshots into an actual deck quickly once slides can be built

### Slide copy pack
- `docs/slide-copy-pack.md`
- best for paste-ready titles and bullets during the actual slide build

### Submission verification checklist
- `docs/submission-verification-checklist.md`
- best for the final pre-recording and pre-submission sweep

### App flow doc
- `docs/app-flow.md`
- best for checking whether the product flow and screen logic still support the intended demo

## Strongest proof points to highlight

- real Zerve notebook pipeline is live end to end
- deployed Streamlit app reads notebook outputs through Zerve variable loading
- the product ranks markets with explanation-rich drilldowns, not just opaque scores
- category quality and judge-facing copy were validated directly in the live deployed preview
- the MVP is intentionally honest about scope, caveats, and what the score does not claim

## Remaining submission-critical gaps

### Still missing
- polished Google Slides deck
- final Google Doc or equivalent office-layer speaker notes / recording plan
- one final checked demo link or presentation flow immediately before submission
- final pass to verify all submission-facing links and artifacts open cleanly

### Current blocker snapshot
- Google currently rejects sign-in in the available managed browser, so slide-deck creation is waiting on a browser session Google accepts
- the latest live Zerve preview recheck is also waiting on a usable authenticated browser state instead of stale preview breadcrumbs

### Not a blocker right now, but still needed before calling the project ready
- collect the final deck, notes, and demo entrypoint in Google Workspace `Documents`
- do a final presentation-quality verification pass instead of only a code/demo verification pass

## Recommended next steps

1. create the Google Slides deck from `docs/submission-deck-outline.md`
2. create the Google Doc with speaker notes / recording plan from `docs/judge-demo-script.md`
3. verify the latest live preview path right before recording
4. do one final submission-quality sweep across demo, slides, notes, and links

## Honest readiness call

Right now the project looks much stronger than a code-only prototype.

It has:
- a live deployed demo path
- a verified local fallback demo path
- a polished judge-facing app
- a judge/demo script
- a deck outline with speaker notes
- a one-take video run sheet
- a demo-safe market shortlist

It does **not** yet have:
- the final polished slides
- the final office-layer notes artifact
- a final pre-submission verification pass across the full submission bundle
- a browser/auth path that can complete the remaining office-layer and live-preview checks

So this should be treated as **near-ready, but not submission-complete yet**.

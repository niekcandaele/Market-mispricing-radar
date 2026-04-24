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
- default path: locked safe local default, which remains the recording/submission path because it is one-command and presentation-safe
- optional live upgrade: current Zerve Streamlit preview from the deploy tab, but only if it opens cleanly at the final check
- source docs: `docs/judge-demo-script.md`, `docs/app-flow.md`
- note: a fresh 2026-04-22 live preview check did recover a real working preview after warm-up, but that does not change the safe-default local choice

### Slides
- status: compact 6-slide deck is built, styled, and readably polished in Google Workspace `Documents`, with embedded speaker notes and proof visuals already in place
- source doc: `docs/submission-deck-outline.md`
- remaining work: optional low-risk layout polish only if it is clearly worth it

### Video / talking track
- status: presenter notes exist in Google Workspace `Documents`, align with the compact deck order, and match the deck speaker notes
- source docs: `docs/judge-demo-script.md`, `docs/video-voiceover-script.md`, `docs/submission-deck-outline.md`, `docs/video-recording-run-sheet.md`, `docs/demo-market-shortlist.md`
- remaining work: record the demo cleanly on the chosen path

### Submission copy
- status: paste-ready source material exists in both the repo and Google Workspace
- source doc: `docs/submission-copy-draft.md`
- remaining work: paste or adapt it into the actual hackathon submission form

### Submission readiness
- status: not submission-complete yet
- reason: the project now has a strong app, real office-layer artifacts, and strong narrative source docs, but it still needs final demo/video/submission execution before it should be called submission-complete; deck work is now optional polish, not a core missing artifact

## Demo entrypoints

### Optional live demo upgrade
- open the current deployed Streamlit preview from the Zerve deploy tab, or recover it directly with bearer-auth `POST /script/<deployment_script_id>/deploy_preview`
- preview URLs rotate, so the deploy tab or direct script trigger is the reliable source of the latest live demo link
- expect brief warm-up behavior on a fresh host: the current observed pattern is ELB `503`, sometimes one timeout, then `200` and a real Streamlit render within about 45 seconds
- if the latest host never clears that warm-up phase, do not spend more submission time on it, use the locked safe local default instead

### Known recent working previews
- `https://1237c1f1-ee724b30.hub.zerve.cloud` (2026-04-22 fresh recovery, observed `503` warm-up before stable `200`)
- `https://0bd71592-a1a1481b.hub.zerve.cloud`
- `https://b1f7cd6e-7de84c75.hub.zerve.cloud`
- `https://f25e450d-8a72464f.hub.zerve.cloud`

These should be treated as useful breadcrumbs, not permanent URLs.

### Safe local default demo
This is now the submission-safe chosen path unless a fresh live preview opens cleanly at the final check.

Right before the real recording take on this path, run the one-command final sweep:

```bash
./scripts/check_safe_local_demo.sh
```

Then launch the demo with:

```bash
./scripts/run_local_demo.sh
```

Defaults:
- refresh limit: `200`
- address: `127.0.0.1`
- port: `8768`

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

### Video voiceover script
- `docs/video-voiceover-script.md`
- best for the literal spoken recording pass when the beat sheet is too abstract

### Recording preflight checklist
- `docs/recording-preflight-checklist.md`
- best for the final go/no-go setup pass right before recording

### Demo market shortlist
- `docs/demo-market-shortlist.md`
- best for quickly choosing a strong drilldown example without improvising live

### Submission form map
- `docs/submission-form-map.md`
- best for turning the repo copy into actual form answers without hunting across docs

### Final submission sequence
- `docs/final-submission-sequence.md`
- best for the exact day-of-submission order while the remaining work is concentrated in recording, form fill, share-post execution, and final link capture

### Presenter cheat sheet
- `docs/presenter-cheat-sheet.md`
- best for the live verbal pitch and likely follow-up questions

### Submission visual assets map
- `docs/submission-visual-assets.md`
- best for using the current screenshot set in slides or submission materials without guessing

### Slide build kit
- `docs/slide-build-kit.md`
- best for turning the outline plus screenshots into an actual deck quickly once slides can be built

### Slide copy pack
- `docs/slide-copy-pack.md`
- best for paste-ready titles and bullets during the actual slide build

### Office-layer asset checklist
- `docs/office-layer-asset-checklist.md`
- best for making sure the final Google Workspace handoff is clean while the remaining live-preview blocker is being worked around

### Final asset register
- `docs/final-asset-register.md`
- best for recording the actual final demo, deck, notes, video, and submission links on submission day

### Final readiness status
- `docs/final-readiness-status.md`
- best for the shortest honest readiness snapshot of what is done, blocked, and still needed

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
- category quality and presentation copy were validated directly in the live deployed preview
- the MVP is intentionally honest about scope, caveats, and what the score does not claim

## Remaining submission-critical gaps

### Still missing
- final visual polish on the compact Google Slides deck
- actual recording execution against the aligned presenter notes / recording plan
- one final checked demo link or presentation flow immediately before submission
- final pass to verify all submission-facing links and artifacts open cleanly

### Current blocker snapshot
- Google Workspace office artifacts now exist and are no longer blocked on auth
- the live deploy seam is now better than before: a valid deployed Streamlit script was recovered from Zerve canvas metadata, the stale probe deploy was directly patched back to the repo app, and a fresh 2026-04-22 bearer-auth preview trigger produced a new working preview again
- the current concrete live-preview behavior is now understood: a fresh host can resolve immediately, serve ELB `503` during warm-up, then turn into a healthy rendered Streamlit app about 45 seconds later
- the remaining practical reason not to switch defaults is operational simplicity, not mystery failure: the locked safe local default is already one-command and fully presentation-safe

### Not a blocker right now, but still needed before calling the project ready
- keep the final deck, notes, submission-copy doc, and demo-entry reference tidy in Google Workspace `Documents`
- do a final presentation-quality verification pass instead of only a code/demo verification pass

## Recommended next steps

While the live-preview path remains an optional upgrade:
1. keep polishing the compact deck and presenter notes
2. treat the locked safe local default as the presentation-safe default path
3. keep late-stage polish focused on consistency, verification freshness, and handoff clarity
4. use the repaired direct deploy-script path if a fresh live host needs to be regenerated right before recording

If choosing to use the live preview:
1. trigger a fresh preview right before recording
2. allow one short warm-up window if the host first returns `503`
3. lock the final demo choice and drilldown example once the app renders cleanly
4. do one final submission-quality sweep across demo, slides, notes, and links

## Honest readiness call

Right now the project looks much stronger than a code-only prototype.

It has:
- a live deployed demo path
- a locked safe local default demo path
- a polished deployed app
- a demo script
- a deck outline with speaker notes
- a slide build kit and slide copy pack
- a one-take video run sheet
- a literal voiceover script for recording
- a recording preflight checklist
- a demo-safe market shortlist
- a final asset register and final readiness-status doc

It does **not** yet have:
- a final pre-submission verification pass across the full submission bundle
- the actual recorded video and final submission links
- the required public share post and its final public URL

Current sharp blocker:
- no verified public Zerve project/share URL yet. The latest authenticated canvas metadata evidence still says `canvas.is_public: false`, and the public-share gate is still red.
- the required share post stays blocked until the notebook is made public in Zerve and the resulting public link is verified
- the next action is explicit: use the Zerve share/privacy control to make the notebook public, then rerun `python3 scripts/check_zerve_public_share.py`
- only clear the blocker when the checker reports `summary.ready_for_share_post_link: true`
- the latest retained notebook-route baseline still ends in the generic Zerve shell plus auth `403`, so the gate is still failing the actual public-route check
- evidence:
  - `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-public-status-20260423T055107Z.json`
  - `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-public-route-check-20260423T230244Z.json`

So this should be treated as **near-ready, but not submission-complete yet**.

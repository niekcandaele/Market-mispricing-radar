# Submission Bundle Index

## Purpose

This document is the single inspection point for submission-facing artifacts.

Use it to answer four questions quickly:
- what is the best demo entrypoint
- what should Niek/Cata say
- what presentation material already exists
- what is still missing before the hackathon submission is truly ready

If someone needs only the shortest operational handoff, use `docs/final-human-handoff.md` first.

## Current status snapshot

Retained evidence manifest:
- `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/submission-evidence-manifest-20260425T1116Z.json`
- includes repo-reference audit evidence; no missing real proof/artifact paths were found
- latest manifest self-check has no missing evidence paths and records the 2026-04-28T16:36Z public gate as share-ready

### Demo
- status: usable, with the locked safe local default reverified on 2026-04-28 through the one-command safe-local sweep, which now writes and rotates the retained proof automatically; current retained baseline: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/safe-local-demo-20260428T050332Z.json` (`refreshId`: `refresh-20260428T050332Z`)
- default path: locked safe local default, which remains the recording/submission path because it is one-command and presentation-safe
- optional live upgrade: current Zerve Streamlit preview from the deploy tab, but only if it opens cleanly at the final check
- source docs: `docs/judge-demo-script.md`, `docs/app-flow.md`
- office note: Google Demo Link Notes was last successfully read back on 2026-04-27; the 2026-04-28 proof refresh is blocked until `gws auth login` repairs Workspace auth
- note: a fresh 2026-04-22 live preview check did recover a real working preview after warm-up, but that does not change the locked safe local default choice

### Slides
- status: previous Google Slides deck was trashed, then the deck was rebuilt from scratch with the updated `slides-generator` skill as a 9-slide HTML deck with generated visuals, proof screenshots, and hidden per-slide notes
- source doc: `docs/submission-deck-outline.md`
- deck artifact: `artifacts/submission/slides-generator-deck/slides.html`
- Drive bundle: `Market Mispricing Radar - Submission Deck (slides-generator HTML bundle)` (`1FFroHF0Gj-wie5AyykylTb08soQT79Bb`); local ZIP QA confirmed the bundle contains `slides.html` plus all six required image assets with no corrupt entries
- Drive PDF export: `Market Mispricing Radar - Submission Deck (PDF)` (`17smwphggaqZGOWXU5CNBgafynE4pAtKh`)
- remaining work: optional low-risk layout polish only if it is clearly worth it

### Video / talking track
- status: presenter notes exist in Google Workspace `Documents/Hackathons/ZerveHack`, and the rebuilt HTML deck includes hidden per-slide notes aligned to the same locked safe local default story
- source docs: `docs/judge-demo-script.md`, `docs/video-voiceover-script.md`, `docs/submission-deck-outline.md`, `docs/video-recording-run-sheet.md`, `docs/demo-market-shortlist.md`
- remaining work: record the demo cleanly on the chosen path

### Submission copy
- status: paste-ready submission copy exists; the live Google submission-copy doc was last refreshed/read back on 2026-04-27 and now needs `gws auth login` before it can be refreshed with the 2026-04-28 proof
- source doc: `docs/submission-copy-draft.md`
- remaining work: paste or adapt it into the actual hackathon submission form

### Agentic Report
- status: optional Zerve-native report generated and verified in the authenticated report view
- report: `https://app.zerve.ai/report/4b2bcec4-48d2-4960-b051-cd465aa18a56`
- source: `zerve/reports/agentic-market-mispricing-report.Rmd`
- instructions/evidence: `docs/agentic-report-upgrade.md`
- caveat: public API readback succeeds, but unauthenticated browser rendering still shows Zerve login/build, so keep the verified public notebook URL as the main judge/share link

### Submission readiness
- status: not submission-complete yet
- reason: the project has a strong app, polished presentation artifacts, and ready submission copy, but it still needs final demo/video/submission execution before it should be called submission-complete; deck work is now optional polish, not a core missing artifact

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

### Agentic Report upgrade
- `docs/agentic-report-upgrade.md`
- best for using the verified Agentic Report as an optional Zerve-native wow-factor, with the public-browser caveat

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
- optional final visual polish on the rebuilt slides-generator HTML deck
- actual recording execution against the aligned presenter notes / recording plan
- one final checked demo link or presentation flow immediately before submission
- final pass to verify all submission-facing links and artifacts open cleanly

### Current final-action snapshot
- Google Workspace office artifacts exist, but refresh/readback is currently blocked by `gws invalid_grant` until `gws auth login` is rerun
- the live deploy seam is now better than before: a valid deployed Streamlit script was recovered from Zerve canvas metadata, the stale probe deploy was directly patched back to the repo app, and a fresh 2026-04-22 bearer-auth preview trigger produced a new working preview again
- the current concrete live-preview behavior is now understood: a fresh host can resolve immediately, serve ELB `503` during warm-up, then turn into a healthy rendered Streamlit app about 45 seconds later
- the remaining practical reason not to switch defaults is operational simplicity, not mystery failure: the locked safe local default is already one-command and fully presentation-safe

### Not a blocker right now, but still needed before calling the project ready
- if using Agentic Reports, open the verified report in the authenticated Zerve session and keep the public-browser caveat honest
- after `gws auth login`, refresh/read back the final notes, submission-copy doc, and demo-entry reference in Google Workspace `Documents/Hackathons/ZerveHack`
- do a final presentation-quality verification pass instead of only a code/demo verification pass

## Recommended next steps

While the live-preview path remains an optional upgrade:
1. keep any remaining deck work limited to low-risk polish on the rebuilt 9-slide HTML/PDF package and presenter notes
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
- verified public Zerve notebook URL is available: `https://app.zerve.ai/notebook/1b13702d-5502-47d1-b1e0-6ba476250dc4`. The latest retained checker reports `summary.ready_for_share_post_link: true`.
- the required share post is unblocked on link availability, but still requires human platform/copy approval before posting
- the next action is the human-approved public post itself; rerun `python3 scripts/check_zerve_public_share.py` only as a final link sanity check
- only clear the blocker when the checker reports `summary.ready_for_share_post_link: true`
- the latest retained route-check evidence uses browser-rendered verification and reports `route_verified: true`, `auth_public_confirmed: true`, and `ready_for_share_post_link: true`
- evidence:
  - `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-public-route-check-20260428T1636Z.json`

So this should be treated as **near-ready, but not submission-complete yet**.

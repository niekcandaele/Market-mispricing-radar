# Final Submission Sequence

## Purpose

This is the last-mile runbook for the day of submission.

Use it when the remaining work needs to happen in the right order without thrashing.

## Current blocker context

The submission package is strong, and Google Workspace artifact creation is no longer the blocker.

Current state:
- Google Slides and Google Docs are available through the authenticated `gws` CLI path
- the locked safe local default was reverified on 2026-04-24 through the one-command safe-local sweep, with the current retained baseline at `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/safe-local-demo-20260424T140336Z.json` (`refreshId`: `refresh-20260424T140336Z`), and remains the demo path unless a fresh live preview opens cleanly enough to justify switching at the final moment
- the live Zerve preview now has a concrete behavior model: a fresh host can resolve immediately, warm through a brief ELB `503` window, then turn healthy

This runbook is ready to use for the office-layer and submission-day steps now, with the live demo recheck treated as a separate final decision.

## Submission-day order of operations

### 1. Lock the demo path first

Why first:
- everything else depends on knowing which demo entrypoint is truly healthy right now

Do:
- treat the locked safe local default as the default path
- if there is still time and attention for one final upgrade attempt, open the current Zerve deploy tab and re-open the freshest preview
- only switch away from the safe local default if the live preview opens cleanly and behaves correctly
- confirm the chosen path actually loads and that Radar, Market Detail, and Methodology behave as expected

If healthy:
- use the chosen path consistently through recording and submission

If the live host never clears warm-up:
- keep the locked safe local default and move on immediately instead of burning time

References:
- `docs/submission-verification-checklist.md`
- `docs/judge-demo-script.md`

### 2. Lock the demo example market

Why now:
- once the demo path is locked, pick the exact drilldown example before making slides or recording

Do:
- choose the strongest current drilldown candidate
- for the verified safe local path, default to `GTA VI released before June 2026?` unless the live run clearly suggests a better example
- avoid awkward or overly niche examples if a cleaner one is available

References:
- `docs/demo-market-shortlist.md`
- `docs/video-recording-run-sheet.md`

### 3. Refine the Google Slides deck

Why before recording:
- the deck clarifies the story and can double as backup structure for the video

Do:
- treat the compact deck as the default
- only do another screenshot/layout or readability pass if there is a clearly beneficial, low-risk improvement
- keep it concise and visually clean
- include problem, solution, product flow, proof/demo, why Zerve matters, and next steps
- do not overpack it with implementation trivia

Reference:
- `docs/submission-deck-outline.md`

### 4. Keep the office-layer notes artifact aligned

Why now:
- the speaker notes or recording notes should match the actual deck and chosen demo path

Do:
- keep the Google Doc and deck speaker notes aligned with the chosen demo path
- use the demo script as the base
- keep the one-take run sheet folded into the notes so the recording flow stays operational, not just conceptual

References:
- `docs/judge-demo-script.md`
- `docs/video-voiceover-script.md`
- `docs/video-recording-run-sheet.md`

### 5. Record the demo video

Why after deck and notes:
- by this point the story, example market, and flow should already be stable

Do:
- run the recording preflight checklist first
- on the safe local default path, run `./scripts/check_safe_local_demo.sh` right before the real take
- use the retained JSON it writes under `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/` as the current proof, and let the script archive the previously active safe-local baseline automatically
- use the one-take run sheet
- use the voiceover script if a literal spoken pass is helpful
- keep the video to one strong story arc
- use the verified chosen demo path
- if the live path degrades, switch to the safe local default immediately
- do not re-decide the demo path mid-take unless the current one is clearly broken

References:
- `docs/recording-preflight-checklist.md`
- `docs/video-voiceover-script.md`
- `docs/video-recording-run-sheet.md`
- `docs/demo-market-shortlist.md`

### 6. Fill the submission form

Why after recording:
- then the form can point to the final chosen assets instead of placeholders

Do:
- use the form map for exact field wording
- prefer the shorter variants if the form fields are cramped
- make sure the wording matches the actual current demo and video

References:
- `docs/submission-form-map.md`
- `docs/submission-copy-draft.md`
- `docs/submission-short-variants.md`

### 7. Handle the required public share post

Why before the final submit click:
- the live Devpost page currently lists a public share post tagging Zerve as a required submission item
- this crosses the normal no-external-posting boundary, so the human should choose the platform and approve the final wording

Do:
- default to one simple LinkedIn post unless there is a better human preference
- use the prepared draft pack instead of improvising under time pressure
- attach one clean screenshot and the final public project link
- if the latest check still says the project is not public in Zerve, first use the Zerve share/privacy control to make it public
- after the privacy change, first recheck the notebook share route at `https://app.zerve.ai/notebook/1b13702d-5502-47d1-b1e0-6ba476250dc4`
- use `python3 scripts/check_zerve_public_share.py` for the route-plus-auth sanity check
- the checker can auto-attempt a best-effort Chromium token extraction path, but prefer a fresh `ZERVE_BEARER` or `--bearer` when available so the gate can confirm both route health and `is_public`
- treat the share-post link as unblocked only when that checker reports `summary.ready_for_share_post_link: true`
- do not treat a bare `200` there as success if it only serves the generic Zerve shell instead of the actual public project page
- only use a different public route if it has been consciously chosen and verified, because the gallery/community path is separate
- the latest retained authenticated metadata baseline currently says `canvas.is_public: false`, so treat the share-post path as blocked until that changes or a human provides the final public link
- confirm the exact Zerve tag on the chosen platform before posting

Reference:
- `docs/share-post-pack.md`

### 8. Run the final verification pass

Why last:
- this is the checkpoint before pressing submit

Do:
- verify the final chosen demo path opens
- verify the final deck and presenter notes open
- verify the video link or upload is correct
- verify the submission form text matches the real MVP scope
- verify no stale preview URL or placeholder artifact slipped in
- update the final asset register with the real final links and file locations

Reference:
- `docs/submission-verification-checklist.md`
- `docs/final-asset-register.md`

## Emergency minimal submission path

If time is collapsing:
1. verify a working demo path, live or safe local default
2. run the recording preflight checklist, and on the safe local path run `./scripts/check_safe_local_demo.sh`, then record the one-take demo using the run sheet and voiceover script
3. paste the default field set from the form map
4. submit with honest scope and working assets

In a crunch, working and credible beats incomplete perfection.

## Fast handoff summary

If another person has to finish the submission quickly, tell them:
- use `docs/final-submission-sequence.md` for order of operations
- use `docs/submission-form-map.md` for the form
- use `docs/recording-preflight-checklist.md`, `docs/video-recording-run-sheet.md`, and `docs/video-voiceover-script.md` for recording
- use `docs/demo-market-shortlist.md` for the drilldown choice
- use `docs/submission-verification-checklist.md` for the final sweep

## Definition of done

The submission is actually ready when all of these are true:
- one healthy demo path is confirmed
- the deck exists
- the presenter notes exist
- the video exists or is ready to upload
- the submission form is filled with final wording
- the final verification pass is complete

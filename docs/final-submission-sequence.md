# Final Submission Sequence

## Purpose

This is the last-mile runbook for the day of submission.

Use it when the browser/auth path is finally available and the remaining work needs to happen in the right order without thrashing.

## Current blocker context

At the moment, the repo-side submission package is strong, but the remaining office-layer finish is blocked by browser/auth state:
- Google Slides creation needs a browser session Google accepts for login
- Google Doc or deck-speaker-note creation depends on the same office-layer browser path
- the final live Zerve preview recheck also needs a usable authenticated browser state

This doc assumes those blockers have just become solvable.

## Submission-day order of operations

### 1. Re-open the current live demo path first

Why first:
- everything else depends on knowing which demo entrypoint is truly healthy right now

Do:
- open the current Zerve deploy tab
- launch or re-open the freshest preview
- confirm the app actually loads
- confirm Radar, Market Detail, and Methodology still behave as expected

If healthy:
- treat the live preview as the primary demo link

If flaky:
- switch immediately to the verified local fallback path instead of burning time

References:
- `docs/submission-verification-checklist.md`
- `docs/judge-demo-script.md`

### 2. Lock the demo example market

Why now:
- once the live path is known, pick the exact drilldown example before making slides or recording

Do:
- choose the strongest current drilldown candidate
- prefer the shortlist order from the repo unless the live run clearly suggests a better example
- avoid awkward or overly niche examples if a cleaner one is available

References:
- `docs/demo-market-shortlist.md`
- `docs/video-recording-run-sheet.md`

### 3. Create the Google Slides deck

Why before recording:
- the deck clarifies the story and can double as backup structure for the video

Do:
- build the slide deck from the outline doc
- keep it concise and visually clean
- include problem, solution, product flow, proof/demo, why Zerve matters, and next steps
- do not overpack it with implementation trivia

Reference:
- `docs/submission-deck-outline.md`

### 4. Create the office-layer notes artifact

Why now:
- the speaker notes or recording notes should match the actual deck and chosen demo path

Do:
- create a Google Doc or put speaker notes directly in the deck
- use the demo script as the base
- fold in the one-take run sheet so the recording flow is operational, not just conceptual

References:
- `docs/judge-demo-script.md`
- `docs/video-recording-run-sheet.md`

### 5. Record the demo video

Why after deck and notes:
- by this point the story, example market, and flow should already be stable

Do:
- use the one-take run sheet
- keep the video to one strong story arc
- use the verified chosen demo path
- if the live path degrades, switch to the local fallback immediately without apology

References:
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

### 7. Run the final verification pass

Why last:
- this is the checkpoint before pressing submit

Do:
- verify the final demo link opens
- verify the final deck and notes artifact open
- verify the video link or upload is correct
- verify the submission form text matches the real MVP scope
- verify no stale preview URL or placeholder artifact slipped in
- update the final asset register with the real final links and file locations

Reference:
- `docs/submission-verification-checklist.md`
- `docs/final-asset-register.md`

## Emergency fallback path

If time is collapsing:
1. verify a working demo path, live or local fallback
2. record the one-take demo using the run sheet
3. paste the safe default field set from the form map
4. submit with honest scope and working assets

In a crunch, working and credible beats incomplete perfection.

## Fast handoff summary

If another person has to finish the submission quickly, tell them:
- use `docs/final-submission-sequence.md` for order of operations
- use `docs/submission-form-map.md` for the form
- use `docs/video-recording-run-sheet.md` for recording
- use `docs/demo-market-shortlist.md` for the drilldown choice
- use `docs/submission-verification-checklist.md` for the final sweep

## Definition of done

The submission is actually ready when all of these are true:
- one healthy demo path is confirmed
- the deck exists
- the notes artifact exists
- the video exists or is ready to upload
- the submission form is filled with final wording
- the final verification pass is complete

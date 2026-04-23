# Office-Layer Asset Checklist

## Purpose

This is the practical checklist for what should exist in Google Workspace `Documents` during the final office-layer finish.

Use it to make the final office-layer finish clean, complete, and easy to inspect.

## Current blocker context

Google Workspace artifact creation itself is no longer blocked, because the authenticated `gws` CLI path is available for Docs, Slides, and Drive work.

Current project-level sharp blocker:
- there is still no verified public Zerve project/share URL
- authenticated canvas metadata previously confirmed `canvas.is_public: false`, and the latest public-share gate still remains red
- that blocks the required public share post until the project is made public in Zerve and the resulting public link is verified
- the next action is now explicit: use the Zerve share/privacy control to make the notebook public, then rerun `python3 scripts/check_zerve_public_share.py`
- only treat the link as ready when that checker reports `summary.ready_for_share_post_link: true`
- evidence:
  - `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-public-status-20260423T055107Z.json`
  - `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-public-route-check-20260423T111000Z.json`

Relevant demo-path note:
- the live Zerve preview path is now understood concretely: a fresh bearer-auth trigger can emit a new host that resolves immediately, serves a short warm-up `503` window, then turns into the real app
- the verified local fallback should still be treated as the safe default path for recording and submission unless a final live check turns clean enough to justify switching

This checklist can still be executed now for the Workspace artifact portion.

## Required Google Workspace artifacts

### 1. Google Slides deck
Create:
- one polished presentation deck for the hackathon submission
- prefer the slide-ready 16:9 screenshots as the default visuals and keep the uncropped PNGs as backup proof captures
- current state: compact 6-slide deck exists, has gone through multiple polish passes, and now has default visual assets plus stronger internal hierarchy for final layout refinement

Source materials:
- `docs/submission-deck-outline.md`
- `docs/slide-build-kit.md`
- `docs/slide-copy-pack.md`
- `docs/submission-visual-assets.md`
- `artifacts/submission/slide-ready/local-radar-view-16x9.png`
- `artifacts/submission/slide-ready/local-market-detail-view-16x9.png`
- `artifacts/submission/slide-ready/local-methodology-view-16x9.png`
- `artifacts/submission/local-radar-view.png`
- `artifacts/submission/local-market-detail-view.png`
- `artifacts/submission/local-methodology-view.png`

### 2. Google Doc or speaker notes artifact
Create one of:
- one Google Doc for recording notes and presenter notes
- or deck speaker notes embedded slide by slide if that is cleaner
- current state: both now exist in useful form, with a structured presenter-notes doc plus embedded slide speaker notes in the deck, and they now align cleanly with the compact deck order and safe demo-path plan

Source materials:
- `docs/judge-demo-script.md`
- `docs/video-voiceover-script.md`
- `docs/video-recording-run-sheet.md`
- `docs/presenter-cheat-sheet.md`
- `docs/demo-market-shortlist.md`

### 3. Final demo link reference
Create or store:
- one clean note in the office layer with the final chosen demo path
- default that note to the verified local fallback unless a last-minute live check actually opens cleanly
- right before the real take on the safe local path, run `./scripts/check_safe_local_demo.sh` instead of relying only on older proof
- current state: demo-link notes doc exists and now also includes explicit default visual pairings for the recording flow

Source materials:
- `docs/submission-verification-checklist.md`
- `docs/final-submission-sequence.md`

### 4. Final submission text reference
Create or store:
- one clean reference doc or note with the exact final wording used in the submission form

Source materials:
- `docs/submission-form-map.md`
- `docs/submission-copy-draft.md`
- `docs/submission-short-variants.md`

## Recommended folder contents in Google Workspace `Documents`

Keep the final office layer tidy.

Recommended set:
- `Market Mispricing Radar - Submission Deck`
- `Market Mispricing Radar - Presenter Notes`
- `Market Mispricing Radar - Final Submission Copy`
- `Market Mispricing Radar - Demo Link Notes`
- `Market Mispricing Radar - local-radar-view-16x9.png`
- `Market Mispricing Radar - local-market-detail-view-16x9.png`
- `Market Mispricing Radar - local-methodology-view-16x9.png`

## What should not be left messy

Avoid:
- duplicate half-finished decks
- stray test docs
- multiple competing note docs with unclear status
- stale preview links with no note about whether they still work

## Order of office-layer creation

Do this in order:
1. lock the local fallback as the default demo path, or switch to live only if the final check is clean
2. on the safe local path, run `./scripts/check_safe_local_demo.sh` right before the real take
3. refine the Slides deck only where a clear polish gain still exists
4. keep the notes artifact aligned with the chosen demo path and current deck
5. record or finalize the video plan
6. store the final submission text reference
7. run the final verification pass

## Done check for the office layer

The office layer is in good shape when:
- the final deck exists
- the notes artifact exists
- the final submission wording is captured in one obvious place
- the chosen demo path is documented
- the `Documents` folder is clean and not full of throwaway artifacts

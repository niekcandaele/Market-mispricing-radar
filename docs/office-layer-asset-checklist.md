# Office-Layer Asset Checklist

## Purpose

This is the practical checklist for what should exist in the Google Workspace office path `Documents/Hackathons/ZerveHack` during the final office-layer finish.

Use it to make the final office-layer finish clean, complete, and easy to inspect.

## Current share-post context

Google Workspace artifact creation itself is no longer blocked, because the authenticated `gws` CLI path is available for Docs, Slides, and Drive work.

Current project-level sharp blocker:
- verified public Zerve notebook URL is available: `https://app.zerve.ai/notebook/1b13702d-5502-47d1-b1e0-6ba476250dc4`. The latest retained public-share checker reports `summary.ready_for_share_post_link: true`.
- the required public share post is unblocked on link availability, but still requires human platform/copy approval before posting
- the next action is the human-approved public post itself; rerun `python3 scripts/check_zerve_public_share.py` only as a final link sanity check
- only treat the link as ready when that checker reports `summary.ready_for_share_post_link: true`
- evidence:
  - `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-public-route-check-20260426T0503Z.json`

Relevant demo-path note:
- the live Zerve preview path is now understood concretely: a fresh bearer-auth trigger can emit a new host that resolves immediately, serves a short warm-up `503` window, then turns into the real app
- the locked safe local default should still be treated as the default path for recording and submission unless a final live check turns clean enough to justify switching

This checklist can still be executed now for the Workspace artifact portion.

## Required Google Workspace artifacts

### 1. Submission deck
Create:
- one polished presentation deck for the hackathon submission
- prefer the slide-ready 16:9 screenshots as the default proof visuals and generated imagery where it strengthens the story
- status: previous Google Slides deck was trashed, then a fresh 9-slide HTML deck was rebuilt with the updated `slides-generator` skill and uploaded as a Drive HTML file plus ZIP bundle

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
- or hidden per-slide notes inside the rebuilt HTML deck if that is cleaner
- status: presenter-notes doc exists, was refreshed and read back on 2026-04-25 to match the rebuilt 9-slide HTML/PDF deck, locked safe local default, Putin drilldown, and public-share blocker wording; the rebuilt HTML deck also includes hidden per-slide notes aligned to the locked safe local default plan

Source materials:
- `docs/judge-demo-script.md`
- `docs/video-voiceover-script.md`
- `docs/video-recording-run-sheet.md`
- `docs/presenter-cheat-sheet.md`
- `docs/demo-market-shortlist.md`

### 3. Final demo link reference
Create or store:
- one clean note in the office layer with the final chosen demo path
- default that note to the locked safe local default unless a last-minute live check actually opens cleanly
- right before the real take on the safe local path, run `./scripts/check_safe_local_demo.sh` instead of relying only on older proof
- use the retained JSON it writes under `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/` as the current safe-local proof, and let the script archive the previously active baseline automatically
- status: demo-link notes doc exists, was refreshed and read back again on 2026-04-25 after the latest safe-local recheck, and now captures the locked safe local default, the auto-written retained proof flow, and the chosen visual pairings for recording

Source materials:
- `docs/submission-verification-checklist.md`
- `docs/final-submission-sequence.md`

### 4. Final submission text reference
Create or store:
- one clean reference doc or note with the exact final wording used in the submission form
- status: final submission-copy doc exists in `Documents/Hackathons/ZerveHack`, was refreshed to match the latest submission copy, and was read back successfully again in the 2026-04-25 office-doc QA pass

Source materials:
- `docs/submission-form-map.md`
- `docs/submission-copy-draft.md`
- `docs/submission-short-variants.md`

## Recommended folder contents in Google Workspace `Documents/Hackathons/ZerveHack`

Keep the final office layer tidy.

Current folder path:
- `Documents` folder id: `1iLofzjfBHLy-EMgC2XJm2yB1K4dF7Oa0`
- `Hackathons` folder id: `1ozJ3D_35aTPa5ORiVOBJne4vCrv8xHOJ`
- `ZerveHack` folder id: `18O-ZVgNpN0-vxbuQHxZjjChnQw82psk8`

Recommended set:
- `Market Mispricing Radar - Submission Deck (HTML)`
- `Market Mispricing Radar - Submission Deck (slides-generator HTML bundle)`
- `Market Mispricing Radar - Submission Deck (PDF)`
- `Market Mispricing Radar - Presenter Notes`
- `Market Mispricing Radar - Final Submission Copy`
- `Market Mispricing Radar - Demo Link Notes`
- `Market Mispricing Radar - local-radar-view-16x9.png`
- `Market Mispricing Radar - local-market-detail-view-16x9.png`
- `Market Mispricing Radar - local-methodology-view-16x9.png`

Current verified state on `2026-04-26`:
- the previous Google Slides deck was trashed
- the `Documents/Hackathons/ZerveHack` folder contains the expected Market Mispricing Radar artifacts
- no extra duplicate presentation decks were present after the rebuild pass
- Presenter Notes, Demo Link Notes, and Final Submission Copy were refreshed and read back with current markers for `refresh-20260426T095005Z`, local PDF upload, Drive `401 Unauthorized` warning, required Zerve tags, and the verified public notebook URL; evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/office-docs-readback-qa-20260426T1149Z.json`
- Drive HTML, ZIP bundle, and PDF export size/md5 checks match the local submission artifacts; evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/drive-deck-files-qa-20260426T0501Z.json`. Unauthenticated Drive opening still returns `401 Unauthorized`, so judge-facing use requires changing sharing or uploading files directly; evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/drive-deck-unauth-open-check-20260426T0856Z.json`

## What should not be left messy

Avoid:
- duplicate half-finished decks
- stray test docs
- multiple competing note docs with unclear status
- stale preview links with no note about whether they still work

## Order of office-layer creation

Do this in order:
1. keep the locked safe local default as the default demo path, or switch to live only if the final check is clean
2. on the safe local path, run `./scripts/check_safe_local_demo.sh` right before the real take and keep the fresh retained JSON it writes as the current proof
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
- the `Documents/Hackathons/ZerveHack` folder is clean and not full of throwaway artifacts

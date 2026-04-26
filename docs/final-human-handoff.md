# Final Human Handoff

Use this when someone needs to finish the ZerveHack submission without reading the whole repo.

## State

- Status: near-ready, not submission-complete.
- Default demo: locked safe local default.
- Current safe-local proof: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/safe-local-demo-20260425T194755Z.json` (`refreshId`: `refresh-20260425T194755Z`).
- Public share-post gate: still blocked; authenticated Zerve metadata now says `canvas.is_public: true`, but the notebook route still renders the generic Zerve shell rather than a verified project page.
- Latest public-route gate: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-public-route-check-20260426T044718Z.json`.
- Retained evidence manifest: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/submission-evidence-manifest-20260425T1116Z.json`.

## Do next

1. Provide/open the exact verified public project URL or fix the Zerve route until the checker sees the real public project page.
2. Rerun `python3 scripts/check_zerve_public_share.py`; only clear the blocker when `summary.ready_for_share_post_link: true`.
3. Record the final short demo using `docs/recording-preflight-checklist.md` and `docs/video-recording-run-sheet.md`.
4. Fill the submission form from `docs/submission-form-map.md`.
5. Publish the required public share post only after human platform/copy approval.
6. Run the final verification pass and update `docs/final-asset-register.md` with real final links.

## Use these links

- Deck PDF: `https://drive.google.com/file/d/17smwphggaqZGOWXU5CNBgafynE4pAtKh/view`
- Deck ZIP: `https://drive.google.com/file/d/1FFroHF0Gj-wie5AyykylTb08soQT79Bb/view`
- Deck HTML: `https://drive.google.com/file/d/1Jdoz2KKe7Tgr602TwS8b-t69Aoj5YzHt/view`

## Demo default

- Command preflight: `./scripts/check_safe_local_demo.sh`
- Command launch: `./scripts/run_local_demo.sh`
- Drilldown: `Putin out as President of Russia by December 31, 2026?`

Do not use a guessed Zerve public URL. Do not post externally without human approval.

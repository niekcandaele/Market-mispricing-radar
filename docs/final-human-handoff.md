# Final Human Handoff

Use this when someone needs to finish the ZerveHack submission without reading the whole repo.

## State

- Status: near-ready, not submission-complete.
- Default demo: locked safe local default.
- Current safe-local proof: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/safe-local-demo-20260428T050332Z.json` (`refreshId`: `refresh-20260428T050332Z`).
- Public Zerve notebook link: verified and share-ready; the remaining public-share task is publishing the required human-approved post.
- Current blocker: Google Workspace auth is expired/revoked (`gws invalid_grant`), so Workspace docs cannot be refreshed until `gws auth login` is rerun.
- Latest public-route gate: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-public-route-check-20260426T0503Z.json`.
- Retained evidence manifest: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/submission-evidence-manifest-20260425T1116Z.json`.
- Latest pre-submit sweep: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/final-pre-submit-sweep-20260428T0521Z.json` (`all_green_before_human_gates: false`).
- Agentic Reports upgrade: source prepared in `zerve/reports/agentic-market-mispricing-report.Rmd`; publish from a Zerve R Markdown block only if there is time to verify it opens cleanly.

## Do next

1. Record the final short demo using `docs/recording-preflight-checklist.md` and `docs/video-recording-run-sheet.md`.
2. Fill the submission form from `docs/submission-form-map.md`.
3. Use the verified public Zerve notebook URL in the submission/share-post materials.
4. Publish the required public share post only after human platform/copy approval.
5. Optional: publish the prepared Agentic Report from `docs/agentic-report-upgrade.md` if Zerve is open and the result can be verified quickly.
6. Run the final verification pass and update `docs/final-asset-register.md` with real final links.

## Use these links

- Public Zerve notebook: `https://app.zerve.ai/notebook/1b13702d-5502-47d1-b1e0-6ba476250dc4`
- Upload deck PDF: `artifacts/submission/market-mispricing-radar-slides-generator-deck.pdf`
- Optional upload ZIP: `artifacts/submission/market-mispricing-radar-slides-generator-deck.zip`
- Local upload manifest: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/local-submission-upload-manifest-20260426T0913Z.json`
- Drive deck links require sharing fix before judge use; unauthenticated checks return `401 Unauthorized`. Evidence: `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/drive-deck-unauth-open-check-20260426T0856Z.json`

## Demo default

- Command preflight: `./scripts/check_safe_local_demo.sh`
- Command launch: `./scripts/run_local_demo.sh`
- Drilldown: `Putin out as President of Russia by December 31, 2026?`

Do not use a guessed Zerve public URL. Do not post externally without human approval.

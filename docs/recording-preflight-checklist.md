# Recording Preflight Checklist

## Purpose

This is the short practical checklist to run right before recording the final hackathon demo.

Use it to avoid wasting a take on preventable setup mistakes.

## Demo path check

Current retained safe-local proof before recording:
- `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/safe-local-demo-20260425T130211Z.json`
- `refreshId`: `refresh-20260425T130211Z`

- [ ] run `./scripts/check_safe_local_demo.sh` before the real take if using the safe local default path
- [ ] keep the fresh retained JSON that script writes under `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/` as the current proof for the take
- [ ] default to the locked safe local default as the primary recording path
- [ ] only switch to the live Zerve preview if the freshest preview opens cleanly right before recording
- [ ] if trying the live path, reopen the freshest preview from the Zerve deploy tab instead of trusting an old rotated URL
- [ ] if the live path never clears its initial warm-up `503` window, stay on the safe local default before recording starts
- [ ] confirm the chosen demo path opens cleanly
- [ ] confirm Radar, Market Detail, and Methodology all load on the chosen path

## Content check

- [ ] lock the exact drilldown market before recording
- [ ] safe local default: `GTA VI released before June 2026?`
- [ ] keep `docs/demo-market-shortlist.md` open or nearby in case the live run clearly suggests a better option
- [ ] decide whether to use the primary voiceover, fuller voiceover, or tight fallback from `docs/video-voiceover-script.md`
- [ ] keep `docs/video-recording-run-sheet.md` open for beat order
- [ ] keep `docs/judge-demo-script.md` nearby for backup phrasing if needed
- [ ] keep the deck PDF nearby as a backup story spine: `https://drive.google.com/file/d/17smwphggaqZGOWXU5CNBgafynE4pAtKh/view`

## Screen check

- [ ] close unrelated tabs or windows
- [ ] make sure the app opens on the intended starting view
- [ ] keep the visible screen clean and presentation-safe
- [ ] confirm the main screenshot-worthy sections are readable at the chosen window size
- [ ] avoid leaving debug clutter, terminal noise, or irrelevant browser chrome in view

## Audio / delivery check

- [ ] make sure the recording setup is capturing audio correctly
- [ ] do one very short test sentence if there is any doubt about audio
- [ ] speak slightly slower than feels natural
- [ ] keep the framing honest: triage signal, not guaranteed profit
- [ ] avoid feature sprawl, keep one clear story arc

## Story check

- [ ] hook: raw market interfaces are weak inspection tools
- [ ] product claim: explainable radar for markets that deserve a second look
- [ ] drilldown claim: show score drivers, signals, and caveats
- [ ] honesty claim: Polymarket-first, explanation-rich MVP
- [ ] Zerve claim: real notebook-to-app pipeline, not a mockup

## Go / no-go rule

Record only if:
- [ ] the chosen demo path is healthy enough for one clean take
- [ ] the chosen path is already locked before the real take starts
- [ ] the drilldown market is already chosen (default safe local choice: `GTA VI released before June 2026?`)
- [ ] the spoken script choice is decided
- [ ] the screen is clean
- [ ] the story fits in about 60 to 90 seconds

If any of those fail, stop and reset before taking the real recording.

## References

- `./scripts/check_safe_local_demo.sh`
- `docs/video-recording-run-sheet.md`
- `docs/video-voiceover-script.md`
- `docs/judge-demo-script.md`
- `docs/demo-market-shortlist.md`
- `docs/submission-verification-checklist.md`

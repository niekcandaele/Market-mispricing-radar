# Submission Form Map

## Purpose

This is the practical bridge between the repo docs and the actual hackathon submission form.

Use it when filling the form so you can paste from one place instead of hunting across multiple docs.

## Core references

- long-form project copy: `docs/submission-copy-draft.md`
- short-form field variants: `docs/submission-short-variants.md`
- demo/video flow: `docs/video-recording-run-sheet.md`
- demo market choice aid: `docs/demo-market-shortlist.md`
- final sweep checklist: `docs/submission-verification-checklist.md`

## Common field map

### Project name
Use:
`Market Mispricing Radar`

### Tagline
Default:
`A live prediction-market radar that surfaces markets whose prices look fragile, stale, extreme, or weakly supported.`

Short fallback:
`An explainable radar for prediction markets that deserve a second look.`

### One-sentence summary
Default:
`Market Mispricing Radar ranks prediction markets that look fragile, stale, extreme, or weakly supported, then explains why they surfaced.`

Alternate:
`Market Mispricing Radar helps an operator find prediction markets that deserve scrutiny instead of forcing them to scan raw odds one market at a time.`

### Short description
Recommended:
`Market Mispricing Radar ranks prediction markets that deserve a second look. It surfaces fragile, stale, extreme, or weakly supported pricing and explains why each market is being flagged.`

Very short fallback:
`Explainable radar for prediction markets that look fragile, stale, or weakly supported, built as a live Zerve notebook-to-app workflow.`

### Longer project summary
Use this:
`Prediction markets are information-dense, but most interfaces still leave the user to do the triage themselves. Market Mispricing Radar turns that into an explainable workflow. It ingests live market data, scores markets whose pricing looks stale, extreme, unstable, or weakly supported, and presents the results in a deployed radar-style app with explanation headlines, drilldown detail, and explicit caveats. The key design choice is honesty. This project does not pretend to know the perfect fair value of every market, and it does not claim guaranteed arbitrage. Instead, it prioritizes which markets look most worth inspecting right now and shows the evidence behind that prioritization.`

### What problem does it solve?
Use this:
`Prediction markets can be useful signals, but raw market lists do not tell an operator what to inspect first. Suspicious or fragile pricing can hide in plain sight, and browsing one market at a time is a weak inspection workflow. Market Mispricing Radar solves that by ranking the markets that deserve scrutiny and explaining why they surfaced.`

### How does it work?
Use this:
`The current MVP fetches live Polymarket data, normalizes and categorizes markets, builds market features, scores fragility signals like staleness, weak support, extremeness, and instability, generates market-level explanations, and deploys the result into a Streamlit app inside Zerve.`

### Why is this a strong ZerveHack project?
Use this:
`This project turns live notebook analysis into a deployed product inside Zerve instead of stopping at a notebook or a static mockup. The same environment handles ingestion, scoring, explanation generation, and the deployed app can actually be inspected and used.`

### Built with
Short version:
`Zerve, Python, Streamlit, Polymarket`

Fuller version:
`Zerve notebooks, Streamlit deployment, Python, and live Polymarket market data`

### Challenges
Use this:
`Turning the project into a credible product required solving both technical and presentation problems: live ingestion quirks, brittle deploy workflows, and multiple rounds of explainability polish.`

### Accomplishments
Use this:
`We proved a real end-to-end Zerve workflow from notebook ingestion and scoring to a deployed app that ranks markets and explains why they surfaced.`

### What did you learn?
Use this:
`The most credible MVP was not to claim perfect fair value, but to rank what deserves scrutiny and explain why. We also learned that for hackathons, product clarity and narrative polish matter almost as much as the underlying technical proof.`

### Future work
Use this:
`The next steps are cross-source comparison with other prediction platforms, stronger confidence calibration, and richer context inputs where they genuinely improve explainability.`

### Honest caveat / scope note
Use this:
`This MVP is Polymarket-first and intentionally honest about that scope. The score is a triage signal, not a promise of profit.`

## Demo link field
Safe default:
- use the verified local fallback path from `docs/submission-verification-checklist.md`

Optional last-minute upgrade only if it opens cleanly:
- current live Zerve preview opened fresh from the deploy tab right before submission

## Video field
Use:
- the recording flow from `docs/video-recording-run-sheet.md`
- the drilldown market order from `docs/demo-market-shortlist.md`

## Required public share-post note

The live Devpost page currently lists a public share post tagging Zerve as required.

Use:
- `docs/share-post-pack.md`

Blocking note:
- if the project is still not public in Zerve or the public Zerve project/share URL is still unresolved, stop and verify that link before trying to satisfy the share-post requirement
- latest authenticated evidence: `canvas.is_public: false` in `/home/catalysm/.openclaw/workspace/state/hackathons/market-mispricing-radar/zerve-public-status-20260423T055107Z.json`

Default recommendation:
- one simple LinkedIn post, unless the human explicitly prefers X or another platform

## Safe default paste set

If the form is awkward and time is short, use this compact set:

- name: `Market Mispricing Radar`
- tagline: `An explainable radar for prediction markets that deserve a second look.`
- short summary: `Market Mispricing Radar ranks prediction markets that look fragile, stale, extreme, or weakly supported, then explains why they surfaced.`
- Zerve fit line: `This project turns live notebook analysis into a deployed product inside Zerve instead of stopping at a notebook or a static mockup.`
- scope caveat: `The score is a triage signal, not a promise of profit.`

## Before final paste

Check `docs/submission-verification-checklist.md` first so the text and links match the actual state of the demo and remaining blockers.

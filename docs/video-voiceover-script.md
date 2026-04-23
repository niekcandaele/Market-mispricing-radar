# Video Voiceover Script

## Purpose

This is the spoken-script layer for the final hackathon demo video.

Use it when the recording run sheet is too structural and the demo script is too broad. This doc is meant to reduce improvisation during the actual take.

## Primary script, about 75 seconds

Start on the Radar view.

"Prediction markets are useful, but most interfaces still make you scan raw odds market by market. Market Mispricing Radar turns that into an explainable workflow by ranking the markets that deserve a second look.

Here on the Radar view, I can immediately see which live markets look fragile, stale, extreme, or weakly supported. Instead of a flat market list, I get ranked cards, explanation headlines, category context, and visible caveats.

Now I can drill into one market and see why it was flagged, what signals are driving the score, and what caveats still apply. The important framing is that this is a triage signal, not a promise of profit or a claim that we know the exact fair value.

The Methodology view keeps the MVP honest. This version is intentionally Polymarket-first and explanation-rich, with clear notes about scope and limitations.

And the Zerve story matters here too. This is a real deployed workflow. The deployed Streamlit app is reading outputs from a real Zerve notebook pipeline end to end, turning live analysis into a usable product." 

## Slightly fuller script, about 90 seconds

"Prediction markets are powerful, but most interfaces still force you to inspect one market at a time. Market Mispricing Radar turns that into a ranked inspection workflow.

On the Radar view, the app surfaces markets whose pricing looks stale, fragile, extreme, or weakly supported. Instead of a raw odds list, I get ranked results with explanation headlines, category context, and warning signals that help me decide what deserves attention first.

When I click into one market, I can see the score drivers, supporting signals, and caveats behind the ranking. That is an important design choice. This project does not pretend to know perfect fair value or guaranteed arbitrage. It is built to help people prioritize scrutiny in a more explainable way.

The Methodology page makes the scope explicit. The MVP is deliberately Polymarket-first, explanation-first, and honest about what the score does and does not claim.

Finally, this is a strong ZerveHack fit because the workflow is real end to end. The same Zerve environment handles ingestion, scoring, explanation generation, and the deployed Streamlit app can actually be inspected and used." 

## Tight fallback script, about 45 seconds

"We built a live radar for prediction markets that deserve a second look. Instead of browsing raw odds market by market, Market Mispricing Radar ranks markets whose pricing looks fragile, stale, extreme, or weakly supported, then explains why they surfaced.

I can drill into one market to see the score drivers, supporting signals, and caveats. The score is a triage signal, not a profit promise.

And this is not a mockup. The app is deployed from a real Zerve notebook pipeline end to end." 

## Delivery notes

- speak a little slower than feels natural
- pause briefly after the hook and before the Zerve close
- do not say "arbitrage" unless a shorter fallback really needs the word
- avoid over-explaining implementation details during the recording
- use the verified local fallback as the default recording path and keep the same script if a live upgrade is not clearly healthy

## Screen sync reminders

These sync points should work cleanly on the verified local fallback path and do not require a live-preview-only setup.

### Radar section
Use while saying:
- ranked markets
- explanation headlines
- category context
- visible caveats

### Detail section
Use while saying:
- why it was flagged
- score drivers
- supporting signals
- caveats still apply

### Methodology / close
Use while saying:
- Polymarket-first
- honest scope
- real Zerve notebook-to-app pipeline

## References

- `docs/video-recording-run-sheet.md`
- `docs/judge-demo-script.md`
- `docs/demo-market-shortlist.md`
- `docs/presenter-cheat-sheet.md`

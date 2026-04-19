# MVP Source Validation

## Purpose

This document locks the current MVP source decision and records the practical limitations that matter for implementation.

It exists to make issue #6 explicit in one place:
- which source we are actually using first
- how that maps to the internal schema
- what limitations we are accepting for MVP

## Current decision

For the MVP, use:
- **Polymarket only**

Do not add a second source until the first end-to-end Zerve pipeline works.

This means the first shipped product is a **single-source anomaly and fragility radar**, not a cross-market disagreement engine.

## Why Polymarket first

Polymarket is the best MVP starting point because it lets us validate the full product loop with minimal scope:
- ingestion
- normalization
- scoring
- explanation
- Streamlit presentation

It is enough to prove that the product can surface interesting markets without drowning the project in cross-source matching too early.

## What this means for the schema

The internal normalized schema is defined in:
- `docs/schema.md`

For MVP, every normalized record should at minimum preserve:
- source identity
- source market ID
- source URL
- title
- status
- price or probability
- timestamps relevant to freshness and resolution
- volume and liquidity when available
- fetch timestamp

That schema is intentionally ready for future multi-source expansion, but the first implementation path is single-source.

## Validated MVP source scope

### Included now
- active Polymarket markets suitable for scoring and display
- metadata needed for ranking, explanation, and debugging

### Deliberately excluded for MVP
- cross-source matching
- fair-value claims across venues
- social/news enrichment
- broad category-specific custom logic
- complex historical calibration

## Known limitations

These limitations are acceptable for MVP and should stay visible.

### 1. Single-source limitations
The first score cannot claim cross-market disagreement because there is no second source yet.

Implication:
- frame the score as fragility, suspiciousness, or worth-inspecting priority
- do not oversell it as true price discovery

### 2. Market structure variation
Not every market will have equally clean or complete fields.

Implication:
- unsupported or messy records may need exclusion or lower confidence
- the pipeline should tolerate missing timestamps or partial metadata

### 3. Freshness can be uneven
Update timestamps, recent movement signals, and effective market activity may vary across records.

Implication:
- freshness-based signals need conservative handling
- missing freshness inputs should reduce confidence rather than create fake certainty

### 4. Liquidity and volume do not equal truth
Thin support can be a useful signal, but it is not itself proof of mispricing.

Implication:
- liquidity should be one component, not the whole story
- explanations should stay explicit about signal limits

### 5. No mandatory history layer yet
The MVP may start with snapshot-oriented logic before a richer historical view exists.

Implication:
- movement or volatility features may begin simple or partial
- the first score should remain interpretable even without deep history

## Scoring implications

Because of the source decision and limitations above, the v1 score should emphasize:
- staleness
- time to resolution
- price extremeness
- liquidity support
- movement anomaly only when available and trustworthy

Reference:
- `docs/scoring-model-v1.md`

## App implications

Because the source scope is narrow, the judge-facing app should be honest about it.

The app should say, directly or indirectly:
- this is a Polymarket-first MVP
- the score ranks markets worth inspecting
- the explanations come from explicit score components

Reference:
- `docs/app-flow.md`

## Completion check for issue #6

This issue is complete when the following are true:
- selected MVP source is documented, yes
- initial schema is drafted, yes
- known limitations are recorded, yes

## Next practical step

After this validation step, the next highest-value work is:
- implementing or testing the first notebook-side Polymarket ingestion path in Zerve
- or turning the score design into an executable first-pass ranking pipeline

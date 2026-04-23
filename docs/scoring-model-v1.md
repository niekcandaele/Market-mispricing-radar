# Scoring Model V1

## Purpose

This document defines the first scoring model for the MVP.

The goal of v1 is not to be perfect. The goal is to be:
- interpretable
- defensible
- easy to debug
- good enough to surface interesting markets

## Scoring philosophy

The first version should score markets for **fragility / suspiciousness**, not claim true fair value with fake precision.

That means the score should answer:

> Which markets look most worth inspecting because something about their current state looks weak, stale, extreme, or structurally suspicious?

This is stronger and more honest than pretending we can fully price every market from scratch in the MVP.

## V1 framing

V1 is a **single-source Polymarket-first fragility score**.

It is not yet:
- a full fair-value estimator
- a cross-venue arbitrage engine
- a calibrated truth oracle

## Candidate components

## 1. Staleness component

### Intuition
Markets that have not updated recently may be lagging reality.

### Inputs
- `time_since_update_hours`
- source freshness baseline

### Why it matters
A market close to an event with stale updates is more suspicious than a frequently updated market.

## 2. Event-horizon component

### Intuition
A market near resolution deserves more scrutiny because stale or unstable pricing matters more when little time remains.

### Inputs
- `time_to_resolution_hours`

### Why it matters
Fragility increases when time is short and there is less room for information correction.

## 3. Extremeness component

### Intuition
Prices far from the midpoint can be reasonable, but they deserve more scrutiny when combined with poor freshness or low support.

### Inputs
- `price_distance_from_mid`

### Why it matters
Extreme probabilities combined with stale data are more interesting than middling prices with active updates.

## 4. Liquidity support component

### Intuition
A price supported by very thin liquidity or weak market depth may be less trustworthy.

### Inputs
- `volume`
- `liquidity`

### Why it matters
Thinly supported prices may be more fragile or easier to distort.

## 5. Volatility or movement anomaly component

### Intuition
Unusual recent movement can indicate instability, information shock, or unresolved uncertainty.

### Inputs
- recent price changes if available
- rolling movement magnitude if recoverable from source data

### Why it matters
Markets with abrupt or erratic recent movement may be especially interesting.

## 6. Data quality component

### Intuition
Some records should be down-weighted if their data is incomplete or unreliable.

### Inputs
- missing timestamps
- malformed values
- unsupported market structures

### Why it matters
We want high scores to reflect real market properties, not bad data.

## Proposed v1 score shape

```text
final_score =
  w1 * staleness_component
+ w2 * event_horizon_component
+ w3 * extremeness_component
+ w4 * liquidity_component
+ w5 * volatility_component
- w6 * data_quality_penalty
```

## Initial weighting guidance

A reasonable first guess:

- staleness: high importance
- event horizon: high importance
- extremeness: medium importance
- liquidity support: medium importance
- volatility anomaly: low to medium importance until proven useful
- data quality penalty: always active

Example starting weights:

```text
staleness = 0.30
event_horizon = 0.25
extremeness = 0.15
liquidity = 0.15
volatility = 0.15
```

These are placeholders for experimentation, not sacred truths.

Current bridge note:
- the mirrored Zerve scoring snippet intentionally follows the tuned local-prototype weighting and interaction logic rather than this earlier placeholder sketch
- that keeps the Zerve bridge aligned with the behavior already validated in the local ranking prototype

## Interaction rules

Some components should amplify each other.

### Important interaction 1
High staleness + short time to resolution should score much higher than either alone.

### Important interaction 2
Extreme price + weak liquidity should score higher than extreme price alone.

### Important interaction 3
Volatility without freshness problems may be informative, but volatility plus poor support is more suspicious.

If simple linear weights are too weak, we can add a small number of rule-based boosts.

## Suggested normalization approach

Each raw component should be normalized to a 0 to 1 scale before combination.

Examples:
- staleness percentile among active markets
- inverse-scaled time-to-resolution score
- absolute distance from 0.5, scaled to 0 to 1
- liquidity weakness transformed so weaker support increases score

## Explanation design

The score must support explanation by construction.

For each market we should keep:
- top contributing components
- component magnitudes
- one primary reason code
- optional caveat flags

Example primary reason codes:
- `stale_near_resolution`
- `extreme_price_low_support`
- `high_instability`
- `weak_data_quality`

## Confidence and caveats

V1 should include visible caveats.

Recommended confidence bands:
- low
- medium
- high

Confidence should be lower when:
- important fields are missing
- volume/liquidity data is sparse
- movement history is incomplete
- a market has unusual structure not handled well by v1

## What would make v1 good enough

V1 is good enough if:
- top results feel plausibly worth inspecting
- explanations match the numeric signals
- obvious garbage does not dominate the rankings
- the score behaves consistently across market categories

## What would make v1 bad

V1 is bad if:
- rankings are dominated by missing data artifacts
- all extreme markets score high regardless of context
- explanations sound smart but do not match the numbers
- the score cannot be debugged quickly

## Deliberate omissions from v1

Do not include yet unless clearly justified:
- heavy LLM-derived sentiment scoring
- cross-platform divergence without a second source working
- complicated fair-value modeling
- deep historical calibration claims we cannot defend

## Planned v2 expansion paths

Once MVP works, possible v2 additions:
- cross-source disagreement component
- Metaculus vs market disagreement component
- social or news attention mismatch component
- historical calibration layer
- category-specific scoring adjustments

## Recommended implementation order

1. implement component calculations separately
2. inspect raw distributions
3. normalize each component
4. combine into first score
5. inspect top-ranked outputs manually
6. tune weights and penalties
7. lock a version and document it

## Working principle

A smaller honest score beats a larger fake one.

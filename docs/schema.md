# Schema

## Purpose

This document defines the initial internal schema for the MVP.

The schema should be:
- simple
- source-agnostic enough to support future expansion
- rich enough for scoring and explanation
- easy to map into Streamlit and optional API responses

For MVP, the first implemented source is Polymarket.

## Design principles

- Keep raw source data separate from normalized records.
- Normalize only what we actually need for scoring, display, and debugging.
- Preserve source IDs and raw links so we can always trace back to the origin.
- Prefer explicit fields over deeply nested structures for the main scoring table.

## Core entities

## 1. Raw source record

This is the minimally transformed payload from the source.

Purpose:
- debugging
- source evolution handling
- traceability

Suggested stored fields:
- `source`
- `source_market_id`
- `fetched_at`
- `raw_payload`

## 2. Normalized market record

This is the main market-level entity used by downstream logic.

### Required fields

- `market_id`
  - internal stable ID for the normalized record
- `source`
  - e.g. `polymarket`
- `source_market_id`
  - source-native identifier
- `source_url`
  - direct source link
- `title`
  - human-readable market title
- `description`
  - source description if available
- `category`
  - source or derived category
- `status`
  - open, closed, resolved, inactive, unknown
- `is_binary`
  - whether the market is binary
- `event_start_at`
  - if available
- `event_end_at`
  - if available
- `resolution_at`
  - if available
- `last_price`
  - latest normalized probability or price on a 0 to 1 scale
- `yes_price`
  - if applicable
- `no_price`
  - if applicable
- `volume`
  - source volume if available
- `liquidity`
  - source liquidity if available
- `last_updated_at`
  - latest source update timestamp if available
- `fetched_at`
  - ingestion timestamp

### Derived fields

- `time_to_resolution_hours`
- `time_since_update_hours`
- `price_distance_from_mid`
- `topic_tags`
- `source_priority`

## Example normalized market record

```json
{
  "market_id": "polymarket_12345",
  "source": "polymarket",
  "source_market_id": "12345",
  "source_url": "https://polymarket.com/event/example",
  "title": "Will X happen by date Y?",
  "description": "...",
  "category": "politics",
  "status": "open",
  "is_binary": true,
  "event_start_at": null,
  "event_end_at": null,
  "resolution_at": "2026-04-28T00:00:00Z",
  "last_price": 0.64,
  "yes_price": 0.64,
  "no_price": 0.36,
  "volume": 125000.0,
  "liquidity": 45000.0,
  "last_updated_at": "2026-04-19T15:00:00Z",
  "fetched_at": "2026-04-19T15:10:00Z",
  "time_to_resolution_hours": 205.8,
  "time_since_update_hours": 0.17,
  "price_distance_from_mid": 0.14,
  "topic_tags": ["politics","elections"],
  "source_priority": 1
}
```

## 3. Feature record

This is the market-level feature vector used for scoring.

### Required fields
- `market_id`
- `source`
- `staleness_score_raw`
- `event_horizon_score_raw`
- `volatility_score_raw`
- `liquidity_score_raw`
- `extremeness_score_raw`
- `data_quality_score_raw`

### Optional later fields
- `cross_source_divergence_raw`
- `forecast_disagreement_raw`
- `social_attention_raw`
- `news_velocity_raw`

## 4. Score record

This is the final ranking artifact.

### Required fields
- `market_id`
- `source`
- `title`
- `final_score`
- `rank`
- `score_version`
- `staleness_component`
- `event_horizon_component`
- `volatility_component`
- `liquidity_component`
- `extremeness_component`
- `confidence_band`
- `primary_reason_code`

## 5. Explanation record

This is what the app uses to explain the ranking.

### Required fields
- `market_id`
- `headline_reason`
- `short_explanation`
- `detailed_explanation`
- `caveats`
- `supporting_signals`

### Example

```json
{
  "market_id": "polymarket_12345",
  "headline_reason": "High score driven by stale pricing near resolution.",
  "short_explanation": "This market has not updated recently and is nearing resolution.",
  "detailed_explanation": "The market shows an elevated fragility score because its latest update is old relative to comparable active markets and the event is close to resolution. Current pricing is also meaningfully away from the midpoint, which increases the impact of stale information.",
  "caveats": [
    "Single-source MVP score",
    "No external news comparison yet"
  ],
  "supporting_signals": [
    "time_since_update_hours",
    "time_to_resolution_hours",
    "price_distance_from_mid"
  ]
}
```

## 6. Refresh metadata record

This supports app trust and debugging.

### Required fields
- `refresh_id`
- `source`
- `fetched_at`
- `market_count`
- `open_market_count`
- `pipeline_version`
- `score_version`
- `notes`

## Table recommendations

For the MVP we should maintain at least these working tables or outputs:
- `normalized_markets`
- `market_features`
- `ranked_markets`
- `market_explanations`
- `refresh_metadata`

## Matching-ready fields for future multi-source expansion

Even if MVP is Polymarket-only, we should preserve fields that help later matching:
- `title`
- `description`
- `category`
- `resolution_at`
- `topic_tags`
- `source_market_id`
- `source_url`

Optional future fields:
- `canonical_question_id`
- `matching_confidence`
- `matched_group_id`

## Data quality rules

### Required for scoring
A record should usually be scoreable only if:
- it is open or actively tradable
- it has a valid title
- it has a current probability or price
- it has a recent fetch timestamp

### Exclude or downgrade when
- title is empty or malformed
- status is unresolved or unsupported in a way we cannot reason about
- critical timestamps are missing for event-sensitive signals
- price is outside expected range
- the record appears duplicated or corrupted

## API and app alignment

The app and optional API should consume the normalized score and explanation records rather than raw source payloads.

That keeps presentation simple and stable.

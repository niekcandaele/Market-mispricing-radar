#!/usr/bin/env python3
"""First scoring block for Zerve-side Polymarket feature output.

Preferred Zerve notebook block name:
- `score_markets`

This snippet expects the previous blocks to have emitted:
- normalized_markets
- market_features
- feature_metadata

Primary block outputs:
- ranked_markets
- scoring_metadata

When run locally, it falls back to importing the mirrored normalization and
feature snippets.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


SOURCE_NAME = "polymarket"
SCORE_VERSION = "v1-zerve-bridge"
SCORING_WEIGHTS = {
    "staleness": 0.35,
    "event_horizon": 0.25,
    "extremeness": 0.05,
    "liquidity": 0.10,
    "volatility": 0.10,
    "stale_resolution_interaction": 0.10,
    "extreme_support_interaction": 0.10,
    "penalty": -0.30,
}


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def coerce_float(value: Any) -> float | None:
    if value in (None, "", "null"):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def confidence_band(penalty: float) -> str:
    if penalty >= 0.5:
        return "low"
    if penalty >= 0.2:
        return "medium"
    return "high"


def primary_reason_code(scores: dict[str, float], market: dict[str, Any]) -> str:
    resolution_hours = coerce_float(market.get("time_to_resolution_hours"))
    if resolution_hours is not None and resolution_hours < 0:
        return "past_resolution_still_open"

    interaction_scores = {
        "stale_near_resolution": scores["staleness_component"] * scores["event_horizon_component"],
        "extreme_price_low_support": scores["extremeness_component"] * scores["liquidity_component"],
        "high_instability": scores["volatility_component"] * max(scores["staleness_component"], 0.35),
        "weak_data_quality": scores["data_quality_penalty"],
    }
    strongest_interaction = max(interaction_scores, key=interaction_scores.get)
    if interaction_scores[strongest_interaction] >= 0.20:
        return strongest_interaction

    base_scores = {
        "staleness_component": scores["staleness_component"],
        "event_horizon_component": scores["event_horizon_component"],
        "extremeness_component": scores["extremeness_component"],
        "liquidity_component": scores["liquidity_component"],
        "volatility_component": scores["volatility_component"],
    }
    strongest = max(base_scores, key=base_scores.get)
    return {
        "staleness_component": "stale_market",
        "event_horizon_component": "near_resolution",
        "extremeness_component": "extreme_price",
        "liquidity_component": "low_support",
        "volatility_component": "high_instability",
    }[strongest]


try:
    normalized_markets
except NameError:
    normalized_markets = None

try:
    market_features
    feature_metadata
except NameError:
    snippet_dir = Path(__file__).resolve().parent
    feature_path = snippet_dir / "polymarket_feature_block.py"
    spec = importlib.util.spec_from_file_location("polymarket_feature_block", feature_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load feature snippet from {feature_path}")
    feature_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(feature_module)
    market_features = feature_module.market_features
    feature_metadata = feature_module.feature_metadata
    if normalized_markets is None:
        normalization_path = snippet_dir / "polymarket_normalization_block.py"
        norm_spec = importlib.util.spec_from_file_location("polymarket_normalization_block", normalization_path)
        if norm_spec is None or norm_spec.loader is None:
            raise RuntimeError(f"Could not load normalization snippet from {normalization_path}")
        normalization_module = importlib.util.module_from_spec(norm_spec)
        norm_spec.loader.exec_module(normalization_module)
        normalized_markets = normalization_module.normalized_markets

if normalized_markets is None:
    raise RuntimeError("normalized_markets is required for score assembly")

normalized_lookup = {
    market.get("market_id"): market
    for market in normalized_markets
    if market.get("market_id") is not None
}

ranked_markets: list[dict[str, Any]] = []
raw_scores: list[float] = []
for feature_row in market_features:
    market_id = feature_row.get("market_id")
    base_market = normalized_lookup.get(market_id, {})
    staleness_component = coerce_float(feature_row.get("staleness_score_raw")) or 0.0
    event_horizon_component = coerce_float(feature_row.get("event_horizon_score_raw")) or 0.0
    extremeness_component = coerce_float(feature_row.get("extremeness_score_raw")) or 0.0
    liquidity_component = coerce_float(feature_row.get("liquidity_score_raw")) or 0.0
    volatility_component = coerce_float(feature_row.get("volatility_score_raw")) or 0.0
    data_penalty = coerce_float(feature_row.get("data_quality_penalty_raw")) or 0.0
    penalty = data_penalty

    resolution_hours = coerce_float(base_market.get("time_to_resolution_hours"))
    staleness_hours = coerce_float(base_market.get("time_since_update_hours"))
    yes_price = coerce_float(base_market.get("yes_price"))

    if resolution_hours is not None:
        if resolution_hours < 0:
            penalty += 0.35
        elif resolution_hours > 720.0:
            penalty += min(0.25, (resolution_hours - 720.0) / 5000.0)
    if staleness_hours is not None and staleness_hours < 1.0:
        penalty += 0.05
    if yes_price is not None:
        if (
            (yes_price <= 0.01 or yes_price >= 0.99)
            and (resolution_hours is None or resolution_hours > 168.0)
            and (staleness_hours is None or staleness_hours < 12.0)
        ):
            penalty += 0.40
        elif (
            (yes_price <= 0.05 or yes_price >= 0.95)
            and (resolution_hours is None or resolution_hours > 720.0)
            and (staleness_hours is None or staleness_hours < 6.0)
        ):
            penalty += 0.20
    penalty = clamp(penalty)
    heuristic_penalty = max(penalty - data_penalty, 0.0)

    raw_score = (
        SCORING_WEIGHTS["staleness"] * staleness_component
        + SCORING_WEIGHTS["event_horizon"] * event_horizon_component
        + SCORING_WEIGHTS["extremeness"] * extremeness_component
        + SCORING_WEIGHTS["liquidity"] * liquidity_component
        + SCORING_WEIGHTS["volatility"] * volatility_component
        + SCORING_WEIGHTS["stale_resolution_interaction"] * staleness_component * event_horizon_component
        + SCORING_WEIGHTS["extreme_support_interaction"] * extremeness_component * liquidity_component
        + SCORING_WEIGHTS["penalty"] * penalty
    )

    component_scores = {
        "staleness_component": round(staleness_component, 4),
        "event_horizon_component": round(event_horizon_component, 4),
        "extremeness_component": round(extremeness_component, 4),
        "liquidity_component": round(liquidity_component, 4),
        "volatility_component": round(volatility_component, 4),
        "data_quality_penalty": round(data_penalty, 4),
        "heuristic_penalty": round(heuristic_penalty, 4),
    }

    ranked_markets.append(
        {
            **base_market,
            **feature_row,
            **component_scores,
            "score_version": SCORE_VERSION,
            "raw_score": raw_score,
            "confidence_band": confidence_band(penalty),
            "primary_reason_code": primary_reason_code(component_scores, base_market),
        }
    )
    raw_scores.append(raw_score)

min_raw = min(raw_scores) if raw_scores else 0.0
max_raw = max(raw_scores) if raw_scores else 1.0
span = max(max_raw - min_raw, 1e-9)
for row in ranked_markets:
    row["final_score"] = round((row["raw_score"] - min_raw) / span, 4)
    del row["raw_score"]

ranked_markets.sort(key=lambda item: item["final_score"], reverse=True)
for index, row in enumerate(ranked_markets, start=1):
    row["rank"] = index

scoring_metadata = {
    "source": SOURCE_NAME,
    "fetched_at": feature_metadata.get("fetched_at") if isinstance(feature_metadata, dict) else None,
    "input_market_count": len(market_features),
    "ranked_market_count": len(ranked_markets),
    "score_version": SCORE_VERSION,
    "weights": SCORING_WEIGHTS,
    "notes": [
        "This bridge snippet keeps component values directly on each ranked row for easy notebook inspection.",
        "It intentionally mirrors the tuned local prototype weights and interaction boosts rather than the earlier placeholder weight sketch in docs/scoring-model-v1.md.",
    ],
}

print(f"ranked_count {scoring_metadata['ranked_market_count']}")
if ranked_markets:
    first = ranked_markets[0]
    print(f"top_market_id {first.get('market_id')}")
    print(f"top_rank {first.get('rank')}")
    print(f"top_score {first.get('final_score')}")
    print(f"top_reason {first.get('primary_reason_code')}")
    print(f"top_confidence {first.get('confidence_band')}")

if __name__ == "__main__":
    print(json.dumps(scoring_metadata, indent=2))

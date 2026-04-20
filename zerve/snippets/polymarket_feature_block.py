#!/usr/bin/env python3
"""First feature-engineering block for Zerve-side normalized Polymarket markets.

Preferred Zerve notebook block name:
- `build_market_features`

This snippet expects the previous normalization block to have emitted:
- normalized_markets
- normalization_metadata

Primary block outputs:
- market_features
- feature_metadata

When run locally, it falls back to importing the mirrored normalization snippet.
"""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
from typing import Any


SOURCE_NAME = "polymarket"


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


def percentile_rank(value: float | None, values: list[float], reverse: bool = False) -> float:
    if value is None or not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        base = 1.0
    else:
        less_or_equal = sum(1 for item in ordered if item <= value)
        base = (less_or_equal - 1) / (len(ordered) - 1)
    return 1.0 - base if reverse else base


def absolute_staleness_signal(hours: float | None) -> float:
    if hours is None:
        return 0.0
    return clamp((hours - 6.0) / 42.0)


def event_horizon_signal(hours: float | None) -> float:
    if hours is None or hours < 0:
        return 0.0
    return clamp((720.0 - hours) / 720.0)


def data_quality_penalty(market: dict[str, Any]) -> float:
    missing = 0
    for key in ["title", "last_price", "last_updated_at", "resolution_at", "liquidity"]:
        value = market.get(key)
        if value in (None, ""):
            missing += 1
    if not market.get("is_binary"):
        missing += 1
    if market.get("status") != "open":
        missing += 1
    return clamp(missing / 6.0)


try:
    normalized_markets
    normalization_metadata
except NameError:
    snippet_dir = Path(__file__).resolve().parent
    normalization_path = snippet_dir / "polymarket_normalization_block.py"
    spec = importlib.util.spec_from_file_location("polymarket_normalization_block", normalization_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load normalization snippet from {normalization_path}")
    normalization_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(normalization_module)
    normalized_markets = normalization_module.normalized_markets
    normalization_metadata = normalization_module.normalization_metadata


staleness_values = [
    coerce_float(market.get("time_since_update_hours"))
    for market in normalized_markets
    if coerce_float(market.get("time_since_update_hours")) is not None
]
staleness_values = [value for value in staleness_values if value is not None]

support_values = [
    math.log1p(
        (coerce_float(market.get("liquidity")) or 0.0)
        + (coerce_float(market.get("volume_24hr")) or coerce_float(market.get("volume")) or 0.0)
    )
    for market in normalized_markets
    if coerce_float(market.get("liquidity")) is not None
    or coerce_float(market.get("volume_24hr")) is not None
    or coerce_float(market.get("volume")) is not None
]

volatility_values = [
    coerce_float(market.get("one_month_price_change_abs"))
    for market in normalized_markets
    if coerce_float(market.get("one_month_price_change_abs")) is not None
]
volatility_values = [value for value in volatility_values if value is not None]

market_features: list[dict[str, Any]] = []
for market in normalized_markets:
    staleness_hours = coerce_float(market.get("time_since_update_hours"))
    resolution_hours = coerce_float(market.get("time_to_resolution_hours"))
    distance_from_mid = coerce_float(market.get("price_distance_from_mid"))
    liquidity = coerce_float(market.get("liquidity"))
    volume = coerce_float(market.get("volume"))
    volume_24hr = coerce_float(market.get("volume_24hr"))
    support_metric = None
    if liquidity is not None or volume_24hr is not None or volume is not None:
        support_metric = math.log1p((liquidity or 0.0) + (volume_24hr or volume or 0.0))

    staleness_score_raw = percentile_rank(staleness_hours, staleness_values) * absolute_staleness_signal(staleness_hours)
    event_horizon_score_raw = event_horizon_signal(resolution_hours)
    extremeness_score_raw = clamp(((distance_from_mid or 0.0) - 0.15) / 0.35)
    liquidity_score_raw = percentile_rank(support_metric, support_values, reverse=True)
    volatility_signal = coerce_float(market.get("one_month_price_change_abs"))
    volatility_score_raw = percentile_rank(volatility_signal, volatility_values)
    data_quality_penalty_raw = data_quality_penalty(market)

    market_features.append(
        {
            "market_id": market.get("market_id"),
            "source": market.get("source") or SOURCE_NAME,
            "source_market_id": market.get("source_market_id"),
            "title": market.get("title"),
            "status": market.get("status"),
            "time_since_update_hours": staleness_hours,
            "time_to_resolution_hours": resolution_hours,
            "price_distance_from_mid": distance_from_mid,
            "liquidity": liquidity,
            "volume": volume,
            "volume_24hr": volume_24hr,
            "support_metric": round(support_metric, 6) if support_metric is not None else None,
            "staleness_score_raw": round(staleness_score_raw, 4),
            "event_horizon_score_raw": round(event_horizon_score_raw, 4),
            "liquidity_score_raw": round(liquidity_score_raw, 4),
            "extremeness_score_raw": round(extremeness_score_raw, 4),
            "volatility_score_raw": round(volatility_score_raw, 4),
            "data_quality_penalty_raw": round(data_quality_penalty_raw, 4),
            "data_quality_score_raw": round(1.0 - data_quality_penalty_raw, 4),
        }
    )

feature_metadata = {
    "source": SOURCE_NAME,
    "fetched_at": normalization_metadata.get("fetched_at") if isinstance(normalization_metadata, dict) else None,
    "input_market_count": len(normalized_markets),
    "feature_market_count": len(market_features),
    "feature_fields": [
        "staleness_score_raw",
        "event_horizon_score_raw",
        "liquidity_score_raw",
        "extremeness_score_raw",
        "volatility_score_raw",
        "data_quality_penalty_raw",
        "data_quality_score_raw",
    ],
    "notes": "Raw feature values are normalized to interpretable 0..1 ranges so they can map cleanly into the planned v1 score components.",
}

print(f"feature_count {feature_metadata['feature_market_count']}")
if market_features:
    first = market_features[0]
    print(f"first_market_id {first.get('market_id')}")
    print(f"first_staleness {first.get('staleness_score_raw')}")
    print(f"first_event_horizon {first.get('event_horizon_score_raw')}")
    print(f"first_liquidity {first.get('liquidity_score_raw')}")
    print(f"first_extremeness {first.get('extremeness_score_raw')}")
    print(f"first_data_penalty {first.get('data_quality_penalty_raw')}")

if __name__ == "__main__":
    print(json.dumps(feature_metadata, indent=2))

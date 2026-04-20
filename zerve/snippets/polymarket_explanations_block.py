#!/usr/bin/env python3
"""Explanation assembly block for Zerve-side ranked Polymarket markets.

This snippet expects the previous scoring block to have emitted:
- ranked_markets
- scoring_metadata

Primary block outputs:
- market_explanations
- explanation_metadata

When run locally, it falls back to importing the mirrored scoring snippet.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


SOURCE_NAME = "polymarket"
SUPPORTING_SIGNALS = [
    "time_since_update_hours",
    "time_to_resolution_hours",
    "price_distance_from_mid",
    "liquidity",
    "volume_24hr",
    "one_month_price_change_abs",
]


def explanation_fields(market: dict[str, Any]) -> dict[str, Any]:
    reason = market["primary_reason_code"]
    stale_hours = market.get("time_since_update_hours")
    end_hours = market.get("time_to_resolution_hours")
    yes_price = market.get("yes_price")

    headline_reason = "This market was flagged for a blend of suspicious score components."
    short_explanation = "The score found a combination of features worth inspecting more closely."
    detailed_explanation = (
        "The prototype flagged this market because several score components combined into a relatively high fragility signal. "
        "The raw fields and component values should be inspected before treating it as a genuinely interesting opportunity."
    )

    if reason == "stale_near_resolution" and stale_hours is not None and end_hours is not None:
        headline_reason = "High score driven by stale updates close to resolution."
        short_explanation = "This market looks slow to update despite having limited time left before resolution."
        detailed_explanation = (
            f"The market has not updated for roughly {stale_hours:.1f} hours while only about {end_hours:.1f} hours remain until resolution. "
            "That stale-near-deadline combination is one of the clearest v1 fragility patterns."
        )
    elif reason == "extreme_price_low_support" and yes_price is not None:
        headline_reason = "Extreme pricing is being carried with relatively weak support."
        short_explanation = "The current probability is far from the midpoint and does not look strongly supported by the weaker-support component."
        detailed_explanation = (
            f"The market is currently priced around {yes_price:.3f}, which is quite far from a neutral midpoint, while the support-side component still looks weak enough to keep it inspectable. "
            "In v1 that combination is treated as a fragile extreme rather than as proof the price is wrong."
        )
    elif reason == "high_instability":
        headline_reason = "Recent movement or instability is doing meaningful work in the score."
        short_explanation = "The movement proxy and nearby supporting components make this market look more unstable than a quiet baseline."
        detailed_explanation = (
            "The volatility proxy is elevated enough to matter, and the surrounding score components do not fully calm that down. "
            "This is the v1 path for markets that look more unstable than simply stale or extreme."
        )
    elif reason == "past_resolution_still_open" and end_hours is not None:
        headline_reason = "The source still presents this market as open even though its end date is in the past."
        short_explanation = "This looks like a source-status inconsistency rather than a normal live market signal."
        detailed_explanation = (
            f"The market still appears open in the fetched payload, but the recorded resolution horizon is about {end_hours:.1f} hours in the past. "
            "That makes it useful as a data-quality or source-behavior flag, even if it is not a strong product-facing candidate."
        )
    elif reason == "weak_data_quality":
        headline_reason = "The record has enough missing or awkward fields to deserve caution."
        short_explanation = "This market is being flagged partly because the available data is incomplete or structurally awkward."
        detailed_explanation = (
            "The current record is not clean enough to treat the score as high-confidence. "
            "Any review should start by validating whether the source fields are trustworthy enough for comparison."
        )

    caveats = ["single-source MVP", f"confidence:{market['confidence_band']}"]
    if stale_hours is not None and stale_hours < 6.0:
        caveats.append("fresh-market caveat")
    if end_hours is not None and end_hours < 0:
        caveats.append("source status may be inconsistent")
    if end_hours is not None and end_hours > 720.0:
        caveats.append("long-horizon market")
    if market.get("data_quality_penalty", 0.0) > 0.0:
        caveats.append("data-quality penalty applied")
    if market.get("heuristic_penalty", 0.0) > 0.0:
        caveats.append("heuristic penalty applied")

    return {
        "headline_reason": headline_reason,
        "short_explanation": short_explanation,
        "detailed_explanation": detailed_explanation,
        "caveats": caveats,
        "supporting_signals": SUPPORTING_SIGNALS,
    }


try:
    ranked_markets
    scoring_metadata
except NameError:
    snippet_dir = Path(__file__).resolve().parent
    scoring_path = snippet_dir / "polymarket_scoring_block.py"
    spec = importlib.util.spec_from_file_location("polymarket_scoring_block", scoring_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load scoring snippet from {scoring_path}")
    scoring_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scoring_module)
    ranked_markets = scoring_module.ranked_markets
    scoring_metadata = scoring_module.scoring_metadata


market_explanations: list[dict[str, Any]] = []
for market in ranked_markets:
    explanation = explanation_fields(market)
    market_explanations.append(
        {
            "market_id": market.get("market_id"),
            "category": market.get("category"),
            "topic_tags": market.get("topic_tags"),
            "headline_reason": explanation["headline_reason"],
            "short_explanation": explanation["short_explanation"],
            "detailed_explanation": explanation["detailed_explanation"],
            "primary_reason_code": market.get("primary_reason_code"),
            "caveats": explanation["caveats"],
            "supporting_signals": explanation["supporting_signals"],
            "supporting_signal_values": {
                signal: market.get(signal)
                for signal in SUPPORTING_SIGNALS
            },
            "score_components": {
                "staleness_component": market.get("staleness_component"),
                "event_horizon_component": market.get("event_horizon_component"),
                "extremeness_component": market.get("extremeness_component"),
                "liquidity_component": market.get("liquidity_component"),
                "volatility_component": market.get("volatility_component"),
                "data_quality_penalty": market.get("data_quality_penalty"),
                "heuristic_penalty": market.get("heuristic_penalty"),
            },
        }
    )

explanation_metadata = {
    "source": SOURCE_NAME,
    "fetched_at": scoring_metadata.get("fetched_at") if isinstance(scoring_metadata, dict) else None,
    "input_market_count": len(ranked_markets),
    "explained_market_count": len(market_explanations),
    "notes": [
        "Explanation text is derived from primary reason codes and explicit score fields rather than hand-written market-specific copy.",
        "Supporting signal values are carried alongside the explanation records for later app-detail rendering.",
    ],
}

print(f"explained_count {explanation_metadata['explained_market_count']}")
if market_explanations:
    first = market_explanations[0]
    print(f"top_market_id {first.get('market_id')}")
    print(f"top_headline {first.get('headline_reason')}")
    print(f"top_reason_code {first.get('primary_reason_code')}")
    print(f"top_caveat_count {len(first.get('caveats', []))}")

if __name__ == "__main__":
    print(json.dumps(explanation_metadata, indent=2))

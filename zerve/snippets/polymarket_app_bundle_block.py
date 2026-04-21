#!/usr/bin/env python3
"""App-bundle assembly block for Zerve-side Polymarket outputs.

Preferred Zerve notebook block name:
- `build_app_bundle`

This snippet expects the previous blocks to have emitted:
- ranked_markets
- market_explanations
- scoring_metadata
- explanation_metadata

Primary block outputs:
- app_bundle
- bundle_metadata

When run locally, it falls back to importing the mirrored explanation snippet.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
from typing import Any


SOURCE_NAME = "polymarket"
PIPELINE_VERSION = "zerve-bridge-v0.1"


def parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def refresh_id_from_fetched_at(value: Any) -> str | None:
    parsed = parse_timestamp(value)
    if parsed is None:
        return None
    return parsed.astimezone(timezone.utc).strftime("refresh-%Y%m%dT%H%M%SZ")


try:
    ranked_markets
    market_explanations
    scoring_metadata
    explanation_metadata
except NameError:
    snippet_dir = Path(__file__).resolve().parent
    explanations_path = snippet_dir / "polymarket_explanations_block.py"
    spec = importlib.util.spec_from_file_location("polymarket_explanations_block", explanations_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load explanation snippet from {explanations_path}")
    explanations_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(explanations_module)
    market_explanations = explanations_module.market_explanations
    explanation_metadata = explanations_module.explanation_metadata
    ranked_markets = explanations_module.ranked_markets
    scoring_metadata = explanations_module.scoring_metadata


category_counts = Counter(
    row.get("category") or "uncategorized"
    for row in ranked_markets
)
explanation_lookup = {
    row.get("market_id"): row
    for row in market_explanations
    if row.get("market_id") is not None
}

fetched_at = None
if isinstance(explanation_metadata, dict):
    fetched_at = explanation_metadata.get("fetched_at")
if fetched_at is None and isinstance(scoring_metadata, dict):
    fetched_at = scoring_metadata.get("fetched_at")

app_bundle = {
    "ranked_markets": [
        {
            "market_id": row.get("market_id"),
            "source": row.get("source"),
            "source_market_id": row.get("source_market_id"),
            "source_url": row.get("source_url"),
            "title": row.get("title"),
            "event_title": row.get("event_title"),
            "category": row.get("category"),
            "topic_tags": row.get("topic_tags"),
            "status": row.get("status"),
            "rank": row.get("rank"),
            "final_score": row.get("final_score"),
            "current_probability": row.get("yes_price"),
            "headline_reason": (explanation_lookup.get(row.get("market_id")) or {}).get("headline_reason") or row.get("headline_reason"),
            "short_explanation": (explanation_lookup.get(row.get("market_id")) or {}).get("short_explanation"),
            "primary_reason_code": row.get("primary_reason_code"),
            "time_since_update_hours": row.get("time_since_update_hours"),
            "time_to_resolution_hours": row.get("time_to_resolution_hours"),
            "confidence_band": row.get("confidence_band"),
        }
        for row in ranked_markets
    ],
    "market_explanations": market_explanations,
    "refresh_metadata": {
        "refresh_id": refresh_id_from_fetched_at(fetched_at),
        "source": SOURCE_NAME,
        "fetched_at": fetched_at,
        "market_count": len(ranked_markets),
        "open_market_count": sum(1 for row in ranked_markets if row.get("status") == "open"),
        "category_breakdown": [
            {"category": category, "market_count": count}
            for category, count in category_counts.most_common()
        ],
        "pipeline_version": PIPELINE_VERSION,
        "score_version": scoring_metadata.get("score_version") if isinstance(scoring_metadata, dict) else None,
        "notes": "Generated from the mirrored Zerve bridge blocks with heuristic category context.",
    },
}

bundle_metadata = {
    "source": SOURCE_NAME,
    "fetched_at": fetched_at,
    "ranked_market_count": len(app_bundle["ranked_markets"]),
    "explained_market_count": len(app_bundle["market_explanations"]),
    "refresh_id": app_bundle["refresh_metadata"].get("refresh_id"),
    "pipeline_version": PIPELINE_VERSION,
    "score_version": app_bundle["refresh_metadata"].get("score_version"),
}

print(f"bundle_ranked_count {bundle_metadata['ranked_market_count']}")
print(f"bundle_explained_count {bundle_metadata['explained_market_count']}")
if app_bundle["ranked_markets"]:
    first = app_bundle["ranked_markets"][0]
    print(f"top_market_id {first.get('market_id')}")
    print(f"top_rank {first.get('rank')}")
    print(f"top_score {first.get('final_score')}")
print(f"refresh_id {app_bundle['refresh_metadata'].get('refresh_id')}")
print(f"category_count {len(app_bundle['refresh_metadata'].get('category_breakdown', []))}")

if __name__ == "__main__":
    print(json.dumps(bundle_metadata, indent=2))

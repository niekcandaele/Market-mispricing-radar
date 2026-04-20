#!/usr/bin/env python3
"""QA summary block for Zerve-side Polymarket app-bundle outputs.

This snippet expects the previous block to have emitted:
- app_bundle
- bundle_metadata

Primary block outputs:
- qa_summary
- refresh_metadata

When run locally, it falls back to importing the mirrored app-bundle snippet.
"""

from __future__ import annotations

from collections import Counter
import importlib.util
import json
from pathlib import Path
from typing import Any


SOURCE_NAME = "polymarket"
TOP_PREVIEW_COUNT = 5


def market_key(row: dict[str, Any]) -> str:
    return str(row.get("market_id") or "")


try:
    app_bundle
    bundle_metadata
except NameError:
    snippet_dir = Path(__file__).resolve().parent
    bundle_path = snippet_dir / "polymarket_app_bundle_block.py"
    spec = importlib.util.spec_from_file_location("polymarket_app_bundle_block", bundle_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load app-bundle snippet from {bundle_path}")
    bundle_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bundle_module)
    app_bundle = bundle_module.app_bundle
    bundle_metadata = bundle_module.bundle_metadata


ranked_markets = app_bundle.get("ranked_markets", [])
market_explanations = app_bundle.get("market_explanations", [])
refresh_metadata = app_bundle.get("refresh_metadata", {})

rank_ids = [market_key(row) for row in ranked_markets if market_key(row)]
explanation_ids = [market_key(row) for row in market_explanations if market_key(row)]
missing_explanations = sorted(set(rank_ids) - set(explanation_ids))
extra_explanations = sorted(set(explanation_ids) - set(rank_ids))
rank_counts = Counter(row.get("rank") for row in ranked_markets if row.get("rank") is not None)
duplicate_ranks = sorted(rank for rank, count in rank_counts.items() if count > 1)
reason_counts = Counter(
    row.get("primary_reason_code") or "unknown"
    for row in ranked_markets
)
confidence_counts = Counter(
    row.get("confidence_band") or "unknown"
    for row in ranked_markets
)
category_counts = Counter(
    row.get("category") or "uncategorized"
    for row in ranked_markets
)

warnings: list[dict[str, Any]] = []
if not ranked_markets:
    warnings.append({"code": "no_ranked_markets", "severity": "high", "message": "No ranked markets were present in the app bundle."})
if len(ranked_markets) != len(market_explanations):
    warnings.append({
        "code": "bundle_count_mismatch",
        "severity": "high",
        "message": "Ranked-market count does not match explanation count.",
        "ranked_market_count": len(ranked_markets),
        "explained_market_count": len(market_explanations),
    })
if missing_explanations:
    warnings.append({
        "code": "missing_explanations",
        "severity": "high",
        "message": "Some ranked markets are missing explanation records.",
        "market_ids": missing_explanations[:10],
        "truncated": len(missing_explanations) > 10,
    })
if extra_explanations:
    warnings.append({
        "code": "orphan_explanations",
        "severity": "medium",
        "message": "Some explanation records do not map to ranked markets.",
        "market_ids": extra_explanations[:10],
        "truncated": len(extra_explanations) > 10,
    })
if duplicate_ranks:
    warnings.append({
        "code": "duplicate_ranks",
        "severity": "medium",
        "message": "Multiple ranked rows share the same rank value.",
        "ranks": duplicate_ranks,
    })
if ranked_markets and confidence_counts.get("low", 0) / max(len(ranked_markets), 1) >= 0.5:
    warnings.append({
        "code": "many_low_confidence_results",
        "severity": "medium",
        "message": "At least half of the ranked markets are currently low confidence.",
        "low_confidence_count": confidence_counts.get("low", 0),
    })
if refresh_metadata.get("open_market_count", 0) == 0 and ranked_markets:
    warnings.append({
        "code": "no_open_markets",
        "severity": "medium",
        "message": "The refresh contains ranked markets but zero open markets in metadata.",
    })
if len(category_counts) <= 1 and ranked_markets:
    warnings.append({
        "code": "thin_category_coverage",
        "severity": "low",
        "message": "The current ranked slice falls into only one inferred category.",
        "category_count": len(category_counts),
    })

qa_summary = {
    "source": SOURCE_NAME,
    "refresh_metadata": refresh_metadata,
    "counts": {
        "ranked_market_count": len(ranked_markets),
        "explained_market_count": len(market_explanations),
        "open_market_count": refresh_metadata.get("open_market_count"),
        "category_count": len(category_counts),
        "warning_count": len(warnings),
    },
    "reason_breakdown": [
        {"reason_code": reason, "market_count": count}
        for reason, count in reason_counts.most_common()
    ],
    "confidence_breakdown": [
        {"confidence_band": band, "market_count": count}
        for band, count in confidence_counts.most_common()
    ],
    "top_preview": [
        {
            "market_id": row.get("market_id"),
            "rank": row.get("rank"),
            "title": row.get("title"),
            "final_score": row.get("final_score"),
            "primary_reason_code": row.get("primary_reason_code"),
            "headline_reason": row.get("headline_reason"),
            "confidence_band": row.get("confidence_band"),
        }
        for row in ranked_markets[:TOP_PREVIEW_COUNT]
    ],
    "validation_checks": {
        "counts_match": len(ranked_markets) == len(market_explanations),
        "missing_explanations": len(missing_explanations),
        "orphan_explanations": len(extra_explanations),
        "duplicate_rank_count": len(duplicate_ranks),
        "refresh_id_present": bool(refresh_metadata.get("refresh_id")),
        "fetched_at_present": bool(refresh_metadata.get("fetched_at")),
    },
    "warnings": warnings,
    "notes": [
        "This QA block is meant for notebook-side sanity checks, not as a replacement for deeper model evaluation.",
        "Warnings are machine-readable so later blocks or the app surface can surface trust signals cleanly.",
    ],
}

print(f"qa_ranked_count {qa_summary['counts']['ranked_market_count']}")
print(f"qa_warning_count {qa_summary['counts']['warning_count']}")
print(f"qa_counts_match {qa_summary['validation_checks']['counts_match']}")
print(f"qa_refresh_id_present {qa_summary['validation_checks']['refresh_id_present']}")
if qa_summary["top_preview"]:
    first = qa_summary["top_preview"][0]
    print(f"top_market_id {first.get('market_id')}")
    print(f"top_reason {first.get('primary_reason_code')}")
    print(f"top_confidence {first.get('confidence_band')}")

if __name__ == "__main__":
    print(json.dumps(qa_summary, indent=2))

#!/usr/bin/env python3
"""Mirrored Streamlit app scaffold for Zerve-side Market Mispricing Radar outputs.

Expected upstream variables in Zerve:
- app_bundle
- qa_summary

In deployed Zerve Streamlit, this app can also load those variables through
`from zerve import variable` using block-level lookups. Override block names with:
- `MMR_ZERVE_APP_BUNDLE_BLOCK`
- `MMR_ZERVE_QA_BLOCK`

When run locally, this file falls back to importing the mirrored bridge blocks.
It is intentionally lightweight and aimed at proving the deployment-layer handoff,
not at replacing the richer local HTML demo.
"""

from __future__ import annotations

import importlib.util
from collections import Counter
import json
import os
from pathlib import Path
from typing import Any

try:
    import streamlit as st
except ImportError:  # pragma: no cover - local syntax validation should still work
    st = None


FILTER_STATE_DEFAULTS = {
    "active_view": "Radar",
    "source_filter": "All",
    "category_filter": "All",
    "min_score": 0.0,
    "result_limit": 10,
    "sort_mode": "score_desc",
    "selected_market_id": None,
}

PENDING_ACTIVE_VIEW_KEY = "_pending_active_view"
PENDING_SELECTED_MARKET_KEY = "_pending_selected_market_id"


SOURCE_NAME = "polymarket"
TOP_PREVIEW_COUNT = 5
LOCAL_BUNDLE_ENV_VAR = "MMR_APP_BUNDLE_PATH"
ZERVE_APP_BUNDLE_BLOCK_ENV_VAR = "MMR_ZERVE_APP_BUNDLE_BLOCK"
ZERVE_QA_BLOCK_ENV_VAR = "MMR_ZERVE_QA_BLOCK"
DEFAULT_ZERVE_APP_BUNDLE_BLOCKS = (
    "build_app_bundle",
    "polymarket_app_bundle_block",
    "app_bundle",
)
DEFAULT_ZERVE_QA_BLOCKS = (
    "build_qa_summary",
    "polymarket_qa_block",
    "qa_summary",
)


def qa_market_key(row: dict[str, Any]) -> str:
    return str(row.get("market_id") or "")


def build_qa_summary(bundle: dict[str, Any]) -> dict[str, Any]:
    ranked_rows = bundle.get("ranked_markets") or []
    explanation_rows = bundle.get("market_explanations") or []
    bundle_refresh_metadata = bundle.get("refresh_metadata") or {}

    rank_ids = [qa_market_key(row) for row in ranked_rows if qa_market_key(row)]
    explanation_ids = [qa_market_key(row) for row in explanation_rows if qa_market_key(row)]
    missing_explanations = sorted(set(rank_ids) - set(explanation_ids))
    extra_explanations = sorted(set(explanation_ids) - set(rank_ids))
    rank_counts = Counter(row.get("rank") for row in ranked_rows if row.get("rank") is not None)
    duplicate_ranks = sorted(rank for rank, count in rank_counts.items() if count > 1)
    reason_counts = Counter(row.get("primary_reason_code") or "unknown" for row in ranked_rows)
    confidence_counts = Counter(row.get("confidence_band") or "unknown" for row in ranked_rows)
    category_counts = Counter(row.get("category") or "uncategorized" for row in ranked_rows)

    warnings: list[dict[str, Any]] = []
    if not ranked_rows:
        warnings.append({
            "code": "no_ranked_markets",
            "severity": "high",
            "message": "No ranked markets were present in the app bundle.",
        })
    if len(ranked_rows) != len(explanation_rows):
        warnings.append({
            "code": "bundle_count_mismatch",
            "severity": "high",
            "message": "Ranked-market count does not match explanation count.",
            "ranked_market_count": len(ranked_rows),
            "explained_market_count": len(explanation_rows),
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
    if ranked_rows and confidence_counts.get("low", 0) / max(len(ranked_rows), 1) >= 0.5:
        warnings.append({
            "code": "many_low_confidence_results",
            "severity": "medium",
            "message": "At least half of the ranked markets are currently low confidence.",
            "low_confidence_count": confidence_counts.get("low", 0),
        })
    if bundle_refresh_metadata.get("open_market_count", 0) == 0 and ranked_rows:
        warnings.append({
            "code": "no_open_markets",
            "severity": "medium",
            "message": "The refresh contains ranked markets but zero open markets in metadata.",
        })
    if len(category_counts) <= 1 and ranked_rows:
        warnings.append({
            "code": "thin_category_coverage",
            "severity": "low",
            "message": "The current ranked slice falls into only one inferred category.",
            "category_count": len(category_counts),
        })

    return {
        "source": SOURCE_NAME,
        "refresh_metadata": bundle_refresh_metadata,
        "counts": {
            "ranked_market_count": len(ranked_rows),
            "explained_market_count": len(explanation_rows),
            "open_market_count": bundle_refresh_metadata.get("open_market_count"),
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
            for row in ranked_rows[:TOP_PREVIEW_COUNT]
        ],
        "validation_checks": {
            "counts_match": len(ranked_rows) == len(explanation_rows),
            "missing_explanations": len(missing_explanations),
            "orphan_explanations": len(extra_explanations),
            "duplicate_rank_count": len(duplicate_ranks),
            "refresh_id_present": bool(bundle_refresh_metadata.get("refresh_id")),
            "fetched_at_present": bool(bundle_refresh_metadata.get("fetched_at")),
        },
        "warnings": warnings,
        "notes": [
            "This QA summary is meant for app-side sanity checks, not as a replacement for deeper model evaluation.",
            "Warnings are machine-readable so the app can surface trust signals cleanly.",
        ],
    }


def load_local_bundle_artifact() -> tuple[dict[str, Any] | None, Path | None]:
    repo_root = Path(__file__).resolve().parents[2]
    configured_path = os.environ.get(LOCAL_BUNDLE_ENV_VAR)
    candidate_paths: list[Path] = []
    if configured_path:
        candidate_paths.append(Path(configured_path).expanduser())
    candidate_paths.append(repo_root / "artifacts" / "streamlit" / "app_bundle.json")

    for path in candidate_paths:
        if not path.exists() or not path.is_file():
            continue
        payload = json.loads(path.read_text())
        if isinstance(payload, dict) and all(key in payload for key in ["ranked_markets", "market_explanations", "refresh_metadata"]):
            return payload, path
        if isinstance(payload, dict) and isinstance(payload.get("app_bundle"), dict):
            return payload["app_bundle"], path
        raise RuntimeError(f"Local app bundle at {path} does not match the expected bundle shape.")

    return None, None


def load_zerve_variable(
    block_env_var: str,
    default_blocks: tuple[str, ...],
    variable_name: str,
) -> tuple[Any | None, str | None, list[dict[str, str]]]:
    try:
        from zerve import variable as zerve_variable
    except ImportError:
        return None, None, []

    configured_block = (os.environ.get(block_env_var) or "").strip()
    block_candidates = [configured_block] if configured_block else list(default_blocks)
    errors: list[dict[str, str]] = []

    for block_name in block_candidates:
        if not block_name:
            continue
        try:
            return zerve_variable(block_name, variable_name), block_name, errors
        except Exception as exc:
            errors.append(
                {
                    "block_name": block_name,
                    "variable_name": variable_name,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

    return None, None, errors


def zerve_block_context() -> str | None:
    if not loaded_zerve_block_names:
        return None
    return ", ".join(
        f"{variable_name}: {block_name}"
        for variable_name, block_name in sorted(loaded_zerve_block_names.items())
    )


bundle_input_origin = "zerve-upstream"
loaded_local_bundle_path: Path | None = None
loaded_zerve_block_names: dict[str, str] = {}
zerve_variable_load_errors: list[dict[str, str]] = []


try:
    app_bundle
except NameError:
    app_bundle = None


try:
    qa_summary
except NameError:
    qa_summary = None


if app_bundle is None:
    app_bundle, app_bundle_block_name, app_bundle_errors = load_zerve_variable(
        ZERVE_APP_BUNDLE_BLOCK_ENV_VAR,
        DEFAULT_ZERVE_APP_BUNDLE_BLOCKS,
        "app_bundle",
    )
    zerve_variable_load_errors.extend(app_bundle_errors)
    if app_bundle is not None and app_bundle_block_name is not None:
        bundle_input_origin = "zerve-variable"
        loaded_zerve_block_names["app_bundle"] = app_bundle_block_name


if qa_summary is None:
    qa_summary, qa_block_name, qa_errors = load_zerve_variable(
        ZERVE_QA_BLOCK_ENV_VAR,
        DEFAULT_ZERVE_QA_BLOCKS,
        "qa_summary",
    )
    zerve_variable_load_errors.extend(qa_errors)
    if qa_summary is not None and qa_block_name is not None:
        bundle_input_origin = "zerve-variable"
        loaded_zerve_block_names["qa_summary"] = qa_block_name


if app_bundle is None:
    app_bundle, loaded_local_bundle_path = load_local_bundle_artifact()
    if app_bundle is not None:
        bundle_input_origin = "local-artifact"


if app_bundle is None:
    snippet_dir = Path(__file__).resolve().parents[1] / "snippets"

    bundle_path = snippet_dir / "polymarket_app_bundle_block.py"
    bundle_spec = importlib.util.spec_from_file_location("polymarket_app_bundle_block", bundle_path)
    if bundle_spec is None or bundle_spec.loader is None:
        raise RuntimeError(f"Could not load app bundle snippet from {bundle_path}")
    bundle_module = importlib.util.module_from_spec(bundle_spec)
    bundle_spec.loader.exec_module(bundle_module)
    app_bundle = bundle_module.app_bundle

    qa_path = snippet_dir / "polymarket_qa_block.py"
    qa_spec = importlib.util.spec_from_file_location("polymarket_qa_block", qa_path)
    if qa_spec is None or qa_spec.loader is None:
        raise RuntimeError(f"Could not load QA snippet from {qa_path}")
    qa_module = importlib.util.module_from_spec(qa_spec)
    qa_spec.loader.exec_module(qa_module)
    qa_summary = qa_module.qa_summary
    bundle_input_origin = "snippet-fallback"


if qa_summary is None:
    qa_summary = build_qa_summary(app_bundle)


ranked_markets = app_bundle.get("ranked_markets", [])
market_explanations = app_bundle.get("market_explanations", [])
refresh_metadata = app_bundle.get("refresh_metadata", {})
ranked_market_lookup = {
    row.get("market_id"): row
    for row in ranked_markets
    if row.get("market_id")
}
explanation_lookup = {
    row.get("market_id"): row
    for row in market_explanations
    if row.get("market_id")
}


def market_label(row: dict[str, Any]) -> str:
    rank = row.get("rank", "?")
    title = row.get("title") or "Untitled market"
    score = row.get("final_score")
    if isinstance(score, (int, float)):
        return f"#{rank} · {title} ({score:.3f})"
    return f"#{rank} · {title}"


def available_categories(rows: list[dict[str, Any]]) -> list[str]:
    return sorted({row.get("category") for row in rows if row.get("category")})


def source_count(rows: list[dict[str, Any]]) -> int:
    return len({row.get("source") for row in rows if row.get("source")})


def category_breakdown_rows() -> list[dict[str, Any]]:
    return refresh_metadata.get("category_breakdown") or []


def filter_rows(
    rows: list[dict[str, Any]],
    source_filter: str,
    category_filter: str,
    min_score: float,
    limit: int,
    sort_mode: str,
) -> list[dict[str, Any]]:
    filtered = []
    for row in rows:
        if source_filter != "All" and row.get("source") != source_filter:
            continue
        if category_filter != "All" and row.get("category") != category_filter:
            continue
        score = row.get("final_score")
        if isinstance(score, (int, float)) and score < min_score:
            continue
        filtered.append(row)

    if sort_mode == "stale_desc":
        filtered.sort(
            key=lambda item: (
                item.get("time_since_update_hours") is None,
                -(item.get("time_since_update_hours") or 0.0),
            )
        )
    elif sort_mode == "resolution_asc":
        filtered.sort(
            key=lambda item: (
                item.get("time_to_resolution_hours") is None,
                item.get("time_to_resolution_hours") or float("inf"),
            )
        )
    else:
        filtered.sort(key=lambda item: item.get("final_score") or 0.0, reverse=True)
    return filtered[:limit]


def top_warning_messages() -> list[str]:
    warnings = []
    for warning in qa_summary.get("warnings", []):
        severity = (warning.get("severity") or "info").upper()
        message = warning.get("message") or warning.get("code") or "Unnamed warning"
        warnings.append(f"{severity}: {message}")
    return warnings



def radar_warning_summary() -> str | None:
    warnings = top_warning_messages()
    if not warnings:
        return None
    warning_count = len(warnings)
    noun = "warning" if warning_count == 1 else "warnings"
    return f"This refresh has {warning_count} active QA {noun}. The landing slice is still visible, but it should be interpreted with those caveats in mind."



def filtered_slice_summary(filtered: list[dict[str, Any]]) -> list[dict[str, Any]]:
    focused_market_id = None if st is None else st.session_state.get("selected_market_id")
    visible_scores = [row.get("final_score") for row in filtered if isinstance(row.get("final_score"), (int, float))]
    visible_categories = {row.get("category") for row in filtered if row.get("category")}
    focused_visible = any(row.get("market_id") == focused_market_id for row in filtered)
    return [
        {"label": "Visible results", "value": len(filtered)},
        {"label": "Top visible score", "value": f"{max(visible_scores):.3f}" if visible_scores else "unknown"},
        {"label": "Visible categories", "value": len(visible_categories)},
        {"label": "Focused in slice", "value": "yes" if focused_visible else "no"},
    ]



def filtered_reason_breakdown(filtered: list[dict[str, Any]]) -> list[dict[str, Any]]:
    reason_counts = Counter(
        row.get("primary_reason_code") or "unknown"
        for row in filtered
    )
    return [
        {"reason_code": reason_code, "count": count}
        for reason_code, count in reason_counts.most_common(5)
    ]



def methodology_live_context_rows() -> list[dict[str, Any]]:
    rows = [
        {"label": "Refresh ID", "value": refresh_metadata.get("refresh_id") or "unknown"},
        {"label": "Fetched at", "value": refresh_metadata.get("fetched_at") or "unknown"},
        {"label": "Source count", "value": source_count(ranked_markets)},
        {"label": "Bundle origin", "value": bundle_input_origin.replace("-", " ")},
        {"label": "QA warnings", "value": len(qa_summary.get("warnings") or [])},
    ]
    block_context = zerve_block_context()
    if block_context:
        rows.append({"label": "Zerve blocks", "value": block_context})
    return rows



def methodology_warning_rows() -> list[dict[str, Any]]:
    rows = []
    for warning in qa_summary.get("warnings", []):
        rows.append(
            {
                "severity": (warning.get("severity") or "info").upper(),
                "code": warning.get("code") or "unknown",
                "message": warning.get("message") or "Unnamed warning",
            }
        )
    return rows



def methodology_sections() -> list[tuple[str, list[str]]]:
    return [
        (
            "What the radar is doing",
            [
                "It ranks markets whose current price deserves a second look because the market appears stale, fragile, extreme, or weakly supported.",
                "It is built to help an operator prioritize inspection, not to bury them under a flat list of odds.",
            ],
        ),
        (
            "How to read the score",
            [
                "A higher score means more signals are pointing at a market that may be unstable, under-supported, or unusually exposed to stale pricing.",
                "The score is a triage signal, not a claim that the market is objectively wrong or that free money exists.",
            ],
        ),
        (
            "Why a market appears near the top",
            [
                "The radar looks for combinations of stale updates, short time horizons, extreme pricing, thin liquidity support, and meaningful recent movement when that data exists.",
                "Each row carries an explanation headline and reason code so the ranking stays inspectable instead of opaque.",
            ],
        ),
        (
            "Current MVP scope",
            [
                "Polymarket-first, with one live source wired end to end inside Zerve.",
                "Explainable component-based scoring rather than a black-box prediction model.",
                "Designed as a strong hackathon MVP, with room to add cross-source comparisons later.",
            ],
        ),
        (
            "What this product does not claim",
            [
                "Not guaranteed arbitrage.",
                "Not a perfect fair-value model.",
                "Not financial advice.",
            ],
        ),
        (
            "Caveats",
            [
                "Single-source MVP, so cross-market confirmation is still limited.",
                "Some market structures are simplified or excluded to keep the first version reliable.",
                "Output quality still depends on source freshness, liquidity visibility, and available metadata.",
            ],
        ),
    ]


def format_hours(value: Any) -> str:
    if not isinstance(value, (int, float)):
        return "unknown"
    return f"{value:.1f}h"


def format_value(value: Any) -> str:
    if value is None:
        return "unknown"
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def component_label(key: str) -> str:
    labels = {
        "staleness_component": "Staleness",
        "event_horizon_component": "Time to resolution",
        "extremeness_component": "Price extremeness",
        "liquidity_component": "Liquidity support",
        "volatility_component": "Volatility",
        "data_quality_penalty": "Data quality penalty",
        "heuristic_penalty": "Heuristic penalty",
    }
    return labels.get(key, key.replace("_", " ").title())


def signal_label(key: str) -> str:
    labels = {
        "time_since_update_hours": "Time since update",
        "time_to_resolution_hours": "Time to resolution",
        "price_distance_from_mid": "Distance from midpoint",
        "liquidity": "Liquidity",
        "volume_24hr": "24h volume",
        "one_month_price_change_abs": "One-month move",
    }
    return labels.get(key, key.replace("_", " ").title())


def score_component_rows(explanation: dict[str, Any]) -> list[dict[str, Any]]:
    components = explanation.get("score_components") or {}
    ordered = [
        "staleness_component",
        "event_horizon_component",
        "extremeness_component",
        "liquidity_component",
        "volatility_component",
        "data_quality_penalty",
        "heuristic_penalty",
    ]
    rows = []
    for key in ordered:
        value = components.get(key)
        if value is None:
            continue
        rows.append({"label": component_label(key), "value": float(value)})
    return rows


def supporting_signal_rows(explanation: dict[str, Any]) -> list[dict[str, Any]]:
    values = explanation.get("supporting_signal_values") or {}
    ordered = [
        "time_since_update_hours",
        "time_to_resolution_hours",
        "price_distance_from_mid",
        "liquidity",
        "volume_24hr",
        "one_month_price_change_abs",
    ]
    rows = []
    for key in ordered:
        rows.append({"signal": signal_label(key), "value": format_value(values.get(key))})
    return rows


def peer_comparison_rows(filtered: list[dict[str, Any]], selected_row: dict[str, Any]) -> list[dict[str, Any]]:
    selected_market_id = selected_row.get("market_id")
    selected_category = selected_row.get("category")
    if not selected_category:
        return []

    peers = [
        row for row in filtered
        if row.get("market_id") != selected_market_id and row.get("category") == selected_category
    ]
    peers.sort(key=lambda item: item.get("final_score") or 0.0, reverse=True)
    return [
        {
            "rank": row.get("rank"),
            "title": row.get("title"),
            "score": row.get("final_score"),
            "probability": row.get("current_probability"),
            "reason": row.get("primary_reason_code"),
        }
        for row in peers[:5]
    ]


def radar_card_rows(filtered: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "market_id": row.get("market_id"),
            "rank": row.get("rank"),
            "title": row.get("title"),
            "headline_reason": row.get("headline_reason"),
            "category": row.get("category"),
            "source": row.get("source"),
            "score": row.get("final_score"),
            "probability": row.get("current_probability"),
            "hours_since_update": row.get("time_since_update_hours"),
            "source_url": row.get("source_url"),
        }
        for row in filtered
    ]


def pipeline_ready() -> bool:
    return bool(ranked_markets and market_explanations)


def unavailable_context_lines() -> list[str]:
    lines = ["The pipeline has not produced a complete app bundle yet."]
    if refresh_metadata.get("refresh_id"):
        lines.append(f"Last known refresh ID: {refresh_metadata.get('refresh_id')}")
    if refresh_metadata.get("fetched_at"):
        lines.append(f"Last known refresh time: {refresh_metadata.get('fetched_at')}")
    return lines


def missing_detail_notes(selected_row: dict[str, Any], explanation: dict[str, Any]) -> list[str]:
    notes = []
    if not selected_row.get("source_url"):
        notes.append("Source link is unavailable for this market.")
    if selected_row.get("time_to_resolution_hours") is None:
        notes.append("Resolution timing is unavailable for this market.")
    if selected_row.get("time_since_update_hours") is None:
        notes.append("Update-age timing is unavailable for this market.")
    if not (explanation.get("supporting_signal_values") or {}):
        notes.append("Supporting signal values are unavailable for this market.")
    if not (explanation.get("score_components") or {}):
        notes.append("Score components are unavailable for this market.")
    return notes


def ensure_filter_defaults() -> None:
    if st is None:
        return
    for key, value in FILTER_STATE_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_filter_state() -> None:
    if st is None:
        return
    for key, value in FILTER_STATE_DEFAULTS.items():
        st.session_state[key] = value


def normalize_filter_choices(source_options: list[str], category_options: list[str]) -> None:
    if st is None:
        return
    if st.session_state.get("source_filter") not in source_options:
        st.session_state["source_filter"] = "All"
    if st.session_state.get("category_filter") not in category_options:
        st.session_state["category_filter"] = "All"
    if st.session_state.get("result_limit") not in [10, 25, 50, 100]:
        st.session_state["result_limit"] = 10
    if st.session_state.get("sort_mode") not in ["score_desc", "stale_desc", "resolution_asc"]:
        st.session_state["sort_mode"] = "score_desc"
    if st.session_state.get("active_view") not in ["Radar", "Market Detail", "Methodology"]:
        st.session_state["active_view"] = "Radar"


def queue_navigation(*, view: str | None = None, market_id: str | None = None) -> None:
    if st is None:
        return
    if view is not None:
        st.session_state[PENDING_ACTIVE_VIEW_KEY] = view
    if market_id is not None:
        st.session_state[PENDING_SELECTED_MARKET_KEY] = market_id



def apply_pending_navigation() -> None:
    if st is None:
        return
    pending_view = st.session_state.pop(PENDING_ACTIVE_VIEW_KEY, None)
    pending_market_id = st.session_state.pop(PENDING_SELECTED_MARKET_KEY, None)
    if pending_view is not None:
        st.session_state["active_view"] = pending_view
    if pending_market_id is not None:
        st.session_state["selected_market_id"] = pending_market_id



def focused_market_outside_filters(filtered: list[dict[str, Any]]) -> bool:
    if st is None:
        return False
    current_market_id = st.session_state.get("selected_market_id")
    if current_market_id not in ranked_market_lookup:
        return False
    filtered_market_ids = {row.get("market_id") for row in filtered if row.get("market_id")}
    return current_market_id not in filtered_market_ids



def filtered_market_ids(filtered: list[dict[str, Any]]) -> list[str]:
    return [row.get("market_id") for row in filtered if row.get("market_id")]



def filtered_position_context(selected_row: dict[str, Any], filtered: list[dict[str, Any]]) -> str | None:
    market_id = selected_row.get("market_id")
    market_ids = filtered_market_ids(filtered)
    if not market_id:
        return None
    if market_id not in market_ids:
        return None
    index = market_ids.index(market_id)
    return f"Showing result {index + 1} of {len(market_ids)} in the current Radar slice."



def adjacent_market_ids(selected_row: dict[str, Any], filtered: list[dict[str, Any]]) -> tuple[str | None, str | None]:
    market_id = selected_row.get("market_id")
    market_ids = filtered_market_ids(filtered)
    if not market_id or market_id not in market_ids:
        return None, None
    index = market_ids.index(market_id)
    previous_id = market_ids[index - 1] if index > 0 else None
    next_id = market_ids[index + 1] if index + 1 < len(market_ids) else None
    return previous_id, next_id



def selected_market(filtered: list[dict[str, Any]]) -> dict[str, Any] | None:
    filtered_market_ids = [row.get("market_id") for row in filtered if row.get("market_id")]

    if st is None:
        if filtered:
            return filtered[0]
        return ranked_markets[0] if ranked_markets else None

    current_market_id = st.session_state.get("selected_market_id")
    if current_market_id not in ranked_market_lookup:
        if filtered_market_ids:
            current_market_id = filtered_market_ids[0]
            st.session_state["selected_market_id"] = current_market_id
        elif ranked_markets:
            current_market_id = ranked_markets[0].get("market_id")
            st.session_state["selected_market_id"] = current_market_id
        else:
            return None

    select_options = list(filtered_market_ids)
    if current_market_id and current_market_id not in select_options:
        select_options = [current_market_id] + select_options

    label_lookup = {market_id: market_label(row) for market_id, row in ranked_market_lookup.items()}
    if current_market_id in ranked_market_lookup and current_market_id not in filtered_market_ids:
        label_lookup[current_market_id] = f"{label_lookup.get(current_market_id, current_market_id)} (outside current filters)"

    selected_market_id = st.selectbox(
        "Select market",
        select_options,
        format_func=lambda item: label_lookup.get(item, item),
        key="selected_market_id",
    )
    return ranked_market_lookup.get(selected_market_id)


def render_app() -> None:
    if st is None:
        raise RuntimeError("streamlit is not installed. Use this file inside Zerve or install streamlit locally.")

    ensure_filter_defaults()
    apply_pending_navigation()

    source_options = ["All"] + sorted({row.get("source") or "unknown" for row in ranked_markets})
    category_options = ["All"] + available_categories(ranked_markets)
    normalize_filter_choices(source_options, category_options)

    st.set_page_config(page_title="Market Mispricing Radar", layout="wide")
    st.title("Market Mispricing Radar")
    st.caption("Find prediction markets whose pricing looks fragile, stale, or weakly supported.")
    st.write("A live decision-support radar for markets that deserve a second look before you trust the current odds.")

    if not pipeline_ready():
        st.warning("Pipeline output is not fully ready yet. The app is showing an honest unavailable state.")
        for line in unavailable_context_lines():
            st.write(f"- {line}")

    with st.sidebar:
        st.header("Navigation")
        st.radio("View", ["Radar", "Market Detail", "Methodology"], key="active_view", label_visibility="collapsed")

        st.header("Controls")
        st.selectbox("Source", source_options, key="source_filter")
        st.selectbox("Category", category_options, key="category_filter")
        st.slider("Minimum score", 0.0, 1.0, step=0.05, key="min_score")
        st.selectbox("Result count", [10, 25, 50, 100], key="result_limit")
        st.selectbox(
            "Sort",
            ["score_desc", "stale_desc", "resolution_asc"],
            format_func=lambda item: {
                "score_desc": "Highest score",
                "stale_desc": "Most stale",
                "resolution_asc": "Closest to resolution",
            }.get(item, item),
            key="sort_mode",
        )
        if st.button("Reset filters", use_container_width=True):
            reset_filter_state()
            st.rerun()

        st.header("Run status")
        st.write(f"Refresh ID: {refresh_metadata.get('refresh_id') or 'unknown'}")
        st.write(f"Fetched at: {refresh_metadata.get('fetched_at') or 'unknown'}")
        st.write(f"Market count: {refresh_metadata.get('market_count') or 0}")
        st.write(f"Open markets: {refresh_metadata.get('open_market_count') or 0}")
        st.write(f"Source count: {source_count(ranked_markets)}")
        st.write(f"Score version: {refresh_metadata.get('score_version') or 'unknown'}")

        block_context = zerve_block_context()
        with st.expander("Operator context", expanded=False):
            st.write(f"Bundle origin: {bundle_input_origin.replace('-', ' ')}")
            if block_context:
                st.caption(f"Zerve blocks: {block_context}")
            elif loaded_local_bundle_path is not None:
                st.caption(str(loaded_local_bundle_path))

        warnings = top_warning_messages()
        if warnings:
            st.header("QA warnings")
            for item in warnings:
                st.warning(item)

    filtered = filter_rows(
        ranked_markets,
        st.session_state["source_filter"],
        st.session_state["category_filter"],
        st.session_state["min_score"],
        st.session_state["result_limit"],
        st.session_state["sort_mode"],
    )

    active_view = st.session_state["active_view"]

    if active_view == "Radar":
        st.subheader("Ranked Radar")
        st.caption("Scan for markets where freshness, extremeness, liquidity, and recent movement point to a price that deserves scrutiny.")
        trust_cols = st.columns(4)
        trust_cols[0].metric("Refresh ID", refresh_metadata.get("refresh_id") or "unknown")
        trust_cols[1].metric("Processed", refresh_metadata.get("market_count") or 0)
        trust_cols[2].metric("Open markets", refresh_metadata.get("open_market_count") or 0)
        trust_cols[3].metric("Sources", source_count(ranked_markets))

        radar_warning = radar_warning_summary()
        warnings = top_warning_messages()
        if radar_warning:
            st.warning(radar_warning)
            with st.expander("View active QA warnings", expanded=True):
                for item in warnings[:5]:
                    st.write(f"- {item}")
                if len(warnings) > 5:
                    st.caption(f"Plus {len(warnings) - 5} additional warning(s) in the full QA summary.")

        if category_breakdown_rows():
            st.markdown("#### Category snapshot")
            st.dataframe(category_breakdown_rows(), use_container_width=True)

        if filtered:
            st.markdown("#### Current filtered slice")
            summary_cols = st.columns(4)
            for column, item in zip(summary_cols, filtered_slice_summary(filtered)):
                column.metric(item["label"], item["value"])

            reason_rows = filtered_reason_breakdown(filtered)
            if reason_rows:
                st.markdown("#### Dominant reason codes in current slice")
                st.dataframe(reason_rows, use_container_width=True)

        if not pipeline_ready():
            st.info("No ranked results are available yet. Refresh the pipeline and try again.")
        elif not filtered:
            st.info("No results match the current filters, so there is no current slice summary to show.")
            if st.button("Reset filters from empty state", key="reset-empty-state"):
                reset_filter_state()
                st.rerun()
        else:
            st.caption(f"Showing {len(filtered)} filtered results. Focus a market to jump directly into the detail view.")
            for row in radar_card_rows(filtered):
                with st.container(border=True):
                    top_left, top_mid, top_right = st.columns([3, 1, 1])
                    with top_left:
                        st.markdown(f"**#{row.get('rank')} · {row.get('title')}**")
                        st.write(row.get("headline_reason") or "No headline reason available.")
                        st.caption(f"{row.get('source') or 'unknown source'} • {row.get('category') or 'uncategorized'}")
                    with top_mid:
                        st.metric("Score", row.get("score") or 0.0)
                    with top_right:
                        st.metric("Probability", row.get("probability") or 0.0)

                    meta_cols = st.columns([1, 1, 2])
                    meta_cols[0].write(f"Update age: {format_hours(row.get('hours_since_update'))}")
                    meta_cols[1].write(f"Focused: {'yes' if row.get('market_id') == st.session_state.get('selected_market_id') else 'no'}")
                    with meta_cols[2]:
                        action_cols = st.columns(2)
                        if action_cols[0].button("Focus in detail", key=f"focus-{row.get('market_id')}", use_container_width=True):
                            queue_navigation(view="Market Detail", market_id=row.get("market_id"))
                            st.rerun()
                        if row.get("source_url"):
                            action_cols[1].link_button("Open source", row["source_url"], use_container_width=True)

    elif active_view == "Market Detail":
        st.subheader("Market Detail")
        st.caption("Drill into one market to see why the radar flagged it, what signals are supporting that view, and what caveats still apply.")
        selected_row = selected_market(filtered)
        if not pipeline_ready():
            st.info("Market detail is unavailable until the pipeline produces ranked markets and explanations.")
        elif selected_row is None:
            st.info("No market is available for the current filters.")
        else:
            if focused_market_outside_filters(filtered):
                st.warning("The focused market is outside the current Radar filters. The detail view is preserving that selection instead of silently swapping to a different market.")
                action_cols = st.columns(2)
                if action_cols[0].button("Reset filters to recover focused market", use_container_width=True):
                    reset_filter_state()
                    queue_navigation(view="Market Detail")
                    st.rerun()
                if action_cols[1].button("Return to Radar", use_container_width=True):
                    queue_navigation(view="Radar")
                    st.rerun()

            explanation = explanation_lookup.get(selected_row.get("market_id"), {})

            position_context = filtered_position_context(selected_row, filtered)
            previous_market_id, next_market_id = adjacent_market_ids(selected_row, filtered)
            if position_context:
                st.caption(position_context)
                nav_cols = st.columns(3)
                if nav_cols[0].button("Previous result", disabled=previous_market_id is None, use_container_width=True):
                    queue_navigation(market_id=previous_market_id)
                    st.rerun()
                if nav_cols[1].button("Back to Radar", use_container_width=True):
                    queue_navigation(view="Radar")
                    st.rerun()
                if nav_cols[2].button("Next result", disabled=next_market_id is None, use_container_width=True):
                    queue_navigation(market_id=next_market_id)
                    st.rerun()
            else:
                st.caption("This market is being shown outside the current Radar slice.")

            st.markdown(f"### {selected_row.get('title')}")
            header_left, header_mid, header_right = st.columns(3)
            with header_left:
                st.write(f"Source: {selected_row.get('source') or 'unknown'}")
                st.write(f"Status: {selected_row.get('status') or 'unknown'}")
                st.write(f"Refresh: {refresh_metadata.get('fetched_at') or 'unknown'}")
                if selected_row.get("source_url"):
                    st.link_button("Open source market", selected_row["source_url"])
            with header_mid:
                st.metric("Radar score", selected_row.get("final_score") or 0.0)
                st.metric("Market probability", selected_row.get("current_probability") or 0.0)
                st.write(f"Confidence band: {selected_row.get('confidence_band') or 'unknown'}")
                st.write(f"Primary reason code: {selected_row.get('primary_reason_code') or 'unknown'}")
            with header_right:
                st.write(f"Resolution horizon: {format_hours(selected_row.get('time_to_resolution_hours'))}")
                st.write(f"Last update age: {format_hours(selected_row.get('time_since_update_hours'))}")
                st.write(f"Category: {selected_row.get('category') or 'unknown'}")
                topics = selected_row.get("topic_tags") or []
                st.write(f"Topics: {', '.join(topics) if topics else 'none'}")

            st.markdown("#### Why this market is flagged")
            st.write(explanation.get("headline_reason") or selected_row.get("headline_reason"))
            st.write(explanation.get("short_explanation") or "No short explanation available.")
            st.write(explanation.get("detailed_explanation") or "No detailed explanation available.")

            st.markdown("#### What is driving the score")
            component_rows = score_component_rows(explanation)
            if component_rows:
                metric_cols = st.columns(min(4, len(component_rows)))
                for index, row in enumerate(component_rows):
                    column = metric_cols[index % len(metric_cols)]
                    with column:
                        st.metric(row["label"], f"{row['value']:.3f}")
                        st.progress(max(0.0, min(1.0, row["value"])))
            else:
                st.write("No score components are available for this market.")

            st.markdown("#### Observed market signals")
            st.dataframe(supporting_signal_rows(explanation), use_container_width=True)

            st.markdown("#### Comparable markets in the current view")
            peer_rows = peer_comparison_rows(filtered, selected_row)
            if peer_rows:
                st.dataframe(peer_rows, use_container_width=True)
            else:
                st.write("No comparable same-category markets are visible in the current filtered result set.")

            st.markdown("#### Caveats")
            caveats = explanation.get("caveats") or []
            if caveats:
                for item in caveats:
                    st.write(f"- {item}")
            else:
                st.write("No caveats were emitted for this market.")

            st.markdown("#### Data quality notes")
            notes = missing_detail_notes(selected_row, explanation)
            if notes:
                for note in notes:
                    st.write(f"- {note}")
            else:
                st.write("No important detail fields are currently missing for this market.")

    else:
        st.subheader("Methodology")
        st.caption("How the radar decides which markets deserve scrutiny, and where the current MVP is intentionally conservative.")
        if pipeline_ready():
            st.markdown("#### Current run context")
            context_cols = st.columns(5)
            for column, item in zip(context_cols, methodology_live_context_rows()):
                column.metric(item["label"], item["value"])

            warning_rows = methodology_warning_rows()
            if warning_rows:
                st.markdown("#### Current QA notes")
                st.dataframe(warning_rows, use_container_width=True)
            else:
                st.write("No QA warnings are active for the current run.")
        else:
            st.info("Live run context is unavailable because the pipeline output is not fully ready yet.")
            for line in unavailable_context_lines():
                st.write(f"- {line}")

        for heading, lines in methodology_sections():
            st.markdown(f"#### {heading}")
            for line in lines:
                st.write(f"- {line}")


def main() -> None:
    render_app()


if __name__ == "__main__":
    main()

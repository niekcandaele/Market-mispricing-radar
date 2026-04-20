#!/usr/bin/env python3
"""Mirrored Streamlit app scaffold for Zerve-side Market Mispricing Radar outputs.

Expected upstream variables in Zerve:
- app_bundle
- qa_summary

When run locally, this file falls back to importing the mirrored bridge blocks.
It is intentionally lightweight and aimed at proving the deployment-layer handoff,
not at replacing the richer local HTML demo.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

try:
    import streamlit as st
except ImportError:  # pragma: no cover - local syntax validation should still work
    st = None


FILTER_STATE_DEFAULTS = {
    "source_filter": "All",
    "category_filter": "All",
    "min_score": 0.0,
    "result_limit": 10,
    "sort_desc": True,
    "selected_market_id": None,
}


try:
    app_bundle
    qa_summary
except NameError:
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


ranked_markets = app_bundle.get("ranked_markets", [])
market_explanations = app_bundle.get("market_explanations", [])
refresh_metadata = app_bundle.get("refresh_metadata", {})
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
    sort_desc: bool,
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

    filtered.sort(key=lambda item: item.get("final_score") or 0.0, reverse=sort_desc)
    return filtered[:limit]


def top_warning_messages() -> list[str]:
    warnings = []
    for warning in qa_summary.get("warnings", []):
        severity = (warning.get("severity") or "info").upper()
        message = warning.get("message") or warning.get("code") or "Unnamed warning"
        warnings.append(f"{severity}: {message}")
    return warnings


def methodology_sections() -> list[tuple[str, list[str]]]:
    return [
        (
            "What the product does",
            [
                "Ranks markets that look stale, fragile, extreme, or weakly supported.",
                "Surfaces interpretable reasons for inspection instead of opaque scores alone.",
            ],
        ),
        (
            "What the product does not claim",
            [
                "Not guaranteed arbitrage.",
                "Not a perfect fair-value model.",
                "Not financial advice.",
            ],
        ),
        (
            "Current MVP scope",
            [
                "Polymarket-first.",
                "Single-source anomaly scoring.",
                "Explainable component-based ranking.",
            ],
        ),
        (
            "Score ingredients",
            [
                "Staleness.",
                "Time to resolution.",
                "Price extremeness.",
                "Liquidity support.",
                "Volatility or movement anomaly when available.",
            ],
        ),
        (
            "Caveats",
            [
                "Single-source MVP.",
                "Some market structures may be simplified or excluded.",
                "Quality depends on source freshness and available metadata.",
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


def selected_market(filtered: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not filtered or st is None:
        return filtered[0] if filtered else None

    market_ids = [row.get("market_id") for row in filtered if row.get("market_id")]
    if not market_ids:
        return filtered[0]

    current_market_id = st.session_state.get("selected_market_id")
    if current_market_id not in market_ids:
        st.session_state["selected_market_id"] = market_ids[0]
        current_market_id = market_ids[0]

    label_lookup = {row.get("market_id"): market_label(row) for row in filtered if row.get("market_id")}
    selected_market_id = st.selectbox(
        "Select market",
        market_ids,
        format_func=lambda item: label_lookup.get(item, item),
        key="selected_market_id",
    )
    return next((row for row in filtered if row.get("market_id") == selected_market_id), filtered[0])


def render_app() -> None:
    if st is None:
        raise RuntimeError("streamlit is not installed. Use this file inside Zerve or install streamlit locally.")

    ensure_filter_defaults()

    source_options = ["All"] + sorted({row.get("source") or "unknown" for row in ranked_markets})
    category_options = ["All"] + available_categories(ranked_markets)
    normalize_filter_choices(source_options, category_options)

    st.set_page_config(page_title="Market Mispricing Radar", layout="wide")
    st.title("Market Mispricing Radar")
    st.caption("Mirrored Zerve Streamlit scaffold")

    if not pipeline_ready():
        st.warning("Pipeline output is not fully ready yet. The app is showing an honest unavailable state.")
        for line in unavailable_context_lines():
            st.write(f"- {line}")

    with st.sidebar:
        st.header("Controls")
        st.selectbox("Source", source_options, key="source_filter")
        st.selectbox("Category", category_options, key="category_filter")
        st.slider("Minimum score", 0.0, 1.0, step=0.05, key="min_score")
        st.selectbox("Result count", [10, 25, 50, 100], key="result_limit")
        st.toggle("Sort highest first", key="sort_desc")
        if st.button("Reset filters", use_container_width=True):
            reset_filter_state()
            st.rerun()

        st.header("Refresh trust")
        st.write(f"Refresh ID: {refresh_metadata.get('refresh_id') or 'unknown'}")
        st.write(f"Fetched at: {refresh_metadata.get('fetched_at') or 'unknown'}")
        st.write(f"Market count: {refresh_metadata.get('market_count') or 0}")
        st.write(f"Open markets: {refresh_metadata.get('open_market_count') or 0}")
        st.write(f"Source count: {source_count(ranked_markets)}")
        st.write(f"Score version: {refresh_metadata.get('score_version') or 'unknown'}")

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
        st.session_state["sort_desc"],
    )

    radar_tab, detail_tab, methodology_tab = st.tabs(["Radar", "Market Detail", "Methodology"])

    with radar_tab:
        st.subheader("Ranked Radar")
        trust_cols = st.columns(4)
        trust_cols[0].metric("Refresh ID", refresh_metadata.get("refresh_id") or "unknown")
        trust_cols[1].metric("Processed", refresh_metadata.get("market_count") or 0)
        trust_cols[2].metric("Open markets", refresh_metadata.get("open_market_count") or 0)
        trust_cols[3].metric("Sources", source_count(ranked_markets))

        if category_breakdown_rows():
            st.markdown("#### Category snapshot")
            st.dataframe(category_breakdown_rows(), use_container_width=True)

        if not pipeline_ready():
            st.info("No ranked results are available yet. Refresh the pipeline and try again.")
        elif not filtered:
            st.info("No results match the current filters.")
            if st.button("Reset filters from empty state", key="reset-empty-state"):
                reset_filter_state()
                st.rerun()
        else:
            st.caption(f"Showing {len(filtered)} filtered results. Use the focus action to sync a market into the detail tab.")
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
                            st.session_state["selected_market_id"] = row.get("market_id")
                            st.success("Focused market updated. Open the Market Detail tab to inspect it.")
                        if row.get("source_url"):
                            action_cols[1].link_button("Open source", row["source_url"], use_container_width=True)

    with detail_tab:
        st.subheader("Market Detail")
        selected_row = selected_market(filtered)
        if not pipeline_ready():
            st.info("Market detail is unavailable until the pipeline produces ranked markets and explanations.")
        elif selected_row is None:
            st.info("No market is available for the current filters.")
        else:
            explanation = explanation_lookup.get(selected_row.get("market_id"), {})

            st.markdown(f"### {selected_row.get('title')}")
            header_left, header_mid, header_right = st.columns(3)
            with header_left:
                st.write(f"Source: {selected_row.get('source') or 'unknown'}")
                st.write(f"Status: {selected_row.get('status') or 'unknown'}")
                st.write(f"Refresh: {refresh_metadata.get('fetched_at') or 'unknown'}")
                if selected_row.get("source_url"):
                    st.link_button("Open source market", selected_row["source_url"])
            with header_mid:
                st.metric("Final score", selected_row.get("final_score") or 0.0)
                st.metric("Current probability", selected_row.get("current_probability") or 0.0)
                st.write(f"Confidence: {selected_row.get('confidence_band') or 'unknown'}")
                st.write(f"Reason code: {selected_row.get('primary_reason_code') or 'unknown'}")
            with header_right:
                st.write(f"Resolution horizon: {format_hours(selected_row.get('time_to_resolution_hours'))}")
                st.write(f"Last update age: {format_hours(selected_row.get('time_since_update_hours'))}")
                st.write(f"Category: {selected_row.get('category') or 'unknown'}")
                topics = selected_row.get("topic_tags") or []
                st.write(f"Topics: {', '.join(topics) if topics else 'none'}")

            st.markdown("#### Explanation")
            st.write(explanation.get("headline_reason") or selected_row.get("headline_reason"))
            st.write(explanation.get("short_explanation") or "No short explanation available.")
            st.write(explanation.get("detailed_explanation") or "No detailed explanation available.")

            st.markdown("#### Score breakdown")
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

            st.markdown("#### Supporting signals")
            st.dataframe(supporting_signal_rows(explanation), use_container_width=True)

            st.markdown("#### Same-category peers")
            peer_rows = peer_comparison_rows(filtered, selected_row)
            if peer_rows:
                st.dataframe(peer_rows, use_container_width=True)
            else:
                st.write("No same-category peers are visible in the current filtered result set.")

            st.markdown("#### Caveats")
            caveats = explanation.get("caveats") or []
            if caveats:
                for item in caveats:
                    st.write(f"- {item}")
            else:
                st.write("No caveats were emitted for this market.")

            st.markdown("#### Missing or unavailable fields")
            notes = missing_detail_notes(selected_row, explanation)
            if notes:
                for note in notes:
                    st.write(f"- {note}")
            else:
                st.write("No important detail fields are currently missing for this market.")

    with methodology_tab:
        st.subheader("Methodology")
        for heading, lines in methodology_sections():
            st.markdown(f"#### {heading}")
            for line in lines:
                st.write(f"- {line}")


def main() -> None:
    render_app()


if __name__ == "__main__":
    main()

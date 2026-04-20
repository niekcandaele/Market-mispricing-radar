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


def methodology_lines() -> list[str]:
    return [
        "Ranks markets that look stale, fragile, extreme, or weakly supported.",
        "Uses interpretable score components rather than opaque model output.",
        "Does not claim guaranteed arbitrage or perfect fair value.",
        "Current MVP is Polymarket-first and single-source by design.",
    ]


def render_app() -> None:
    if st is None:
        raise RuntimeError("streamlit is not installed. Use this file inside Zerve or install streamlit locally.")

    st.set_page_config(page_title="Market Mispricing Radar", layout="wide")
    st.title("Market Mispricing Radar")
    st.caption("Mirrored Zerve Streamlit scaffold")

    with st.sidebar:
        st.header("Controls")
        source_options = ["All"] + sorted({row.get("source") or "unknown" for row in ranked_markets})
        category_options = ["All"] + available_categories(ranked_markets)
        source_filter = st.selectbox("Source", source_options, index=0)
        category_filter = st.selectbox("Category", category_options, index=0)
        min_score = st.slider("Minimum score", 0.0, 1.0, 0.0, 0.05)
        result_limit = st.selectbox("Result count", [10, 25, 50, 100], index=0)
        sort_desc = st.toggle("Sort highest first", value=True)

        st.header("Refresh trust")
        st.write(f"Refresh ID: {refresh_metadata.get('refresh_id') or 'unknown'}")
        st.write(f"Fetched at: {refresh_metadata.get('fetched_at') or 'unknown'}")
        st.write(f"Market count: {refresh_metadata.get('market_count') or 0}")
        st.write(f"Open markets: {refresh_metadata.get('open_market_count') or 0}")
        st.write(f"Score version: {refresh_metadata.get('score_version') or 'unknown'}")

        warnings = top_warning_messages()
        if warnings:
            st.header("QA warnings")
            for item in warnings:
                st.warning(item)

    filtered = filter_rows(ranked_markets, source_filter, category_filter, min_score, result_limit, sort_desc)

    radar_tab, detail_tab, methodology_tab = st.tabs(["Radar", "Market Detail", "Methodology"])

    with radar_tab:
        st.subheader("Ranked Radar")
        if not filtered:
            st.info("No results match the current filters. Reset or lower the score threshold.")
        else:
            radar_rows = [
                {
                    "rank": row.get("rank"),
                    "title": row.get("title"),
                    "source": row.get("source"),
                    "category": row.get("category"),
                    "probability": row.get("current_probability"),
                    "score": row.get("final_score"),
                    "headline_reason": row.get("headline_reason"),
                    "hours_since_update": row.get("time_since_update_hours"),
                }
                for row in filtered
            ]
            st.dataframe(radar_rows, use_container_width=True)

    with detail_tab:
        st.subheader("Market Detail")
        if not filtered:
            st.info("No market is available for the current filters.")
        else:
            selected_label = st.selectbox(
                "Select market",
                [market_label(row) for row in filtered],
                index=0,
            )
            selected_row = next(row for row in filtered if market_label(row) == selected_label)
            explanation = explanation_lookup.get(selected_row.get("market_id"), {})

            left, right = st.columns([2, 1])
            with left:
                st.markdown(f"### {selected_row.get('title')}")
                st.write(explanation.get("headline_reason") or selected_row.get("headline_reason"))
                st.write(explanation.get("short_explanation") or "No short explanation available.")
                st.write(explanation.get("detailed_explanation") or "No detailed explanation available.")
                if selected_row.get("source_url"):
                    st.link_button("Open source market", selected_row["source_url"])
            with right:
                st.metric("Final score", selected_row.get("final_score") or 0.0)
                st.metric("Current probability", selected_row.get("current_probability") or 0.0)
                st.write(f"Confidence: {selected_row.get('confidence_band') or 'unknown'}")
                st.write(f"Reason code: {selected_row.get('primary_reason_code') or 'unknown'}")
                st.write(f"Status: {selected_row.get('status') or 'unknown'}")

            st.markdown("#### Score breakdown")
            st.json(explanation.get("score_components") or {}, expanded=False)

            st.markdown("#### Supporting signals")
            st.json(explanation.get("supporting_signal_values") or {}, expanded=False)

            st.markdown("#### Caveats")
            caveats = explanation.get("caveats") or []
            if caveats:
                for item in caveats:
                    st.write(f"- {item}")
            else:
                st.write("No caveats were emitted for this market.")

    with methodology_tab:
        st.subheader("Methodology")
        for line in methodology_lines():
            st.write(f"- {line}")
        st.markdown("#### Current scope")
        st.write("Polymarket-first, component-based anomaly ranking, honest caveats, and refresh-tied outputs.")


def main() -> None:
    render_app()


if __name__ == "__main__":
    main()

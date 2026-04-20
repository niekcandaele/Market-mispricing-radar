#!/usr/bin/env python3
"""Export a local app bundle artifact for the mirrored Streamlit app."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from polymarket_ranker import app_bundle, fetch_markets, normalize_market, rank_markets, utc_now


DEFAULT_OUTPUT = Path("artifacts/streamlit/app_bundle.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=200, help="number of markets to fetch")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="path to write the app bundle JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    fetched_at = utc_now()
    raw_markets = fetch_markets(args.limit)
    normalized = [normalize_market(item, fetched_at) for item in raw_markets]
    ranked = rank_markets(normalized)
    bundle = app_bundle(ranked, raw_markets, fetched_at)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(bundle, indent=2) + "\n")

    summary = {
        "output": str(args.output),
        "refresh_id": bundle["refresh_metadata"].get("refresh_id"),
        "ranked_market_count": len(bundle["ranked_markets"]),
        "warning_hint": "Run the Streamlit app with MMR_APP_BUNDLE_PATH set to this file.",
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

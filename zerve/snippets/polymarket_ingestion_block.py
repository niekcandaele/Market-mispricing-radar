#!/usr/bin/env python3
"""Normalization-ready Polymarket ingestion snippet for a Zerve Python block.

This file is meant to be easy to paste into a Zerve development-layer block,
but it can also be run locally for validation.

Primary block outputs:
- source_config
- polymarket_raw_markets
- ingestion_metadata
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen

SOURCE_NAME = "polymarket"
BASE_URL = "https://gamma-api.polymarket.com/markets"
DEFAULT_LIMIT = 200
DEFAULT_TIMEOUT_SECONDS = 30
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_source_config(limit: int = DEFAULT_LIMIT) -> dict[str, object]:
    return {
        "source": SOURCE_NAME,
        "endpoint": "markets",
        "base_url": BASE_URL,
        "closed": False,
        "limit": limit,
        "timeout_seconds": DEFAULT_TIMEOUT_SECONDS,
        "request_headers": REQUEST_HEADERS,
    }


def fetch_polymarket_markets(config: dict[str, object]) -> tuple[list[dict[str, object]], str]:
    params = urlencode(
        {
            "closed": "true" if config["closed"] else "false",
            "limit": str(config["limit"]),
        }
    )
    request_url = f"{config['base_url']}?{params}"
    request = Request(request_url, headers=config["request_headers"])
    with urlopen(request, timeout=int(config["timeout_seconds"])) as response:
        payload = response.read().decode("utf-8")
    return json.loads(payload), request_url


def first_market_summary(markets: list[dict[str, object]]) -> dict[str, object] | None:
    if not markets:
        return None
    first = markets[0]
    return {
        "id": first.get("id"),
        "question": first.get("question"),
        "slug": first.get("slug"),
        "active": first.get("active"),
        "closed": first.get("closed"),
        "end_date_iso": first.get("endDate") or first.get("end_date_iso"),
    }


source_config = build_source_config()
fetched_at = utc_now_iso()
polymarket_raw_markets, request_url = fetch_polymarket_markets(source_config)
first_market = first_market_summary(polymarket_raw_markets)
ingestion_metadata = {
    "source": SOURCE_NAME,
    "fetched_at": fetched_at,
    "request_url": request_url,
    "request_limit": source_config["limit"],
    "market_count": len(polymarket_raw_markets),
    "first_market": first_market,
    "notes": "Browser-like headers are intentionally kept in the request to avoid Zerve-side HTTP 403 failures.",
}

print(f"refresh_at {ingestion_metadata['fetched_at']}")
print(f"request_url {ingestion_metadata['request_url']}")
print(f"market_count {ingestion_metadata['market_count']}")
if first_market:
    print(f"first_question {first_market['question']}")
    print(f"first_slug {first_market['slug']}")
    print(f"first_id {first_market['id']}")

if __name__ == "__main__":
    print(json.dumps(ingestion_metadata, indent=2))

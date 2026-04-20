#!/usr/bin/env python3
"""Normalization-ready Polymarket ingestion snippet for a Zerve Python block.

Preferred Zerve notebook block name:
- `fetch_polymarket_data`

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
DEFAULT_FETCH_LIMIT = 350
DEFAULT_ACTIVE_LIMIT = 250
DEFAULT_TIMEOUT_SECONDS = 30
PIPELINE_VERSION = "ingestion-v2"
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_refresh_id(source: str, fetched_at: str) -> str:
    compact = fetched_at.replace("-", "").replace(":", "").replace("T", "-").replace("Z", "z")
    return f"{source}-{compact}"


def build_source_config(fetch_limit: int = DEFAULT_FETCH_LIMIT, active_limit: int = DEFAULT_ACTIVE_LIMIT) -> dict[str, object]:
    return {
        "source": SOURCE_NAME,
        "endpoint": "markets",
        "base_url": BASE_URL,
        "closed": False,
        "fetch_limit": fetch_limit,
        "active_limit": active_limit,
        "timeout_seconds": DEFAULT_TIMEOUT_SECONDS,
        "request_headers": REQUEST_HEADERS,
    }


def fetch_polymarket_markets(config: dict[str, object]) -> tuple[list[dict[str, object]], str]:
    params = urlencode(
        {
            "closed": "true" if config["closed"] else "false",
            "limit": str(config["fetch_limit"]),
        }
    )
    request_url = f"{config['base_url']}?{params}"
    request = Request(request_url, headers=config["request_headers"])
    with urlopen(request, timeout=int(config["timeout_seconds"])) as response:
        payload = response.read().decode("utf-8")
    return json.loads(payload), request_url


def coerce_float(value: object) -> float | None:
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


def is_active_market(raw: dict[str, object]) -> bool:
    if raw.get("closed") or raw.get("archived"):
        return False
    if raw.get("active") or raw.get("acceptingOrders") or raw.get("automaticallyActive"):
        return True
    return False


def stable_market_order_key(raw: dict[str, object]) -> tuple[float, float, str, str]:
    liquidity = coerce_float(raw.get("liquidity")) or 0.0
    volume = coerce_float(raw.get("volume")) or 0.0
    end_date = str(raw.get("endDate") or raw.get("end_date_iso") or "")
    market_id = str(raw.get("id") or "")
    return (-liquidity, -volume, end_date, market_id)


def select_output_markets(markets: list[dict[str, object]], active_limit: int) -> list[dict[str, object]]:
    active_markets = [market for market in markets if is_active_market(market)]
    active_markets.sort(key=stable_market_order_key)
    return active_markets[:active_limit]


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
        "liquidity": coerce_float(first.get("liquidity")),
        "volume": coerce_float(first.get("volume")),
        "end_date_iso": first.get("endDate") or first.get("end_date_iso"),
    }


def build_ingestion_metadata(
    source_config: dict[str, object],
    request_url: str,
    fetched_at: str,
    fetched_markets: list[dict[str, object]],
    output_markets: list[dict[str, object]],
) -> dict[str, object]:
    first_market = first_market_summary(output_markets)
    return {
        "refresh_id": build_refresh_id(SOURCE_NAME, fetched_at),
        "pipeline_version": PIPELINE_VERSION,
        "source": SOURCE_NAME,
        "fetched_at": fetched_at,
        "request_url": request_url,
        "request_fetch_limit": source_config["fetch_limit"],
        "request_active_limit": source_config["active_limit"],
        "fetched_market_count": len(fetched_markets),
        "open_market_count": sum(1 for market in fetched_markets if is_active_market(market)),
        "market_count": len(output_markets),
        "first_market": first_market,
        "sample_market_ids": [market.get("id") for market in output_markets[:5]],
        "notes": "Browser-like headers are intentionally kept in the request to avoid Zerve-side HTTP 403 failures. The named output `polymarket_raw_markets` is now the active, normalization-ready slice.",
    }


source_config = build_source_config()
fetched_at = utc_now_iso()
fetched_markets, request_url = fetch_polymarket_markets(source_config)
polymarket_raw_markets = select_output_markets(fetched_markets, int(source_config["active_limit"]))
ingestion_metadata = build_ingestion_metadata(
    source_config,
    request_url,
    fetched_at,
    fetched_markets,
    polymarket_raw_markets,
)
first_market = ingestion_metadata["first_market"]

print(f"refresh_id {ingestion_metadata['refresh_id']}")
print(f"refresh_at {ingestion_metadata['fetched_at']}")
print(f"request_url {ingestion_metadata['request_url']}")
print(f"fetched_market_count {ingestion_metadata['fetched_market_count']}")
print(f"open_market_count {ingestion_metadata['open_market_count']}")
print(f"market_count {ingestion_metadata['market_count']}")
if first_market:
    print(f"first_question {first_market['question']}")
    print(f"first_slug {first_market['slug']}")
    print(f"first_id {first_market['id']}")

if __name__ == "__main__":
    print(json.dumps(ingestion_metadata, indent=2))

#!/usr/bin/env python3
"""First normalization block for Zerve-side Polymarket ingestion output.

Preferred Zerve notebook block name:
- `normalize_markets`

This snippet expects the previous ingestion block to have emitted:
- polymarket_raw_markets
- ingestion_metadata

Primary block outputs:
- normalized_markets
- normalization_metadata

When run locally, it falls back to importing the mirrored ingestion snippet.
"""

from __future__ import annotations

import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SOURCE_NAME = "polymarket"
SOURCE_PRIORITY = 1


def parse_iso(value: Any) -> datetime | None:
    if not value or not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


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


def parse_jsonish_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, list) else []
        except json.JSONDecodeError:
            return []
    return []


def first_event(raw: dict[str, Any]) -> dict[str, Any]:
    events = raw.get("events")
    if isinstance(events, list) and events and isinstance(events[0], dict):
        return events[0]
    return {}


def yes_no_prices(raw: dict[str, Any]) -> tuple[float | None, float | None]:
    outcomes = parse_jsonish_list(raw.get("outcomes"))
    prices = [coerce_float(item) for item in parse_jsonish_list(raw.get("outcomePrices"))]
    if not outcomes or not prices or len(outcomes) != len(prices):
        return (coerce_float(raw.get("lastTradePrice")), None)

    yes_price = None
    no_price = None
    for outcome, price in zip(outcomes, prices):
        if price is None:
            continue
        label = str(outcome).strip().lower()
        if label == "yes":
            yes_price = price
        elif label == "no":
            no_price = price

    if yes_price is None and prices:
        yes_price = prices[0]
    if no_price is None and len(prices) > 1:
        no_price = prices[1]
    return yes_price, no_price


def market_status(raw: dict[str, Any]) -> str:
    if raw.get("closed"):
        return "closed"
    if raw.get("active") and not raw.get("archived"):
        return "open"
    if raw.get("archived"):
        return "inactive"
    return "unknown"


def build_source_url(raw: dict[str, Any]) -> str | None:
    slug = raw.get("slug")
    if isinstance(slug, str) and slug:
        return f"https://polymarket.com/event/{slug}"
    market_id = raw.get("id")
    if market_id is not None:
        return f"https://polymarket.com/market/{market_id}"
    return None


def inferred_category(raw: dict[str, Any], event: dict[str, Any]) -> str | None:
    for candidate in [event.get("category"), raw.get("category")]:
        if isinstance(candidate, str) and candidate.strip():
            return candidate.strip().lower()
    return None


def topic_tags(raw: dict[str, Any], event: dict[str, Any], category: str | None) -> list[str]:
    tags: list[str] = []
    for candidate in [event.get("tags"), raw.get("tags")]:
        if isinstance(candidate, list):
            tags.extend(str(item).strip().lower() for item in candidate if str(item).strip())
    if category and category not in tags:
        tags.insert(0, category)
    seen: set[str] = set()
    deduped: list[str] = []
    for tag in tags:
        if tag not in seen:
            seen.add(tag)
            deduped.append(tag)
    return deduped[:6]


def hours_between(later: datetime | None, earlier: datetime | None) -> float | None:
    if later is None or earlier is None:
        return None
    return (later - earlier).total_seconds() / 3600.0


def normalize_market(raw: dict[str, Any], fetched_at: datetime, fetched_at_iso: str) -> dict[str, Any]:
    event = first_event(raw)
    updated_at = parse_iso(raw.get("updatedAt") or event.get("updatedAt"))
    event_start_at = parse_iso(raw.get("startDate") or raw.get("startDateIso") or event.get("startDate"))
    event_end_at = parse_iso(raw.get("endDate") or raw.get("endDateIso") or event.get("endDate"))
    resolution_at = event_end_at
    yes_price, no_price = yes_no_prices(raw)
    last_price = yes_price if yes_price is not None else coerce_float(raw.get("lastTradePrice"))
    liquidity = coerce_float(raw.get("liquidityNum")) or coerce_float(raw.get("liquidity"))
    volume = coerce_float(raw.get("volumeNum")) or coerce_float(raw.get("volume"))
    volume_24hr = coerce_float(raw.get("volume24hr")) or coerce_float(raw.get("volume24hrClob"))
    one_month_price_change_abs = abs(coerce_float(raw.get("oneMonthPriceChange")) or 0.0)
    category = inferred_category(raw, event)
    market_id = raw.get("id")
    source_market_id = str(market_id) if market_id is not None else None
    time_since_update_hours = hours_between(fetched_at, updated_at)
    if time_since_update_hours is not None:
        time_since_update_hours = max(time_since_update_hours, 0.0)
    time_to_resolution_hours = hours_between(resolution_at, fetched_at)
    price_distance_from_mid = abs(last_price - 0.5) if last_price is not None else None

    return {
        "market_id": f"polymarket_{source_market_id}" if source_market_id else None,
        "source": SOURCE_NAME,
        "source_market_id": source_market_id,
        "source_url": build_source_url(raw),
        "title": raw.get("question") or None,
        "description": raw.get("description") or event.get("description") or None,
        "category": category,
        "status": market_status(raw),
        "is_binary": len(parse_jsonish_list(raw.get("outcomes"))) == 2,
        "event_start_at": event_start_at.isoformat().replace("+00:00", "Z") if event_start_at else None,
        "event_end_at": event_end_at.isoformat().replace("+00:00", "Z") if event_end_at else None,
        "resolution_at": resolution_at.isoformat().replace("+00:00", "Z") if resolution_at else None,
        "last_price": last_price,
        "yes_price": yes_price,
        "no_price": no_price,
        "volume": volume,
        "volume_24hr": volume_24hr,
        "liquidity": liquidity,
        "last_updated_at": updated_at.isoformat().replace("+00:00", "Z") if updated_at else None,
        "fetched_at": fetched_at_iso,
        "time_to_resolution_hours": time_to_resolution_hours,
        "time_since_update_hours": time_since_update_hours,
        "price_distance_from_mid": price_distance_from_mid,
        "one_month_price_change_abs": one_month_price_change_abs,
        "topic_tags": topic_tags(raw, event, category),
        "source_priority": SOURCE_PRIORITY,
        "event_title": event.get("title") or None,
    }


try:
    polymarket_raw_markets
    ingestion_metadata
except NameError:
    snippet_dir = Path(__file__).resolve().parent
    ingestion_path = snippet_dir / "polymarket_ingestion_block.py"
    spec = importlib.util.spec_from_file_location("polymarket_ingestion_block", ingestion_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load ingestion snippet from {ingestion_path}")
    ingestion_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ingestion_module)
    polymarket_raw_markets = ingestion_module.polymarket_raw_markets
    ingestion_metadata = ingestion_module.ingestion_metadata


fetched_at_iso = ingestion_metadata.get("fetched_at") if isinstance(ingestion_metadata, dict) else None
fetched_at = parse_iso(fetched_at_iso) or datetime.now(timezone.utc)
normalized_markets = [normalize_market(raw, fetched_at, fetched_at_iso or fetched_at.isoformat().replace("+00:00", "Z")) for raw in polymarket_raw_markets]
normalization_metadata = {
    "source": SOURCE_NAME,
    "fetched_at": fetched_at_iso or fetched_at.isoformat().replace("+00:00", "Z"),
    "input_market_count": len(polymarket_raw_markets),
    "normalized_market_count": len(normalized_markets),
    "open_market_count": sum(1 for row in normalized_markets if row.get("status") == "open"),
    "first_market_id": normalized_markets[0].get("market_id") if normalized_markets else None,
    "notes": "Normalization preserves missing values as null when Polymarket does not provide a trustworthy field.",
}

print(f"normalized_count {normalization_metadata['normalized_market_count']}")
print(f"open_market_count {normalization_metadata['open_market_count']}")
if normalized_markets:
    first = normalized_markets[0]
    print(f"first_market_id {first.get('market_id')}")
    print(f"first_title {first.get('title')}")
    print(f"first_status {first.get('status')}")
    print(f"first_source_url {first.get('source_url')}")

if __name__ == "__main__":
    print(json.dumps(normalization_metadata, indent=2))

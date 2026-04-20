#!/usr/bin/env python3
"""Local first-pass Polymarket ranking prototype.

Fetches active Polymarket markets, normalizes a core field subset, computes a
simple fragility score inspired by docs/scoring-model-v1.md, and prints the top
ranked results.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
import urllib.request
from typing import Any

API_URL = "https://gamma-api.polymarket.com/markets?closed=false&limit={limit}"
USER_AGENT = "Mozilla/5.0 (compatible; MarketMispricingRadar/0.1; +https://git.home.candaele.dev/jefkes-workspace/market-mispricing-radar)"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=200, help="number of markets to fetch")
    parser.add_argument("--top", type=int, default=15, help="number of ranked rows to print")
    parser.add_argument("--json", action="store_true", help="emit ranked rows as JSON")
    return parser.parse_args()


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.UTC)


def parse_iso(value: Any) -> dt.datetime | None:
    if not value or not isinstance(value, str):
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
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


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def percentile_rank(value: float | None, values: list[float], reverse: bool = False) -> float:
    if value is None or not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        base = 1.0
    else:
        less_or_equal = sum(1 for item in ordered if item <= value)
        base = (less_or_equal - 1) / (len(ordered) - 1)
    return 1.0 - base if reverse else base


def fetch_markets(limit: int) -> list[dict[str, Any]]:
    request = urllib.request.Request(
        API_URL.format(limit=limit),
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if not isinstance(payload, list):
        raise RuntimeError("Polymarket API returned a non-list payload")
    return payload


def yes_no_prices(market: dict[str, Any]) -> tuple[float | None, float | None]:
    outcomes = parse_jsonish_list(market.get("outcomes"))
    prices = [coerce_float(item) for item in parse_jsonish_list(market.get("outcomePrices"))]
    if not outcomes or not prices or len(outcomes) != len(prices):
        return (coerce_float(market.get("lastTradePrice")), None)

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
    return (yes_price, no_price)


def normalize_market(raw: dict[str, Any], fetched_at: dt.datetime) -> dict[str, Any]:
    updated_at = parse_iso(raw.get("updatedAt"))
    resolution_at = parse_iso(raw.get("endDate") or raw.get("endDateIso"))
    yes_price, no_price = yes_no_prices(raw)
    liquidity = coerce_float(raw.get("liquidityNum")) or coerce_float(raw.get("liquidity"))
    volume = coerce_float(raw.get("volumeNum")) or coerce_float(raw.get("volume"))
    volume_24hr = coerce_float(raw.get("volume24hr")) or coerce_float(raw.get("volume24hrClob"))
    one_month_change = abs(coerce_float(raw.get("oneMonthPriceChange")) or 0.0)
    slug = raw.get("slug") or raw.get("id")
    status = "open" if raw.get("active") and not raw.get("closed") and not raw.get("archived") else "unknown"
    title = raw.get("question") or ""

    time_since_update_hours = None
    if updated_at is not None:
        time_since_update_hours = max((fetched_at - updated_at).total_seconds() / 3600.0, 0.0)

    time_to_resolution_hours = None
    if resolution_at is not None:
        time_to_resolution_hours = (resolution_at - fetched_at).total_seconds() / 3600.0

    price_distance_from_mid = None
    if yes_price is not None:
        price_distance_from_mid = abs(yes_price - 0.5)

    return {
        "market_id": f"polymarket_{raw.get('id')}",
        "source": "polymarket",
        "source_market_id": str(raw.get("id")),
        "source_url": f"https://polymarket.com/event/{slug}",
        "title": title,
        "status": status,
        "is_binary": len(parse_jsonish_list(raw.get("outcomes"))) == 2,
        "resolution_at": resolution_at.isoformat().replace("+00:00", "Z") if resolution_at else None,
        "last_price": yes_price,
        "yes_price": yes_price,
        "no_price": no_price,
        "volume": volume,
        "volume_24hr": volume_24hr,
        "liquidity": liquidity,
        "last_updated_at": updated_at.isoformat().replace("+00:00", "Z") if updated_at else None,
        "fetched_at": fetched_at.isoformat().replace("+00:00", "Z"),
        "time_to_resolution_hours": time_to_resolution_hours,
        "time_since_update_hours": time_since_update_hours,
        "price_distance_from_mid": price_distance_from_mid,
        "one_month_price_change_abs": one_month_change,
    }


def data_quality_penalty(market: dict[str, Any]) -> float:
    missing = 0
    for key in ["title", "yes_price", "last_updated_at", "resolution_at", "liquidity"]:
        value = market.get(key)
        if value in (None, ""):
            missing += 1
    if not market.get("is_binary"):
        missing += 1
    if market.get("status") != "open":
        missing += 1
    return clamp(missing / 6.0)


def primary_reason_code(scores: dict[str, float], market: dict[str, Any]) -> str:
    if market.get("time_to_resolution_hours") is not None and market["time_to_resolution_hours"] < 0:
        return "past_resolution_still_open"

    interaction_scores = {
        "stale_near_resolution": scores["staleness_component"] * scores["event_horizon_component"],
        "extreme_price_low_support": scores["extremeness_component"] * scores["liquidity_component"],
        "high_instability": scores["volatility_component"] * max(scores["staleness_component"], 0.35),
        "weak_data_quality": scores["data_quality_penalty"],
    }
    strongest_interaction = max(interaction_scores, key=interaction_scores.get)
    if interaction_scores[strongest_interaction] >= 0.20:
        return strongest_interaction

    base_scores = {
        "staleness_component": scores["staleness_component"],
        "event_horizon_component": scores["event_horizon_component"],
        "extremeness_component": scores["extremeness_component"],
        "liquidity_component": scores["liquidity_component"],
        "volatility_component": scores["volatility_component"],
    }
    strongest = max(base_scores, key=base_scores.get)
    return {
        "staleness_component": "stale_market",
        "event_horizon_component": "near_resolution",
        "extremeness_component": "extreme_price",
        "liquidity_component": "low_support",
        "volatility_component": "high_instability",
    }[strongest]


def confidence_band(penalty: float) -> str:
    if penalty >= 0.5:
        return "low"
    if penalty >= 0.2:
        return "medium"
    return "high"


def rank_markets(markets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    staleness_values = [m["time_since_update_hours"] for m in markets if m["time_since_update_hours"] is not None]
    resolution_values = [m["time_to_resolution_hours"] for m in markets if m["time_to_resolution_hours"] is not None and m["time_to_resolution_hours"] >= 0]
    support_values = [math.log1p((m["liquidity"] or 0.0) + (m["volume_24hr"] or 0.0)) for m in markets if (m["liquidity"] is not None or m["volume_24hr"] is not None)]
    volatility_values = [m["one_month_price_change_abs"] for m in markets if m["one_month_price_change_abs"] is not None]

    ranked: list[dict[str, Any]] = []
    raw_scores: list[float] = []
    for market in markets:
        staleness_component = percentile_rank(market["time_since_update_hours"], staleness_values)
        if market["time_to_resolution_hours"] is not None and market["time_to_resolution_hours"] < 0:
            event_horizon_component = 1.0
        else:
            event_horizon_component = percentile_rank(market["time_to_resolution_hours"], resolution_values, reverse=True)
        extremeness_component = clamp((market["price_distance_from_mid"] or 0.0) * 2.0)
        support_metric = None
        if market["liquidity"] is not None or market["volume_24hr"] is not None:
            support_metric = math.log1p((market["liquidity"] or 0.0) + (market["volume_24hr"] or 0.0))
        liquidity_component = percentile_rank(support_metric, support_values, reverse=True)
        volatility_component = percentile_rank(market["one_month_price_change_abs"], volatility_values)
        penalty = data_quality_penalty(market)

        raw_score = (
            0.30 * staleness_component
            + 0.20 * event_horizon_component
            + 0.15 * extremeness_component
            + 0.15 * liquidity_component
            + 0.10 * volatility_component
            + 0.05 * staleness_component * event_horizon_component
            + 0.05 * extremeness_component * liquidity_component
            - 0.20 * penalty
        )

        component_scores = {
            "staleness_component": round(staleness_component, 4),
            "event_horizon_component": round(event_horizon_component, 4),
            "extremeness_component": round(extremeness_component, 4),
            "liquidity_component": round(liquidity_component, 4),
            "volatility_component": round(volatility_component, 4),
            "data_quality_penalty": round(penalty, 4),
        }

        ranked.append({
            **market,
            **component_scores,
            "raw_score": raw_score,
            "confidence_band": confidence_band(penalty),
            "primary_reason_code": primary_reason_code(component_scores, market),
        })
        raw_scores.append(raw_score)

    min_raw = min(raw_scores) if raw_scores else 0.0
    max_raw = max(raw_scores) if raw_scores else 1.0
    span = max(max_raw - min_raw, 1e-9)
    for market in ranked:
        market["final_score"] = round((market["raw_score"] - min_raw) / span, 4)
        del market["raw_score"]

    ranked.sort(key=lambda item: item["final_score"], reverse=True)
    for index, market in enumerate(ranked, start=1):
        market["rank"] = index
    return ranked


def format_rows(rows: list[dict[str, Any]]) -> str:
    header = "rank  score  reason                     yes   hrs_to_end  hrs_stale  title"
    line = "-" * len(header)
    rendered = [header, line]
    for row in rows:
        rendered.append(
            f"{row['rank']:>4}  {row['final_score']:.3f}  "
            f"{row['primary_reason_code'][:24]:<24}  "
            f"{(row['yes_price'] if row['yes_price'] is not None else float('nan')):>4.2f}  "
            f"{(row['time_to_resolution_hours'] if row['time_to_resolution_hours'] is not None else float('nan')):>10.1f}  "
            f"{(row['time_since_update_hours'] if row['time_since_update_hours'] is not None else float('nan')):>9.1f}  "
            f"{row['title'][:90]}"
        )
    return "\n".join(rendered)


def main() -> int:
    args = parse_args()
    fetched_at = utc_now()
    raw_markets = fetch_markets(args.limit)
    normalized = [normalize_market(item, fetched_at) for item in raw_markets]
    ranked = rank_markets(normalized)
    top_rows = ranked[: args.top]

    summary = {
        "fetched_at": fetched_at.isoformat().replace("+00:00", "Z"),
        "market_count": len(raw_markets),
        "open_market_count": sum(1 for item in normalized if item["status"] == "open"),
        "top_count": len(top_rows),
    }

    if args.json:
        json.dump({"summary": summary, "rows": top_rows}, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(json.dumps(summary, indent=2))
        print()
        print(format_rows(top_rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

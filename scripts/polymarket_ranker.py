#!/usr/bin/env python3
"""Local first-pass Polymarket ranking prototype.

Fetches active Polymarket markets, normalizes a core field subset, computes a
simple fragility score inspired by docs/scoring-model-v1.md, and prints the top
ranked results.
"""

from __future__ import annotations

import argparse
from collections import Counter
import datetime as dt
import json
import math
import re
import sys
import urllib.request
from typing import Any

API_URL = "https://gamma-api.polymarket.com/markets?closed=false&limit={limit}"
USER_AGENT = "Mozilla/5.0 (compatible; MarketMispricingRadar/0.1; +https://git.home.candaele.dev/jefkes-workspace/market-mispricing-radar)"
PIPELINE_VERSION = "local-prototype-v0.4"
SCORE_VERSION = "v1-prototype"

CATEGORY_RULES: list[tuple[str, list[str]]] = [
    ("sports", ["nba", "nfl", "mlb", "nhl", "soccer", "football", "ufc", "fight", "tennis", "golf", "f1", "formula 1", "championship", "world cup", "playoff", "finals"]),
    ("politics", ["election", "president", "senate", "house", "parliament", "prime minister", "trump", "biden", "democrat", "republican", "vote", "mayor", "governor"]),
    ("crypto", ["bitcoin", "btc", "ethereum", "eth", "solana", "sol", "crypto", "token", "memecoin", "dogecoin", "airdrop"]),
    ("finance-business", ["fed", "inflation", "recession", "gdp", "tariff", "ipo", "stock", "nasdaq", "s&p", "earnings", "economy", "interest rate"]),
    ("technology", ["ai", "openai", "gpt", "anthropic", "google", "meta", "microsoft", "tesla", "apple", "iphone", "robot", "chip", "semiconductor"]),
    ("science-health", ["covid", "vaccine", "fda", "clinical", "space", "spacex", "nasa", "drug", "trial", "mars", "rocket"]),
    ("entertainment", ["movie", "album", "song", "music", "netflix", "oscar", "emmy", "grammy", "gta", "game", "trailer", "drake", "rihanna", "celebrity"]),
    ("world", ["ukraine", "russia", "china", "israel", "gaza", "ceasefire", "earthquake", "pope", "india", "europe", "iran"]),
]

TOPIC_RULES: list[tuple[str, list[str]]] = [
    ("ai", ["ai", "openai", "gpt", "anthropic"]),
    ("crypto", ["bitcoin", "btc", "ethereum", "eth", "crypto", "token", "solana", "sol"]),
    ("elections", ["election", "vote", "president", "senate", "parliament"]),
    ("war-geopolitics", ["ukraine", "russia", "ceasefire", "israel", "gaza", "iran", "china"]),
    ("music", ["album", "song", "music", "drake", "rihanna"]),
    ("gaming", ["gta", "game", "xbox", "playstation", "nintendo"]),
    ("movies-tv", ["movie", "netflix", "oscar", "emmy", "series"]),
    ("sports", ["nba", "nfl", "mlb", "nhl", "soccer", "ufc", "tennis", "golf", "f1", "formula 1"]),
    ("macro", ["fed", "inflation", "recession", "gdp", "tariff", "interest rate", "economy"]),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=500, help="number of markets to fetch")
    parser.add_argument("--top", type=int, default=15, help="number of ranked rows to print")
    parser.add_argument("--json", action="store_true", help="emit ranked rows as JSON")
    parser.add_argument("--app-json", action="store_true", help="emit an app-ready JSON bundle")
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


def absolute_staleness_signal(hours: float | None) -> float:
    if hours is None:
        return 0.0
    return clamp((hours - 6.0) / 42.0)


def event_horizon_signal(hours: float | None) -> float:
    if hours is None or hours < 0:
        return 0.0
    return clamp((720.0 - hours) / 720.0)


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


def first_event(raw: dict[str, Any]) -> dict[str, Any]:
    events = raw.get("events")
    if isinstance(events, list) and events and isinstance(events[0], dict):
        return events[0]
    return {}


def keyword_matches(text: str, keyword: str) -> bool:
    pattern = rf"(?<![a-z0-9]){re.escape(keyword.lower())}(?![a-z0-9])"
    return re.search(pattern, text) is not None


def infer_category_and_topics(raw: dict[str, Any]) -> tuple[str, list[str], str | None]:
    event = first_event(raw)
    text = " ".join(
        str(value)
        for value in [
            raw.get("question"),
            raw.get("description"),
            raw.get("slug"),
            event.get("title"),
            event.get("description"),
            event.get("slug"),
        ]
        if value
    ).lower()

    category = "general"
    for candidate, keywords in CATEGORY_RULES:
        if any(keyword_matches(text, keyword) for keyword in keywords):
            category = candidate
            break

    topic_tags: list[str] = []
    for tag, keywords in TOPIC_RULES:
        if any(keyword_matches(text, keyword) for keyword in keywords):
            topic_tags.append(tag)

    if category != "general" and category not in topic_tags:
        topic_tags.insert(0, category)
    if not topic_tags:
        topic_tags = [category]

    event_title = event.get("title") if isinstance(event.get("title"), str) else None
    return category, topic_tags[:4], event_title


def normalize_market(raw: dict[str, Any], fetched_at: dt.datetime) -> dict[str, Any]:
    updated_at = parse_iso(raw.get("updatedAt"))
    resolution_at = parse_iso(raw.get("endDate") or raw.get("endDateIso"))
    yes_price, no_price = yes_no_prices(raw)
    category, topic_tags, event_title = infer_category_and_topics(raw)
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
        "description": raw.get("description") or None,
        "event_title": event_title,
        "category": category,
        "topic_tags": topic_tags,
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


def explanation_fields(market: dict[str, Any]) -> dict[str, Any]:
    reason = market["primary_reason_code"]
    stale_hours = market.get("time_since_update_hours")
    end_hours = market.get("time_to_resolution_hours")
    yes_price = market.get("yes_price")

    headline_reason = "This market was flagged for a blend of suspicious score components."
    short_explanation = "The score found a combination of features worth inspecting more closely."
    detailed_explanation = (
        "The prototype flagged this market because several score components combined into a relatively high fragility signal. "
        "The raw fields and component values should be inspected before treating it as a genuinely interesting opportunity."
    )

    if reason == "stale_near_resolution":
        headline_reason = "High score driven by stale updates close to resolution."
        short_explanation = "This market looks slow to update despite having limited time left before resolution."
        detailed_explanation = (
            f"The market has not updated for roughly {stale_hours:.1f} hours while only about {end_hours:.1f} hours remain until resolution. "
            "That stale-near-deadline combination is one of the clearest v1 fragility patterns."
        )
    elif reason == "extreme_price_low_support":
        headline_reason = "Extreme pricing is being carried with relatively weak support."
        short_explanation = "The current probability is far from the midpoint and does not look strongly supported by the weaker-support component."
        detailed_explanation = (
            f"The market is currently priced around {yes_price:.3f}, which is quite far from a neutral midpoint, while the support-side component still looks weak enough to keep it inspectable. "
            "In v1 that combination is treated as a fragile extreme rather than as proof the price is wrong."
        )
    elif reason == "high_instability":
        headline_reason = "Recent movement or instability is doing meaningful work in the score."
        short_explanation = "The movement proxy and nearby supporting components make this market look more unstable than a quiet baseline."
        detailed_explanation = (
            "The volatility proxy is elevated enough to matter, and the surrounding score components do not fully calm that down. "
            "This is the v1 path for markets that look more unstable than simply stale or extreme."
        )
    elif reason == "past_resolution_still_open":
        headline_reason = "The source still presents this market as open even though its end date is in the past."
        short_explanation = "This looks like a source-status inconsistency rather than a normal live market signal."
        detailed_explanation = (
            f"The market still appears open in the fetched payload, but the recorded resolution horizon is about {end_hours:.1f} hours in the past. "
            "That makes it useful as a data-quality or source-behavior flag, even if it is not a strong product-facing candidate."
        )
    elif reason == "weak_data_quality":
        headline_reason = "The record has enough missing or awkward fields to deserve caution."
        short_explanation = "This market is being flagged partly because the available data is incomplete or structurally awkward."
        detailed_explanation = (
            "The current record is not clean enough to treat the score as high-confidence. "
            "Any review should start by validating whether the source fields are trustworthy enough for comparison."
        )

    caveats = ["single-source MVP", f"confidence:{market['confidence_band']}"]
    if stale_hours is not None and stale_hours < 6.0:
        caveats.append("fresh-market caveat")
    if end_hours is not None and end_hours < 0:
        caveats.append("source status may be inconsistent")
    if end_hours is not None and end_hours > 720.0:
        caveats.append("long-horizon market")
    if market.get("data_quality_penalty", 0.0) > 0.0:
        caveats.append("data-quality penalty applied")
    if market.get("heuristic_penalty", 0.0) > 0.0:
        caveats.append("heuristic penalty applied")

    supporting_signals = [
        "time_since_update_hours",
        "time_to_resolution_hours",
        "price_distance_from_mid",
        "liquidity",
        "volume_24hr",
        "one_month_price_change_abs",
    ]

    return {
        "headline_reason": headline_reason,
        "short_explanation": short_explanation,
        "detailed_explanation": detailed_explanation,
        "caveats": caveats,
        "supporting_signals": supporting_signals,
    }


def rank_markets(markets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    staleness_values = [m["time_since_update_hours"] for m in markets if m["time_since_update_hours"] is not None]
    support_values = [math.log1p((m["liquidity"] or 0.0) + (m["volume_24hr"] or 0.0)) for m in markets if (m["liquidity"] is not None or m["volume_24hr"] is not None)]
    volatility_values = [m["one_month_price_change_abs"] for m in markets if m["one_month_price_change_abs"] is not None]

    ranked: list[dict[str, Any]] = []
    raw_scores: list[float] = []
    for market in markets:
        staleness_component = percentile_rank(market["time_since_update_hours"], staleness_values) * absolute_staleness_signal(market["time_since_update_hours"])
        event_horizon_component = event_horizon_signal(market["time_to_resolution_hours"])
        extremeness_component = clamp(((market["price_distance_from_mid"] or 0.0) - 0.15) / 0.35)
        support_metric = None
        if market["liquidity"] is not None or market["volume_24hr"] is not None:
            support_metric = math.log1p((market["liquidity"] or 0.0) + (market["volume_24hr"] or 0.0))
        liquidity_component = percentile_rank(support_metric, support_values, reverse=True)
        volatility_component = percentile_rank(market["one_month_price_change_abs"], volatility_values)
        data_penalty = data_quality_penalty(market)
        penalty = data_penalty

        if market["time_to_resolution_hours"] is not None:
            if market["time_to_resolution_hours"] < 0:
                penalty += 0.35
            elif market["time_to_resolution_hours"] > 720.0:
                penalty += min(0.25, (market["time_to_resolution_hours"] - 720.0) / 5000.0)
        if market["time_since_update_hours"] is not None and market["time_since_update_hours"] < 1.0:
            penalty += 0.05
        if market["yes_price"] is not None:
            if (
                (market["yes_price"] <= 0.01 or market["yes_price"] >= 0.99)
                and (market["time_to_resolution_hours"] is None or market["time_to_resolution_hours"] > 168.0)
                and (market["time_since_update_hours"] is None or market["time_since_update_hours"] < 12.0)
            ):
                penalty += 0.40
            elif (
                (market["yes_price"] <= 0.05 or market["yes_price"] >= 0.95)
                and (market["time_to_resolution_hours"] is None or market["time_to_resolution_hours"] > 720.0)
                and (market["time_since_update_hours"] is None or market["time_since_update_hours"] < 6.0)
            ):
                penalty += 0.20
        penalty = clamp(penalty)
        heuristic_penalty = max(penalty - data_penalty, 0.0)

        raw_score = (
            0.35 * staleness_component
            + 0.25 * event_horizon_component
            + 0.05 * extremeness_component
            + 0.10 * liquidity_component
            + 0.10 * volatility_component
            + 0.10 * staleness_component * event_horizon_component
            + 0.10 * extremeness_component * liquidity_component
            - 0.30 * penalty
        )

        component_scores = {
            "staleness_component": round(staleness_component, 4),
            "event_horizon_component": round(event_horizon_component, 4),
            "extremeness_component": round(extremeness_component, 4),
            "liquidity_component": round(liquidity_component, 4),
            "volatility_component": round(volatility_component, 4),
            "data_quality_penalty": round(data_penalty, 4),
            "heuristic_penalty": round(heuristic_penalty, 4),
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
        market.update(explanation_fields(market))

    ranked.sort(key=lambda item: item["final_score"], reverse=True)
    for index, market in enumerate(ranked, start=1):
        market["rank"] = index
    return ranked


def ranked_market_record(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "market_id": row["market_id"],
        "source": row["source"],
        "source_market_id": row["source_market_id"],
        "source_url": row["source_url"],
        "title": row["title"],
        "event_title": row["event_title"],
        "category": row["category"],
        "topic_tags": row["topic_tags"],
        "status": row["status"],
        "rank": row["rank"],
        "final_score": row["final_score"],
        "current_probability": row["yes_price"],
        "headline_reason": row["headline_reason"],
        "primary_reason_code": row["primary_reason_code"],
        "time_since_update_hours": row["time_since_update_hours"],
        "time_to_resolution_hours": row["time_to_resolution_hours"],
        "confidence_band": row["confidence_band"],
    }


def market_explanation_record(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "market_id": row["market_id"],
        "category": row["category"],
        "topic_tags": row["topic_tags"],
        "headline_reason": row["headline_reason"],
        "short_explanation": row["short_explanation"],
        "detailed_explanation": row["detailed_explanation"],
        "primary_reason_code": row["primary_reason_code"],
        "caveats": row["caveats"],
        "supporting_signals": row["supporting_signals"],
        "supporting_signal_values": {
            "time_since_update_hours": row["time_since_update_hours"],
            "time_to_resolution_hours": row["time_to_resolution_hours"],
            "price_distance_from_mid": row["price_distance_from_mid"],
            "liquidity": row["liquidity"],
            "volume_24hr": row["volume_24hr"],
            "one_month_price_change_abs": row["one_month_price_change_abs"],
        },
        "score_components": {
            "staleness_component": row["staleness_component"],
            "event_horizon_component": row["event_horizon_component"],
            "extremeness_component": row["extremeness_component"],
            "liquidity_component": row["liquidity_component"],
            "volatility_component": row["volatility_component"],
            "data_quality_penalty": row["data_quality_penalty"],
            "heuristic_penalty": row["heuristic_penalty"],
        },
    }


def app_bundle(rows: list[dict[str, Any]], raw_markets: list[dict[str, Any]], fetched_at: dt.datetime) -> dict[str, Any]:
    category_counts = Counter(row["category"] for row in rows)
    return {
        "ranked_markets": [ranked_market_record(row) for row in rows],
        "market_explanations": [market_explanation_record(row) for row in rows],
        "refresh_metadata": {
            "refresh_id": fetched_at.strftime("refresh-%Y%m%dT%H%M%SZ"),
            "source": "polymarket",
            "fetched_at": fetched_at.isoformat().replace("+00:00", "Z"),
            "market_count": len(raw_markets),
            "open_market_count": sum(1 for row in rows if row["status"] == "open"),
            "category_breakdown": [
                {"category": category, "market_count": count}
                for category, count in category_counts.most_common()
            ],
            "pipeline_version": PIPELINE_VERSION,
            "score_version": SCORE_VERSION,
            "notes": "Generated from the local prototype app-ready bundle mode with heuristic category context.",
        },
    }


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

    if args.app_json:
        json.dump(app_bundle(ranked, raw_markets, fetched_at), sys.stdout, indent=2)
        sys.stdout.write("\n")
    elif args.json:
        json.dump({"summary": summary, "rows": top_rows}, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(json.dumps(summary, indent=2))
        print()
        print(format_rows(top_rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

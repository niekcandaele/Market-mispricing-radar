#!/usr/bin/env python3
import argparse
import base64
import json
import os
import re
import subprocess
import sys
import tempfile
import textwrap
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CANVAS_ID = "1b13702d-5502-47d1-b1e0-6ba476250dc4"
CANVAS_API = "https://canvas.api.zerve.ai"
NOTEBOOK_URL = f"https://app.zerve.ai/notebook/{CANVAS_ID}"
DEFAULT_TIMEOUT = 20
LOGTO_CLIENT_ID = "oqry5w7u269xm5iyxtq0z"
CHROMIUM_LEVELDB_DIR = Path.home() / ".config/chromium/Default/Local Storage/leveldb"
JWT_RE = re.compile(rb"eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+")


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def decode_jwt_payload(token):
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        payload = parts[1] + "=" * (-len(parts[1]) % 4)
        return json.loads(base64.urlsafe_b64decode(payload.encode("ascii")))
    except Exception:
        return None


def extract_candidate_bearers_from_leveldb(leveldb_dir=CHROMIUM_LEVELDB_DIR):
    candidates = []
    if not leveldb_dir.exists():
        return candidates
    seen = set()
    for path in sorted(leveldb_dir.iterdir()):
        if path.is_dir():
            continue
        try:
            data = path.read_bytes()
        except Exception:
            continue
        for match in JWT_RE.finditer(data):
            token = match.group().decode("ascii", "ignore")
            if token in seen:
                continue
            seen.add(token)
            payload = decode_jwt_payload(token)
            if not isinstance(payload, dict):
                continue
            aud = payload.get("aud")
            iss = payload.get("iss")
            exp = payload.get("exp")
            if aud != LOGTO_CLIENT_ID or iss != "https://auth.zerve.io/oidc" or not isinstance(exp, int):
                continue
            candidates.append(
                {
                    "token": token,
                    "exp": exp,
                    "iat": payload.get("iat"),
                    "sub": payload.get("sub"),
                    "source_file": path.name,
                }
            )
    candidates.sort(key=lambda item: item.get("exp", 0), reverse=True)
    return candidates


def resolve_bearer(explicit_bearer=None):
    if explicit_bearer:
        return explicit_bearer, {"source": "arg_or_env"}

    candidates = extract_candidate_bearers_from_leveldb()
    if not candidates:
        return None, {"source": "chromium_leveldb", "found": False}

    chosen = candidates[0]
    metadata = {
        "source": "chromium_leveldb",
        "found": True,
        "selected_source_file": chosen["source_file"],
        "selected_exp": chosen.get("exp"),
        "selected_iat": chosen.get("iat"),
        "candidate_count": len(candidates),
    }
    return chosen["token"], metadata


def http_json(url, headers=None, timeout=DEFAULT_TIMEOUT):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", "replace")
        return {
            "status": resp.status,
            "url": resp.geturl(),
            "headers": dict(resp.headers.items()),
            "json": json.loads(body),
        }


def http_text(url, headers=None, timeout=DEFAULT_TIMEOUT):
    req = urllib.request.Request(
        url,
        headers=headers
        or {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147 Safari/537.36"
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read(4096).decode("utf-8", "replace")
        return {
            "status": resp.status,
            "url": resp.geturl(),
            "headers": dict(resp.headers.items()),
            "body_excerpt": body[:500],
        }


def interpret_public_route(body_excerpt):
    body = (body_excerpt or "").lower()
    looks_like_generic_shell = (
        "data work for the ai era" in body
        or 'og:title" content="zerve ai' in body
        or 'content="zerve, ai, platform"' in body
    )
    mentions_canvas = CANVAS_ID in body or "/notebook/" in body
    return {
        "looks_like_generic_shell": looks_like_generic_shell,
        "mentions_canvas_id": CANVAS_ID in body,
        "route_looks_verified": (not looks_like_generic_shell) and mentions_canvas,
    }


def try_public_route(url):
    try:
        res = http_text(url)
        return {"ok": True, **res, "interpretation": interpret_public_route(res.get("body_excerpt", ""))}
    except urllib.error.HTTPError as e:
        body = e.read(2048).decode("utf-8", "replace")
        return {
            "ok": False,
            "status": e.code,
            "url": e.geturl(),
            "headers": dict(e.headers.items()),
            "body_excerpt": body[:500],
            "interpretation": interpret_public_route(body[:500]),
            "error": f"HTTPError {e.code}",
        }
    except Exception as e:
        return {"ok": False, "error": repr(e)}


def try_browser_public_route(url):
    """Render the route with Playwright because Zerve notebooks are client-side apps.

    The static CloudFront response can look like a generic Zerve shell even when the
    browser-rendered public notebook is valid. Treat the route as verified only when
    the rendered page exposes the project title and public/view-only notebook chrome.
    """
    js = textwrap.dedent(
        f"""
        const fs = require('fs');
        function loadPlaywright() {{
          return require('playwright');
        }}
        const {{ chromium }} = loadPlaywright();
        (async () => {{
          const browser = await chromium.launch({{ headless: true }});
          const context = await browser.newContext({{ viewport: {{ width: 1440, height: 1200 }} }});
          const page = await context.newPage();
          const result = {{ url: {json.dumps(url)}, checked_at: new Date().toISOString() }};
          try {{
            const resp = await page.goto(result.url, {{ waitUntil: 'domcontentloaded', timeout: 60000 }});
            result.initial_status = resp && resp.status();
            await page.waitForTimeout(12000);
            result.final_url = page.url();
            result.title = await page.title().catch(() => null);
            const body = await page.locator('body').innerText({{ timeout: 5000 }}).catch(() => '');
            result.body_excerpt = body.slice(0, 2000);
            result.signals = {{
              has_project_name: body.includes('Market Mispricing Radar') || (result.title || '').includes('Market Mispricing Radar'),
              has_view_only: body.includes('View only'),
              has_streamlit_block: body.includes('Streamlit'),
              has_canvas_view: body.includes('Canvas View'),
              has_not_found: /not found|404/i.test(body),
            }};
            result.route_looks_verified = Boolean(
              result.signals.has_project_name &&
              result.signals.has_view_only &&
              result.signals.has_canvas_view &&
              !result.signals.has_not_found
            );
          }} catch (error) {{
            result.error = String(error.stack || error);
            result.route_looks_verified = false;
          }} finally {{
            console.log(JSON.stringify(result));
            await context.close();
            await browser.close();
          }}
        }})().catch((error) => {{ console.log(JSON.stringify({{ error: String(error.stack || error), route_looks_verified: false }})); }});
        """
    )
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
            f.write(js)
            script_path = f.name
        proc = subprocess.run(["node", script_path], capture_output=True, text=True, timeout=90, check=False)
        stdout = (proc.stdout or "").strip().splitlines()[-1] if proc.stdout else "{}"
        result = json.loads(stdout)
        result["ok"] = proc.returncode == 0 or "error" not in result
        return result
    except Exception as e:
        return {"ok": False, "route_looks_verified": False, "error": repr(e)}
    finally:
        try:
            Path(script_path).unlink()
        except Exception:
            pass


def try_canvas_status(bearer):
    headers = {"Authorization": f"Bearer {bearer}"}
    result = {"used_bearer": True}
    try:
        canvas = http_json(f"{CANVAS_API}/canvas/{CANVAS_ID}", headers=headers)
        result["canvas"] = {
            "status": canvas["status"],
            "url": canvas["url"],
            "is_public": canvas["json"].get("is_public"),
            "is_community": canvas["json"].get("is_community"),
            "name": canvas["json"].get("name"),
        }
    except Exception as e:
        result["canvas_error"] = repr(e)

    try:
        layout = http_json(f"{CANVAS_API}/canvas/canvas_layout/{CANVAS_ID}", headers=headers)
        result["canvas_layout"] = {
            "status": layout["status"],
            "url": layout["url"],
            "canvas_is_public": layout["json"].get("canvas", {}).get("is_public"),
            "canvas_is_community": layout["json"].get("canvas", {}).get("is_community"),
        }
    except Exception as e:
        result["canvas_layout_error"] = repr(e)

    return result


def derive_summary(result):
    route_check = result.get("public_route_check", {})
    interpretation = route_check.get("interpretation", {})
    browser_route_check = result.get("browser_public_route_check", {})
    route_verified = bool(interpretation.get("route_looks_verified") or browser_route_check.get("route_looks_verified"))

    auth_check = result.get("auth_check", {})
    canvas_public = auth_check.get("canvas", {}).get("is_public")
    layout_public = auth_check.get("canvas_layout", {}).get("canvas_is_public")
    auth_public_confirmed = bool(canvas_public is True or layout_public is True)
    auth_checked = bool(auth_check.get("used_bearer"))

    ready_for_share_post_link = route_verified and auth_public_confirmed

    if ready_for_share_post_link:
        next_action = "Public project page looks verified and authenticated status confirms public visibility."
    elif not auth_checked:
        next_action = "Route checked, but authenticated public-status confirmation is still missing. Re-run with a fresh bearer if available."
    elif not auth_public_confirmed:
        next_action = "Authenticated status still does not confirm public visibility. Make the notebook public in Zerve, then re-run."
    elif not route_verified:
        next_action = "Notebook route still does not look like a verified public project page. Do not use it for the share post yet."
    else:
        next_action = "Share-post link is not ready yet."

    return {
        "route_verified": route_verified,
        "auth_checked": auth_checked,
        "auth_public_confirmed": auth_public_confirmed,
        "ready_for_share_post_link": ready_for_share_post_link,
        "next_action": next_action,
    }


def main():
    parser = argparse.ArgumentParser(description="Check Zerve public-share readiness for Market Mispricing Radar.")
    parser.add_argument("--output", help="Write JSON result to this path.")
    parser.add_argument("--bearer", help="Bearer token for authenticated canvas checks. Defaults to ZERVE_BEARER env var, then best-effort Chromium extraction.")
    args = parser.parse_args()

    explicit_bearer = args.bearer or os.environ.get("ZERVE_BEARER")
    bearer, bearer_meta = resolve_bearer(explicit_bearer)

    result = {
        "checked_at": now_iso(),
        "canvas_id": CANVAS_ID,
        "notebook_share_url": NOTEBOOK_URL,
        "public_route_check": try_public_route(NOTEBOOK_URL),
        "browser_public_route_check": try_browser_public_route(NOTEBOOK_URL),
        "auth_check": {"used_bearer": False, "note": "Pass --bearer, set ZERVE_BEARER, or rely on best-effort Chromium token extraction."},
        "bearer_resolution": bearer_meta,
    }

    if bearer:
        result["auth_check"] = try_canvas_status(bearer)

    result["summary"] = derive_summary(result)

    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    print(text)
    return 0 if result["summary"]["ready_for_share_post_link"] else 1


if __name__ == "__main__":
    sys.exit(main())

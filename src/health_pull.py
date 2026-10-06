#!/usr/bin/env python3
"""Pulls last week's numbers for every Taliferro web property and app and
writes public/health/health.json for the /health cockpit page.

    python3 src/health_pull.py                # last full Mon-Sun week
    python3 src/health_pull.py --end 2026-10-04

Writes two files into public/health/:
  health.json  plain data, for local use and design work; never deployed
               (firebase.json ignores it)
  data.enc     the same JSON, AES-256-CBC encrypted (openssl, PBKDF2-SHA256)
               with the password in ~/keys/health-password.txt; the /health
               page decrypts it in the browser

Standard library only. The Google service-account JWT is signed with the
openssl CLI because this Mac's Python cryptography build will not load.

GA4: the service account (HEALTH_GA_KEY, default ~/keys/taliferrotech-*.json)
is a Viewer on both properties. App Store: ratings from Apple's public lookup,
reviews from the App Store Connect API (key C4PA96WUD3, App Manager), weekly
downloads from the Sales reports API (key S44CYAM8ZM, Sales role, since App
Manager keys can't read sales) plus the vendor number in ~/keys/asc-vendor.txt.

The headline number is engaged sessions (GA's "real visit": 10s+, 2+ pages or
a key event), not users. Most raw users are data-center bots (Moses Lake, San
Jose, Des Moines, Ashburn, Singapore at 0-2 seconds), and every localhost hit
is a Cypress run from a deploy, so localhost is dropped entirely.
"""
import argparse
import base64
import csv
import datetime as dt
import glob
import gzip
import io
import json
import os
import subprocess
import tempfile
import time
import urllib.parse
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "public" / "health" / "health.json"
GA_KEY = os.environ.get("HEALTH_GA_KEY") or next(iter(sorted(glob.glob(os.path.expanduser("~/keys/taliferrotech-*.json")))), "")
PASSWORD_FILE = Path(os.environ.get("HEALTH_PASSWORD_FILE", "~/keys/health-password.txt")).expanduser()
ASC_KEY_ID, ASC_ISSUER = "C4PA96WUD3", "d19396a2-82f5-4aa8-97b7-9ccf24196d32"
ASC_KEY = next((Path(p).expanduser() for p in [os.environ.get("ASC_KEY", ""), "~/keys/AuthKey_C4PA96WUD3.p8",
                                                   "~/Dropbox/corporate/AuthKey_C4PA96WUD3.p8"]
                if p and Path(p).expanduser().is_file()), None)
ASC_SALES_KEY_ID = "S44CYAM8ZM"
ASC_SALES_KEY = Path(os.environ.get("ASC_SALES_KEY", "~/keys/AuthKey_S44CYAM8ZM.p8")).expanduser()
ASC_VENDOR_FILE = Path("~/keys/asc-vendor.txt").expanduser()
PBKDF2_ITER = 210000  # must match public/health/index.html

TECH, GROUP = "440375536", "170189229"  # GA4 properties: taliferrotech, Taliferro

# One cockpit row per property. stream = GA4 stream id; host = the site's own
# hostname (other hostnames on a stream, localhost included, are test runs or
# stray copies of the tag and are ignored). events = the success events that
# matter for that row.
PROPERTIES = [
    # name, group, property, stream, host, url, events, app store id
    ("Taliferro Tech", "Company", TECH, "16044446676", "taliferro.tech", "https://taliferro.tech",
     ["get_started", "contact", "app_store_click"], None),
    ("Taliferro Group", "Company", GROUP, "13266253031", "taliferro.com", "https://taliferro.com", [], None),
    ("Find", "Intelligence", TECH, "15742921959", "find.taliferro.tech", "https://find.taliferro.tech", [], "6806954591"),
    ("TODD", "Intelligence", TECH, "8131343193", "todd.taliferro.tech", "https://todd.taliferro.tech", [], None),
    ("Ask TODD", "Intelligence", TECH, "15742948079", "ask.taliferro.tech", "https://ask.taliferro.tech", [], None),
    ("Maya", "Intelligence", TECH, "15743322007", "maya.taliferro.tech", "https://maya.taliferro.tech", [], None),
    ("Moves", "Intelligence", TECH, "15743464048", "moves.taliferro.tech", "https://moves.taliferro.tech", [], None),
    ("Pulse", "Intelligence", TECH, "15742937805", "pulse.taliferro.tech", "https://pulse.taliferro.tech", [], None),
    ("Network", "Grow", TECH, "15742898390", "network.taliferro.tech", "https://network.taliferro.tech", [], None),
    ("Lead Vault", "Grow", TECH, "15743478025", "lead-vault.taliferro.tech", "https://lead-vault.taliferro.tech", [], None),
    ("Outreach", "Grow", TECH, "15742946776", "outreach.taliferro.tech", "https://outreach.taliferro.tech", [], None),
    ("Social", "Grow", TECH, "15743464052", "social.taliferro.tech", "https://social.taliferro.tech", [], None),
    ("SayIt", "Grow", TECH, "15742971797", "sayit.taliferro.tech", "https://sayit.taliferro.tech", [], None),
    ("Docs", "Create", TECH, "15743468020", "docs.taliferro.tech", "https://docs.taliferro.tech", [], None),
    ("Email Creator", "Create", TECH, "16044468969", "emails.taliferro.tech", "https://emails.taliferro.tech",
     ["email_created", "email_downloaded"], None),
    ("Email Signature", "Create", TECH, "15742948824", "signature.taliferro.tech", "https://signature.taliferro.tech", [], None),
    ("Image Creator", "Create", TECH, "16044494225", "images.taliferro.tech", "https://images.taliferro.tech",
     ["image_created", "image_downloaded"], None),
    ("Music", "Listen", GROUP, "16044461409", "music.taliferro.com", "https://music.taliferro.com",
     ["radio_play", "app_store_click"], "6806499542"),
]
# Tag added (or fixed) on this date; earlier weeks have no data by design.
TRACKING_SINCE = {"Taliferro Tech": "2026-10-05", "Music": "2026-10-05", "Email Creator": "2026-10-05",
                  "Image Creator": "2026-10-05", "Ask TODD": "2026-10-05", "Docs": "2026-10-05"}

# Below this many engaged sessions in both weeks a % change is noise, so the
# row is reported as "low" instead of green/yellow/red.
MIN_ENGAGED = 10
YELLOW_BELOW, RED_BELOW = -0.05, -0.20


# ------------------------------------------------------------ Google auth

def b64url(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def ga_token():
    key = json.loads(Path(GA_KEY).read_text())
    now = int(time.time())
    head = b64url(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    claim = b64url(json.dumps({"iss": key["client_email"], "scope": "https://www.googleapis.com/auth/analytics.readonly",
                               "aud": "https://oauth2.googleapis.com/token", "iat": now, "exp": now + 3600}).encode())
    sig = openssl_sign(key["private_key"], f"{head}.{claim}".encode())
    body = urllib.parse.urlencode({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                                   "assertion": f"{head}.{claim}.{b64url(sig)}"}).encode()
    return json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", body))["access_token"]


def openssl_sign(pem_text, data):
    with tempfile.NamedTemporaryFile("w", suffix=".pem") as pem:
        os.chmod(pem.name, 0o600)
        pem.write(pem_text)
        pem.flush()
        return subprocess.run(["openssl", "dgst", "-sha256", "-sign", pem.name], input=data,
                              capture_output=True, check=True).stdout


def run_report(token, prop, body):
    req = urllib.request.Request(f"https://analyticsdata.googleapis.com/v1beta/properties/{prop}:runReport",
                                 json.dumps(body).encode(), {"Authorization": f"Bearer {token}",
                                                             "Content-Type": "application/json"})
    rows = json.load(urllib.request.urlopen(req)).get("rows", [])
    return [([d["value"] for d in r["dimensionValues"]], [float(m["value"]) for m in r["metricValues"]]) for r in rows]


# ------------------------------------------------------------ GA4 pull

def pull_ga(token, weeks):
    """Returns {stream_id: {"web": {week: [engaged, users, sessions, views, engagement_sec]}, "events": {name: {week: n}}}}."""
    ranges = [{"startDate": s, "endDate": e, "name": k} for k, (s, e) in weeks.items()]
    events = sorted({e for p in PROPERTIES for e in p[6]})
    data = {}
    for prop in sorted({p[2] for p in PROPERTIES}):
        hosts = {p[3]: p[4] for p in PROPERTIES if p[2] == prop}
        traffic = run_report(token, prop, {
            "dimensions": [{"name": "streamId"}, {"name": "hostName"}],
            "metrics": [{"name": "engagedSessions"}, {"name": "activeUsers"}, {"name": "sessions"},
                        {"name": "screenPageViews"}, {"name": "userEngagementDuration"}],
            "dateRanges": ranges, "limit": 1000})
        for (stream, host, week), vals in traffic:
            if hosts.get(stream) == host:
                data.setdefault(stream, {}).setdefault("web", {})[week] = vals
        if events:
            # Same host rule as traffic, so test runs on localhost don't count.
            counts = run_report(token, prop, {
                "dimensions": [{"name": "streamId"}, {"name": "hostName"}, {"name": "eventName"}],
                "metrics": [{"name": "eventCount"}], "dateRanges": ranges,
                "dimensionFilter": {"filter": {"fieldName": "eventName", "inListFilter": {"values": events}}}})
            for (stream, host, name, week), (n,) in counts:
                if hosts.get(stream) != host:
                    continue
                data.setdefault(stream, {}).setdefault("events", {}).setdefault(name, {})[week] = int(n)
    return data


# ------------------------------------------------------------ App Store

def pull_ratings(app_id):
    """Public lookup: no credentials. Ratings only appear once enough people rate."""
    try:
        r = json.load(urllib.request.urlopen(f"https://itunes.apple.com/lookup?id={app_id}&country=us", timeout=20))
        r = (r.get("results") or [{}])[0]
        return {"name": r.get("trackName"), "url": (r.get("trackViewUrl") or "").split("?")[0],
                "version": r.get("version"), "rating": r.get("averageUserRating"),
                "rating_count": r.get("userRatingCount", 0)}
    except Exception as e:  # never fail the whole pull over Apple's lookup
        return {"error": str(e)}


def asc_token(key_id=ASC_KEY_ID, key_file=None):
    """ES256 JWT for App Store Connect; openssl returns a DER signature, JWS wants raw r||s."""
    now = int(time.time())
    head = b64url(json.dumps({"alg": "ES256", "kid": key_id, "typ": "JWT"}).encode())
    claim = b64url(json.dumps({"iss": ASC_ISSUER, "iat": now, "exp": now + 1100, "aud": "appstoreconnect-v1"}).encode())
    der = openssl_sign((key_file or ASC_KEY).read_text(), f"{head}.{claim}".encode())
    i = 2 if der[1] < 0x80 else 3  # SEQUENCE { INTEGER r, INTEGER s }
    rlen = der[i + 1]
    r = der[i + 2:i + 2 + rlen]
    j = i + 2 + rlen
    s_ = der[j + 2:j + 2 + der[j + 1]]
    raw = r.lstrip(b"\0").rjust(32, b"\0") + s_.lstrip(b"\0").rjust(32, b"\0")
    return f"{head}.{claim}.{b64url(raw)}"


def asc_get(token, path, accept="application/json"):
    req = urllib.request.Request("https://api.appstoreconnect.apple.com" + path,
                                 headers={"Authorization": f"Bearer {token}", "Accept": accept})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def pull_reviews(token, app_id):
    data = json.loads(asc_get(token, f"/v1/apps/{app_id}/customerReviews?sort=-createdDate&limit=5"))
    return [{k: x["attributes"].get(k) for k in ("rating", "title", "body", "createdDate", "territory")}
            for x in data.get("data", [])]


def pull_downloads(token, vendor, sunday):
    """Units per Apple ID from the WEEKLY sales summary for the week ending `sunday`.
    Product types: 1*/F1* first-time downloads, 3* re-downloads, 7* updates (a rough
    count of devices that still have the app installed)."""
    q = urllib.parse.urlencode({"filter[frequency]": "WEEKLY", "filter[reportType]": "SALES",
                                "filter[reportSubType]": "SUMMARY", "filter[version]": "1_1",
                                "filter[vendorNumber]": vendor, "filter[reportDate]": sunday})
    try:
        raw = gzip.decompress(asc_get(token, f"/v1/salesReports?{q}", "application/a-gzip"))
    except urllib.error.HTTPError as e:
        if e.code == 404:  # Apple returns 404 for a week with no sales rows at all
            return {}
        raise
    out = {}
    for row in csv.DictReader(io.StringIO(raw.decode()), delimiter="\t"):
        kind = row.get("Product Type Identifier", "")
        key = ("downloads" if kind[:1] == "1" or kind.startswith("F1") else "redownloads" if kind[:1] == "3"
               else "updates" if kind[:1] == "7" else None)
        if key:
            slot = out.setdefault(row["Apple Identifier"], {"downloads": 0, "redownloads": 0, "updates": 0})
            slot[key] += int(float(row.get("Units") or 0))
    return out


def pull_app_store(weeks, app_ids):
    """{app_id: {...}} plus a status string for the report."""
    if not ASC_KEY:
        return {}, "no App Store Connect key found"
    token = asc_token()
    out = {a: {"reviews": [], "downloads": None} for a in app_ids}
    notes = []
    for a in app_ids:
        try:
            out[a]["reviews"] = pull_reviews(token, a)
        except Exception as e:
            notes.append(f"reviews {a}: {e}")
    vendor = ASC_VENDOR_FILE.read_text().strip() if ASC_VENDOR_FILE.is_file() else ""
    if not vendor:
        notes.append("downloads need the vendor number in ~/keys/asc-vendor.txt")
    elif not ASC_SALES_KEY.is_file():
        notes.append(f"downloads need the Sales-role key at {ASC_SALES_KEY}")
    else:
        try:
            sales = asc_token(ASC_SALES_KEY_ID, ASC_SALES_KEY)
            per_week = {w: pull_downloads(sales, vendor, end) for w, (_, end) in weeks.items()}
            for a in app_ids:
                out[a]["downloads"] = {w: per_week[w].get(a, {"downloads": 0, "redownloads": 0, "updates": 0}) for w in per_week}
        except Exception as e:
            notes.append(f"downloads: {e}")
    return out, "; ".join(notes) or "ok"


# ------------------------------------------------------------ scoring

def change(now, prev):
    return None if not prev else round((now - prev) / prev, 3)


def status(now, prev):
    if now == 0 and prev == 0:
        return "none"
    if now == 0:
        return "red"
    if max(now, prev) < MIN_ENGAGED:
        return "low"
    c = change(now, prev)
    if c is None or c >= YELLOW_BELOW:
        return "green"
    return "yellow" if c >= RED_BELOW else "red"


def summarise(block):
    """[engaged, users, sessions, views, engagement_sec] per week -> dict with deltas."""
    block = block or {}
    cur, prev = block.get("this", [0] * 5), block.get("prev", [0] * 5)
    out = {}
    for i, k in enumerate(["engaged_sessions", "users_incl_bots", "sessions", "views"]):
        out[k] = {"this": int(cur[i]), "prev": int(prev[i]), "change": change(cur[i], prev[i])}
    out["engagement_rate"] = round(cur[0] / cur[2], 3) if cur[2] else None
    out["engaged_sec_per_session"] = round(cur[4] / cur[0]) if cur[0] else 0
    return out


def build(end):
    start = end - dt.timedelta(days=6)
    weeks = {"this": (start.isoformat(), end.isoformat()),
             "prev": ((start - dt.timedelta(days=7)).isoformat(), (end - dt.timedelta(days=7)).isoformat())}
    ga = pull_ga(ga_token(), weeks)
    apps, apps_status = pull_app_store(weeks, [p[7] for p in PROPERTIES if p[7]])
    rows = []
    for name, group, prop, stream, host, url, events, app_id in PROPERTIES:
        d = ga.get(stream, {})
        web = summarise(d.get("web"))
        now, prev = web["engaged_sessions"]["this"], web["engaged_sessions"]["prev"]
        since = TRACKING_SINCE.get(name)
        new = bool(since and since > weeks["prev"][0])
        ev = {e: {"this": d.get("events", {}).get(e, {}).get("this", 0),
                  "prev": d.get("events", {}).get(e, {}).get("prev", 0)} for e in events}
        notes = []
        if new:
            notes.append(f"Tracking started {since}; no full week to compare yet.")
        elif web["users_incl_bots"]["this"] == 0:
            notes.append("No GA data this week; check the tag and the site.")
        rows.append({
            "name": name, "group": group, "url": url, "host": host, "tracking_since": since,
            "engaged_sessions": web["engaged_sessions"],
            "status": "new" if new else status(now, prev),
            "web": web, "events": ev,
            "app_store": {**pull_ratings(app_id), **apps.get(app_id, {})} if app_id else None,
            "notes": notes,
        })
    total_now = sum(r["engaged_sessions"]["this"] for r in rows)
    total_prev = sum(r["engaged_sessions"]["prev"] for r in rows)
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "week": {"start": weeks["this"][0], "end": weeks["this"][1]},
        "prev_week": {"start": weeks["prev"][0], "end": weeks["prev"][1]},
        "thresholds": {"min_engaged_sessions": MIN_ENGAGED, "yellow_below": YELLOW_BELOW, "red_below": RED_BELOW},
        "totals": {"engaged_sessions": {"this": total_now, "prev": total_prev, "change": change(total_now, total_prev)},
                   "by_status": {s: sum(r["status"] == s for r in rows)
                                 for s in ["green", "yellow", "red", "low", "new", "none"]}},
        "app_store_status": apps_status,
        "properties": rows,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--end", help="last day of the week (YYYY-MM-DD); default: last Sunday")
    ap.add_argument("--stdout", action="store_true", help="print instead of writing health.json")
    a = ap.parse_args()
    today = dt.date.today()
    end = dt.date.fromisoformat(a.end) if a.end else today - dt.timedelta(days=today.isoweekday() % 7 or 7)
    report = build(end)
    text = json.dumps(report, indent=1)
    if a.stdout:
        print(text)
        return
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(OUT.parents[2])}: week {report['week']['start']}..{report['week']['end']}, "
          f"{len(report['properties'])} properties, {report['totals']['by_status']}; app store: {report['app_store_status']}")
    if PASSWORD_FILE.is_file():
        enc = OUT.with_name("data.enc")
        subprocess.run(["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-iter", str(PBKDF2_ITER), "-md", "sha256",
                        "-salt", "-in", str(OUT), "-out", str(enc), "-pass", f"file:{PASSWORD_FILE}"], check=True)
        print(f"wrote {enc.relative_to(OUT.parents[2])} (encrypted)")
    else:
        print(f"no {PASSWORD_FILE}: data.enc not written, so the /health page has nothing new to show")


if __name__ == "__main__":
    main()

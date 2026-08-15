#!/usr/bin/env python3
"""Applies site_config.py to every generated page. Idempotent — safe to re-run."""
import os, re, json, glob, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_config import *   # noqa

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
FILES = sorted(glob.glob("**/*.html", recursive=True))
stats = {k: 0 for k in ("phone", "schema_url", "aggregate", "placeid", "order_url",
                        "analytics", "hours", "canonical")}


def is_duluth_page(f):
    return any(k in f.lower() for k in ("duluth", "gas-south", "sugarloaf", "johns-creek",
                                        "suwanee", "berkeley", "norcross", "peachtree-corners",
                                        "sugar-hill", "dunwoody"))


# ---------------------------------------------------------------- ANALYTICS LOADER
ANALYTICS = '''<script src="{r}assets/config.js"></script>
<script src="{r}assets/analytics.js" defer></script>'''

OLD_ANALYTICS = re.compile(
    r'<!-- GOOGLE ANALYTICS 4.*?-->\s*<!-- META PIXEL.*?-->\s*', re.S)

for f in FILES:
    depth = f.count("/")
    r = "../" * depth
    s = open(f, encoding="utf-8").read()
    orig = s

    # ---- 1. phone numbers from config only ----
    for bad in ("(321) 333-2984", "321-333-2984", "3213332984"):
        if bad in s:
            s = s.replace(bad, LOCATIONS["duluth"]["phone_display"]); stats["phone"] += 1
    if "+13213332984" in s:
        s = s.replace("+13213332984", LOCATIONS["duluth"]["phone_raw"]); stats["phone"] += 1

    # ---- 2. order URL from config ----
    if "order.online/business/13060526" in s:
        s = s.replace("https://order.online/business/13060526", ORDER_URL); stats["order_url"] += 1

    # ---- 3. analytics placeholders -> centralised, inert loader ----
    if "GOOGLE ANALYTICS 4" in s or "PIXEL_ID" in s:
        s = OLD_ANALYTICS.sub("", s)
        s = re.sub(r'<!-- META PIXEL.*?-->\s*', "", s, flags=re.S)
        s = re.sub(r'<!-- GOOGLE ANALYTICS 4.*?-->\s*', "", s, flags=re.S)
        stats["analytics"] += 1
    if "assets/analytics.js" not in s:
        s = s.replace("</head>", ANALYTICS.format(r=r) + "\n</head>", 1)

    # ---- 4. Google review placeholders -> disabled CTA ----
    if "PLACE_ID_" in s:
        for slug in ("buckhead", "duluth"):
            pid = LOCATIONS[slug]["google_place_id"]
            token = "PLACE_ID_" + slug.upper()
            if pid:
                s = s.replace(token, pid)
            else:
                # remove the whole anchor rather than ship a broken link
                s = re.sub(
                    r'<a href="https://search\.google\.com/local/writereview\?placeid=%s">(.*?)</a>' % token,
                    r'<span class="cta-disabled" aria-disabled="true">\1 — link pending</span>', s)
        stats["placeid"] += 1

    # ---- 5. JSON-LD: clean URLs, config hours/phones, drop aggregateRating ----
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            obj = json.loads(blk)
        except Exception:
            continue
        before = json.dumps(obj)

        def walk(o):
            if isinstance(o, dict):
                # clean URLs on every URL-bearing field
                for key in ("url", "@id", "item", "mainEntityOfPage", "menu", "contentUrl", "embedUrl"):
                    v = o.get(key)
                    if isinstance(v, str) and v.startswith(PRODUCTION_HOST) and v.endswith(".html"):
                        o[key] = v[:-5] if not v.endswith("/index.html") else v[:-len("index.html")]
                        stats["schema_url"] += 1
                    elif isinstance(v, str) and v.endswith("/index.html"):
                        o[key] = v[:-len("index.html")]
                if o.get("@type") == "Restaurant":
                    dul = "Duluth" in json.dumps(o)
                    L = LOCATIONS["duluth" if dul else "buckhead"]
                    o["telephone"] = L["phone_raw"]
                    o["openingHoursSpecification"] = L["hours_schema"]
                    o["geo"] = {"@type": "GeoCoordinates", "latitude": L["lat"], "longitude": L["lng"]}
                    if not EMIT_AGGREGATE_RATING and "aggregateRating" in o:
                        del o["aggregateRating"]; stats["aggregate"] += 1
                    stats["hours"] += 1
                if not EMIT_AGGREGATE_RATING and "aggregateRating" in o:
                    del o["aggregateRating"]; stats["aggregate"] += 1
                for v in list(o.values()):
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(obj)
        if json.dumps(obj) != before:
            s = s.replace(blk, json.dumps(obj, indent=2))

    # ---- 6. canonical / og:url must be clean production URLs ----
    want = canonical(f)
    if f not in NOINDEX_PAGES:
        new_s = re.sub(r'<link rel="canonical" href="[^"]*"',
                       '<link rel="canonical" href="%s"' % want, s)
        new_s = re.sub(r'<meta property="og:url" content="[^"]*"',
                       '<meta property="og:url" content="%s"' % want, new_s)
        if new_s != s:
            stats["canonical"] += 1
        s = new_s

    if s != orig:
        open(f, "w", encoding="utf-8").write(s)

print("FIXES APPLIED")
for k, v in stats.items():
    print("  %-12s %d" % (k, v))

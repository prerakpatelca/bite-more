#!/usr/bin/env python3
"""
BITE MORE — AUTOMATED PRE-LAUNCH SEO CHECK
==========================================
Run from the site root:  python3 seo_prelaunch_check.py
Exit code 0 = GO, 1 = blockers found.

Standard library only. No dependencies.
"""
import os, re, sys, json, glob, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_config import (PRODUCTION_HOST, NETLIFY_HOST, LOCATIONS, FORBIDDEN_STRINGS,
                         NOINDEX_PAGES, clean_url, EMIT_AGGREGATE_RATING)

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
HTML = sorted(glob.glob("**/*.html", recursive=True))
SRC = [p for p in glob.glob("*.py")]
results, blockers = [], []


def check(name, ok, detail="", blocking=True):
    results.append((name, "PASS" if ok else "FAIL", detail))
    if not ok and blocking:
        blockers.append((name, detail))
    return ok


# ---------------------------------------------------------------- 1 forbidden strings
hits = []
for f in HTML + SRC + ["sitemap.xml", "robots.txt", "netlify.toml",
                       "assets/config.js", "assets/analytics.js", "assets/site.js", "assets/video.js"]:
    if not os.path.exists(f):
        continue
    body = open(f, encoding="utf-8", errors="ignore").read()
    for bad in FORBIDDEN_STRINGS:
        if bad in body:
            # site_config.py legitimately lists them as forbidden
            if f in ("site_config.py", "apply_config.py", "seo_prelaunch_check.py"):
                continue
            for i, line in enumerate(body.split("\n"), 1):
                if bad in line:
                    hits.append("%s:%d  %s" % (f, i, bad))
check("Old Duluth phone / placeholders absent", not hits, "; ".join(hits[:6]))

# ---------------------------------------------------------------- 2 canonicals
missing = multiple = wronghost = conflict = 0
bad_detail = []
for f in HTML:
    s = open(f, encoding="utf-8").read()
    c = re.findall(r'<link rel="canonical" href="([^"]+)"', s)
    if f in NOINDEX_PAGES:
        continue
    if not c:
        missing += 1; bad_detail.append(f + " missing"); continue
    if len(c) > 1:
        multiple += 1; bad_detail.append(f + " multiple")
    u = c[0]
    if not u.startswith(PRODUCTION_HOST) or NETLIFY_HOST in u or "localhost" in u:
        wronghost += 1; bad_detail.append("%s host=%s" % (f, u))
    want = PRODUCTION_HOST + clean_url(f)
    if u != want:
        conflict += 1; bad_detail.append("%s is=%s want=%s" % (f, u, want))
check("Canonical tags", missing == multiple == wronghost == conflict == 0,
      "missing=%d multiple=%d wronghost=%d conflict=%d %s" % (missing, multiple, wronghost, conflict, bad_detail[:3]))

# ---------------------------------------------------------------- 3 JSON-LD
blocks = parse_err = stale_phone = stale_html = agg = ph = 0
jd = []
OLD_PHONES = ["(321) 333-2984", "+13213332984"]
for f in HTML:
    s = open(f, encoding="utf-8").read()
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        blocks += 1
        try:
            o = json.loads(b)
        except Exception as e:
            parse_err += 1; jd.append("%s %s" % (f, str(e)[:40])); continue
        t = json.dumps(o)
        if any(p in t for p in OLD_PHONES):
            stale_phone += 1; jd.append(f + " stale phone")
        if re.search(r'"(?:url|@id|item|mainEntityOfPage|menu)":\s*"[^"]*\.html"', t):
            stale_html += 1; jd.append(f + " .html schema url")
        if not EMIT_AGGREGATE_RATING and "aggregateRating" in t:
            agg += 1; jd.append(f + " aggregateRating")
        if "PLACE_ID_" in t or "G-XXXX" in t:
            ph += 1
check("JSON-LD parsing", parse_err == 0, "errors=%d %s" % (parse_err, jd[:3]))
check("Clean schema URLs", stale_html == 0, "%d pages" % stale_html)
check("AggregateRating removed", agg == 0, "%d instances" % agg)
check("Schema placeholders", ph == 0, "%d" % ph)

# ---------------------------------------------------------------- 4 sitemap vs canonical
sm = open("sitemap.xml", encoding="utf-8").read() if os.path.exists("sitemap.xml") else ""
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
dupes = [u for u, c in collections.Counter(locs).items() if c > 1]
canon = {PRODUCTION_HOST + clean_url(f) for f in HTML if f not in NOINDEX_PAGES}
noindexed = {PRODUCTION_HOST + clean_url(f) for f in NOINDEX_PAGES}
conf = [u for u in locs if u not in canon]
inx = [u for u in locs if u in noindexed]
dothtml = [u for u in locs if u.endswith(".html")]
check("Sitemap vs canonicals", not conf and not dupes and not inx and not dothtml,
      "urls=%d dupes=%d conflicts=%d noindex=%d .html=%d %s"
      % (len(locs), len(dupes), len(conf), len(inx), len(dothtml), conf[:3]))

# ---------------------------------------------------------------- 5 robots
rb = open("robots.txt", encoding="utf-8").read() if os.path.exists("robots.txt") else ""
check("robots.txt", "Sitemap: %s/sitemap.xml" % PRODUCTION_HOST in rb
      and "Disallow: /" not in rb.replace("Disallow: /\n", "DISALLOWALL")
      and ".css" not in rb and ".js" not in rb, "")

# ---------------------------------------------------------------- 6 titles / meta / h1
titles, descs = collections.Counter(), collections.Counter()
no_t = no_d = h1_zero = h1_multi = 0
for f in HTML:
    if f in NOINDEX_PAGES:
        continue
    s = open(f, encoding="utf-8").read()
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    d = re.search(r'<meta name="description" content="(.*?)"', s, re.S)
    if not t or not t.group(1).strip(): no_t += 1
    else: titles[t.group(1).strip()] += 1
    if not d or not d.group(1).strip(): no_d += 1
    else: descs[d.group(1).strip()] += 1
    h = len(re.findall(r"<h1", s))
    if h == 0: h1_zero += 1
    elif h > 1: h1_multi += 1
dup_t = [x for x, c in titles.items() if c > 1]
dup_d = [x for x, c in descs.items() if c > 1]
check("Missing titles", no_t == 0, str(no_t))
check("Duplicate titles", not dup_t, "%d: %s" % (len(dup_t), dup_t[:2]))
check("Missing descriptions", no_d == 0, str(no_d))
check("Duplicate descriptions", not dup_d, "%d: %s" % (len(dup_d), dup_d[:2]), blocking=False)
check("H1 structure", h1_zero == 0 and h1_multi == 0, "zero=%d multiple=%d" % (h1_zero, h1_multi))

# ---------------------------------------------------------------- 7 internal links
allpaths = set(HTML)
broken = []
for f in HTML:
    d = os.path.dirname(f)
    s = open(f, encoding="utf-8").read()
    for h in re.findall(r'<a [^>]*href="([^"]+)"', s):
        if h.startswith(("http", "mailto:", "tel:", "#", "data:")):
            continue
        h = h.split("#")[0].split("?")[0]
        if not h:
            continue
        if h.startswith("/"):
            t = h.lstrip("/")
        else:
            t = os.path.normpath(os.path.join(d, h))
        if t in ("", "."):
            t = "index.html"
        cands = {t, t + ".html", os.path.join(t, "index.html").replace("\\", "/")}
        if not (cands & allpaths):
            broken.append("%s -> %s" % (f, h))
check("Internal links", not broken, "%d broken: %s" % (len(broken), broken[:4]))

# ---------------------------------------------------------------- 8 NAP consistency
nap = []
for f in HTML:
    s = open(f, encoding="utf-8").read()
    for slug, L in LOCATIONS.items():
        other = LOCATIONS["duluth" if slug == "buckhead" else "buckhead"]
        # a page naming one location's address must not carry the other's phone as its own
        if L["street"] in s and other["phone_display"] in s and L["phone_display"] not in s:
            nap.append("%s %s address without %s phone" % (f, L["name"], L["name"]))
check("NAP consistency", not nap, "%d: %s" % (len(nap), nap[:3]))

# ---------------------------------------------------------------- 9 hours consistency
hrs = []
for f in HTML:
    s = open(f, encoding="utf-8").read()
    if "Closed</span>" in s or "closed Mondays" in s:
        hrs.append(f + " stale 'closed Monday'")
check("Location hours consistent", not hrs, "%d: %s" % (len(hrs), hrs[:3]))

# ---------------------------------------------------------------- 10 images
imgs = miss_alt = empty_alt = lazy_iss = 0
for f in HTML:
    s = open(f, encoding="utf-8").read()
    for tag in re.findall(r"<img[^>]*>", s):
        imgs += 1
        if "alt=" not in tag: miss_alt += 1
        elif re.search(r'alt=""', tag) and "poster" not in tag: empty_alt += 1
        if "loading=" not in tag and "class=\"poster\"" not in tag: lazy_iss += 1
check("Image alt attributes", miss_alt == 0 and empty_alt == 0,
      "total=%d missing=%d empty=%d" % (imgs, miss_alt, empty_alt))

# ---------------------------------------------------------------- 11 autoplay audio
audio = []
for f in HTML:
    s = open(f, encoding="utf-8").read()
    for tag in re.findall(r"<video[^>]*>", s):
        if "autoplay" in tag and "muted" not in tag:
            audio.append(f)
check("No autoplay audio", not audio, "%d: %s" % (len(audio), audio[:3]))

# ---------------------------------------------------------------- 12 host consistency
hosts = []
for f in HTML:
    s = open(f, encoding="utf-8").read()
    if NETLIFY_HOST in s or "localhost" in s:
        hosts.append(f)
check("Production host consistency", not hosts, "%d: %s" % (len(hosts), hosts[:3]))

# ---------------------------------------------------------------- 13 redirects
tomlsrc = open("netlify.toml", encoding="utf-8").read() if os.path.exists("netlify.toml") else ""
froms = re.findall(r'from = "([^"]+)"', tomlsrc)
tos = re.findall(r'to = "([^"]+)"', tomlsrc)
loops = [a for a, b in zip(froms, tos) if a == b]
chains = [b for b in tos if b in froms]
dead = []
for b in tos:
    if b.startswith("/") and not b.startswith("/404"):
        t = b.lstrip("/")
        if not ({t, t + ".html", t + "/index.html"} & allpaths):
            dead.append(b)
check("Redirect rules", not loops and not chains and not dead,
      "loops=%d chains=%d dead=%s" % (len(loops), len(chains), dead[:3]))

# ---------------------------------------------------------------- report
print("=" * 62)
print("BITE MORE — PRE-LAUNCH SEO CHECK")
print("=" * 62)
w = max(len(r[0]) for r in results)
for name, res, detail in results:
    print("%-*s  %s  %s" % (w, name, res, detail if res == "FAIL" else ""))
print("-" * 62)
print("HTML pages: %d | JSON-LD blocks: %d | sitemap URLs: %d | images: %d"
      % (len(HTML), blocks, len(locs), imgs))
print("=" * 62)
if blockers:
    print("DO NOT DEPLOY YET — %d blocker(s):" % len(blockers))
    for n, d in blockers:
        print("  - %s: %s" % (n, d))
    sys.exit(1)
print("GO FOR PRODUCTION")
sys.exit(0)

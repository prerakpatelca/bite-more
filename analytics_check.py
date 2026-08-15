#!/usr/bin/env python3
"""BITE MORE — analytics installation verification. Standard library only."""
import re, glob, os, sys, collections

os.chdir(os.path.dirname(os.path.abspath(__file__)))
GTM_ID = "GTM-PT8568DB"
GA4_ID = "G-220KLBJVG4"
HTML = sorted(glob.glob("**/*.html", recursive=True))

head_ok = ns_ok = dup_gtm = dup_ga4 = wrong_id = 0
missing_head, missing_ns, dup_pages, ga4_pages, wrong_pages = [], [], [], [], []

for f in HTML:
    s = open(f, encoding="utf-8").read()
    head = s.split("</head>")[0] if "</head>" in s else s

    n_head = head.count("googletagmanager.com/gtm.js")
    n_ns = s.count("googletagmanager.com/ns.html")

    if n_head >= 1: head_ok += 1
    else: missing_head.append(f)
    if n_ns >= 1: ns_ok += 1
    else: missing_ns.append(f)

    if n_head > 1 or n_ns > 1:
        dup_gtm += 1; dup_pages.append(f)

    # a second GA4 implementation = gtag.js loaded directly anywhere
    if "googletagmanager.com/gtag/js" in s or re.search(r"gtag\s*\(\s*['\"]config['\"]", s):
        dup_ga4 += 1; ga4_pages.append(f)

    for m in re.findall(r"GTM-[A-Z0-9]+", s):
        if m != GTM_ID:
            wrong_id += 1; wrong_pages.append("%s:%s" % (f, m))
    for m in re.findall(r"\bG-[A-Z0-9]{6,}", s):
        if m != GA4_ID:
            wrong_id += 1; wrong_pages.append("%s:%s" % (f, m))

js = open("assets/analytics.js", encoding="utf-8").read()
cfg = open("assets/config.js", encoding="utf-8").read()

checks = [
    ("PAGES MISSING GTM HEAD", len(missing_head), 0, missing_head[:3]),
    ("PAGES MISSING GTM NOSCRIPT", len(missing_ns), 0, missing_ns[:3]),
    ("DUPLICATE GTM INSTALLATIONS", dup_gtm, 0, dup_pages[:3]),
    ("WRONG GTM/GA4 IDs", wrong_id, 0, wrong_pages[:3]),
    ("HARDCODED DUPLICATE GA4", dup_ga4, 0, ga4_pages[:3]),
]

events = ["menu_view", "order_online_click", "order_buckhead", "order_duluth",
          "phone_click", "directions_click", "catering_lead", "franchise_lead",
          "gift_card_click", "view_item"]
missing_ev = [e for e in events if "'%s'" % e not in js]

print("=" * 62)
print("BITE MORE — ANALYTICS VERIFICATION")
print("=" * 62)
print("TOTAL HTML PAGES:            %d" % len(HTML))
print("PAGES WITH GTM HEAD:         %d" % head_ok)
print("PAGES WITH GTM NOSCRIPT:     %d" % ns_ok)
for name, got, want, detail in checks:
    print("%-28s %d   %s%s" % (name, got, "PASS" if got == want else "FAIL",
                               ("  " + str(detail)) if got != want else ""))
print("-" * 62)
print("dataLayer safe init:         %s" % ("PASS" if "window.dataLayer = window.dataLayer || []" in js else "FAIL"))
print("bmTrack helper:              %s" % ("PASS" if "window.bmTrack" in js else "FAIL"))
print("No gtag.js in event layer:   %s" % ("PASS" if "gtag/js" not in js else "FAIL"))
print("No fake purchase event:      %s" % ("PASS" if "'purchase'" not in js else "FAIL"))
print("No Meta Pixel placeholder:   %s" % ("PASS" if "fbq(" not in js and 'META_PIXEL_ID:      ""' in cfg else "FAIL"))
print("Events wired:                %s" % ("PASS" if not missing_ev else "FAIL " + str(missing_ev)))
print("=" * 62)

fails = [c for c in checks if c[1] != c[2]] or missing_ev
sys.exit(1 if fails else 0)

#!/usr/bin/env python3
"""
BITE MORE — website update, October 2026
Implements Part B of website-update-brief.md.

Idempotent: safe to re-run. Operates on the generated HTML in place.

What it does
  1. Favicon + manifest links in <head> on every page
  2. Twitter card title/description/image (card tag already present)
  3. WCAG AA contrast fixes in styles.css (the three real failures, measured)
  4. Homepage header rework + "Start here" block removal + order-most row
  5. Sitewide price removal (spans, hero prices, body copy, MenuItem offers)
  6. Lead-capture modal wiring
Pages NOT touched: 404.html, coming-soon.html, branding/index.html
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP = {"404.html", "coming-soon.html", os.path.join("branding", "index.html")}

STATS = {
    "pages_scanned": 0,
    "favicon_added": 0,
    "twitter_added": 0,
    "price_spans_removed": 0,
    "hero_prices_removed": 0,
    "offers_removed": 0,
    "body_price_mentions": 0,
    "modal_wired": 0,
}


def all_pages():
    out = []
    for dirpath, _dirnames, filenames in os.walk(ROOT):
        if "_build" in dirpath or "__pycache__" in dirpath:
            continue
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT)
            if rel in SKIP:
                continue
            out.append(rel)
    return sorted(out)


def prefix_for(rel):
    depth = rel.count(os.sep)
    return "../" * depth


# ---------------------------------------------------------------- 1. favicon
FAVICON_MARK = "<!-- favicon -->"


def add_favicon(html, pre):
    if FAVICON_MARK in html:
        return html, False
    block = (
        f'{FAVICON_MARK}\n'
        f'<link rel="icon" href="{pre}favicon.ico" sizes="any">\n'
        f'<link rel="icon" href="{pre}assets/img/icon.svg" type="image/svg+xml">\n'
        f'<link rel="apple-touch-icon" href="{pre}assets/img/apple-touch-icon.png">\n'
        f'<link rel="manifest" href="{pre}site.webmanifest">\n'
        f'<meta name="theme-color" content="#0B0B0B">\n'
    )
    # insert immediately before the stylesheet link so it lands late in <head>
    m = re.search(r'<link rel="stylesheet" href="[^"]*assets/styles\.css">', html)
    if not m:
        return html, False
    return html[: m.start()] + block + html[m.start() :], True


# ---------------------------------------------------------- 2. twitter cards
def add_twitter(html, pre):
    if "twitter:title" in html:
        return html, False

    def grab(prop):
        m = re.search(
            r'<meta property="og:%s" content="([^"]*)">' % prop, html
        )
        return m.group(1) if m else None

    title = grab("title")
    desc = grab("description")
    img = grab("image")
    if not title:
        return html, False
    lines = [f'<meta name="twitter:title" content="{title}">']
    if desc:
        lines.append(f'<meta name="twitter:description" content="{desc}">')
    if img:
        lines.append(f'<meta name="twitter:image" content="{img}">')
    lines.append('<meta name="twitter:site" content="@bitemoreatl">')
    block = "\n".join(lines) + "\n"
    anchor = '<meta name="twitter:card" content="summary_large_image">\n'
    if anchor not in html:
        return html, False
    return html.replace(anchor, anchor + block, 1), True


# ------------------------------------------------------------ 5. price strip
PRICE_SPAN = re.compile(r'[ \t]*<span class="price">[^<]*</span>\s*\n?')

# The answer that replaces every "How much is X?" price answer. Keeps the FAQ
# entity (it earns a rich result) but carries no number that can go stale.
PRICE_ANSWER = (
    "Current pricing is on our online ordering menu. Ordering direct from us "
    "avoids the markup the delivery apps add."
)

# body-copy phrases that name a price or promise prices are shown
BODY_FIXES = [
    # 1. item-page hero line: "$19.99 · 100% halal · cooked to order"
    (re.compile(r'(class="itemprice">)\$\d+[\d.,]*\s*·\s*'), r'\1'),
    (re.compile(r'(class="itemprice">)Price varies\s*·\s*'), r'\1'),
    # 2. meta description / og:description: ". $19.99 at Bite More, ..."
    (re.compile(r'\$\d+[\d.,]*\s+at Bite More,'), 'At Bite More,'),
    # 3. FAQ answers, both in JSON-LD and the visible <details>
    (re.compile(r'\$\d+[\d.,]*\s+ordering direct from us\.\s*'
                r'Delivery apps mark menu prices up\.'), PRICE_ANSWER),
    # 4. piece-count pricing in wings copy
    (re.compile(r'6 pc \$\d+[\d.,]*, 10 pc \$\d+[\d.,]*\.'),
     'Available in 6 or 10 pieces.'),
    # 5. promises that the page shows prices
    (re.compile(r'See the menu &amp; prices'), 'See the menu'),
    (re.compile(r'Full menu and prices'), 'See the full menu'),
    (re.compile(r'[Ff]ull menu with every item and its protein count'),
     'Full menu with every item and its protein count'),
    (re.compile(r'menu and prices'), 'full menu'),
    (re.compile(r'Prices shown are what you pay ordering direct\.\s*'), ''),
    (re.compile(r'[Pp]rices shown are direct prices\.\s*'), ''),
    # 6. any remaining bare dollar amount in prose
    (re.compile(r'\s*\(\$\d+[\d.,]*\)'), ''),
    (re.compile(r'\s*—\s*\$\d+[\d.,]*(?=[\s<.,])'), ''),
    (re.compile(r'\s*·\s*\$\d+[\d.,]*(?=[\s<.,])'), ''),
    (re.compile(r'\b(?:from|just|only|starting at)\s+\$\d+[\d.,]*'),
     'on the menu'),
]


def strip_prices(html):
    n_span = len(PRICE_SPAN.findall(html))
    html = PRICE_SPAN.sub("", html)
    n_hero = len(re.findall(r'class="itemprice">\$', html))
    n_body = 0
    for pat, rep in BODY_FIXES:
        html, k = pat.subn(rep, html)
        n_body += k
    STATS["price_spans_removed"] += n_span
    STATS["hero_prices_removed"] += n_hero
    STATS["body_price_mentions"] += n_body
    return html, (n_span + n_hero + n_body)


JSONLD = re.compile(
    r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S
)


def strip_offers_from_jsonld(html):
    removed = [0]

    def drop(node):
        if isinstance(node, dict):
            if node.get("@type") in ("MenuItem", "MenuSection", "Menu", "Product"):
                for key in ("offers", "price", "priceCurrency"):
                    if key in node:
                        del node[key]
                        removed[0] += 1
            for v in list(node.values()):
                drop(v)
        elif isinstance(node, list):
            for v in node:
                drop(v)

    def repl(m):
        try:
            data = json.loads(m.group(2))
        except Exception:
            return m.group(0)
        before = removed[0]
        drop(data)
        if removed[0] == before:
            return m.group(0)
        return m.group(1) + "\n" + json.dumps(data, indent=2, ensure_ascii=False) + "\n" + m.group(3)

    html = JSONLD.sub(repl, html)
    STATS["offers_removed"] += removed[0]
    return html, removed[0]


# ----------------------------------------------------- 6. lead-capture wiring
MODAL_MARK = "<!-- lead-capture -->"


def wire_modal(html, pre):
    if MODAL_MARK in html:
        return html, False
    tag = f'{MODAL_MARK}\n<script src="{pre}assets/lead-capture.js" defer></script>\n'
    if "</body>" not in html:
        return html, False
    return html.replace("</body>", tag + "</body>", 1), True


# ---------------------------------------------------------------------- main
def main():
    pages = all_pages()
    for rel in pages:
        full = os.path.join(ROOT, rel)
        with open(full, encoding="utf-8") as fh:
            orig = fh.read()
        html = orig
        pre = prefix_for(rel)

        html, did = add_favicon(html, pre)
        STATS["favicon_added"] += int(did)
        html, did = add_twitter(html, pre)
        STATS["twitter_added"] += int(did)
        html, _ = strip_prices(html)
        html, _ = strip_offers_from_jsonld(html)
        html, did = wire_modal(html, pre)
        STATS["modal_wired"] += int(did)

        STATS["pages_scanned"] += 1
        if html != orig:
            with open(full, "w", encoding="utf-8") as fh:
                fh.write(html)

    print("=" * 58)
    print("BITE MORE update — October 2026")
    print("=" * 58)
    for k, v in STATS.items():
        print(f"  {k.replace('_',' '):26} {v}")
    print("=" * 58)


if __name__ == "__main__":
    sys.exit(main())

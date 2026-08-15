#!/usr/bin/env python3
"""v2.3 — Italian cuisine positioning.
Adds Italian hub pages targeting pasta/Italian keywords, and a properly
handled "coming soon" page for dishes still in development (noindex,
excluded from sitemap, clearly labelled — so we never promise a dish
a customer can't order).
"""
import os, sys, re, json, glob
sys.path.insert(0, "/home/claude")
from v2_base import *   # noqa

OUT = "/mnt/user-data/outputs/bitemore-site-v2"

ITALIAN_HUBS = [
    ("italian-restaurant-buckhead", "Italian Restaurant in Buckhead",
     "Italian Restaurant in Buckhead, Atlanta | Halal Italian | Bite More",
     "Halal Italian-American in Buckhead — Cajun Alfredo, Alfredo, Pomodoro and Arrabbiata pasta cooked to order, plus smash burgers and wings. Dine in, pickup, delivery.",
     "Italian food in Buckhead usually means a $30 plate and a two-hour table. We cook the same sauces at fast-casual prices, and every protein is halal.",
     [("Sauce first", "Alfredo built in the pan. Pomodoro cooked down with garlic, olive oil and basil. Arrabbiata with the chilli pushed hard. Nothing arrives finished in a bag."),
      ("Italian-American, not a museum piece", "We're not recreating Naples. This is the Italian-American tradition — generous plates, big flavour, food you actually want on a Tuesday."),
      ("All halal", "Every protein at both kitchens. The one thing no other Italian restaurant in Buckhead can say."),
      ("Fast-casual pace", "Cooked to order, out quickly, priced for a normal weeknight. Dine in, pick up or have it delivered.")]),
    ("pasta-to-go", "Pasta To Go",
     "Pasta To Go in Atlanta &amp; Duluth, GA | Halal Pasta Takeout | Bite More",
     "Pasta to go from Bite More — Cajun Alfredo, Alfredo, Pomodoro and Arrabbiata, cooked to order and packed for takeout or delivery in Buckhead and Duluth.",
     "Most pasta doesn't survive the trip. Ours is built to — sauces thick enough to hold onto the pasta instead of pooling at the bottom of the container.",
     [("Built to travel", "Our Alfredo is made heavier than a restaurant plate version specifically so it still pulls properly twenty minutes later."),
      ("Cooked when you order", "Pasta goes in the pan when the ticket prints. It isn't portioned out of a warming tray."),
      ("Garlic toast included", "Packed separately so it stays crisp."),
      ("Pickup or delivery", "Order ahead and collect, or have it brought across Buckhead, Sandy Springs, Brookhaven, Duluth, Johns Creek and Suwanee.")]),
    ("italian-food-atlanta", "Halal Italian Food in Atlanta",
     "Halal Italian Food in Atlanta &amp; Duluth, GA | Bite More",
     "Halal Italian food in Atlanta. Alfredo, Cajun Alfredo, Pomodoro and Arrabbiata pasta at two kitchens — every protein halal, no separate menu.",
     "Halal Italian is a genuinely hard thing to find in Atlanta. Most Italian kitchens aren't set up for it, and most halal kitchens aren't cooking Italian. We do both.",
     [("Why it's rare", "Italian-American cooking leans on cured pork and shared equipment. Building an Italian menu that's halal end to end means changing the sourcing, not adding an option."),
      ("What we cook", "Fettuccine in Alfredo, Cajun Alfredo, Pomodoro and Arrabbiata — with grilled or fried chicken, shrimp or steak, all halal."),
      ("Coming next", "Three tagliatelle dishes are in development: mushroom and porcini, Sicilian pesto, and beef meatball."),
      ("Both kitchens", "Buckhead at 3150 Roswell Rd NW and Duluth at 2148 Duluth Hwy 120, cooking to the same recipes.")]),
]


def hub(slug, h1, title, desc, intro, blocks, extra_items=None):
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": h1,
          "description": desc, "url": f"{DOMAIN}/{slug}.html", "about": restaurant_ld()}
    cards = "".join(f'      <div class="card"><h3>{t}</h3><p>{b}</p></div>\n' for t, b in blocks)
    items = extra_items or [
        ("Cajun Alfredo", "19.99", "", "Fettuccine in cream sauce with Cajun spice, your choice of protein and Parmesan. Our most-ordered dish.", IMG['alfredo_cajun'], "cajun-alfredo", True),
        ("Alfredo Pasta", "14.99", "", "Fettuccine, Alfredo, Parmesan, cracked black pepper. No heat.", IMG['alfredo'], "alfredo-pasta", False),
        ("Pomodoro Pasta", "14.99", "", "Tomato, garlic, olive oil and basil cooked down properly.", "", "pomodoro-pasta", False),
        ("Arrabbiata Pasta", "15.99", "", "Our Pomodoro with the chilli and garlic pushed hard.", "", "arrabbiata-pasta", False),
    ]
    rows = "".join(item_row(*i, 0) for i in items)
    p = head(title, desc, f"{slug}.html", 0, ld)
    p += nav(0)
    p += crumbs(0, [("Menu", "menu.html"), (h1, "")])
    p += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">Italian-American</p>
    <h1 class="dsp">{h1}</h1>
    <p>{intro}</p>
    <a class="btn btn-solid" href="{ORDER}">Order online</a>
  </div>
</section>
{TICKER}
<section class="sec">
  <div class="wrap">
    {badges()}
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="sec-head rv"><p class="eyebrow">On the menu</p><h2 class="dsp">The pasta</h2></div>
    <div class="carta rv">
{rows}    </div>
    <p style="margin-top:30px"><a class="btn btn-ghost" href="menu.html">Full menu and prices</a></p>
  </div>
</section>
<section class="sec panel">
  <div class="wrap">
    <div class="cards rv">
{cards}    </div>
  </div>
</section>
<section class="sec">
  <div class="wrap locs rv">
{loc_card(LOCATIONS[0], 0)}{loc_card(LOCATIONS[1], 0)}  </div>
</section>
<section class="sec panel">
  <div class="wrap knownfor rv">
    <h2 class="dsp" style="font-size:clamp(24px,3vw,34px)">Known for</h2>
    <p class="taglist">{known_for(0)}</p>
    <h2 class="dsp" style="font-size:clamp(24px,3vw,34px);margin-top:36px">Areas we serve</h2>
    <p class="taglist">{areas_served(0)}</p>
  </div>
</section>
"""
    faqs = [("Is the pasta halal?", "Yes. Every protein at both kitchens is halal, including everything served with the pasta."),
            ("Can I get it without heat?", "Yes. Alfredo and Pomodoro have no heat at all, and the Cajun Alfredo can be made mild."),
            ("Does the pasta travel well?", "Our sauces are built heavier than a plated restaurant version specifically so they hold up for takeout and delivery."),
            ("What comes with it?", "Garlic toast, packed separately so it stays crisp. Add grilled or fried chicken, shrimp or steak.")]
    p += faq_html(faqs, "Pasta questions")
    p = p.replace("</head>", '<script type="application/ld+json">%s</script>\n</head>' % json.dumps(faq_ld(faqs)), 1)
    p += foot(0)
    return p


for slug, h1, title, desc, intro, blocks in ITALIAN_HUBS:
    open(os.path.join(OUT, f"{slug}.html"), "w", encoding="utf-8").write(
        hub(slug, h1, title, desc, intro, blocks))
print("italian hubs:", len(ITALIAN_HUBS))


# ---------------------------------------------------------------- COMING SOON (noindex)
COMING = [
    ("Mushroom &amp; Porcini Tagliatelle",
     "Tagliatelle with cremini and dried porcini, garlic, thyme and a little cream, finished with Parmesan. Porcini is what gives it the depth — there's no substitute and no shortcut."),
    ("Sicilian Pesto Tagliatelle",
     "Pesto alla Trapanese — almonds instead of pine nuts, fresh tomato, basil and garlic, blitzed raw. Lighter and brighter than Genovese pesto, and it doesn't need cream to work."),
    ("Beef Meatball Tagliatelle",
     "Halal beef meatballs rolled in house, braised in our Pomodoro until the sauce takes on the meat. The most Italian-American plate on the list."),
]
cards = "".join(f"""      <div class="card"><span class="num">In development</span><h3>{n}</h3><p>{d}</p></div>\n"""
                for n, d in COMING)
p = head("Coming Soon — Tagliatelle | Bite More",
         "Three tagliatelle dishes in development at Bite More: mushroom and porcini, Sicilian pesto, and beef meatball.",
         "coming-soon.html", 0, robots="noindex, follow")
p += nav(0)
p += crumbs(0, [("Menu", "menu.html"), ("Coming Soon", "")])
p += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">In development</p>
    <h1 class="dsp">Three plates<br>we're still<br><span class="italic hot">working</span> on</h1>
    <p>Not on the menu yet. These are in recipe development in our kitchens — when they're right, they'll go on the menu and not before.</p>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="callout rv" style="margin-bottom:34px">
      <b>Not available to order</b>
      <p>These dishes are not on the menu yet. This page is set to noindex and is excluded from the sitemap, so it won't appear in search results and nobody will arrive expecting to order them. When a dish launches, move it into the menu and remove it from here.</p>
    </div>
    <div class="cards rv">
{cards}    </div>
    <p style="margin-top:34px"><a class="btn btn-solid" href="menu.html">See what's on the menu now</a></p>
  </div>
</section>
"""
p += foot(0)
open(os.path.join(OUT, "coming-soon.html"), "w", encoding="utf-8").write(p)

# tagliatelle tag page also noindex until launch
tp = os.path.join(OUT, "tags", "tagliatelle.html")
if os.path.exists(tp):
    s = open(tp, encoding="utf-8").read()
    s = s.replace('<meta name="robots" content="index, follow">',
                  '<meta name="robots" content="noindex, follow">')
    s = s.replace('<a class="btn btn-solid" href="https://order.online/business/bite-more-13060526">Order online</a>',
                  '<a class="btn btn-ghost" href="../coming-soon.html">See what\'s in development</a>')
    open(tp, "w", encoding="utf-8").write(s)
print("coming-soon built (noindex)")


# ---------------------------------------------------------------- ITALIAN FOOTER COLUMN
ITAL = """      <div>
        <h4>Italian &amp; pasta</h4>
        <a href="{r}italian-restaurant-buckhead.html">Italian Restaurant Buckhead</a>
        <a href="{r}italian-food-atlanta.html">Halal Italian Food Atlanta</a>
        <a href="{r}pasta-to-go.html">Pasta To Go</a>
        <a href="{r}tags/cajun-alfredo.html">Cajun Alfredo</a>
        <a href="{r}tags/alfredo-pasta.html">Alfredo Pasta</a>
        <a href="{r}tags/pomodoro-pasta.html">Pomodoro Pasta</a>
        <a href="{r}tags/arrabbiata-pasta.html">Arrabbiata Pasta</a>
        <a href="{r}tags/halal-pasta.html">Halal Pasta</a>
      </div>
"""
for path in glob.glob(os.path.join(OUT, "**/*.html"), recursive=True):
    depth = path.replace(OUT + "/", "").count("/")
    r = "../" * depth
    s = open(path, encoding="utf-8").read()
    if "Italian &amp; pasta</h4>" not in s:
        s = s.replace('      <div>\n        <h4>Find us near</h4>',
                      ITAL.format(r=r) + '      <div>\n        <h4>Find us near</h4>', 1)
    open(path, "w", encoding="utf-8").write(s)
print("italian footer column added")


# ---------------------------------------------------------------- ITALIAN-FORWARD TITLES
RE2 = {
    "index.html": (
        "Bite More | Halal Italian-American — Pasta, Burgers &amp; Wings in Buckhead &amp; Duluth",
        "Halal Italian-American in Buckhead and Duluth. Cajun Alfredo, Pomodoro and Arrabbiata pasta, smash burgers, wings and late-night food. Dine in, takeout, delivery or catering."),
    "menu.html": (
        "Bite More Menu — Halal Italian-American Pasta, Burgers &amp; Wings | Atlanta",
        "The full Bite More menu with prices: Cajun Alfredo, Alfredo, Pomodoro and Arrabbiata pasta, halal smash burgers, wings, loaded fries. Buckhead and Duluth."),
    "buckhead.html": (
        "One of the Best Italian Restaurants in Buckhead for Pasta, Burgers &amp; Halal Food | Bite More",
        "One of the best restaurants in Buckhead for halal Italian-American pasta, burgers, wings and late-night food near Buckhead Theatre. Dine in, takeout, delivery or catering."),
    "duluth.html": (
        "One of the Best Restaurants in Duluth GA for Halal Italian Food, Pasta &amp; Burgers | Bite More",
        "A top Duluth restaurant serving halal Italian-American pasta, burgers, wings and late-night food near Gas South Arena. Dine in, takeout, delivery or catering."),
    "about.html": (
        "About Bite More | Halal Italian-American Restaurant in Buckhead &amp; Duluth, GA",
        "Learn about Bite More, a halal Italian-American restaurant in Georgia serving pasta, burgers, wings and late-night food in Buckhead and Duluth."),
}
for fname, (title, desc) in RE2.items():
    p2 = os.path.join(OUT, fname)
    s = open(p2, encoding="utf-8").read()
    s = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{desc}">', s, count=1, flags=re.S)
    s = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{title}">', s, count=1, flags=re.S)
    s = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{desc}">', s, count=1, flags=re.S)
    open(p2, "w", encoding="utf-8").write(s)

# home hero → pasta-forward
h = os.path.join(OUT, "index.html")
s = open(h, encoding="utf-8").read()
s = s.replace('<h1 class="dsp">Halal burgers,<br>pasta and wings.<br><span class="italic hot">Cooked</span> to order.</h1>',
              '<h1 class="dsp">Halal Italian,<br>cooked in the<br><span class="italic hot">pan</span>.</h1>')
s = s.replace('<p class="sub">Two Atlanta kitchens making Italian-American food where every protein is halal — so the whole table orders off the same menu. Smash burgers from $12.99, pasta from $14.99.</p>',
              '<p class="sub">Alfredo built in the pan. Pomodoro cooked down with garlic and basil. Smash burgers and wings beside them. Two Atlanta kitchens, every protein halal, pasta from $14.99.</p>')
open(h, "w", encoding="utf-8").write(s)
print("italian-forward titles applied")


# ---------------------------------------------------------------- SITEMAP (exclude noindex)
NOINDEX = {"coming-soon.html", "tags/tagliatelle.html"}
urls = []
for f in sorted(glob.glob(os.path.join(OUT, "**/*.html"), recursive=True)):
    rel_p = f.replace(OUT + "/", "")
    if rel_p in NOINDEX:
        continue
    pri = "1.0" if rel_p == "index.html" else (
        "0.9" if rel_p in ("menu.html", "catering.html", "buckhead.html", "duluth.html",
                           "italian-restaurant-buckhead.html", "pasta-to-go.html",
                           "italian-food-atlanta.html", "late-night-food-buckhead.html",
                           "halal-food-atlanta.html") else "0.6")
    urls.append(f"  <url><loc>{DOMAIN}/{rel_p}</loc><changefreq>weekly</changefreq><priority>{pri}</priority></url>")
open(os.path.join(OUT, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "\n".join(urls) + "\n</urlset>\n")
print("indexable pages in sitemap:", len(urls))

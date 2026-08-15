#!/usr/bin/env python3
"""v2.4 — a page per menu item + the remaining winnable keyword hubs."""
import os, sys, re, json, glob
sys.path.insert(0, "/home/claude")
from v2_base import *   # noqa

OUT = "/mnt/user-data/outputs/bitemore-site-v2"
os.makedirs(os.path.join(OUT, "menu"), exist_ok=True)


def slugify(n):
    s = n.lower().replace("&amp;", "and").replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


# ---------------------------------------------------------------- per-item pages
ITEM_SEO = {
    # slug: (title suffix keyword, meta angle)
    "oklahoma-onion-smash-burger": "Our highest-rated burger. Double smash patties with onions caramelised into the crust.",
    "signature-smash-burger": "Two halal beef patties, pepper jack, Smash Sauce, potato bun.",
    "classic-smash-burger": "Two patties, American cheese, Smash Sauce. Nothing in the way.",
    "cajun-alfredo": "Our most-ordered dish. Cream sauce, Cajun spice, choice of protein, garlic toast.",
    "alfredo-pasta": "Fettuccine, Alfredo, Parmesan, cracked pepper. No heat.",
    "pomodoro-pasta": "Tomato, garlic, olive oil and basil, cooked down properly.",
    "arrabbiata-pasta": "Pomodoro with the chilli and garlic pushed hard.",
    "mac-attack-fries": "Fries under mac and cheese and crispy fried chicken with chipotle mayo.",
    "10-pc-chicken-wings": "Ten halal wings, oven-baked then lightly fried, tossed to order. ~60g protein.",
    "6-pc-chicken-wings": "Six halal wings, oven-baked then lightly fried, tossed to order.",
}

all_items = [(sec, it) for sec, note, items in MENU for it in items]
item_slugs = {it[0]: slugify(it[0]) for sec, it in all_items}

built = 0
for sec_name, (name, price, macro, desc, img, tag, hero) in all_items:
    slug = item_slugs[name]
    siblings = [i for s, i in all_items if s == sec_name and i[0] != name][:3]
    rows = "".join(item_row(*i, 1) for i in siblings)
    price_line = f"${price}" if price != "—" else "Price varies"
    macro_line = f" · {macro}" if macro else ""
    title = f"{name} in Buckhead &amp; Duluth, GA | Halal | Bite More"
    meta = f"{ITEM_SEO.get(slug, desc)[:110]} {price_line} at Bite More, Buckhead and Duluth. 100% halal, cooked to order."
    ld = {"@context": "https://schema.org", "@type": "MenuItem", "name": name,
          "description": desc, "url": f"{DOMAIN}/menu/{slug}.html",
          "suitableForDiet": "https://schema.org/HalalDiet"}
    if price != "—":
        ld["offers"] = {"@type": "Offer", "price": price, "priceCurrency": "USD",
                        "availability": "https://schema.org/InStock"}
    faqs = [(f"Is the {name} halal?", "Yes. Every protein at both Bite More kitchens is 100% halal."),
            (f"How much is the {name}?", f"{price_line} ordering direct from us. Delivery apps mark menu prices up."),
            (f"Where can I get the {name}?", "Both locations — 3150 Roswell Rd NW in Buckhead and 2148 Duluth Hwy 120 in Duluth."),
            ("Can I order it for delivery?", "Yes. Pickup and delivery across metro Atlanta, or dine in at either kitchen.")]
    p = head(title, meta, f"menu/{slug}.html", 1, ld)
    p += nav(1)
    p += crumbs(1, [("Menu", "menu.html"), (name, "")])
    hero_img = f'<div class="hero-art"><img src="{img}" alt="{name}" width="600" height="470" style="aspect-ratio:4/3"></div>' if img else ""
    p += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">{sec_name}</p>
    <h1 class="dsp">{name}</h1>
    <p>{desc}</p>
    <p class="itemprice">{price_line}{macro_line} · 100% halal · cooked to order</p>
    <a class="btn btn-solid" href="{ORDER}">Order online</a>
    <a class="btn btn-ghost" href="../menu.html" style="margin-left:10px">Full menu</a>
  </div>
</section>
{TICKER}
<section class="sec">
  <div class="wrap">
    {'<div class="split rv">' + hero_img + '<div>' if img else '<div class="rv">'}
    {badges()}
    <p class="muted" style="margin-top:22px;max-width:52ch;color:var(--muted)">Served at both kitchens — Buckhead and Duluth cook to the same build sheets, so it lands the same either way.</p>
    {'</div></div>' if img else '</div>'}
  </div>
</section>
<section class="sec panel">
  <div class="wrap">
    <div class="sec-head rv"><p class="eyebrow">Also in {sec_name}</p><h2 class="dsp">Try these too</h2></div>
    <div class="carta rv">
{rows}    </div>
    <p style="margin-top:28px"><a class="btn btn-ghost" href="../menu.html">See the full menu</a></p>
  </div>
</section>
<section class="sec">
  <div class="wrap locs rv">
{loc_card(LOCATIONS[0], 1)}{loc_card(LOCATIONS[1], 1)}  </div>
</section>
<section class="sec panel">
  <div class="wrap knownfor rv">
    <h2 class="dsp" style="font-size:clamp(24px,3vw,34px)">Known for</h2>
    <p class="taglist">{known_for(1)}</p>
    <h2 class="dsp" style="font-size:clamp(24px,3vw,34px);margin-top:36px">Areas we serve</h2>
    <p class="taglist">{areas_served(1)}</p>
  </div>
</section>
"""
    p += faq_html(faqs, f"About the {name}")
    p = p.replace("</head>", '<script type="application/ld+json">%s</script>\n</head>' % json.dumps(faq_ld(faqs)), 1)
    p += foot(1)
    open(os.path.join(OUT, "menu", f"{slug}.html"), "w", encoding="utf-8").write(p)
    built += 1
print("item pages:", built)


# ---------------------------------------------------------------- link item pages from the menu
mp = os.path.join(OUT, "menu.html")
s = open(mp, encoding="utf-8").read()
for name, slug in item_slugs.items():
    s = s.replace(f"<h3>{name} ", f'<h3><a href="menu/{slug}.html" class="itemlink">{name}</a> ', 1)
    s = s.replace(f"<h3>{name}</h3>", f'<h3><a href="menu/{slug}.html" class="itemlink">{name}</a></h3>', 1)
open(mp, "w", encoding="utf-8").write(s)


# ---------------------------------------------------------------- remaining keyword hubs
HUBS2 = [
    ("wings-to-go", "Wings To Go", "Wings To Go Near Me | Halal Wings Takeout in Atlanta | Bite More",
     "Wings to go from Bite More — halal wings oven-baked then lightly fried, tossed to order. 6 pc $11.99, 10 pc $15.99. Buckhead and Duluth pickup or delivery.",
     "Wings that travel badly are the whole problem with wing takeout. Ours are baked first, then fried briefly, so the skin holds up on the drive instead of going soft in the box.",
     [("Baked, then fried", "Baking cooks them through without drying them out. The fry is short and only there for the crunch."),
      ("Tossed when you order", "Sauce goes on at the end, not in advance. That's why they don't arrive soggy."),
      ("Six or ten", "$11.99 for six, $15.99 for ten, or six with fries for $12."),
      ("Order ahead", "Put it in before you leave and collect it, or have it delivered across metro Atlanta.")],
     [("10 pc Chicken Wings", "15.99", "~60g protein", "Ten wings, tossed to order.", IMG['wings'], "chicken-wings", True),
      ("6 pc Chicken Wings", "11.99", "~36g protein", "Six wings, tossed to order.", "", "chicken-wings", False),
      ("6 pc Wings with Fries", "12.00", "", "Six wings and a side of house fries.", "", "chicken-wings", False)]),
    ("best-wings-buckhead", "Wings in Buckhead", "Best Wings in Buckhead, Atlanta | Halal Wings | Bite More",
     "Halal wings in Buckhead — oven-baked then lightly fried, tossed to order in the flavour you pick. 6 pc $11.99, 10 pc $15.99. Open till midnight Thu–Sun.",
     "Most Buckhead wings are dropped straight in the fryer. We bake first so they cook through, then fry briefly for the crunch, then toss them when you order.",
     [("Flavours", "Mild, hot, lemon pepper, garlic parmesan and BBQ, tossed at the pass."),
      ("All halal", "Every wing at both kitchens. No separate order, no questions."),
      ("Late", "Kitchen runs till midnight Thursday through Sunday — two minutes from the Buckhead Theatre."),
      ("Protein", "Ten wings runs about 60g. The numbers are on the menu because people ask.")],
     [("10 pc Chicken Wings", "15.99", "~60g protein", "Ten wings, tossed to order.", IMG['wings'], "chicken-wings", True),
      ("6 pc Chicken Wings", "11.99", "~36g protein", "Six wings, tossed to order.", "", "chicken-wings", False)]),
    ("best-restaurants-buckhead", "Restaurants in Buckhead", "One of the Best Restaurants in Buckhead, Atlanta | Bite More",
     "Looking for the best restaurants in Buckhead? Bite More serves halal Italian-American pasta, smash burgers and wings on Roswell Rd. Dine in, takeout, delivery, catering.",
     "Buckhead has no shortage of restaurants. It has very few where the whole table can order off one menu regardless of what they eat.",
     [("What we cook", "Halal Italian-American — Cajun Alfredo, Pomodoro and Arrabbiata pasta, smash burgers, wings and loaded fries."),
      ("Fast-casual, not fast food", "Cooked to order at fast-casual prices. No two-hour table and no $30 plate."),
      ("Where we are", "3150 Roswell Rd NW, Suite A1 — minutes from Lenox Square and two from the Buckhead Theatre."),
      ("Open late", "Till midnight Thursday through Sunday, which most of the neighbourhood isn't.")],
     None),
    ("best-restaurants-duluth", "Restaurants in Duluth GA", "One of the Best Restaurants in Duluth, GA | Halal Food | Bite More",
     "Looking for the best restaurants in Duluth GA? Bite More serves halal burgers, wings and Italian-American pasta on Duluth Hwy 120, minutes from Gas South Arena.",
     "Duluth is full of good food and short on places where a mixed group can all eat the same thing. Every protein we serve is halal, so that problem goes away.",
     [("What we cook", "Halal Italian-American — pasta, smash burgers, wings, loaded fries and slow-cooked birria."),
      ("Near the arena", "Minutes from Gas South Arena and Sugarloaf Mills. Order ahead before an event."),
      ("Office lunch", "We deliver and cater to the Duluth Hwy 120 and Peachtree Industrial office parks."),
      ("Where we are", "2148 Duluth Hwy 120, Suite 117, Duluth, GA 30097.")],
     None),
    ("halal-food-duluth", "Halal Food in Duluth GA", "Halal Food in Duluth, GA | Halal Restaurant | Bite More",
     "Halal food in Duluth GA — 100% halal burgers, wings, pasta and loaded fries at Bite More on Duluth Hwy 120. Every protein halal, no separate menu.",
     "Our Duluth kitchen is fully halal. Not a halal option on a mixed menu — every protein we buy, for every dish, every day.",
     [("Fully halal", "There is no non-halal menu, so there is nothing to ask about and nothing to avoid."),
      ("What we cook", "Smash burgers, wings, Cajun Alfredo and Pomodoro pasta, loaded fries and birria."),
      ("Serving Gwinnett", "Duluth, Johns Creek, Suwanee, Berkeley Lake, Norcross, Peachtree Corners and Sugar Hill."),
      ("Halal catering", "Trays for 20 to 200 for community events, offices and weddings across Gwinnett.")],
     None),
    ("burgers-duluth", "Burgers in Duluth GA", "Best Burgers in Duluth, GA | Halal Smash Burgers | Bite More",
     "Halal smash burgers in Duluth GA from $12.99. Two patties smashed on the flat top, Smash Sauce, potato bun. Dine in, pickup or delivery on Duluth Hwy 120.",
     "Thin patties smashed hard on a hot flat top give you lace edges and a crust. Thick patties don't. That's the whole argument for a smash burger.",
     [("Halal beef", "Every patty, no exceptions, at both kitchens."),
      ("The Oklahoma", "Onions pressed into the patty on the flat top so they caramelise into the crust. Our highest-rated dish."),
      ("From $12.99", "Classic Smash $12.99, Signature $13.99, Oklahoma Onion $14.99."),
      ("Where", "2148 Duluth Hwy 120, Suite 117 — minutes from Gas South Arena.")],
     [("Oklahoma Onion Smash Burger", "14.99", "~38g protein", "Onions pressed into the crust, American cheese, Smash Sauce.", IMG['oklahoma'], "oklahoma-onion-smash", True),
      ("Signature Smash Burger", "13.99", "~38g protein", "Two patties, pepper jack, lettuce, tomato, pickles, Smash Sauce.", IMG['smash'], "smash-burger", False),
      ("Classic Smash Burger", "12.99", "~30g protein", "Two patties, American cheese, Smash Sauce.", "", "smash-burger", False)]),
    ("dinner-buckhead", "Dinner in Buckhead", "Dinner in Buckhead, Atlanta | Halal Dinner Late | Bite More",
     "Dinner in Buckhead at Bite More — halal pasta, smash burgers and wings cooked to order. Dine in, takeout or delivery, open till midnight Thursday–Sunday.",
     "Dinner in Buckhead can mean a reservation and a wine list, or it can mean eating well without making an evening of it. We're the second one.",
     [("Sit down or take it home", "Dining rooms at both kitchens, or order ahead and collect."),
      ("Late kitchen", "Till midnight Thursday through Sunday — long after most of Buckhead has stopped cooking."),
      ("Pasta and burgers", "Cajun Alfredo, Pomodoro, Arrabbiata, smash burgers, wings and loaded fries."),
      ("Groups", "Ten or more, call ahead. Twenty or more, catering is the better route.")],
     None),
]

for slug, h1, title, desc, intro, blocks, items in HUBS2:
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": h1,
          "description": desc, "url": f"{DOMAIN}/{slug}.html", "about": restaurant_ld()}
    cards = "".join(f'      <div class="card"><h3>{t}</h3><p>{b}</p></div>\n' for t, b in blocks)
    default = [("Oklahoma Onion Smash Burger", "14.99", "~38g protein", "Our highest-rated dish.", IMG['oklahoma'], "oklahoma-onion-smash", True),
               ("Cajun Alfredo", "19.99", "", "Our most-ordered dish.", IMG['alfredo_cajun'], "cajun-alfredo", False),
               ("Mac Attack Fries", "19.99", "", "Named more often in our reviews than anything else.", IMG['macfries'], "loaded-fries", False)]
    rows = "".join(item_row(*i, 0) for i in (items or default))
    p = head(title, desc, f"{slug}.html", 0, ld)
    p += nav(0)
    p += crumbs(0, [(h1, "")])
    p += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">Bite More</p>
    <h1 class="dsp">{h1}</h1>
    <p>{intro}</p>
    <a class="btn btn-solid" href="{ORDER}">Order online</a>
  </div>
</section>
{TICKER}
<section class="sec">
  <div class="wrap">{badges()}</div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="sec-head rv"><p class="eyebrow">What to order</p><h2 class="dsp">Start here</h2></div>
    <div class="carta rv">
{rows}    </div>
  </div>
</section>
<section class="sec panel">
  <div class="wrap"><div class="cards rv">
{cards}  </div></div>
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
    p += foot(0)
    open(os.path.join(OUT, f"{slug}.html"), "w", encoding="utf-8").write(p)
print("keyword hubs:", len(HUBS2))


# ---------------------------------------------------------------- footer: menu items column
menu_links = "".join(
    f'        <a href="{{r}}menu/{item_slugs[n]}.html">{n}</a>\n'
    for n in ["Oklahoma Onion Smash Burger", "Cajun Alfredo", "Mac Attack Fries",
              "Alfredo Pasta", "Pomodoro Pasta", "10 pc Chicken Wings",
              "Nashville Hot Chicken Sandwich", "Birria Smash"] if n in item_slugs)
MORE = """      <div>
        <h4>Popular dishes</h4>
""" + menu_links + """      </div>
      <div>
        <h4>More</h4>
        <a href="{r}wings-to-go.html">Wings To Go</a>
        <a href="{r}best-wings-buckhead.html">Best Wings Buckhead</a>
        <a href="{r}best-restaurants-buckhead.html">Restaurants in Buckhead</a>
        <a href="{r}best-restaurants-duluth.html">Restaurants in Duluth GA</a>
        <a href="{r}halal-food-duluth.html">Halal Food Duluth</a>
        <a href="{r}burgers-duluth.html">Burgers Duluth GA</a>
        <a href="{r}dinner-buckhead.html">Dinner in Buckhead</a>
      </div>
"""
for path in glob.glob(os.path.join(OUT, "**/*.html"), recursive=True):
    depth = path.replace(OUT + "/", "").count("/")
    r = "../" * depth
    s = open(path, encoding="utf-8").read()
    if "Popular dishes</h4>" not in s:
        s = s.replace('      <div>\n        <h4>Italian &amp; pasta</h4>',
                      MORE.format(r=r) + '      <div>\n        <h4>Italian &amp; pasta</h4>', 1)
    open(path, "w", encoding="utf-8").write(s)

# styles
with open(os.path.join(OUT, "assets", "styles.css"), "a") as f:
    f.write("""
.itemprice{font-family:var(--display);font-weight:900;font-variation-settings:"wdth" 112;
  font-size:20px;color:var(--orange);margin-top:20px;letter-spacing:.02em}
a.itemlink{text-decoration:none}
a.itemlink:hover{color:var(--orange);text-decoration:underline}
""")

# sitemap
NOINDEX = {"coming-soon.html", "tags/tagliatelle.html"}
urls = []
for f in sorted(glob.glob(os.path.join(OUT, "**/*.html"), recursive=True)):
    rp = f.replace(OUT + "/", "")
    if rp in NOINDEX:
        continue
    pri = "1.0" if rp == "index.html" else ("0.9" if rp in ("menu.html", "catering.html", "buckhead.html", "duluth.html") else "0.6")
    urls.append(f"  <url><loc>{DOMAIN}/{rp}</loc><changefreq>weekly</changefreq><priority>{pri}</priority></url>")
open(os.path.join(OUT, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "\n".join(urls) + "\n</urlset>\n")
print("indexable pages:", len(urls))

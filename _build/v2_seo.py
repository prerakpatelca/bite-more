#!/usr/bin/env python3
"""v2.2 — applies the Jan 2026 SEO audit findings.
Adds landmark pages, late-night and halal hub pages, lunch, events, contact.
Rewrites titles/H1/meta on core pages to the audit's keyword targets.
"""
import os, sys, re, json, glob
sys.path.insert(0, "/home/claude")
from v2_base import *   # noqa

OUT = "/mnt/user-data/outputs/bitemore-site-v2"

# ---------------------------------------------------------------- landmark pages
# (slug, H1, title, meta, SV note, which kitchen, distance line, intro, angle)
LANDMARKS = [
    ("restaurants-near-buckhead-theatre", "Restaurants Near the Buckhead Theatre",
     "Restaurants Near Buckhead Theatre | Bite More — Open Till Midnight",
     "Eating before or after a show at the Buckhead Theatre? Bite More is 2 minutes up Roswell Rd — halal burgers, pasta and wings, kitchen open till midnight Thu–Sun.",
     "buckhead",
     "About 2 minutes up Roswell Rd from the theatre — 3150 Roswell Rd NW, Suite A1.",
     "Doors at the Buckhead Theatre usually open an hour before the set, and most kitchens nearby stop cooking before the encore. Ours runs until midnight Thursday through Sunday.",
     [("Before the show", "Order ahead and pick up on the way. Smash burgers and loaded fries travel well and take about ten minutes."),
      ("After the show", "We're still cooking to order at midnight Thursday through Sunday. Nothing sitting under a lamp."),
      ("Show your ticket", "Same-day Buckhead Theatre ticket gets you 10% off the whole order, dine-in or pickup.")]),
    ("restaurants-near-gas-south-arena", "Restaurants Near Gas South Arena",
     "Restaurants Near Gas South Arena, Duluth GA | Bite More",
     "Eating near Gas South Arena in Duluth? Bite More serves halal burgers, pasta and wings minutes away. Group orders, catering and late hours Thu–Sun.",
     "duluth",
     "Minutes from Gas South Arena — 2148 Duluth Hwy 120, Suite 117, Duluth, GA.",
     "Gas South Arena packs out for concerts, games and graduations, and the food inside costs what arena food costs. We're a few minutes away.",
     [("Before an event", "Order ahead for pickup and eat before doors. Faster than the concession line and considerably better."),
      ("Groups", "Coming with a crowd? We do trays for 20 to 200 — call ahead and we'll have it ready."),
      ("After", "Kitchen runs late Thursday through Sunday, so post-event food is still cooked to order.")]),
    ("restaurants-near-piedmont-park", "Restaurants Near Piedmont Park",
     "Restaurants Near Piedmont Park, Atlanta | Bite More",
     "Looking for food near Piedmont Park? Bite More serves halal burgers, pasta, wings and loaded fries in Buckhead. Takeout, delivery and late hours.",
     "buckhead",
     "A short drive north of the park — 3150 Roswell Rd NW, Suite A1, Atlanta.",
     "Piedmont Park is where Atlanta spends its Saturdays, and food options around it thin out fast once you leave the 10th Street side.",
     [("Takeout for the park", "Burgers, wings and loaded fries pack well. Order ahead and collect on the way over."),
      ("After the park", "Dining room is open if you'd rather sit down. Kitchen goes till midnight Thursday through Sunday."),
      ("Feeding a group", "Picnic, game or gathering — we do trays for 20 to 200.")]),
    ("restaurants-near-lenox-square", "Restaurants Near Lenox Square Mall",
     "Restaurants Near Lenox Square Mall, Buckhead | Bite More",
     "Eating near Lenox Square? Bite More is minutes away in Buckhead — halal burgers, pasta, wings and loaded fries. Dine in, pickup or delivery.",
     "buckhead",
     "Minutes from Lenox Square and Phipps Plaza — 3150 Roswell Rd NW, Suite A1.",
     "Mall food courts have their place. This isn't that. We're a few minutes from Lenox on Roswell Road, cooking to order.",
     [("Shopping break", "Sit down for twenty minutes and eat something cooked properly."),
      ("Takeout", "Order ahead on the way out of the mall and skip the wait."),
      ("Late hours", "Open till midnight Thursday through Sunday, well past mall closing.")]),
    ("restaurants-near-atlanta-history-center", "Restaurants Near the Atlanta History Center",
     "Restaurants Near Atlanta History Center | Bite More Buckhead",
     "Food near the Atlanta History Center in Buckhead. Bite More serves halal burgers, pasta and wings — dine in, pickup or delivery.",
     "buckhead",
     "A few minutes from the History Center — 3150 Roswell Rd NW, Suite A1.",
     "Half a day at the History Center earns you a proper lunch. We're a few minutes away on Roswell Road.",
     [("Lunch after", "Cooked to order, fast enough that you're not waiting around."),
      ("Groups and school trips", "Trays for 20 to 200 with a day or two of notice."),
      ("Everything halal", "Every protein at both kitchens, so mixed groups order off one menu.")]),
    ("restaurants-near-sugarloaf-mills", "Restaurants Near Sugarloaf Mills",
     "Restaurants Near Sugarloaf Mills, Duluth GA | Bite More",
     "Eating near Sugarloaf Mills in Duluth? Bite More serves halal burgers, pasta, wings and loaded fries minutes away. Pickup, delivery and catering.",
     "duluth",
     "Minutes from Sugarloaf Mills — 2148 Duluth Hwy 120, Suite 117, Duluth, GA.",
     "Sugarloaf Mills is a long day of walking. The food court is what it is. We're a few minutes down the road.",
     [("Shopping break", "Cooked to order, generous plates, in and out quickly."),
      ("Family groups", "Everything is halal, so nobody's reading labels or asking questions."),
      ("Takeout home", "Order ahead and collect on the way out.")]),
]

# ---------------------------------------------------------------- hub pages
HUBS = [
    ("late-night-food-buckhead", "Late Night Food in Buckhead",
     "Late Night Food in Buckhead, Atlanta | Open Till Midnight | Bite More",
     "Late night food in Buckhead — halal burgers, wings, pasta and loaded fries cooked to order till midnight Thursday–Sunday. Takeout and delivery from Bite More.",
     "Most Buckhead kitchens stop cooking well before the neighbourhood stops going out. Ours runs until midnight Thursday through Sunday, and everything is still made when you order it.",
     [("What's still cooking", "The full menu. Smash burgers, wings, Cajun Alfredo, Mac Attack Fries — nothing gets held back after 10pm."),
      ("Cooked, not held", "Late-night food usually means whatever was made earlier. If a burger arrives in ninety seconds, it wasn't cooked for you. Ours takes the time it takes."),
      ("After a show", "Two minutes from the Buckhead Theatre. Same-day ticket gets 10% off."),
      ("Takeout and delivery", "Order ahead for pickup or have it delivered across Buckhead, Sandy Springs, Brookhaven and Midtown.")],
     "buckhead"),
    ("halal-food-atlanta", "Halal Food in Atlanta",
     "Halal Food in Atlanta &amp; Duluth, GA | Bite More — 100% Halal Kitchens",
     "100% halal food in Atlanta and Duluth. Halal burgers, pasta, wings and loaded fries at two kitchens — every protein halal, no separate menu, nothing to ask at the counter.",
     "Bite More is fully halal at both kitchens. Every protein, every day, no separate menu and no asterisks. We cook Italian-American food — pasta, smash burgers, wings — and source all of it halal.",
     [("What fully halal means", "Some restaurants offer a halal item alongside non-halal dishes cooked on shared equipment. That's a different thing. Every protein we buy is halal, so there is no 'halal option' — there's just the menu."),
      ("What we cook", "Italian-American. Cajun Alfredo and Alfredo pasta, smash burgers, wings baked then fried, loaded fries, Nashville hot chicken and slow-cooked birria."),
      ("Where to find us", "Buckhead at 3150 Roswell Rd NW, and Duluth at 2148 Duluth Hwy 120. Dine in, pickup or delivery across metro Atlanta."),
      ("Halal catering", "Trays for 20 to 200 across metro Atlanta. One menu the whole room can eat, so there's no separate tray in the corner.")],
     None),
    ("lunch-buckhead", "Lunch in Buckhead",
     "Lunch in Buckhead, Atlanta | Fast Halal Lunch | Bite More",
     "Lunch in Buckhead — halal burgers, pasta and wings cooked to order, fast enough for a lunch break. Order ahead for pickup or delivery from Bite More.",
     "Lunch in Buckhead usually means a queue, a $22 salad, or whatever you can eat at your desk. We cook to order and we're quick about it.",
     [("Order ahead", "Put the order in before you leave the office and collect it. Ten minutes, not forty."),
      ("What's fast", "Smash burgers, loaded fries and wings move quickest. Pasta takes a few minutes longer and is worth it."),
      ("Protein on the menu", "Grilled chicken runs about 55g, ten wings about 60g. The numbers are on every item because people ask."),
      ("Office lunch", "Feeding a team? Group orders and trays for 20 to 200, delivered hot and set up.")],
     "buckhead"),
]


def landmark_page(slug, h1, title, desc, loc_slug, distance, intro, blocks):
    L = [l for l in LOCATIONS if l["slug"] == loc_slug][0]
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": h1,
          "description": desc, "url": f"{DOMAIN}/{slug}.html", "about": restaurant_ld(L)}
    cards = "".join(f'      <div class="card"><h3>{t}</h3><p>{b}</p></div>\n' for t, b in blocks)
    p = head(title, desc, f"{slug}.html", 0, ld)
    p += nav(0)
    p += crumbs(0, [("Locations", "locations.html"), (h1, "")])
    p += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">Nearby</p>
    <h1 class="dsp">{h1}</h1>
    <p>{intro}</p>
    <a class="btn btn-solid" href="{ORDER}">Order online</a>
  </div>
  <div class="wrap">
    <p class="crossst">{distance}</p>
    <div class="svc"><span>Dine in</span><span>Pickup</span><span>Delivery</span><span>Catering</span><span>Free parking</span></div>
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
    <div class="cards rv">
{cards}    </div>
  </div>
</section>
<section class="sec panel">
  <div class="wrap">
    <div class="sec-head rv"><p class="eyebrow">What to order</p><h2 class="dsp">The three<br>people reorder</h2></div>
    <div class="carta rv">
{item_row("Oklahoma Onion Smash Burger", "14.99", "~38g protein", "Double smash patties with onions pressed into the crust. Our highest-rated dish.", IMG['oklahoma'], "oklahoma-onion-smash", True, 0)}{item_row("Cajun Alfredo", "19.99", "", "Cream sauce with Cajun spice, choice of protein, garlic toast on the side.", IMG['alfredo_cajun'], "cajun-alfredo", False, 0)}{item_row("Mac Attack Fries", "19.99", "", "Fries under mac and cheese and crispy fried chicken with chipotle mayo.", IMG['macfries'], "loaded-fries", False, 0)}    </div>
    <div class="locs rv" style="grid-template-columns:1fr;max-width:560px;margin-top:34px">
{loc_card(L, 0)}    </div>
  </div>
</section>
<section class="sec">
  <div class="wrap knownfor rv">
    <h2 class="dsp" style="font-size:clamp(24px,3vw,34px)">Known for</h2>
    <p class="taglist">{known_for(0)}</p>
    <h2 class="dsp" style="font-size:clamp(24px,3vw,34px);margin-top:36px">Areas we serve</h2>
    <p class="taglist">{areas_served(0, loc_slug)}</p>
  </div>
</section>
"""
    faqs = [(f"How far is Bite More from here?", distance),
            ("What time do you close?", "Closed Mondays. Tuesday and Wednesday until 10pm. Thursday through Sunday until midnight."),
            ("Is the food halal?", "Yes — every protein at both kitchens is 100% halal."),
            ("Can I order ahead for pickup?", "Yes. Order online and collect when it's ready.")]
    p += faq_html(faqs, "Getting here")
    p = p.replace("</head>", '<script type="application/ld+json">%s</script>\n</head>' % json.dumps(faq_ld(faqs)), 1)
    p += foot(0)
    return p


def hub_page(slug, h1, title, desc, intro, blocks, loc_slug):
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": h1,
          "description": desc, "url": f"{DOMAIN}/{slug}.html", "about": restaurant_ld()}
    cards = "".join(f'      <div class="card"><h3>{t}</h3><p>{b}</p></div>\n' for t, b in blocks)
    p = head(title, desc, f"{slug}.html", 0, ld)
    p += nav(0)
    p += crumbs(0, [(h1, "")])
    p += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">{'Buckhead' if loc_slug else 'Atlanta &amp; Duluth'}</p>
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
    <div class="cards rv">
{cards}    </div>
  </div>
</section>
<section class="sec panel">
  <div class="wrap">
    <div class="sec-head rv"><p class="eyebrow">What to order</p><h2 class="dsp">Start here</h2></div>
    <div class="carta rv">
{item_row("Oklahoma Onion Smash Burger", "14.99", "~38g protein", "Our highest-rated dish across the delivery platforms.", IMG['oklahoma'], "oklahoma-onion-smash", True, 0)}{item_row("Cajun Alfredo", "19.99", "", "Our most-ordered dish. Cream sauce, Cajun spice, garlic toast.", IMG['alfredo_cajun'], "cajun-alfredo", False, 0)}{item_row("10 pc Chicken Wings", "15.99", "~60g protein", "Oven-baked then lightly fried, tossed in the flavor you pick.", IMG['wings'], "chicken-wings", False, 0)}    </div>
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
    p += foot(0)
    return p


for slug, h1, title, desc, loc, dist, intro, blocks in LANDMARKS:
    open(os.path.join(OUT, f"{slug}.html"), "w", encoding="utf-8").write(
        landmark_page(slug, h1, title, desc, loc, dist, intro, blocks))

for slug, h1, title, desc, intro, blocks, loc in HUBS:
    open(os.path.join(OUT, f"{slug}.html"), "w", encoding="utf-8").write(
        hub_page(slug, h1, title, desc, intro, blocks, loc))

print("landmark + hub pages:", len(LANDMARKS) + len(HUBS))


# ---------------------------------------------------------------- CONTACT
ct_faqs = [("What are your hours?", "Closed Mondays. Tuesday and Wednesday 11am–10pm. Thursday through Sunday 11am–midnight."),
           ("Do you take large group bookings?", "For groups over ten, call ahead so we can prep. Over twenty, catering is usually the better fit."),
           ("How do I book catering?", "Send a date and headcount through the catering page and we'll come back with a menu and per-person price the same day."),
           ("Is there parking?", "Yes, both locations have lot parking on site.")]
p = head("Contact | Bite More — Buckhead &amp; Duluth, GA",
         "Contact Bite More in Buckhead or Duluth for takeout, delivery, catering and events. Directions, hours and phone numbers for both Atlanta locations.",
         "contact.html", 0, faq_ld(ct_faqs))
p += nav(0)
p += crumbs(0, [("Contact", "")])
p += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">Contact</p>
    <h1 class="dsp">Get in <span class="italic hot">touch</span></h1>
    <p>Two kitchens, two phone numbers, and a person on the end of both.</p>
  </div>
</section>
{TICKER}
<section class="sec">
  <div class="wrap">
    <div class="locs rv">
{loc_card(LOCATIONS[0], 0)}{loc_card(LOCATIONS[1], 0)}    </div>
    <div class="cards rv" style="margin-top:30px">
      <div class="card"><h3>Catering</h3><p>catering@bitemore.us — or send a headcount and date through the catering page for a same-day quote.</p></div>
      <div class="card"><h3>Franchise</h3><p>franchise@bitemore.us — territory enquiries and operator applications.</p></div>
      <div class="card"><h3>Careers</h3><p>careers@bitemore.us — kitchen and front-of-house roles at both locations.</p></div>
    </div>
    <div class="knownfor rv" style="margin-top:44px">
      <h2 class="dsp" style="font-size:clamp(24px,3vw,34px)">Neighbourhoods we serve</h2>
      <p class="taglist">{areas_served(0)}</p>
    </div>
  </div>
</section>
"""
p += faq_html(ct_faqs, "Common questions")
p += foot(0)
open(os.path.join(OUT, "contact.html"), "w", encoding="utf-8").write(p)


# ---------------------------------------------------------------- EVENTS
p = head("Events &amp; Group Dining | Bite More — Buckhead &amp; Duluth",
         "Group dining, private events and event catering at Bite More in Buckhead and Duluth. Game days, birthdays, office parties and community events.",
         "events.html", 0, restaurant_ld())
p += nav(0)
p += crumbs(0, [("Events", "")])
p += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">Events &amp; groups</p>
    <h1 class="dsp">Bring the<br>whole <span class="italic hot">room</span></h1>
    <p>Game days, birthdays, graduations, office parties and community events — at either kitchen or wherever you're holding it.</p>
    <a class="btn btn-solid" href="catering.html">Plan an event</a>
  </div>
</section>
{TICKER}
<section class="sec">
  <div class="wrap">
    <div class="cards rv">
      <div class="card"><h3>Group dining</h3><p>Ten or more? Call ahead and we'll prep so you're not waiting. Both dining rooms take groups.</p></div>
      <div class="card"><h3>Game days</h3><p>Wings, sliders and loaded fries by the tray. Order the day before and collect before kickoff.</p></div>
      <div class="card"><h3>Birthdays &amp; graduations</h3><p>Trays for 20 to 200, delivered hot and set up, or eat in with us.</p></div>
      <div class="card"><h3>Office parties</h3><p>Full buffet line with optional staff. Popular with the Duluth office parks.</p></div>
      <div class="card"><h3>Community events</h3><p>Mosque, school and neighbourhood events. Everything halal, so one menu covers the room.</p></div>
      <div class="card"><h3>Near the venues</h3><p>Minutes from the <a href="restaurants-near-buckhead-theatre.html">Buckhead Theatre</a> and <a href="restaurants-near-gas-south-arena.html">Gas South Arena</a>.</p></div>
    </div>
    <p style="margin-top:34px"><a class="btn btn-solid" href="catering.html">See catering packages</a></p>
  </div>
</section>
"""
p += foot(0)
open(os.path.join(OUT, "events.html"), "w", encoding="utf-8").write(p)


# ---------------------------------------------------------------- TITLE / META REWRITES
REWRITES = {
    "index.html": (
        "Bite More | Burgers, Wings, Halal Options &amp; Late-Night Food — Buckhead &amp; Duluth",
        "Burgers, wings, pasta, halal options &amp; late-night food in Buckhead and Duluth. Dine in, order takeout, delivery, or catering from Bite More."),
    "menu.html": (
        "Bite More Menu — Italian-American Favorites | Buckhead &amp; Duluth",
        "Explore the Bite More menu: Italian-American favorites, burgers, wings, pasta, sandwiches and late-night food in Buckhead and Duluth. Prices and protein counts included."),
    "buckhead.html": (
        "One of the Best Restaurants in Buckhead for Burgers, Wings &amp; Halal Food | Bite More",
        "One of the best restaurants in Buckhead for burgers, wings, pasta, halal options &amp; late-night food near Buckhead Theatre. Dine in, takeout, delivery or catering."),
    "duluth.html": (
        "One of the Best Restaurants in Duluth GA for Halal Food, Burgers &amp; Wings | Bite More",
        "A top Duluth restaurant serving burgers, wings, pasta, halal options &amp; late-night food near Gas South Arena. Dine in, takeout, delivery or catering."),
    "catering.html": (
        "Catering Services in Buckhead &amp; Duluth | Halal Catering | Bite More",
        "Catering services in Buckhead and Duluth for offices, parties &amp; events with halal options. Trays for 20 to 200, delivered hot and set up."),
    "franchise.html": (
        "Restaurant Franchise Opportunities in Georgia | Bite More",
        "Learn about restaurant franchise opportunities with Bite More across Georgia. Two proven Atlanta kitchens, documented systems and a trademarked brand."),
    "about.html": (
        "About Bite More | Italian-American Restaurant in Buckhead &amp; Duluth, GA",
        "Learn about Bite More, an Italian-American restaurant in Georgia serving burgers, wings, pasta, halal options and late-night food in Buckhead and Duluth."),
    "gift-cards.html": (
        "Bite More Gift Cards | Halal Burgers, Wings &amp; Pasta in Buckhead &amp; Duluth",
        "View the Bite More gift card and explore halal burgers, wings, pasta and sandwiches in Buckhead and Duluth. Perfect for quick takeout orders."),
    "careers.html": (
        "Join Our Team | Restaurant Jobs in Buckhead &amp; Duluth | Bite More",
        "Join the Bite More team in Buckhead or Duluth. Explore restaurant job opportunities in a fast-paced, halal kitchen environment."),
    "delivery.html": (
        "Food Delivery in Buckhead &amp; Duluth GA | Halal Takeout | Bite More",
        "Buckhead and Duluth food delivery from Bite More. Halal burgers, wings to go, pasta to go and late-night takeout. Order direct and skip the app markup."),
}
for fname, (title, desc) in REWRITES.items():
    p = os.path.join(OUT, fname)
    if not os.path.exists(p):
        continue
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content=".*?">',
               f'<meta name="description" content="{desc}">', s, count=1, flags=re.S)
    s = re.sub(r'<meta property="og:title" content=".*?">',
               f'<meta property="og:title" content="{title}">', s, count=1, flags=re.S)
    s = re.sub(r'<meta property="og:description" content=".*?">',
               f'<meta property="og:description" content="{desc}">', s, count=1, flags=re.S)
    open(p, "w", encoding="utf-8").write(s)
print("rewrote titles/meta on", len(REWRITES), "pages")


# ---------------------------------------------------------------- NAV + FOOTER LINKS
NEWLINKS = """        <a href="{r}late-night-food-buckhead.html">Late Night Food</a>
        <a href="{r}halal-food-atlanta.html">Halal Food Atlanta</a>
        <a href="{r}lunch-buckhead.html">Lunch in Buckhead</a>
        <a href="{r}restaurants-near-buckhead-theatre.html">Near Buckhead Theatre</a>
        <a href="{r}restaurants-near-gas-south-arena.html">Near Gas South Arena</a>
        <a href="{r}restaurants-near-piedmont-park.html">Near Piedmont Park</a>
        <a href="{r}restaurants-near-lenox-square.html">Near Lenox Square</a>
        <a href="{r}restaurants-near-sugarloaf-mills.html">Near Sugarloaf Mills</a>
"""
for path in glob.glob(os.path.join(OUT, "**/*.html"), recursive=True):
    depth = path.replace(OUT + "/", "").count("/")
    r = "../" * depth
    s = open(path, encoding="utf-8").read()
    if "Near Gas South Arena</a>" not in s:
        block = '      <div>\n        <h4>Find us near</h4>\n' + NEWLINKS.format(r=r) + '      </div>\n'
        s = s.replace('      <div>\n        <h4>Follow</h4>', block + '      <div>\n        <h4>Follow</h4>', 1)
    # add events + contact + delivery to the Visit column
    if f'href="{r}events.html"' not in s:
        s = s.replace(f'<a href="{r}catering.html">Catering</a>',
                      f'<a href="{r}catering.html">Catering</a><a href="{r}events.html">Events</a>'
                      f'<a href="{r}delivery.html">Delivery</a><a href="{r}contact.html">Contact</a>', 1)
    open(path, "w", encoding="utf-8").write(s)
print("footer links added")


# ---------------------------------------------------------------- SITEMAP
urls = []
for f in sorted(glob.glob(os.path.join(OUT, "**/*.html"), recursive=True)):
    rel_p = f.replace(OUT + "/", "")
    pri = "1.0" if rel_p == "index.html" else (
        "0.9" if rel_p in ("menu.html", "catering.html", "buckhead.html", "duluth.html",
                           "late-night-food-buckhead.html", "halal-food-atlanta.html") else "0.6")
    urls.append(f"  <url><loc>{DOMAIN}/{rel_p}</loc><changefreq>weekly</changefreq><priority>{pri}</priority></url>")
open(os.path.join(OUT, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "\n".join(urls) + "\n</urlset>\n")
print("total pages:", len(urls))

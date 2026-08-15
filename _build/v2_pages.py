#!/usr/bin/env python3
import os
from site_config import LOCATIONS, ORDER_URL, PRODUCTION_HOST  # single source of truth, sys
sys.path.insert(0, "/home/claude")
from v2_base import *   # noqa

pages = {}   # path -> (html, changefreq, priority)


def write(path, html, pri="0.7", freq="weekly"):
    pages[path] = (html, freq, pri)


# =========================================================== HOME
faqs_home = [
    ("Is Bite More halal?",
     "Yes. Every protein at both locations is 100% halal — there is no separate halal menu because there is no non-halal menu."),
    ("What kind of food is Bite More?",
     "Halal Italian-American. Pasta, smash burgers, wings and loaded fries, cooked to order at two Atlanta kitchens."),
    ("Where is Bite More located?",
     "Two locations: 3150 Roswell Rd NW, Suite A1 in Buckhead, Atlanta, and 2148 Duluth Hwy 120, Suite 117 in Duluth, GA."),
    ("What are your hours?",
     "Closed Mondays. Tuesday and Wednesday 11am–10pm. Thursday through Sunday 11am–midnight."),
    ("Do you deliver?",
     "Yes — delivery and pickup across Buckhead, Sandy Springs, Brookhaven, Duluth, Johns Creek and the surrounding areas. Ordering direct from us costs less than the delivery apps."),
    ("Do you cater?",
     "Yes. Full trays for 20 to 200 guests across metro Atlanta, delivered hot and set up."),
]

home = head("Bite More | Halal Burgers, Pasta &amp; Wings in Buckhead &amp; Duluth, GA",
            "Halal Italian-American in Atlanta. Oklahoma Onion Smash from $14.99, Cajun Alfredo, Mac Attack Fries. Cooked to order, protein on every item. Buckhead &amp; Duluth.",
            "", 0, restaurant_ld())
home += nav(0, "")
home += f"""<section class="hero">
  <div class="wrap hero-in">
    <div>
      <p class="eyebrow">Buckhead &amp; Duluth · Atlanta, GA</p>
      <h1 class="dsp">Halal burgers,<br>pasta and wings.<br><span class="italic hot">Cooked</span> to order.</h1>
      <p class="sub">Two Atlanta kitchens making Italian-American food where every protein is halal — so the whole table orders off the same menu. Smash burgers from $12.99, pasta from $14.99.</p>
      <div class="hero-cta">
        <a class="btn btn-solid" href="{ORDER}">Order online</a>
        <a class="btn btn-ghost" href="menu.html">See the menu &amp; prices</a>
      </div>
      <div class="hero-meta">
        <span><b>{RATING} ★</b> · {RATING_COUNT}+ ratings</span>
        <span>Dine in · Pickup · Delivery</span>
        <span>Open till midnight Thu–Sun</span>
      </div>
    </div>
    <div class="hero-art">
      <img src="{IMG['oklahoma']}" alt="Oklahoma Onion Smash Burger with caramelized onions and melted cheese" width="600" height="750">
      <div class="seal"><b>100%</b><em>halal</em><small>Both kitchens</small></div>
    </div>
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
    <div class="sec-head rv">
      <p class="eyebrow">Start here</p>
      <h2 class="dsp">The three<br>people reorder</h2>
      <p>Prices shown are what you pay ordering direct. Full menu with every item and its protein count is one click away.</p>
    </div>
    <div class="carta rv">
{item_row("Oklahoma Onion Smash Burger", "14.99", "~38g protein", "Double smash patties with onions pressed into the crust, American cheese and Smash Sauce. Our highest-rated dish on the delivery platforms.", IMG['oklahoma'], "oklahoma-onion-smash", True, 0)}{item_row("Cajun Alfredo", "19.99", "", "Fettuccine in cream sauce with Cajun spice, your choice of protein, Parmesan and garlic toast. Our most-ordered dish.", IMG['alfredo_cajun'], "cajun-alfredo", False, 0)}{item_row("Mac Attack Fries", "19.99", "", "Fries under creamy mac and cheese and crispy fried chicken with chipotle mayo. The one reviewers name most.", IMG['macfries'], "loaded-fries", False, 0)}    </div>
    <p style="margin-top:32px"><a class="btn btn-ghost" href="menu.html">Full menu and prices</a></p>
  </div>
</section>

<section class="sec panel">
  <div class="wrap">
    <div class="sec-head rv">
      <p class="eyebrow">Why order direct</p>
      <h2 class="dsp">Same kitchen.<br><span class="italic hot">Less</span> markup.</h2>
    </div>
    <div class="split rv">
      <p class="pull">Ordering from us costs less than ordering the same food through a delivery app — and we can actually fix it if something's wrong.</p>
      <ul class="std-list">
        <li><b>Straight to our kitchen</b><span>Your ticket prints on our line, not in a queue behind a platform.</span></li>
        <li><b>No app markup</b><span>Delivery apps mark our menu up. Our prices are our prices.</span></li>
        <li><b>Something wrong? Call us</b><span>(470) 514-8473 Buckhead, (943) 296-4518 Duluth. A person answers.</span></li>
        <li><b>More stays here</b><span>Commission on a third-party order can run 15–30%. Ordering direct keeps it in the kitchen.</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head rv">
      <p class="eyebrow">Find us</p>
      <h2 class="dsp">Two kitchens<br>in Atlanta</h2>
    </div>
    <div class="locs rv">
{loc_card(LOCATIONS[0], 0)}{loc_card(LOCATIONS[1], 0)}    </div>
  </div>
</section>

<section class="sec panel">
  <div class="wrap">
    <div class="sec-head rv">
      <p class="eyebrow">Feeding a crowd</p>
      <h2 class="dsp">Catering for<br>20 to 200</h2>
      <p>Office lunches, weddings, graduations and game days across metro Atlanta. Full trays, delivered hot and set up before guests arrive.</p>
    </div>
    <a class="btn btn-solid rv" href="catering.html">See catering</a>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="knownfor rv">
      <h2 class="dsp" style="font-size:clamp(26px,3.4vw,40px)">What we're known for</h2>
      <p>{known_for(0)}</p>
      <h2 class="dsp" style="font-size:clamp(26px,3.4vw,40px);margin-top:40px">Areas we serve</h2>
      <p>{areas_served(0)}</p>
    </div>
  </div>
</section>

"""
home += faq_html(faqs_home, "Questions we get")
home += foot(0)
# merge FAQ schema into home
home = home.replace("</head>", '<script type="application/ld+json">%s</script>\n</head>'
                    % json.dumps(faq_ld(faqs_home)), 1)
write("index.html", home, "1.0", "weekly")


# =========================================================== MENU
menu_ld = {"@context": "https://schema.org", "@type": "Menu", "name": "Bite More Menu",
           "hasMenuSection": []}
sections_html = ""
for sec_name, sec_note, items in MENU:
    rows = "".join(item_row(n, p, m, d, i, t, h, 0) for n, p, m, d, i, t, h in items)
    note = f'<p class="cat-note rv">{sec_note}</p>' if sec_note else ""
    sections_html += f"""    <h2 class="dsp cat-title rv">{sec_name}</h2>
    {note}
    <div class="carta">
{rows}    </div>
"""
    menu_ld["hasMenuSection"].append({
        "@type": "MenuSection", "name": sec_name,
        "hasMenuItem": [{"@type": "MenuItem", "name": n,
                         "description": d,
                         **({"offers": {"@type": "Offer", "price": p, "priceCurrency": "USD"}}
                            if p != "—" else {})}
                        for n, p, m, d, i, t, h in items]})

menu = head("Menu &amp; Prices | Bite More — Halal Burgers, Pasta &amp; Wings, Atlanta",
            "Full Bite More menu with prices. Halal smash burgers from $12.99, Cajun Alfredo $19.99, wings from $11.99, loaded fries. Protein counts on every item.",
            "menu.html", 0, menu_ld)
menu += nav(0, "menu.html")
menu += crumbs(0, [("Menu", "menu.html")])
menu += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">Menu &amp; Prices</p>
    <h1 class="dsp">Everything we<br>cook, and what<br>it <span class="italic hot">costs</span></h1>
    <p>Every protein is halal. Every item is cooked when you order it. Protein counts are listed because people ask — and prices are here because you shouldn't have to open an app to find them.</p>
    <a class="btn btn-solid" href="{ORDER}">Order online</a>
  </div>
</section>
{TICKER}
<section class="sec">
  <div class="wrap">
{sections_html}    <p style="margin-top:40px" class="rv"><a class="btn btn-solid" href="{ORDER}">Order online</a></p>
  </div>
</section>
"""
menu_faqs = [
    ("Is everything on the menu halal?",
     "Yes. Every protein at both locations is halal. There is no separate menu and nothing to ask at the counter."),
    ("Do you have vegetarian options?",
     "Alfredo Pasta, mac and cheese, garlic toast and all of our fries are made without meat."),
    ("Can I get the Cajun Alfredo mild?",
     "Yes. Ask for mild, or order the Alfredo Pasta, which has no heat at all."),
    ("Why do you list protein counts?",
     "Because customers ask. Grilled chicken runs about 55g, ten wings about 60g, a smash burger about 38g."),
    ("Are prices the same on the delivery apps?",
     "No. Third-party apps mark menu prices up to cover their commission. The prices on this page are our direct prices."),
]
menu += faq_html(menu_faqs, "Menu questions")
menu = menu.replace("</head>", '<script type="application/ld+json">%s</script>\n</head>'
                    % json.dumps(faq_ld(menu_faqs)), 1)
menu += foot(0)
write("menu.html", menu, "0.9", "weekly")


# =========================================================== TAG PAGES
name_index = {n: (n, p, m, d, i, t, h) for _, _, items in MENU for n, p, m, d, i, t, h in items}

for slug, (h1, title, desc, intro, related) in TAGS.items():
    rows = "".join(item_row(*name_index[n][:-1], name_index[n][-1], 1)
                   for n in related if n in name_index)
    other = "".join(f'<a href="{s}.html">{v[0]}</a>' for s, v in TAGS.items() if s != slug)
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": h1,
          "description": desc, "url": f"{DOMAIN}/tags/{slug}.html",
          "about": {"@type": "Restaurant", "name": "Bite More",
                    "servesCuisine": ["Halal", "Italian-American"],
                    "aggregateRating": {"@type": "AggregateRating",
                                        "ratingValue": RATING, "reviewCount": RATING_COUNT}}}
    p = head(title, desc, f"tags/{slug}.html", 1, ld)
    p += nav(1)
    p += crumbs(1, [("Menu", "menu.html"), (h1, "")])
    p += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">Known for</p>
    <h1 class="dsp">{h1}</h1>
    <p>{intro}</p>
    <a class="btn btn-solid" href="{ORDER}">Order online</a>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="carta rv">
{rows}    </div>
    <p style="margin-top:30px"><a class="btn btn-ghost" href="../menu.html">See the full menu</a></p>
  </div>
</section>
<section class="sec panel">
  <div class="wrap">
    {badges()}
    <div class="knownfor rv" style="margin-top:40px">
      <h2 class="dsp" style="font-size:clamp(24px,3vw,34px)">Also on the menu</h2>
      <p class="taglist">{other}</p>
      <h2 class="dsp" style="font-size:clamp(24px,3vw,34px);margin-top:36px">Where we deliver</h2>
      <p class="taglist">{areas_served(1)}</p>
    </div>
  </div>
</section>
<section class="sec">
  <div class="wrap locs rv">
{loc_card(LOCATIONS[0], 1)}{loc_card(LOCATIONS[1], 1)}  </div>
</section>
"""
    p += foot(1)
    write(f"tags/{slug}.html", p, "0.6")


# =========================================================== PLACE PAGES
for slug, area, home_loc in PLACES:
    L = [l for l in LOCATIONS if l["slug"] == home_loc][0]
    title = f"Halal Food Delivery in {area}, GA | Bite More"
    desc = (f"Halal burgers, pasta, wings and loaded fries delivered to {area}. "
            f"Cooked to order at our {L['name']} kitchen. Order direct and skip the app markup.")
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": title,
          "description": desc, "url": f"{DOMAIN}/places/{slug}.html",
          "about": restaurant_ld(L)}
    others = "".join(f'<a href="{s}.html">{n}</a>' for s, n, _ in PLACES if s != slug)
    p = head(title, desc, f"places/{slug}.html", 1, ld)
    p += nav(1)
    p += crumbs(1, [("Locations", "locations.html"), (area, "")])
    p += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">Delivery &amp; pickup</p>
    <h1 class="dsp">Halal food<br>delivered to<br><span class="italic hot">{area}</span></h1>
    <p>We cook for {area} out of our {L['name']} kitchen — {L['blurb']} Halal smash burgers, Cajun Alfredo, wings and loaded fries, made when you order.</p>
    <a class="btn btn-solid" href="{ORDER}">Order to {area}</a>
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
    <div class="sec-head rv">
      <p class="eyebrow">Most ordered in {area}</p>
      <h2 class="dsp">What to get</h2>
    </div>
    <div class="carta rv">
{item_row("Oklahoma Onion Smash Burger", "14.99", "~38g protein", "Double smash patties with onions pressed into the crust. Our highest-rated dish.", IMG['oklahoma'], "oklahoma-onion-smash", True, 1)}{item_row("Cajun Alfredo", "19.99", "", "Cream sauce with Cajun spice, your choice of protein, garlic toast on the side.", IMG['alfredo_cajun'], "cajun-alfredo", False, 1)}{item_row("Mac Attack Fries", "19.99", "", "Fries under mac and cheese and crispy fried chicken with chipotle mayo.", IMG['macfries'], "loaded-fries", False, 1)}    </div>
  </div>
</section>
<section class="sec panel">
  <div class="wrap">
    <div class="sec-head rv">
      <p class="eyebrow">Your kitchen</p>
      <h2 class="dsp">{L['name']}</h2>
    </div>
    <div class="locs rv" style="grid-template-columns:1fr">
{loc_card(L, 1)}    </div>
    <div class="knownfor rv" style="margin-top:40px">
      <h2 class="dsp" style="font-size:clamp(24px,3vw,34px)">We're known for</h2>
      <p class="taglist">{known_for(1)}</p>
      <h2 class="dsp" style="font-size:clamp(24px,3vw,34px);margin-top:36px">We also deliver to</h2>
      <p class="taglist">{others}</p>
    </div>
  </div>
</section>
"""
    p += faq_html([
        (f"Do you deliver to {area}?",
         f"Yes. We deliver to {area} from our {L['name']} kitchen at {L['street']}, {L['city']}, GA. You can order direct from us or through the delivery apps — direct costs less."),
        (f"Is there halal food in {area}?",
         f"Bite More serves 100% halal Italian-American food to {area} — smash burgers, pasta, wings and loaded fries. Every protein is halal at both of our kitchens."),
        ("What time do you close?",
         "Closed Mondays. Tuesday and Wednesday until 10pm. Thursday through Sunday until midnight."),
        ("Can I pick up instead?",
         f"Yes. Order ahead and collect from our {L['name']} location at {L['street']}."),
    ], f"Ordering in {area}")
    p += foot(1)
    write(f"places/{slug}.html", p, "0.5")


# =========================================================== LOCATION PAGES
for L in LOCATIONS:
    nearby = ", ".join(n for s, n, h in PLACES if h == L["slug"])
    title = f"Bite More {L['name']} | Halal Burgers, Pasta &amp; Wings in {L['city']}, GA"
    desc = (f"Bite More {L['name']} — halal Italian-American at {L['street']}, {L['city']}, GA. "
            f"Smash burgers, Cajun Alfredo, wings. Dine in, pickup or delivery. {RATING}★.")
    p = head(title, desc, f"{L['slug']}.html", 0, restaurant_ld(L))
    p += nav(0, "locations.html")
    p += crumbs(0, [("Locations", "locations.html"), (L["name"], "")])
    p += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">{L['city']}, GA</p>
    <h1 class="dsp">Bite More<br><span class="italic hot">{L['name']}</span></h1>
    <p>{L['blurb']} Halal Italian-American cooked to order — burgers, pasta, wings and loaded fries.</p>
    <a class="btn btn-solid" href="{ORDER}">Order from {L['name']}</a>
  </div>
</section>
{TICKER}
<section class="sec">
  <div class="wrap">
    {badges()}
    <div class="locs rv" style="grid-template-columns:1fr;max-width:560px;margin-top:40px">
{loc_card(L, 0)}    </div>
  </div>
</section>
<section class="sec panel">
  <div class="wrap">
    <div class="sec-head rv">
      <p class="eyebrow">Most ordered here</p>
      <h2 class="dsp">What to get</h2>
    </div>
    <div class="carta rv">
{item_row("Oklahoma Onion Smash Burger", "14.99", "~38g protein", "Our highest-rated dish across the delivery platforms.", IMG['oklahoma'], "oklahoma-onion-smash", True, 0)}{item_row("Cajun Alfredo", "19.99", "", "Our most-ordered dish. Cream sauce, Cajun spice, garlic toast.", IMG['alfredo_cajun'], "cajun-alfredo", False, 0)}{item_row("Mac Attack Fries", "19.99", "", "Named more often in our reviews than anything else.", IMG['macfries'], "loaded-fries", False, 0)}    </div>
    <p style="margin-top:30px"><a class="btn btn-ghost" href="menu.html">Full menu and prices</a></p>
  </div>
</section>
<section class="sec">
  <div class="wrap knownfor rv">
    <h2 class="dsp" style="font-size:clamp(24px,3vw,34px)">Delivering to</h2>
    <p>{nearby}</p>
    <h2 class="dsp" style="font-size:clamp(24px,3vw,34px);margin-top:36px">Known for</h2>
    <p class="taglist">{known_for(0)}</p>
  </div>
</section>
"""
    p += faq_html([
        (f"Where is Bite More {L['name']}?", f"{L['street']}, {L['city']}, GA {L['zip']}. Call {L['tel']}."),
        ("What are the hours?", "Closed Mondays. Tuesday and Wednesday 11am–10pm. Thursday through Sunday 11am–midnight."),
        ("Is the food halal?", "Yes — every protein at this location is 100% halal."),
        ("Can I dine in?", "Yes, there's a dining room. You can also order ahead for pickup or have it delivered."),
        ("Do you cater from this location?", f"Yes. We cater from {L['name']} across the surrounding area — trays for 20 to 200 guests."),
    ], f"Visiting {L['name']}")
    p += foot(0)
    write(f"{L['slug']}.html", p, "0.8")


# =========================================================== LOCATIONS INDEX
p = head("Locations | Bite More — Buckhead &amp; Duluth, GA",
         "Bite More locations, hours and delivery areas. Buckhead on Roswell Rd and Duluth on Duluth Hwy 120. Open until midnight Thursday–Sunday.",
         "locations.html", 0, restaurant_ld())
p += nav(0, "locations.html")
p += crumbs(0, [("Locations", "")])
p += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">Find us</p>
    <h1 class="dsp">Two kitchens<br>in Atlanta</h1>
    <p>Same recipes, same spice blends, same build sheets. Dine in, pick up, or have it brought to you.</p>
  </div>
</section>
{TICKER}
<section class="sec">
  <div class="wrap">
    <div class="locs rv">
{loc_card(LOCATIONS[0], 0)}{loc_card(LOCATIONS[1], 0)}    </div>
  </div>
</section>
<section class="sec panel">
  <div class="wrap">
    <div class="sec-head rv">
      <p class="eyebrow">Delivery</p>
      <h2 class="dsp">Where we deliver</h2>
    </div>
    <div class="split rv">
      <div>
        <p class="eyebrow" style="color:var(--bone)">From Buckhead</p>
        <p class="taglist" style="margin-top:12px">{areas_served(0, 'buckhead')}</p>
      </div>
      <div>
        <p class="eyebrow" style="color:var(--bone)">From Duluth</p>
        <p class="taglist" style="margin-top:12px">{areas_served(0, 'duluth')}</p>
      </div>
    </div>
  </div>
</section>
"""
p += foot(0)
write("locations.html", p, "0.8")

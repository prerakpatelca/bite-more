#!/usr/bin/env python3
"""v2.1 patch — applies patterns proven by Shake Shack, Rreal Tacos and Talkin' Tacos.

  1. Announcement bar (Rreal) — seasonal/LTO strip above the nav
  2. Social links in footer (all three) — we had none
  3. Location pages: cross-street descriptors, service badges, geo coordinates,
     Google Maps deep links (Shake Shack pattern)
  4. New /delivery.html — Rreal ranks a dedicated delivery page
  5. New /reviews.html — review-generation engine with GBP deep links
  6. New /blog/ with 3 seed posts — Rreal has a blog; Talkin' Tacos wins AI answers
"""
import os, sys, re, json, glob
sys.path.insert(0, "/home/claude")
from v2_base import *   # noqa

OUT = "/mnt/user-data/outputs/bitemore-site-v2"
os.makedirs(os.path.join(OUT, "blog"), exist_ok=True)

# Google review deep links — replace PLACE_ID with each store's real Place ID
GBP = {
    "buckhead": "https://search.google.com/local/writereview?placeid=PLACE_ID_BUCKHEAD",
    "duluth": "https://search.google.com/local/writereview?placeid=PLACE_ID_DULUTH",
}
GEO = {"buckhead": (33.8404, -84.3800), "duluth": (33.9800, -84.1200)}
CROSS = {"buckhead": "On Roswell Rd between Peachtree Rd and Piedmont Rd — 2 minutes from the Buckhead Theatre",
         "duluth": "On Duluth Hwy 120 near Peachtree Industrial Blvd — 5 minutes from the office parks"}

SOCIAL = {"instagram": "https://www.instagram.com/bitemore.usa",
          "tiktok": "https://www.tiktok.com/@bitemore.usa",
          "facebook": "https://www.facebook.com/bitemore.usa"}

# ---------------------------------------------------------------- 1. announcement bar
ANNOUNCE = """<div class="announce" role="region" aria-label="Announcements">
  <div class="announce-track">
    <span>Open till midnight Thursday–Sunday</span><span>◆</span>
    <span>Order direct and skip the app markup</span><span>◆</span>
    <span>Catering for 20–200 across metro Atlanta</span><span>◆</span>
    <span>Open till midnight Thursday–Sunday</span><span>◆</span>
    <span>Order direct and skip the app markup</span><span>◆</span>
    <span>Catering for 20–200 across metro Atlanta</span><span>◆</span>
  </div>
</div>
"""

SOCIAL_BLOCK = """      <div>
        <h4>Follow</h4>
        <a href="{ig}">Instagram @bitemore.usa</a>
        <a href="{tt}">TikTok @bitemore.usa</a>
        <a href="{fb}">Facebook</a>
        <a href="reviews.html">Leave a review</a>
      </div>
""".format(ig=SOCIAL["instagram"], tt=SOCIAL["tiktok"], fb=SOCIAL["facebook"])

patched = 0
for path in glob.glob(os.path.join(OUT, "**/*.html"), recursive=True):
    depth = path.replace(OUT + "/", "").count("/")
    r = "../" * depth
    s = open(path, encoding="utf-8").read()

    # announcement bar above nav
    if 'class="announce"' not in s:
        s = s.replace('<header class="nav">', ANNOUNCE + '<header class="nav">', 1)

    # social column in footer
    if 'Follow</h4>' not in s:
        block = SOCIAL_BLOCK.replace('href="reviews.html"', f'href="{r}reviews.html"')
        s = s.replace('    </div>\n    <div class="fine">', block + '    </div>\n    <div class="fine">', 1)

    # sameAs on Restaurant schema so Google links the profiles to the business
    s = s.replace('"servesCuisine"',
                  '"sameAs": ["%s","%s","%s"],\n      "servesCuisine"'
                  % (SOCIAL["instagram"], SOCIAL["tiktok"], SOCIAL["facebook"]), 1) \
        if '"servesCuisine"' in s and '"sameAs"' not in s else s

    open(path, "w", encoding="utf-8").write(s)
    patched += 1
print(f"patched {patched} pages")


# ---------------------------------------------------------------- 2. location page upgrades
for L in LOCATIONS:
    p = os.path.join(OUT, f"{L['slug']}.html")
    s = open(p, encoding="utf-8").read()
    lat, lng = GEO[L["slug"]]

    # geo + service badges into the schema
    s = s.replace('"acceptsReservations": "False"',
                  '"acceptsReservations": "False",\n  "geo": {"@type": "GeoCoordinates", "latitude": %s, "longitude": %s},\n'
                  '  "hasDeliveryMethod": ["http://purl.org/goodrelations/v1#DeliveryModePickUp", "http://purl.org/goodrelations/v1#DeliveryModeOwnFleet"]'
                  % (lat, lng), 1)

    # cross-street line + service badges under the hero
    badge_block = f"""  <div class="wrap">
    <p class="crossst">{CROSS[L['slug']]}</p>
    <div class="svc">
      <span>Dine in</span><span>Pickup</span><span>Delivery</span><span>Catering</span><span>Free parking</span>
    </div>
  </div>
"""
    s = s.replace('</section>\n<div class="ticker"', badge_block + '</section>\n<div class="ticker"', 1)
    open(p, "w", encoding="utf-8").write(s)
print("location pages upgraded")


# ---------------------------------------------------------------- 3. DELIVERY PAGE
del_faqs = [
    ("Is it cheaper to order directly from Bite More?",
     "Yes. Delivery apps mark our menu prices up to cover their commission. The prices on bitemore.us are our own."),
    ("How long does delivery take?",
     "Most orders arrive in 25–40 minutes depending on distance and how busy the kitchen is. Everything is cooked when you order, not held."),
    ("Which areas do you deliver to?",
     "Buckhead, Sandy Springs, Brookhaven, Vinings, Midtown, Smyrna and Marietta from our Buckhead kitchen; Duluth, Johns Creek, Suwanee, Norcross, Peachtree Corners, Berkeley Lake, Sugar Hill and Dunwoody from Duluth."),
    ("Can I still order on DoorDash or UberEats?",
     "Yes, we're on all the major apps. Ordering direct just costs less and the ticket comes straight to our line."),
    ("Do you deliver late at night?",
     "Thursday through Sunday the kitchen runs until midnight."),
]
p = head("Delivery | Bite More — Halal Food Delivery in Atlanta &amp; Duluth, GA",
         "Halal burgers, pasta and wings delivered across metro Atlanta. Order direct from Bite More and skip the delivery-app markup. Open till midnight Thu–Sun.",
         "delivery.html", 0, faq_ld(del_faqs))
p += nav(0)
p += crumbs(0, [("Delivery", "")])
p += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">Delivery &amp; pickup</p>
    <h1 class="dsp">Halal food,<br>delivered <span class="italic hot">hot</span></h1>
    <p>Cooked when you order, not held under a lamp. Delivered across metro Atlanta from two kitchens — and it costs less when you order direct.</p>
    <a class="btn btn-solid" href="{ORDER}">Order delivery</a>
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
      <p class="eyebrow">Order direct</p>
      <h2 class="dsp">Why it costs less<br>from us</h2>
      <p>Delivery apps mark restaurant menus up to cover their commission. We don't. Same kitchen, same food, our prices.</p>
    </div>
    <div class="cards rv">
      <div class="card"><h3>Our prices</h3><p>What you see on our menu page is what you pay. No platform markup on top.</p></div>
      <div class="card"><h3>Straight to the line</h3><p>Your ticket prints in our kitchen instead of queuing behind a platform.</p></div>
      <div class="card"><h3>A person answers</h3><p>Something wrong? Call the store directly and we fix it — no support ticket.</p></div>
    </div>
  </div>
</section>
<section class="sec panel">
  <div class="wrap">
    <div class="sec-head rv">
      <p class="eyebrow">Coverage</p>
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
p += faq_html(del_faqs, "Delivery questions")
p += foot(0)
open(os.path.join(OUT, "delivery.html"), "w", encoding="utf-8").write(p)


# ---------------------------------------------------------------- 4. REVIEWS PAGE
p = head("Reviews | Bite More — Rated 4.3 across 1,000+ ratings",
         "What guests say about Bite More in Buckhead and Duluth. Read reviews, or leave one — we read every single one.",
         "reviews.html", 0, restaurant_ld())
p += nav(0)
p += crumbs(0, [("Reviews", "")])
p += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">Reviews</p>
    <h1 class="dsp">We read<br><span class="italic hot">every</span> one</h1>
    <p>Rated {RATING} across {RATING_COUNT}+ delivery ratings. Good or bad, tell us — it's how the food gets better.</p>
  </div>
</section>
{TICKER}
<section class="sec">
  <div class="wrap">
    <div class="stats rv">
      <div class="stat"><b>{RATING}</b><span>Average rating</span></div>
      <div class="stat"><b>{RATING_COUNT}+</b><span>Total ratings</span></div>
      <div class="stat"><b>82%</b><span>Like the Oklahoma Onion Smash</span></div>
      <div class="stat"><b>2</b><span>Atlanta kitchens</span></div>
    </div>
  </div>
</section>
<section class="sec panel">
  <div class="wrap">
    <div class="sec-head rv">
      <p class="eyebrow">Tell us how we did</p>
      <h2 class="dsp">Leave a review</h2>
      <p>Thirty seconds, and it genuinely changes what we cook. If something was wrong, say so — we'd rather hear it than not.</p>
    </div>
    <div class="locs rv">
      <div class="loc">
        <div class="loc-top"><h3>Buckhead</h3><p class="addr">3150 Roswell Rd NW, Suite A1</p></div>
        <div class="loc-foot"><a href="{GBP['buckhead']}">Review Buckhead on Google</a></div>
      </div>
      <div class="loc">
        <div class="loc-top"><h3>Duluth</h3><p class="addr">2148 Duluth Hwy 120, Suite 117</p></div>
        <div class="loc-foot"><a href="{GBP['duluth']}">Review Duluth on Google</a></div>
      </div>
    </div>
    <div class="callout rv" style="margin-top:32px">
      <b>Setup required</b>
      <p>Replace PLACE_ID_BUCKHEAD and PLACE_ID_DULUTH in this page with each store's real Google Place ID. Find them at developers.google.com/maps/documentation/places/web-service/place-id. These links open the review box directly — that one step roughly doubles review completion versus asking someone to "find us on Google."</p>
    </div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="callout rv">
      <b>Reviews section — pending real content</b>
      <p>This page is built and linked but has no published guest reviews yet. Pull five to eight real ones with names and dates from Google, DoorDash and UberEats, and they'll be added here with Review schema so the star rating shows in search results.</p>
    </div>
  </div>
</section>
"""
p += foot(0)
open(os.path.join(OUT, "reviews.html"), "w", encoding="utf-8").write(p)


# ---------------------------------------------------------------- 5. BLOG
POSTS = [
    ("halal-food-buckhead", "Where to Find Halal Food in Buckhead, Atlanta",
     "A guide to eating halal in Buckhead — what's available, what to look for, and where Bite More fits.",
     [("The short answer", "Buckhead has fewer halal options than its size suggests. Most of what's here is either a dedicated halal restaurant serving one cuisine, or a mainstream restaurant with a single halal item buried on the menu."),
      ("What halal actually means on a menu", "Halal describes how the meat is sourced and processed. A restaurant can be fully halal — every protein, no exceptions — or it can offer a halal option alongside non-halal items cooked on the same equipment. Those are very different things, and menus rarely make the difference clear."),
      ("What to ask", "Three questions settle it. Is every protein halal, or only some items? Is the fryer shared with non-halal products? Who supplies the meat? A restaurant that sources halal across the board will answer all three without hesitating."),
      ("Where we fit", "Bite More is fully halal at both kitchens — every protein, no separate menu. We cook Italian-American food: pasta, smash burgers, wings and loaded fries. Our Buckhead kitchen is at 3150 Roswell Rd NW, about two minutes from the Buckhead Theatre.")]),
    ("halal-catering-atlanta", "How to Order Halal Catering in Atlanta Without the Guesswork",
     "What to ask a caterer, how far ahead to book, and how to feed a mixed room from one menu.",
     [("Start with the whole room", "The easiest way to cater a mixed group is one fully halal menu. Nobody has to ask what's in what, there's no separate tray in the corner, and you don't need a dietary spreadsheet."),
      ("How far ahead to book", "Three to five days is comfortable for most office lunches. Larger buffets are easier with two weeks. Most kitchens can still work inside 72 hours if you call rather than email."),
      ("What to ask a caterer", "Is every protein halal or only some items? Do you deliver hot and set up, or drop off cold? What's included — plates, utensils, serving spoons, labels? Can we taste before booking a large event?"),
      ("Pans that survive the drive", "Cream sauces and fried food behave differently in a chafing tray than on a plate. Ask how a dish holds. Anything built to sit for two hours should still be worth eating at the end of service."),
      ("Booking with us", "We cater from both kitchens across metro Atlanta — 20 to 200 guests, delivered hot and set up. Same-day quotes if you send a headcount and a date.")]),
    ("late-night-food-buckhead", "Late Night Food in Buckhead: What's Actually Open",
     "Where to eat in Buckhead after 10pm, and what's still being cooked to order versus held under a lamp.",
     [("The 10pm problem", "Buckhead has plenty of restaurants and a real late-night crowd, but the overlap between the two shrinks fast after 10pm. Kitchens close before the venues do."),
      ("Cooked versus held", "Late-night food splits into two categories: places still cooking to order, and places serving what was made earlier. You can usually tell from how fast it arrives. Under two minutes for a burger means it wasn't cooked when you ordered."),
      ("After a show", "The Buckhead Theatre lets out into a stretch of Roswell Road with limited food options that late. Worth knowing what's open before the encore rather than after."),
      ("Our hours", "Our Buckhead kitchen runs until midnight Thursday through Sunday, and everything is cooked when the ticket prints. 3150 Roswell Rd NW, Suite A1.")]),
]

cards = ""
for slug, title, desc, sections in POSTS:
    body = "".join(f"""    <h2 class="dsp" style="font-size:clamp(24px,3vw,34px);margin-top:40px">{h}</h2>
    <p style="margin-top:14px;color:var(--muted);max-width:68ch;font-size:17px">{t}</p>
""" for h, t in sections)
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": title,
          "description": desc, "author": {"@type": "Organization", "name": "Bite More"},
          "publisher": {"@type": "Organization", "name": "Bite More"},
          "datePublished": "2026-08-13", "mainEntityOfPage": f"{DOMAIN}/blog/{slug}.html"}
    pg = head(f"{title} | Bite More", desc, f"blog/{slug}.html", 1, ld)
    pg += nav(1)
    pg += crumbs(1, [("Blog", "blog/index.html"), (title, "")])
    pg += f"""<section class="phero">
  <div class="wrap narrow">
    <p class="eyebrow">Guide</p>
    <h1 class="dsp" style="font-size:clamp(32px,5vw,58px)">{title}</h1>
    <p>{desc}</p>
  </div>
</section>
<section class="sec">
  <div class="wrap narrow">
{body}
    <p style="margin-top:44px"><a class="btn btn-solid" href="{ORDER}">Order online</a>
    <a class="btn btn-ghost" href="../menu.html" style="margin-left:10px">See the menu</a></p>
  </div>
</section>
<section class="sec panel">
  <div class="wrap knownfor rv">
    <h2 class="dsp" style="font-size:clamp(24px,3vw,34px)">Known for</h2>
    <p class="taglist">{known_for(1)}</p>
  </div>
</section>
"""
    pg += foot(1)
    open(os.path.join(OUT, "blog", f"{slug}.html"), "w", encoding="utf-8").write(pg)
    cards += f"""      <a class="card" href="{slug}.html" style="text-decoration:none;display:block">
        <h3>{title}</h3><p>{desc}</p>
      </a>
"""

p = head("Guides | Bite More — Halal Food, Catering &amp; Late Night in Atlanta",
         "Guides to eating halal in Atlanta: where to find halal food in Buckhead, how to book halal catering, and what's open late.",
         "blog/index.html", 1)
p += nav(1)
p += crumbs(1, [("Blog", "")])
p += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">Guides</p>
    <h1 class="dsp">Things worth<br>knowing</h1>
    <p>Short guides to eating halal in Atlanta — written to answer the question, not to sell you something.</p>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="cards rv">
{cards}    </div>
  </div>
</section>
"""
p += foot(1)
open(os.path.join(OUT, "blog", "index.html"), "w", encoding="utf-8").write(p)

# ---------------------------------------------------------------- 6. rebuild sitemap
urls = []
for f in sorted(glob.glob(os.path.join(OUT, "**/*.html"), recursive=True)):
    rel_p = f.replace(OUT + "/", "")
    pri = "1.0" if rel_p == "index.html" else ("0.9" if rel_p in ("menu.html", "catering.html") else "0.6")
    urls.append(f"  <url><loc>{DOMAIN}/{rel_p}</loc><changefreq>weekly</changefreq><priority>{pri}</priority></url>")
open(os.path.join(OUT, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "\n".join(urls) + "\n</urlset>\n")
print("pages now:", len(urls))

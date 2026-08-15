#!/usr/bin/env python3
"""Bite More site v2 — built from the research findings.
Generates ~45 crawlable pages: core pages, 12 dish tag pages, 20 neighborhood pages,
2 location pages, sitemap and robots.txt, with JSON-LD on every page.
"""
import os
from site_config import LOCATIONS, ORDER_URL, PRODUCTION_HOST  # single source of truth, json, textwrap

OUT = "/mnt/user-data/outputs/bitemore-site-v2"
DOMAIN = "https://bitemore.us"
ORDER = "https://order.online/business/bite-more-13060526"

for d in ("", "assets", "tags", "places"):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)

# ---------------------------------------------------------------- config
# EDIT THESE IN ONE PLACE. Hours must match DoorDash, UberEats, Grubhub,
# Google Business Profile and Yelp exactly — they currently do not.
# Per-location hours. Buckhead runs to 3am Fri/Sat — a real competitive advantage.
HOURS_BUCKHEAD = [("Monday – Wednesday", "11:00 am – 12:00 am"), ("Thursday", "11:00 am – 1:00 am"),
                  ("Friday – Saturday", "11:00 am – 3:00 am"), ("Sunday", "11:00 am – 1:00 am")]
HOURS_DULUTH = [("Monday – Wednesday", "11:00 am – 9:00 pm"), ("Thursday – Sunday", "11:00 am – 11:00 pm")]
HOURS_HUMAN = HOURS_BUCKHEAD
HOURS_SCHEMA = [
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday"],
     "opens": "11:00", "closes": "22:00"},
    {"@type": "OpeningHoursSpecification",
     "dayOfWeek": ["Thursday", "Friday", "Saturday", "Sunday"],
     "opens": "11:00", "closes": "00:00"},
]
RATING, RATING_COUNT = "4.3", "1000"

IMG = {
    "alfredo_cajun": "https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1200,height=672,format=auto/https://doordash-static.s3-us-west-2.amazonaws.com/media/photosV2/03c17c92-ef13-4ad6-9691-aa3ecbe50927-retina-large.jpeg",
    "alfredo": "https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1200,height=672,format=auto/https://doordash-static.s3-us-west-2.amazonaws.com/media/photosV2/989a6c54-6fb9-45e6-bddd-8fa53680a946-retina-large.jpeg",
    "smash": "https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1200,height=672,format=auto/https://doordash-static.s3-us-west-2.amazonaws.com/media/photosV2/a0a3d79f-04c8-44c4-8cf0-6b920ce3b90c-3c4206e7-8644-4af0-b859-6be1c44924ac-retina-large.jpg",
    "oklahoma": "https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1200,height=672,format=auto/https://doordash-static.s3-us-west-2.amazonaws.com/media/photosV2/ddf9caad-5219-43f6-a71c-2eb58c473f9e-retina-large.jpeg",
    "wings": "https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1200,height=672,format=auto/https://doordash-static.s3-us-west-2.amazonaws.com/media/photosV2/adbf9d13-deae-4907-9282-bcd59d015a30-retina-large.jpeg",
    "macfries": "https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1200,height=672,format=auto/https://doordash-static.s3-us-west-2.amazonaws.com/media/photosV2/c8157c55-468a-43c6-a399-baf5f7050768-retina-large.jpeg",
    "prep": "https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1200,height=672,format=auto/https://doordash-static.s3-us-west-2.amazonaws.com/media/photosV2/e7bf169d-839b-41fc-a251-f952ea0445f7-retina-large.jpeg",
    "spread": "https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1200,height=672,format=auto/https://doordash-static.s3-us-west-2.amazonaws.com/media/store/header/7ea468b5-419a-4a92-b032-7cabde11fa5c.jpg",
}

LOCATIONS = [
    dict(slug="buckhead", name="Buckhead", street="3150 Roswell Rd NW, Suite A1",
         city="Atlanta", zip="30305", tel="(470) 514-8473", telraw="+14705148473",
         blurb="Ninety seconds from the Buckhead Theatre, minutes from Lenox.",
         maps="https://maps.google.com/?q=3150+Roswell+Rd+NW+Suite+A1+Atlanta+GA+30305"),
    dict(slug="duluth", name="Duluth", street="2148 Duluth Hwy 120, Suite 117",
         city="Duluth", zip="30097", tel="(943) 296-4518", telraw="+19432964518",
         blurb="Five minutes from the Duluth Hwy and Peachtree Industrial office parks.",
         maps="https://maps.google.com/?q=2148+Duluth+Hwy+120+Suite+117+Duluth+GA+30097"),
]

# menu — prices as listed on the delivery platforms (Aug 2026).
# Direct prices should be set BELOW these. See README.
MENU = [
    ("Smash Burgers", "Clean halal beef, smashed on the flat top, Engelman's potato bun.", [
        ("Oklahoma Onion Smash Burger", "14.99", "~38g protein",
         "Double smash patties with grilled onions pressed into the crust, American cheese and Smash Sauce. Our highest-rated dish.", IMG["oklahoma"], "oklahoma-onion-smash", True),
        ("Signature Smash Burger", "13.99", "~38g protein",
         "Two beef patties, pepper jack, lettuce, tomato, pickles and Smash Sauce.", IMG["smash"], "smash-burger", False),
        ("Classic Smash Burger", "12.99", "~30g protein",
         "Two patties, American cheese, Smash Sauce. Nothing else in the way.", "", "smash-burger", False),
        ("Smash Melt", "13.99", "", "Smash patties and melted cheese griddled on Texas toast.", "", "smash-burger", False),
    ]),
    ("Pasta", "Sauces built in the pan, not poured from a jug. Cooked to order, served with garlic toast.", [
        ("Cajun Alfredo", "19.99", "", "Fettuccine in cream sauce with Cajun spice, your choice of protein and Parmesan. Our most-ordered dish.", IMG["alfredo_cajun"], "cajun-alfredo", True),
        ("Alfredo Pasta", "14.99", "", "Fettuccine, Alfredo, Parmesan, cracked black pepper. No heat.", IMG["alfredo"], "alfredo-pasta", False),
        ("Pomodoro Pasta", "14.99", "", "San Marzano-style tomato sauce cooked down with garlic, olive oil and basil. Simple, and unforgiving if you get it wrong.", "", "pomodoro-pasta", False),
        ("Arrabbiata Pasta", "15.99", "", "Our Pomodoro with chilli and garlic pushed hard. Angry, as the name says.", "", "arrabbiata-pasta", False),
    ]),
    ("Chicken", "Hand-breaded, marinated in house.", [
        ("Nashville Hot Chicken Sandwich", "14.99", "40g+ protein",
         "Two Nashville-spiced tenders, slaw, pickles, cheese and creamy sauce on a potato bun.", "", "nashville-hot-chicken", False),
        ("Flame Grilled Chicken Sandwich", "11.99", "~55g protein",
         "Grilled chicken breast, lettuce, tomato, banana peppers and cheese. The leanest thing on the menu.", "", "high-protein", False),
        ("Classic Fried Chicken Sandwich", "11.99", "40g+ protein",
         "Crispy fried chicken, lettuce, tomato, Chipotle Mayo.", "", "chicken-tenders", False),
        ("Chicken Tenders", "—", "5pc ~29g · 10pc ~58g protein",
         "Hand-breaded and fried to order. Five or ten pieces.", "", "chicken-tenders", False),
    ]),
    ("Wings", "Oven-baked, then lightly fried. Choose your flavor.", [
        ("6 pc Chicken Wings", "11.99", "~36g protein", "Six wings, tossed to order.", IMG["wings"], "chicken-wings", False),
        ("10 pc Chicken Wings", "15.99", "~60g protein", "Ten wings, tossed to order.", "", "chicken-wings", False),
        ("6 pc Wings with Fries", "12.00", "", "Six wings and a side of house fries.", "", "chicken-wings", False),
    ]),
    ("Loaded Fries & Sides", "Built to share, ordered as a main more often than not.", [
        ("Mac Attack Fries", "19.99", "", "Fries under creamy mac and cheese and crispy fried chicken, finished with chipotle mayo.", IMG["macfries"], "loaded-fries", True),
        ("Hot Nashville Fries", "14.99", "", "Nashville tenders, house slaw and dill pickles over fries with Suicide Sauce.", "", "loaded-fries", False),
        ("Garlic Parmesan Fries", "9.99", "", "Fries tossed in garlic butter and Parmesan.", "", "loaded-fries", False),
        ("Mac N Cheese", "6.99", "", "Creamy, cheesy, made in house.", "", "mac-and-cheese", False),
        ("Cajun Fries", "5.99", "", "House Cajun blend — smoky, garlicky, a real kick.", "", "loaded-fries", False),
        ("House Fries", "4.99", "", "Hand-seasoned. Our highest-rated side.", "", "loaded-fries", False),
    ]),
    ("Birria", "Slow-cooked halal birria. Consommé on the side.", [
        ("Birria Smash", "15.99", "", "Birria and a crispy smash patty with melted cheese on a potato bun.", "", "birria", False),
        ("Birria Fries", "16.99", "", "House fries, slow-cooked birria, crispy onions.", "", "birria", False),
        ("Birria Mac & Cheese", "14.99", "", "Creamy mac and cheese topped with birria.", "", "birria", False),
        ("Birria Grilled Cheese", "22.99", "", "Birria and American cheese griddled on Texas toast.", "", "birria", False),
    ]),
    ("Desserts & Lemonades", "", [
        ("Dulce de Leche Churros", "7.99", "", "Crisp outside, soft inside.", "", "", False),
        ("Fried Oreo", "7.99", "", "Six pieces, dusted.", "", "", False),
        ("Sunset Peach Lemonade", "4.99", "", "House lemonade with peach. Reviewers ask for it by name.", "", "", False),
        ("Pink Dragon Fruit Lemonade", "4.99", "", "House lemonade, dragon fruit.", "", "", False),
    ]),
]

# dish tag pages: slug -> (h1, title, meta, intro, related item names)
TAGS = {
    "halal-burgers": ("Halal Burgers in Atlanta",
        "Halal Burgers in Atlanta & Duluth, GA | Bite More",
        "Clean halal beef smashed to order at two Atlanta kitchens. Oklahoma Onion Smash, Signature Smash and Classic Smash from $12.99.",
        "Every burger we serve is 100% halal beef — not a special order, not a separate menu. Smashed hard on the flat top so the edges crisp, on an Engelman's potato bun.",
        ["Oklahoma Onion Smash Burger", "Signature Smash Burger", "Classic Smash Burger", "Smash Melt"]),
    "oklahoma-onion-smash": ("Oklahoma Onion Smash Burger",
        "Oklahoma Onion Smash Burger in Atlanta | Bite More",
        "Double smash patties with onions pressed into the crust, American cheese and Smash Sauce. ~38g protein, $14.99. Buckhead & Duluth.",
        "Thin-sliced onions go onto the patty and get pressed into the flat top so they caramelize into the crust rather than sitting on top of it. This is our highest-rated dish across the delivery platforms.",
        ["Oklahoma Onion Smash Burger", "Signature Smash Burger"]),
    "smash-burger": ("Smash Burgers",
        "Best Smash Burgers in Buckhead, Atlanta | Bite More",
        "Halal smash burgers made to order in Buckhead and Duluth. Two patties, crisp lace edges, Smash Sauce. From $12.99.",
        "A smash burger is about surface area. Thin patties pressed hard onto a hot flat top give you lace edges and a crust you cannot get from a thick patty.",
        ["Oklahoma Onion Smash Burger", "Signature Smash Burger", "Classic Smash Burger"]),
    "cajun-alfredo": ("Cajun Alfredo",
        "Cajun Alfredo Pasta in Atlanta | Bite More",
        "Fettuccine in cream sauce with Cajun spice, choice of protein and Parmesan. Garlic toast included. Halal. Buckhead & Duluth.",
        "Cream sauce built in the pan, not poured from a jug, with our Cajun blend and your choice of protein. It's the dish people order most and the one they come back for.",
        ["Cajun Alfredo", "Alfredo Pasta"]),
    "alfredo-pasta": ("Alfredo Pasta",
        "Halal Alfredo Pasta in Atlanta, GA | Bite More",
        "Fettuccine, Alfredo, Parmesan, cracked pepper, garlic toast. No heat. $14.99 at Buckhead and Duluth.",
        "The version without the Cajun heat. Fettuccine, Parmesan, black pepper, garlic toast on the side.",
        ["Alfredo Pasta", "Cajun Alfredo"]),
    "pomodoro-pasta": ("Pomodoro Pasta",
        "Pomodoro Pasta in Atlanta, GA | Halal Italian | Bite More",
        "Tomato, garlic, olive oil and basil cooked down properly. Halal Pomodoro pasta in Buckhead and Duluth, $14.99, with garlic toast.",
        "Four ingredients and nowhere to hide. Tomato, garlic, good olive oil and basil, cooked down until the sauce holds onto the pasta instead of sitting under it.",
        ["Pomodoro Pasta", "Arrabbiata Pasta", "Cajun Alfredo"]),
    "arrabbiata-pasta": ("Arrabbiata Pasta",
        "Arrabbiata Pasta in Atlanta, GA | Halal Italian | Bite More",
        "Pomodoro with chilli and garlic pushed hard. Halal arrabbiata pasta in Buckhead and Duluth, $15.99, served with garlic toast.",
        "Arrabbiata means angry. Our Pomodoro base with chilli and garlic taken further than most kitchens are willing to — heat that builds rather than hits.",
        ["Arrabbiata Pasta", "Pomodoro Pasta", "Cajun Alfredo"]),
    "tagliatelle": ("Tagliatelle",
        "Tagliatelle in Atlanta, GA | Halal Italian Pasta | Bite More",
        "Tagliatelle coming soon to Bite More — mushroom and porcini, Sicilian pesto, and beef meatball. Halal Italian in Buckhead and Duluth.",
        "Wider ribbons hold heavier sauces. Three tagliatelle dishes are in development in our kitchens right now.",
        ["Cajun Alfredo", "Pomodoro Pasta"]),
    "halal-pasta": ("Halal Pasta in Atlanta",
        "Halal Pasta & Italian Food in Atlanta, GA | Bite More",
        "Halal Italian-American pasta in Buckhead and Duluth. Cajun Alfredo, Alfredo Pasta, garlic toast. Every protein halal.",
        "Italian-American pasta is hard to find halal in Atlanta. Every protein on our pasta menu is halal, so there's nothing to ask at the counter.",
        ["Cajun Alfredo", "Alfredo Pasta"]),
    "chicken-wings": ("Chicken Wings",
        "Chicken Wings in Buckhead & Duluth, GA | Bite More",
        "Halal wings oven-baked then lightly fried, tossed to order. 6 pc $11.99, 10 pc $15.99.",
        "Baked first so they cook through, then fried briefly for the crunch. Tossed in your flavor when you order, not before.",
        ["6 pc Chicken Wings", "10 pc Chicken Wings", "6 pc Wings with Fries"]),
    "loaded-fries": ("Loaded Fries",
        "Loaded Fries in Atlanta, GA | Bite More",
        "Mac Attack Fries, Hot Nashville Fries, Birria Fries and Garlic Parmesan Fries. Halal, made to order.",
        "Our fries are the highest-rated thing we make. These are what happens when we put things on top of them.",
        ["Mac Attack Fries", "Hot Nashville Fries", "Garlic Parmesan Fries", "House Fries"]),
    "mac-and-cheese": ("Mac & Cheese",
        "Mac and Cheese in Atlanta, GA | Bite More",
        "Creamy mac and cheese made in house. As a side, loaded on fries, or topped with slow-cooked halal birria.",
        "Made in house and mentioned by name in more of our reviews than anything else on the menu.",
        ["Mac N Cheese", "Mac Attack Fries", "Birria Mac & Cheese"]),
    "nashville-hot-chicken": ("Nashville Hot Chicken",
        "Nashville Hot Chicken in Atlanta, GA | Bite More",
        "Halal Nashville hot chicken sandwich and loaded Nashville fries. 40g+ protein, $14.99.",
        "Nashville-spiced tenders with slaw and pickles to cool it down. Available as a sandwich or over fries.",
        ["Nashville Hot Chicken Sandwich", "Hot Nashville Fries"]),
    "chicken-tenders": ("Chicken Tenders & Sandwiches",
        "Halal Chicken Tenders & Sandwiches in Atlanta | Bite More",
        "Hand-breaded halal chicken tenders and sandwiches, marinated in house. 5 or 10 pieces. From $11.99.",
        "Hand-breaded and marinated in our kitchen, fried when you order. Five or ten pieces, or on a bun.",
        ["Chicken Tenders", "Classic Fried Chicken Sandwich", "Flame Grilled Chicken Sandwich"]),
    "birria": ("Birria",
        "Halal Birria in Atlanta, GA | Bite More",
        "Slow-cooked halal birria — smash burger, fries, mac and cheese, grilled cheese. Consommé on the side.",
        "Slow-cooked halal birria with consommé for dipping, served four ways.",
        ["Birria Smash", "Birria Fries", "Birria Mac & Cheese", "Birria Grilled Cheese"]),
    "high-protein": ("High Protein Meals",
        "High Protein Meals in Buckhead, Atlanta | Bite More",
        "Halal high-protein meals in Atlanta. Grilled chicken ~55g, wings ~60g, smash burgers ~38g. Macros on every item.",
        "We put the protein count on the menu because people ask. If you train in Buckhead and you're tired of choosing between clean and edible, these are the numbers.",
        ["Flame Grilled Chicken Sandwich", "10 pc Chicken Wings", "Chicken Tenders", "Oklahoma Onion Smash Burger"]),
    "late-night-food": ("Late Night Food",
        "Late Night Food in Buckhead, Atlanta | Bite More",
        "Kitchen open until midnight Thursday through Sunday in Buckhead. Halal burgers, wings, pasta and loaded fries.",
        "Cooked to order until midnight Thursday through Sunday. Not sitting under a lamp waiting for you.",
        ["Oklahoma Onion Smash Burger", "Mac Attack Fries", "10 pc Chicken Wings", "Cajun Alfredo"]),
}

PLACES = [
    ("buckhead", "Buckhead", "buckhead"), ("garden-hills", "Garden Hills", "buckhead"),
    ("peachtree-park", "Peachtree Park", "buckhead"), ("peachtree-hills", "Peachtree Hills", "buckhead"),
    ("pine-hills", "Pine Hills", "buckhead"), ("lindbergh-morosgo", "Lindbergh / Morosgo", "buckhead"),
    ("south-tuxedo-park", "South Tuxedo Park", "buckhead"), ("brookhaven", "Brookhaven", "buckhead"),
    ("sandy-springs", "Sandy Springs", "buckhead"), ("vinings", "Vinings", "buckhead"),
    ("midtown-atlanta", "Midtown Atlanta", "buckhead"), ("morningside-lenox-park", "Morningside / Lenox Park", "buckhead"),
    ("smyrna", "Smyrna", "buckhead"), ("marietta", "Marietta", "buckhead"),
    ("duluth", "Duluth", "duluth"), ("johns-creek", "Johns Creek", "duluth"),
    ("suwanee", "Suwanee", "duluth"), ("berkeley-lake", "Berkeley Lake", "duluth"),
    ("norcross", "Norcross", "duluth"), ("peachtree-corners", "Peachtree Corners", "duluth"),
    ("sugar-hill", "Sugar Hill", "duluth"), ("dunwoody", "Dunwoody", "duluth"),
]

NAV = [("menu.html", "Menu"), ("catering.html", "Catering"),
       ("locations.html", "Locations"), ("about.html", "About"),
       ("franchise.html", "Franchise")]


def rel(depth):
    return "../" * depth


def head(title, desc, canonical, depth, jsonld=None, robots="index, follow"):
    r = rel(depth)
    ld = ""
    if jsonld:
        ld = '\n<script type="application/ld+json">%s</script>' % json.dumps(jsonld, indent=2)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{DOMAIN}/{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{DOMAIN}/{canonical}">
<meta property="og:image" content="{IMG['oklahoma']}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,400..900;1,62..125,400..900&family=Fraunces:ital,opsz,wght@0,9..144,400..900;1,9..144,400..900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/styles.css">{ld}
<!-- META PIXEL — replace PIXEL_ID and uncomment before running ads.
<script>
!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init','PIXEL_ID');fbq('track','PageView');
</script>
-->
</head>
<body>
"""


def nav(depth, current=""):
    r = rel(depth)
    links = "".join(
        f'      <a class="lnk" href="{r}{h}"{" aria-current=\"page\"" if h == current else ""}>{l}</a>\n'
        for h, l in NAV)
    mob = "".join(f'    <a href="{r}{h}">{l}</a>\n' for h, l in [("index.html", "Home")] + NAV)
    return f"""<header class="nav">
  <div class="wrap nav-in">
    <a class="brand" href="{r}index.html">Bite<span>&nbsp;More</span></a>
{links}      <button class="burger" aria-expanded="false" aria-label="Open menu">Menu</button>
    <a class="order" href="{ORDER}">Order Online</a>
  </div>
  <div class="mobile-menu">
{mob}  </div>
</header>
"""


def crumbs(depth, trail):
    r = rel(depth)
    items = ['<a href="%sindex.html">Home</a>' % r]
    for label, href in trail[:-1]:
        items.append('<a href="%s%s">%s</a>' % (r, href, label))
    items.append("<span>%s</span>" % trail[-1][0])
    return '<nav class="crumbs"><div class="wrap">%s</div></nav>\n' % " › ".join(items)


TICKER = """<div class="ticker" aria-hidden="true">
  <div class="marquee">
    <span>Oklahoma Onion Smash <i>◆</i></span><span>Cajun Alfredo <i>◆</i></span><span>Mac Attack Fries <i>◆</i></span>
    <span>Scratch Sauces <i>◆</i></span><span>Cooked To Order <i>◆</i></span><span>100% Halal <i>◆</i></span>
    <span>Oklahoma Onion Smash <i>◆</i></span><span>Cajun Alfredo <i>◆</i></span><span>Mac Attack Fries <i>◆</i></span>
    <span>Scratch Sauces <i>◆</i></span><span>Cooked To Order <i>◆</i></span><span>100% Halal <i>◆</i></span>
  </div>
</div>
"""


def badges():
    return """<div class="trio">
  <div><b>100% Halal</b><span>Every protein, both kitchens</span></div>
  <div><b>Made to Order</b><span>Nothing waits under a lamp</span></div>
  <div><b>Protein on the Menu</b><span>Grams listed on every item</span></div>
</div>
"""


def foot(depth):
    r = rel(depth)
    tagcols = "".join(f'<a href="{r}tags/{s}.html">{v[0]}</a>' for s, v in list(TAGS.items())[:8])
    placecols = "".join(f'<a href="{r}places/{s}.html">{n}</a>' for s, n, _ in PLACES[:12])
    return f"""<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <p class="brand">Bite<span>&nbsp;More</span></p>
        <p class="fmuted">Halal Italian-American<br>Buckhead &amp; Duluth, GA</p>
        <p class="fmuted" style="margin-top:14px">Buckhead (470) 514-8473<br>Duluth (943) 296-4518</p>
      </div>
      <div>
        <h4>Visit</h4>
        <a href="{r}menu.html">Menu</a><a href="{r}locations.html">Locations</a>
        <a href="{r}buckhead.html">Buckhead</a><a href="{r}duluth.html">Duluth</a>
        <a href="{r}catering.html">Catering</a><a href="{r}gift-cards.html">Gift Cards</a>
      </div>
      <div>
        <h4>Company</h4>
        <a href="{r}about.html">About</a><a href="{r}team.html">Our Team</a>
        <a href="{r}careers.html">Careers</a><a href="{r}franchise.html">Franchise</a>
        <a href="{ORDER}">Order Online</a>
      </div>
      <div>
        <h4>What we're known for</h4>
        {tagcols}
      </div>
      <div>
        <h4>Areas we serve</h4>
        {placecols}
      </div>
    </div>
    <div class="fine">
      <span>© 2026 Bite More Brands LLC. All rights reserved.</span>
      <span>Rated {RATING} across {RATING_COUNT}+ delivery ratings</span>
    </div>
  </div>
</footer>
<script src="{r}assets/site.js"></script>
</body>
</html>
"""


def restaurant_ld(loc=None, url="", name="Bite More"):
    def one(l):
        return {
            "@type": "Restaurant", "name": f"Bite More {l['name']}",
            "servesCuisine": ["Italian-American", "Halal", "American"],
            "priceRange": "$$", "url": f"{DOMAIN}/{l['slug']}.html",
            "telephone": l["telraw"], "menu": f"{DOMAIN}/menu.html",
            "acceptsReservations": "False",
            "address": {"@type": "PostalAddress", "streetAddress": l["street"],
                        "addressLocality": l["city"], "addressRegion": "GA",
                        "postalCode": l["zip"], "addressCountry": "US"},
            "openingHoursSpecification": HOURS_SCHEMA,
            "aggregateRating": {"@type": "AggregateRating", "ratingValue": RATING,
                                "reviewCount": RATING_COUNT},
        }
    if loc:
        return one(loc)
    return {"@context": "https://schema.org", "@graph": [one(l) for l in LOCATIONS]}


def faq_ld(pairs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}}
                           for q, a in pairs]}


def faq_html(pairs, heading="Questions"):
    body = "".join(
        f"      <details><summary>{q}</summary><p>{a}</p></details>\n" for q, a in pairs)
    return f"""<section class="sec panel">
  <div class="wrap narrow">
    <div class="sec-head rv" style="margin-bottom:24px">
      <p class="eyebrow">FAQ</p>
      <h2 class="dsp">{heading}</h2>
    </div>
    <div class="faq rv">
{body}    </div>
  </div>
</section>
"""


def known_for(depth):
    r = rel(depth)
    links = ", ".join(f'<a href="{r}tags/{s}.html">{v[0]}</a>' for s, v in TAGS.items())
    return links


def areas_served(depth, only=None):
    r = rel(depth)
    items = [p for p in PLACES if only is None or p[2] == only]
    return ", ".join(f'<a href="{r}places/{s}.html">{n}</a>' for s, n, _ in items)


def loc_card(l, depth):
    r = rel(depth)
    hrs = "".join(f'<div><span class="day">{d}</span><span{" class=\"closed\"" if h=="Closed" else ""}>{h}</span></div>'
                  for d, h in HOURS_HUMAN)
    return f"""      <div class="loc">
        <div class="loc-top">
          <h3><a href="{r}{l['slug']}.html">{l['name']}</a></h3>
          <p class="addr">{l['street']}<br>{l['city']}, GA {l['zip']}</p>
          <a class="tel" href="tel:{l['telraw']}">{l['tel']}</a>
        </div>
        <div class="hours">{hrs}</div>
        <div class="loc-foot">
          <a href="{ORDER}">Order from {l['name']}</a>
          <a class="alt" href="{l['maps']}">Directions</a>
        </div>
      </div>
"""


def item_row(name, price, macro, desc, img, tag, hero, depth):
    r = rel(depth)
    imgtag = f'<img src="{img}" alt="{name}" loading="lazy" width="112" height="88">' if img else ""
    cls = "item" + ("" if img else " noimg")
    link = f'<a class="tagref" href="{r}tags/{tag}.html">More {TAGS[tag][0].lower()} →</a>' if tag and tag in TAGS else ""
    macro_html = f'<span class="macro">{macro}</span>' if macro else ""
    badge = '<span class="tag top">Highest rated</span>' if hero else ""
    return f"""      <div class="{cls}">
        {imgtag}
        <div>
          <h3>{name} {macro_html}</h3>
          <p>{desc}</p>
          {link}
        </div>
        <span class="price">{'$' + price if price != '—' else 'Varies'}</span>
        {badge}
      </div>
"""

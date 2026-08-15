#!/usr/bin/env python3
import sys, os, json
sys.path.insert(0, "/home/claude")
exec(open("/home/claude/v2_pages.py").read())

# =========================================================== CATERING
cat_faqs = [
    ("How much notice do you need?", "Three to five days is comfortable for most events. Larger buffets are easier with two weeks. Inside 72 hours, call us — we can usually still make it work."),
    ("Is the catering menu fully halal?", "Yes. Every protein we serve is halal, at both locations and for every event, so there is nothing to flag to your guests."),
    ("Do you deliver and set up?", "Yes — delivered hot in chafing setups, laid out and labeled, with plates, utensils and serving spoons."),
    ("Can we build a custom menu?", "Yes, and most larger bookings do. We cook from scratch, so if you want something we don't run daily, ask and we'll price it."),
    ("What about vegetarian guests?", "Alfredo Pasta, mac and cheese, garlic toast and our fries are all meat-free, and buffet packages include a vegetarian tray."),
    ("Do you cater to Duluth office parks?", "Yes. Our Duluth kitchen covers the Duluth Hwy 120 and Peachtree Industrial office parks, Johns Creek, Suwanee and Peachtree Corners."),
]
p = head("Catering | Bite More — Halal Catering in Atlanta &amp; Gwinnett",
         "Halal Italian-American catering for offices, weddings and events across metro Atlanta. Trays for 20 to 200 guests, delivered hot and set up. Same-day quotes.",
         "catering.html", 0, faq_ld(cat_faqs))
p += nav(0, "catering.html")
p += crumbs(0, [("Catering", "")])
p += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">Catering</p>
    <h1 class="dsp">One menu the<br>whole room<br>can <span class="italic hot">eat</span></h1>
    <p>Every protein we cook is halal, so there's no separate tray in the corner and nobody at your event eating around the food. Full pans of Cajun Alfredo, smash sliders, wings and garlic toast for 20 to 200 guests.</p>
    <a class="btn btn-solid" href="#request">Request a quote</a>
  </div>
</section>
{TICKER}
<section class="sec">
  <div class="wrap">
    <div class="sec-head rv">
      <p class="eyebrow">Why teams book us</p>
      <h2 class="dsp">Nobody remembers<br>a sandwich platter</h2>
      <p>We send the food people already order for themselves — the Cajun Alfredo, the smash sliders, the Mac Attack Fries — in trays sized to your headcount.</p>
    </div>
    <div class="cards rv">
      <div class="card"><h3>Pasta that holds</h3><p>Our Alfredo is built thick enough to sit in a chafing tray through service and still pull like it left the pan.</p></div>
      <div class="card"><h3>Something to pick up</h3><p>Smash sliders, wings tossed in the flavor you pick, loaded fries. Handheld food keeps a room moving.</p></div>
      <div class="card"><h3>Set up, not dropped off</h3><p>Delivered hot in chafing setups, laid out and labeled so guests serve themselves.</p></div>
      <div class="card"><h3>One menu, whole room</h3><p>All halal. No separate tray, no questions from your guests, no dietary spreadsheet.</p></div>
      <div class="card"><h3>Cooked the morning of</h3><p>Sauces go on the stove the day of your event, not made ahead to suit our schedule.</p></div>
      <div class="card"><h3>Same-day quotes</h3><p>Send a headcount and a date; we come back with a menu and a per-person price that day.</p></div>
    </div>
  </div>
</section>

<section class="sec panel">
  <div class="wrap">
    <div class="sec-head rv">
      <p class="eyebrow">Packages</p>
      <h2 class="dsp">Pick a size,<br>we'll handle it</h2>
      <p>Starting points, not fixed menus — swap anything.</p>
    </div>
    <div class="pkgs rv">
      <div class="pkg">
        <div class="pkg-top"><h3>The Office</h3><p class="serves">Serves 20 – 30</p></div>
        <ul><li>Two pasta trays — Cajun Alfredo and Alfredo</li><li>Grilled chicken on the side</li><li>Garlic toast</li><li>Two trays of seasoned fries</li><li>Plates, utensils, serving spoons, labels</li></ul>
        <div class="pkg-foot"><a href="#request">Request a quote</a></div>
      </div>
      <div class="pkg featured">
        <div class="pkg-top"><h3>The Spread</h3><p class="serves">Serves 40 – 70 · Most booked</p></div>
        <ul><li>Three pasta trays with two proteins</li><li>Smash slider tray</li><li>Wings in two flavors</li><li>Mac Attack Fries and mac &amp; cheese</li><li>Garlic toast and house sauces</li><li>Chafing setup, plates, utensils, labels</li></ul>
        <div class="pkg-foot"><a href="#request">Request a quote</a></div>
      </div>
      <div class="pkg">
        <div class="pkg-top"><h3>The Hall</h3><p class="serves">Serves 80 – 200</p></div>
        <ul><li>Full buffet line built with you</li><li>Pasta, sliders, wings, sides</li><li>Vegetarian tray included</li><li>On-site setup and hot holding</li><li>Optional staff to run the line</li><li>Tasting before you book</li></ul>
        <div class="pkg-foot"><a href="#request">Request a quote</a></div>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="request">
  <div class="wrap split even">
    <div class="rv">
      <p class="eyebrow">Request a quote</p>
      <h2 class="dsp" style="font-size:clamp(30px,4vw,50px);margin:12px 0 0">Tell us about<br>your event</h2>
      <p style="color:var(--muted);margin-top:18px;max-width:44ch">Send the details and we'll come back with a menu and a per-person price the same day. Inside 72 hours, call us.</p>
      <p style="margin-top:24px"><a class="tel" href="tel:+14705148473" style="font-size:20px;font-weight:900">(470) 514-8473</a> <span class="fmuted">Buckhead</span></p>
      <p style="margin-top:10px"><a class="tel" href="tel:+19432964518" style="font-size:20px;font-weight:900">(943) 296-4518</a> <span class="fmuted">Duluth</span></p>
    </div>
    <div class="form rv">
      <div class="fgrid">
        <div class="field"><label for="name">Your name</label><input id="name" type="text" placeholder="First and last"></div>
        <div class="field"><label for="org">Company or event</label><input id="org" type="text" placeholder="Optional"></div>
        <div class="field"><label for="email">Email</label><input id="email" type="email" placeholder="you@email.com"></div>
        <div class="field"><label for="phone">Phone</label><input id="phone" type="tel" placeholder="(___) ___-____"></div>
        <div class="field"><label for="date">Event date</label><input id="date" type="date"></div>
        <div class="field"><label for="guests">Guests</label><select id="guests"><option>20 – 30</option><option>30 – 50</option><option>50 – 80</option><option>80 – 120</option><option>120 – 200</option><option>200+</option></select></div>
        <div class="field full"><label for="loc">Nearest kitchen</label><select id="loc"><option>Buckhead</option><option>Duluth</option><option>Not sure</option></select></div>
        <div class="field full"><label for="notes">Anything else</label><textarea id="notes" placeholder="Venue, timing, dietary needs, dishes you have in mind"></textarea></div>
      </div>
      <a class="btn btn-solid" href="mailto:catering@bitemore.us">Send request</a>
      <p class="form-note">We reply within one business day. Monday requests go out Tuesday — the kitchens are closed Mondays.</p>
    </div>
  </div>
</section>
"""
p += faq_html(cat_faqs, "Catering FAQ")
p += foot(0)
write("catering.html", p, "0.9")


# =========================================================== ABOUT
p = head("About | Bite More — Halal Italian-American in Atlanta",
         "How Bite More built two Atlanta kitchens serving halal Italian-American food. Scratch sauces, in-house dough, the same recipes at Buckhead and Duluth.",
         "about.html", 0, restaurant_ld())
p += nav(0, "about.html")
p += crumbs(0, [("About", "")])
p += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">About us</p>
    <h1 class="dsp">Two kitchens.<br>One recipe book.<br><span class="italic hot">No</span> shortcuts.</h1>
    <p>Bite More cooks Italian-American food — pasta, smash burgers, wings — and sources every protein halal. Not a separate menu. Not a special order. Just how we buy.</p>
  </div>
</section>
{TICKER}
<section class="sec">
  <div class="wrap split rv">
    <div>
      <p class="eyebrow">What we're for</p>
      <p class="pull" style="max-width:26ch;margin-top:16px">Bold, accessible food that honors both halal integrity and the tradition of Italian-American cooking.</p>
      <p style="color:var(--muted);margin-top:24px;max-width:52ch">At a price and a speed that fits how people actually eat — lunch between meetings, dinner after work, a late order on the way home.</p>
    </div>
    <div><img src="{IMG['prep']}" alt="Prep work in the Bite More kitchen" style="border-radius:3px;width:100%;height:380px;object-fit:cover" loading="lazy"></div>
  </div>
</section>
<section class="sec panel">
  <div class="wrap">
    <div class="sec-head rv"><p class="eyebrow">The story</p><h2 class="dsp">How we got here</h2></div>
    <ul class="timeline rv">
      <li><b>The problem</b><h3>Two menus, two standards</h3><p>If you eat halal, Italian-American food has mostly meant asking questions at the counter. The places that were halal often traded on that alone, and the food came second.</p></li>
      <li><b>The first kitchen</b><h3>One storefront in Buckhead</h3><p>We started with a single Atlanta location and one rule: cook the food we'd want to eat, source it clean, and don't advertise a compromise because there isn't one.</p></li>
      <li><b>Proving it</b><h3>A second kitchen in Duluth</h3><p>The second location was the test — could the food travel? Duluth cooks to the same build sheets and the same spice blends as Buckhead.</p></li>
      <li><b>Now</b><h3>A brand, not a restaurant</h3><p>Documented recipes, standardized prep, a registered trademark and two proven kitchens.</p></li>
    </ul>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="sec-head rv"><p class="eyebrow">What we hold to</p><h2 class="dsp">Six things<br>we don't bend on</h2></div>
    <div class="cards rv">
      <div class="card"><span class="num">01</span><h3>Made in our kitchen</h3><p>Sauces, dough and spice blends produced in house. Nothing arrives finished in a bag with our name on it.</p></div>
      <div class="card"><span class="num">02</span><h3>Cooked, not held</h3><p>Pasta hits the pan when the ticket prints. Wings come out of the oven before they see the fryer.</p></div>
      <div class="card"><span class="num">03</span><h3>Protein on the menu</h3><p>We list the grams because people ask. Grilled chicken ~55g, ten wings ~60g, a smash burger ~38g.</p></div>
      <div class="card"><span class="num">04</span><h3>The same every time</h3><p>Documented builds and standardized prep, so your order tastes the way it did last time at either location.</p></div>
      <div class="card"><span class="num">05</span><h3>Halal sourcing, no asterisks</h3><p>Every protein, both kitchens. It's how we buy — not who we cook for. Everyone eats the same menu.</p></div>
      <div class="card"><span class="num">06</span><h3>Built to grow</h3><p>Everything written down, so an operator in another city can open a kitchen that tastes like ours.</p></div>
    </div>
  </div>
</section>
<section class="sec panel">
  <div class="wrap">
    <div class="stats rv">
      <div class="stat"><b>2</b><span>Atlanta kitchens</span></div>
      <div class="stat"><b>{RATING_COUNT}+</b><span>Delivery ratings</span></div>
      <div class="stat"><b>{RATING}</b><span>Average rating</span></div>
      <div class="stat"><b>100%</b><span>Halal sourcing</span></div>
    </div>
  </div>
</section>
"""
p += foot(0)
write("about.html", p, "0.7")


# =========================================================== TEAM
p = head("Our Team | Bite More — Atlanta",
         "The people cooking at Bite More Buckhead and Duluth. Kitchen leadership, front of house and the team behind the recipes.",
         "team.html", 0)
p += nav(0)
p += crumbs(0, [("About", "about.html"), ("Our Team", "")])
p += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">Our team</p>
    <h1 class="dsp">The people<br>on the <span class="italic hot">line</span></h1>
    <p>Two kitchens, one recipe book, and the people who cook it every day.</p>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="cards rv">
      <div class="card"><h3>Kitchen leadership</h3><p>Add a short bio and a photo for your head chef or kitchen manager at each location. Real names and faces are what make this page rank and convert.</p></div>
      <div class="card"><h3>Front of house</h3><p>Add the manager who runs service. Guests recognise them and Google rewards pages with real people on them.</p></div>
      <div class="card"><h3>Founder</h3><p>Add the founding story in first person — who started it and why halal Italian-American. This is the paragraph journalists quote.</p></div>
    </div>
    <div class="callout rv" style="margin-top:36px">
      <b>Placeholder page</b>
      <p>This page is built and linked but needs real names, roles, photos and one-line bios before launch. It exists because your competitor has one and it earns local trust signals — but empty is worse than absent, so fill it or remove it from the nav.</p>
    </div>
  </div>
</section>
"""
p += foot(0)
write("team.html", p, "0.4")


# =========================================================== CAREERS
p = head("Careers | Bite More — Now Hiring in Buckhead &amp; Duluth, GA",
         "Join Bite More. Kitchen and front-of-house roles at our Buckhead and Duluth locations in Atlanta, GA. Apply online.",
         "careers.html", 0, {"@context": "https://schema.org", "@type": "WebPage",
                             "name": "Careers at Bite More"})
p += nav(0)
p += crumbs(0, [("Careers", "")])
p += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">Careers</p>
    <h1 class="dsp">Come cook<br>with <span class="italic hot">us</span></h1>
    <p>We're hiring at both Atlanta kitchens. If you care about doing it properly and showing up when you said you would, we want to talk.</p>
    <a class="btn btn-solid" href="mailto:careers@bitemore.us">Apply now</a>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="sec-head rv"><p class="eyebrow">Open roles</p><h2 class="dsp">What we're<br>hiring for</h2></div>
    <div class="cards rv">
      <div class="card"><h3>Line cook</h3><p>Buckhead and Duluth. Flat top, fry station and pasta. Experience helps; attitude matters more.</p></div>
      <div class="card"><h3>Prep cook</h3><p>Morning shifts. Sauces, dough and portioning to our build sheets.</p></div>
      <div class="card"><h3>Cashier / front of house</h3><p>Taking orders, running the counter, keeping the dining room right.</p></div>
      <div class="card"><h3>Shift lead</h3><p>Running service, managing the line, closing the store.</p></div>
      <div class="card"><h3>Catering driver</h3><p>Delivering and setting up trays for events. Clean license required.</p></div>
      <div class="card"><h3>Always open</h3><p>Not on the list? Send your details anyway — we hire good people when we meet them.</p></div>
    </div>
    <div class="callout rv" style="margin-top:36px">
      <b>Before launch</b>
      <p>Confirm which of these roles are actually open, add pay ranges, and set up careers@bitemore.us. Job postings with pay ranges get materially more applicants — and Google indexes them separately.</p>
    </div>
    <p style="margin-top:34px"><a class="btn btn-solid" href="mailto:careers@bitemore.us">Send your details</a></p>
  </div>
</section>
"""
p += foot(0)
write("careers.html", p, "0.5")


# =========================================================== GIFT CARDS
p = head("Gift Cards | Bite More — Atlanta &amp; Duluth, GA",
         "Bite More gift cards for Buckhead and Duluth. Halal burgers, pasta and wings. Available in store — online gift cards coming soon.",
         "gift-cards.html", 0)
p += nav(0)
p += crumbs(0, [("Gift Cards", "")])
p += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">Gift cards</p>
    <h1 class="dsp">Give someone<br>a good <span class="italic hot">dinner</span></h1>
    <p>Redeemable at both Atlanta kitchens, on anything on the menu. Available at the counter today; online purchase is coming.</p>
    <a class="btn btn-solid" href="tel:+14705148473">Call to buy</a>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="cards rv">
      <div class="card"><h3>Any amount</h3><p>Set the value at the counter. No expiry, no fees.</p></div>
      <div class="card"><h3>Both locations</h3><p>Use at Buckhead or Duluth, dine in or pickup.</p></div>
      <div class="card"><h3>Good for teams</h3><p>Buying for staff or clients? Call us and we'll sort a batch.</p></div>
    </div>
    <div class="callout rv" style="margin-top:36px">
      <b>Revenue note</b>
      <p>Gift cards are prepaid, commission-free revenue and they bring a new customer with them. Worth enabling digital gift cards when you migrate off the DoorDash storefront — your closest competitor sells them online.</p>
    </div>
  </div>
</section>
"""
p += foot(0)
write("gift-cards.html", p, "0.4")


# =========================================================== FRANCHISE
fr_faqs = [
    ("Which markets are open?", "Most of them. We're awarding territory selectively and prioritising markets with an underserved halal-observant population and a strong operator ready to run it."),
    ("Do I need restaurant experience?", "It helps significantly. We'll also consider investor groups who bring an experienced operating partner."),
    ("What does the buildout look like?", "A compact fast-casual footprint with dine-in seating, a standardised kitchen layout and an equipment spec we provide. No bar, no alcohol licence."),
    ("Do I have to source halal?", "Yes. It's the foundation of the brand and it's written into the agreement. We provide the approved vendor list."),
]
p = head("Franchise | Bite More — Own a Halal Italian-American Kitchen",
         "Franchise Bite More. Two proven Atlanta kitchens, documented recipes, a trademarked brand and an open category. Selecting operators market by market.",
         "franchise.html", 0, faq_ld(fr_faqs))
p += nav(0, "franchise.html")
p += crumbs(0, [("Franchise", "")])
p += f"""<section class="phero">
  <div class="wrap">
    <p class="eyebrow">Franchise</p>
    <h1 class="dsp">Bring Bite More<br>to <span class="italic hot">your</span> market</h1>
    <p>Italian-American food travels everywhere and never goes out of style. We've built it into a fast-casual system with documented recipes, a trademarked brand and two Atlanta kitchens running the playbook.</p>
    <a class="btn btn-solid" href="#apply">Start the conversation</a>
  </div>
</section>
{TICKER}
<section class="sec">
  <div class="wrap">
    <div class="sec-head rv">
      <p class="eyebrow">The opportunity</p>
      <h2 class="dsp">An open lane<br>in a crowded market</h2>
      <p>Pasta is one of the most reliable categories in American restaurants — high margin and familiar to everyone — and it's mostly sold either as a $30 sit-down plate or a frozen one. We put it in a fast-casual box with burgers and wings beside it, then sourced the whole menu halal.</p>
    </div>
    <div class="cards rv">
      <div class="card"><span class="num">01</span><h3>Proven in two kitchens</h3><p>Not a concept deck. Two operating Atlanta locations with real sales history and {RATING_COUNT}+ delivery ratings.</p></div>
      <div class="card"><span class="num">02</span><h3>Documented systems</h3><p>Build sheets, prep guides, a proprietary spice system and standardised recipes — written down so the food travels.</p></div>
      <div class="card"><span class="num">03</span><h3>Trademarked brand</h3><p>A registered USPTO trademark and an identity built for expansion.</p></div>
      <div class="card"><span class="num">04</span><h3>Efficient footprint</h3><p>Fast-casual format, compact kitchen, no bar programme and no alcohol licence to chase.</p></div>
      <div class="card"><span class="num">05</span><h3>Four revenue lines</h3><p>Dine-in, pickup, delivery and catering out of the same kitchen.</p></div>
      <div class="card"><span class="num">06</span><h3>A wider table</h3><p>Halal sourcing opens a customer base that travels for food it trusts, without narrowing who else walks in.</p></div>
    </div>
  </div>
</section>
<section class="sec panel" id="apply">
  <div class="wrap split even">
    <div class="rv">
      <p class="eyebrow">Apply</p>
      <h2 class="dsp" style="font-size:clamp(30px,4vw,50px);margin:12px 0 0">Tell us about<br>your market</h2>
      <p style="color:var(--muted);margin-top:18px;max-width:44ch">Send the basics and our team will follow up to set an introduction call. Everything you share stays confidential.</p>
    </div>
    <div class="form rv">
      <div class="fgrid">
        <div class="field"><label for="fname">Your name</label><input id="fname" type="text"></div>
        <div class="field"><label for="fphone">Phone</label><input id="fphone" type="tel"></div>
        <div class="field"><label for="femail">Email</label><input id="femail" type="email"></div>
        <div class="field"><label for="fmarket">Target market</label><input id="fmarket" type="text" placeholder="City and state"></div>
        <div class="field full"><label for="fexp">Restaurant experience</label><select id="fexp"><option>Currently operate restaurants</option><option>Previously operated restaurants</option><option>Multi-unit franchisee, another brand</option><option>Investor, will hire an operator</option><option>New to the industry</option></select></div>
        <div class="field full"><label for="fnotes">Anything else</label><textarea id="fnotes" placeholder="Sites you're considering, timeline, questions"></textarea></div>
      </div>
      <a class="btn btn-solid" href="mailto:franchise@bitemore.us">Submit application</a>
      <p class="form-note">Submitting this is not a franchise offer. A franchise offering is made only through a franchise disclosure document where required by law.</p>
    </div>
  </div>
</section>
"""
p += faq_html(fr_faqs, "Franchise FAQ")
p += foot(0)
write("franchise.html", p, "0.7")


# =========================================================== WRITE FILES
for path, (html, freq, pri) in pages.items():
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)

# sitemap
urls = "".join(
    f"  <url><loc>{DOMAIN}/{p}</loc><changefreq>{f}</changefreq><priority>{pr}</priority></url>\n"
    for p, (h, f, pr) in sorted(pages.items()))
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')

with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(f"""# Bite More — allow everything, including AI crawlers.
# The previous site returned HTTP 403 to crawlers, which is why it had
# zero LLM mentions and only 353 ranking keywords.
User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
""")

print(f"{len(pages)} pages written")
for p in sorted(pages):
    print("  ", p)

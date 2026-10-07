#!/usr/bin/env python3
"""
Builds app.html and thanks.html by cloning the shell of about.html, so the
nav, footer, GTM, analytics and script tags stay identical to every other
page and cannot drift.

The app page ships with a "Notify me" capture rather than store buttons:
the App Store and Google Play URLs have not been supplied, and dead or
invented store links are worse than an honest waitlist.
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
HOST = "https://bitemore.us"
ORDER = "https://order.online/business/bite-more-13060526"

src = open(os.path.join(ROOT, "about.html"), encoding="utf-8").read()

# --- split the template -----------------------------------------------------
head_end = src.index("</head>")
head = src[:head_end]
rest = src[head_end:]

crumbs = re.search(r'<nav class="crumbs">.*?</nav>\n', rest, re.S)
shell_top = rest[: crumbs.start()]          # </head> ... <header> closed
foot_start = rest.index('<footer class="foot">')
shell_bottom = rest[foot_start:]            # footer + scripts + </body></html>


def head_for(title, desc, canon, extra_ld=""):
    h = head
    h = re.sub(r"<title>.*?</title>", "<title>%s</title>" % title, h, flags=re.S)
    h = re.sub(r'<meta name="description" content=".*?">',
               '<meta name="description" content="%s">' % desc, h, flags=re.S)
    h = re.sub(r'<link rel="canonical" href=".*?">',
               '<link rel="canonical" href="%s">' % canon, h)
    h = re.sub(r'<meta property="og:title" content=".*?">',
               '<meta property="og:title" content="%s">' % title, h, flags=re.S)
    h = re.sub(r'<meta property="og:description" content=".*?">',
               '<meta property="og:description" content="%s">' % desc, h, flags=re.S)
    h = re.sub(r'<meta property="og:url" content=".*?">',
               '<meta property="og:url" content="%s">' % canon, h)
    # strip the About page's own JSON-LD graph, keep the Restaurant/Org ones out
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\n', "", h, flags=re.S)
    return h + extra_ld


def crumb(label, slug):
    return ('<nav class="crumbs"><div class="wrap"><a href="./">Home</a> › '
            '<span>%s</span></div></nav>\n' % label)


# ============================================================== app.html
APP_TITLE = ("Bite More App | Order Halal Italian-American in Buckhead "
             "&amp; Duluth, Atlanta")
APP_DESC = ("Get the Bite More app for halal Italian-American food in Buckhead "
            "and Duluth, Atlanta. Order direct, skip the delivery-app markup, "
            "and earn on every order. Join the list and we will send it the day "
            "it launches.")

APP_LD = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "MobileApplication",
      "@id": "%(host)s/app#app",
      "name": "Bite More",
      "applicationCategory": "FoodAndDrinkApplication",
      "operatingSystem": "iOS, Android",
      "description": "Order halal Italian-American food direct from Bite More in Buckhead and Duluth, Atlanta. Pasta, smash burgers, wings and loaded fries, with rewards on every direct order.",
      "url": "%(host)s/app",
      "inLanguage": "en-US",
      "availableOnDevice": "iPhone, iPad, Android phone, Android tablet",
      "releaseNotes": "In development. Join the list to be told when it launches.",
      "publisher": {
        "@type": "Organization",
        "@id": "%(host)s/#organization",
        "name": "Bite More Brands LLC"
      }
    },
    {
      "@type": "WebPage",
      "@id": "%(host)s/app",
      "url": "%(host)s/app",
      "name": "Bite More App",
      "description": "The Bite More app for halal Italian-American food in Buckhead and Duluth, Atlanta.",
      "isPartOf": {"@id": "%(host)s/#website"},
      "about": {"@id": "%(host)s/app#app"},
      "breadcrumb": {"@id": "%(host)s/app#breadcrumb"}
    },
    {
      "@type": "BreadcrumbList",
      "@id": "%(host)s/app#breadcrumb",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "%(host)s/"},
        {"@type": "ListItem", "position": 2, "name": "App", "item": "%(host)s/app"}
      ]
    },
    {
      "@type": "FAQPage",
      "@id": "%(host)s/app#faq",
      "mainEntity": [
        {"@type": "Question", "name": "Is the Bite More app available yet?",
         "acceptedAnswer": {"@type": "Answer", "text": "Not yet. It is in development. Join the list on this page and we will email you the download link the day it goes live on the App Store and Google Play."}},
        {"@type": "Question", "name": "Can I order from Bite More in the meantime?",
         "acceptedAnswer": {"@type": "Answer", "text": "Yes. Order direct from our online menu, call either kitchen, or walk in. Buckhead is at 3150 Roswell Rd NW, Suite A1, and Duluth is at 2148 Duluth Hwy 120, Suite 117."}},
        {"@type": "Question", "name": "Why order through the app instead of a delivery app?",
         "acceptedAnswer": {"@type": "Answer", "text": "A third-party delivery app can take 15 to 30 percent of the order in commission. Ordering direct keeps that in the kitchen, which is what lets us hold our menu pricing."}},
        {"@type": "Question", "name": "Will the app work for both Buckhead and Duluth?",
         "acceptedAnswer": {"@type": "Answer", "text": "Yes. You pick your kitchen when you order, so a Duluth order is never routed to Buckhead."}},
        {"@type": "Question", "name": "Is all the food halal?",
         "acceptedAnswer": {"@type": "Answer", "text": "Yes. Every protein at both Bite More kitchens is 100%% halal. It is how we buy, not a separate menu."}}
      ]
    }
  ]
}
</script>
''' % {"host": HOST}

APP_BODY = '''<section class="phero">
  <div class="wrap">
    <p class="eyebrow">Bite More app</p>
    <h1 class="dsp">Order direct.<br><span class="italic hot">Keep</span> the markup.</h1>
    <p>Halal Italian-American in Buckhead and Duluth. The app is in development — join the list and we will send you the download the day it lands, along with the offers we only run for our own list.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="app-hero">
      <div>
        <h2 class="dsp" style="font-size:clamp(26px,3.4vw,40px)">What it will do</h2>
        <ul class="std-list" style="margin-top:26px">
          <li><b>One tap reorder</b><span>Your usual Cajun Alfredo or Oklahoma Onion Smash, without rebuilding the order every time.</span></li>
          <li><b>Pick your kitchen</b><span>Buckhead or Duluth, chosen before you order — never routed to the wrong one.</span></li>
          <li><b>Rewards on direct orders</b><span>Points on every order placed with us rather than through a third-party app.</span></li>
          <li><b>Live order status</b><span>From the moment it hits the pass to the moment it is ready.</span></li>
          <li><b>App-only offers</b><span>Run for our own list, not on the delivery platforms.</span></li>
          <li><b>Catering in a few taps</b><span>Our catering packages feed 10 to 100+, booked straight from your phone.</span></li>
        </ul>
        <div class="app-stores">
          <span class="store-btn soon" aria-disabled="true">App Store — coming soon</span>
          <span class="store-btn soon" aria-disabled="true">Google Play — coming soon</span>
        </div>
        <p class="app-note">We are not linking to a store page that does not exist yet. Join the list below and you will hear from us first.</p>
      </div>
      <div>
        <div class="app-shots" aria-hidden="true">
          <div class="app-shot"><span>Menu</span></div>
          <div class="app-shot"><span>Reorder</span></div>
          <div class="app-shot"><span>Rewards</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec panel">
  <div class="wrap narrow">
    <div class="sec-head rv">
      <p class="eyebrow">Get it first</p>
      <h2 class="dsp">Tell us where<br>to send it</h2>
      <p>First name and email is all we need. No spam, and you can unsubscribe from any message we send.</p>
    </div>
    <form class="form" name="bite-more-app-waitlist" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="thanks">
      <input type="hidden" name="form-name" value="bite-more-app-waitlist">
      <p class="bm-lead-hp"><label>Leave blank<input name="bot-field"></label></p>
      <div class="field">
        <label for="appName">First name</label>
        <input id="appName" name="first_name" type="text" autocomplete="given-name" required>
      </div>
      <div class="field">
        <label for="appEmail">Email</label>
        <input id="appEmail" name="email" type="email" autocomplete="email" required>
      </div>
      <div class="field">
        <label for="appPhone">Phone (optional)</label>
        <input id="appPhone" name="phone" type="tel" autocomplete="tel">
      </div>
      <div class="field">
        <label for="appLoc">Closest kitchen</label>
        <select id="appLoc" name="location">
          <option value="buckhead">Buckhead</option>
          <option value="duluth">Duluth</option>
          <option value="either">Either</option>
        </select>
      </div>
      <button type="submit" class="btn btn-solid" style="margin-top:8px">Put me on the list</button>
      <p class="form-note">We will only use this to tell you about the app and our own offers.</p>
    </form>
  </div>
</section>

<section class="sec">
  <div class="wrap narrow">
    <div class="sec-head rv">
      <p class="eyebrow">Order now</p>
      <h2 class="dsp">You do not have<br>to wait for the app</h2>
      <p>Order direct from the online menu today, or call either kitchen. Both locations trade seven days a week, and Buckhead runs till 3am on Friday and Saturday.</p>
    </div>
    <p style="margin-top:28px">
      <a class="btn btn-solid" href="%(order)s">Order Now</a>
      <a class="btn btn-ghost" href="menu">See the menu</a>
      <a class="btn btn-ghost" href="locations">Both locations</a>
    </p>
  </div>
</section>

<section class="sec panel">
  <div class="wrap narrow">
    <div class="sec-head rv">
      <h2 class="dsp">Questions we get</h2>
    </div>
    <div class="faq">
      <details><summary>Is the Bite More app available yet?</summary><p>Not yet — it is in development. Join the list on this page and we will email you the download link the day it goes live on the App Store and Google Play.</p></details>
      <details><summary>Can I order from Bite More in the meantime?</summary><p>Yes. Order direct from our online menu, call either kitchen, or walk in. Buckhead is at 3150 Roswell Rd NW, Suite A1, Atlanta. Duluth is at 2148 Duluth Hwy 120, Suite 117.</p></details>
      <details><summary>Why order through the app instead of a delivery app?</summary><p>A third-party delivery app can take 15 to 30 percent of the order in commission. Ordering direct keeps that in the kitchen, which is what lets us hold our menu pricing.</p></details>
      <details><summary>Will the app work for both Buckhead and Duluth?</summary><p>Yes. You pick your kitchen when you order, so a Duluth order is never routed to Buckhead.</p></details>
      <details><summary>Is all the food halal?</summary><p>Yes. Every protein at both Bite More kitchens is 100%% halal. It is how we buy, not a separate menu or a special order.</p></details>
    </div>
  </div>
</section>
''' % {"order": ORDER}

app = (head_for(APP_TITLE, APP_DESC, HOST + "/app", APP_LD)
       + shell_top
       + crumb("App", "app")
       + APP_BODY
       + shell_bottom)

open(os.path.join(ROOT, "app.html"), "w", encoding="utf-8").write(app)

# =========================================================== thanks.html
T_TITLE = "Thanks | Bite More — Halal Italian-American, Buckhead &amp; Duluth"
T_DESC = ("Thanks for joining the Bite More list. Halal Italian-American food "
          "in Buckhead and Duluth, Atlanta.")
T_LD = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "@id": "%(host)s/thanks",
  "url": "%(host)s/thanks",
  "name": "Thanks",
  "isPartOf": {"@id": "%(host)s/#website"}
}
</script>
''' % {"host": HOST}

T_BODY = '''<section class="phero">
  <div class="wrap">
    <p class="eyebrow">You are on the list</p>
    <h1 class="dsp">Thanks.<br><span class="italic hot">Now</span> eat something.</h1>
    <p>We have got your details. You will hear from us when the app launches, and when we run something worth knowing about. In the meantime the kitchens are open.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap narrow">
    <p>
      <a class="btn btn-solid" href="%(order)s">Order Now</a>
      <a class="btn btn-ghost" href="menu">See the menu</a>
      <a class="btn btn-ghost" href="locations">Both locations</a>
    </p>
  </div>
</section>
''' % {"order": ORDER}

thanks = (head_for(T_TITLE, T_DESC, HOST + "/thanks", T_LD)
          + shell_top
          + crumb("Thanks", "thanks")
          + T_BODY
          + shell_bottom)
# a confirmation page has no business in search results
thanks = thanks.replace('<meta name="robots" content="index, follow">',
                        '<meta name="robots" content="noindex, follow">')
open(os.path.join(ROOT, "thanks.html"), "w", encoding="utf-8").write(thanks)

print("built app.html (%d bytes) and thanks.html (%d bytes)" % (len(app), len(thanks)))

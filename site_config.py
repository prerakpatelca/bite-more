#!/usr/bin/env python3
"""
BITE MORE — SINGLE SOURCE OF TRUTH
==================================
Every location fact, phone number, hour and analytics ID lives here and
NOWHERE else. Generators and validators both import this module.

If a value is wrong here, it is wrong everywhere — which is the point.
Previously these were hard-coded across dozens of files, which is how the
old Duluth phone number and the "Closed Monday" error survived for weeks.
"""

PRODUCTION_HOST = "https://bitemore.us"
NETLIFY_HOST = "https://bite-more.netlify.app"

# Ordering. One URL today; per-location URLs go here when they exist.
ORDER_URL = "https://order.online/business/bite-more-13060526"
ORDER_URL_BUCKHEAD = ORDER_URL   # TODO: replace when a Buckhead-specific URL exists
ORDER_URL_DULUTH = ORDER_URL     # TODO: replace when a Duluth-specific URL exists

# ---------------------------------------------------------------------------
# LOCATIONS — approved values, confirmed by the owner 2026-08-13
# ---------------------------------------------------------------------------
LOCATIONS = {
    "buckhead": {
        "slug": "buckhead",
        "name": "Buckhead",
        "legal_name": "Bite More Buckhead",
        "street": "3150 Roswell Rd NW, Suite A1",
        "city": "Atlanta",
        "region": "GA",
        "zip": "30305",
        "phone_display": "(470) 514-8473",
        "phone_raw": "+14705148473",
        "lat": 33.8404,
        "lng": -84.3800,
        "maps": "https://maps.google.com/?q=3150+Roswell+Rd+NW+Suite+A1+Atlanta+GA+30305",
        "order_url": ORDER_URL_BUCKHEAD,
        "cross_street": "On Roswell Rd between Peachtree Rd and Piedmont Rd — 2 minutes from the Buckhead Theatre",
        "hours_human": [
            ("Monday – Wednesday", "11:00 am – 12:00 am"),
            ("Thursday", "11:00 am – 1:00 am"),
            ("Friday – Saturday", "11:00 am – 3:00 am", "late"),
            ("Sunday", "11:00 am – 1:00 am"),
        ],
        "hours_schema": [
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Monday", "Tuesday", "Wednesday"], "opens": "11:00", "closes": "00:00"},
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Thursday"], "opens": "11:00", "closes": "01:00"},
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Friday", "Saturday"], "opens": "11:00", "closes": "03:00"},
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Sunday"], "opens": "11:00", "closes": "01:00"},
        ],
        "hours_sentence": "11am–12am Monday to Wednesday, 11am–1am Thursday, 11am–3am Friday and Saturday, and 11am–1am Sunday.",
        # No verified Google Place ID supplied. Review CTA stays disabled while empty.
        "google_place_id": "",
    },
    "duluth": {
        "slug": "duluth",
        "name": "Duluth",
        "legal_name": "Bite More Duluth",
        "street": "2148 Duluth Hwy 120, Suite 117",
        "city": "Duluth",
        "region": "GA",
        "zip": "30097",
        "phone_display": "(943) 296-4518",
        "phone_raw": "+19432964518",
        "lat": 33.9800,
        "lng": -84.1200,
        "maps": "https://maps.google.com/?q=2148+Duluth+Hwy+120+Suite+117+Duluth+GA+30097",
        "order_url": ORDER_URL_DULUTH,
        "cross_street": "On Duluth Hwy 120 near Peachtree Industrial Blvd — 5 minutes from the office parks",
        "hours_human": [
            ("Monday – Wednesday", "11:00 am – 9:00 pm"),
            ("Thursday – Sunday", "11:00 am – 11:00 pm"),
        ],
        "hours_schema": [
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Monday", "Tuesday", "Wednesday"], "opens": "11:00", "closes": "21:00"},
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Thursday", "Friday", "Saturday", "Sunday"], "opens": "11:00", "closes": "23:00"},
        ],
        "hours_sentence": "11am–9pm Monday to Wednesday and 11am–11pm Thursday to Sunday.",
        "google_place_id": "",
    },
}

# Retired values. The validator fails the build if any of these reappear.
FORBIDDEN_STRINGS = [
    "(321) 333-2984", "321-333-2984", "321 333 2984", "3213332984", "+13213332984",
    "PLACE_ID_BUCKHEAD", "PLACE_ID_DULUTH",
    "G-XXXXXXXXXX", "'PIXEL_ID'", '"PIXEL_ID"',   # placeholder VALUES, not the config key names
    "order.online/business/13060526",   # numeric-only order URL, superseded
]

# ---------------------------------------------------------------------------
# ANALYTICS — no IDs supplied. Empty = integration stays inert.
# Fill these two values in assets/config.js to activate. Nothing else to change.
# ---------------------------------------------------------------------------
GA4_MEASUREMENT_ID = ""
META_PIXEL_ID = ""

TRACKED_EVENTS = [
    "order_online_click", "order_buckhead", "order_duluth", "phone_click",
    "directions_click", "catering_lead", "franchise_lead", "gift_card_click",
]

# ---------------------------------------------------------------------------
# RATINGS — visible social proof only.
# Verified 2026-08: DoorDash 4.3 (1,000+), UberEats 4.3 (1,000+).
# NOT verified: 4.8, 4.9, 1,100+. Google shows a different, lower figure on a
# much smaller sample, so these are labelled "delivery ratings" everywhere and
# are deliberately NOT emitted as aggregateRating structured data.
# ---------------------------------------------------------------------------
RATING_DISPLAY = "4.3"
RATING_COUNT_DISPLAY = "1,000+"
RATING_LABEL = "delivery ratings"
EMIT_AGGREGATE_RATING = False

NOINDEX_PAGES = {"coming-soon.html", "tags/tagliatelle.html", "404.html"}


def location(slug):
    return LOCATIONS[slug]


def hours_rows_html(slug):
    """Render the visible hours table for one location."""
    out = []
    for row in LOCATIONS[slug]["hours_human"]:
        day, time = row[0], row[1]
        cls = ' class="late"' if len(row) > 2 else ""
        out.append(f'<div><span class="day">{day}</span><span{cls}>{time}</span></div>')
    return "".join(out)


def clean_url(path):
    """index.html -> /, foo.html -> /foo, blog/index.html -> /blog/"""
    if path == "index.html":
        return "/"
    if path.endswith("/index.html"):
        return "/" + path[:-len("index.html")]
    if path.endswith(".html"):
        return "/" + path[:-5]
    return "/" + path


def canonical(path):
    return PRODUCTION_HOST + clean_url(path)

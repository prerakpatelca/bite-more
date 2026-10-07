# ANALYTICS IMPLEMENTATION REPORT — BITE MORE

**Date:** 14 August 2026
**Scope:** 108 HTML pages
**Verified with:** `analytics_check.py` (static scan) and `test_analytics.js`
(jsdom — loads real pages, dispatches real clicks, asserts real dataLayer output)

---

## INSTALLED IDs

```
GTM:  GTM-PT8568DB
GA4:  G-220KLBJVG4   (configured inside GTM — NOT hard-coded on the site)
```

---

## PRE-EXISTING TRACKING FOUND

A project-wide search for `GTM-`, `G-`, `gtag(`, `googletagmanager.com`,
`google-analytics.com`, `dataLayer`, `analytics.js`, `gtag.js` returned **one**
implementation: `assets/analytics.js`, which contained a direct `gtag.js` loader
and a Meta Pixel loader, both inert behind empty IDs.

**Consolidated.** The gtag.js loader was removed — GA4 now loads only via GTM, so
duplicate page_views are structurally impossible. The Meta Pixel loader was removed
because no Pixel ID exists. No unrelated integration was touched.

```
DUPLICATE GTM INSTALLATIONS:        0
WRONG GTM IDs:                      0
HARDCODED DUPLICATE GA4:            0
```

---

## WEBSITE INSTALLATION

| Check | Result |
|---|---|
| GTM head snippet | **PASS** — 108/108 |
| GTM noscript | **PASS** — 108/108 |
| All pages | **PASS** |
| Duplicate GTM | **PASS** — 0 |
| Duplicate GA4 | **PASS** — 0 |

```
TOTAL HTML PAGES:            108
PAGES WITH GTM HEAD:         108
PAGES MISSING GTM HEAD:        0
PAGES WITH GTM NOSCRIPT:     108
PAGES MISSING GTM NOSCRIPT:    0
```

Head snippet sits immediately after the viewport meta — as high as possible while
keeping charset and viewport first, which browsers require. Loads async, does not
block render. Noscript iframe is the first element after `<body>`.

---

## EVENTS — TESTED, NOT ASSUMED

`test_analytics.js` loads the actual generated pages in jsdom and dispatches actual
click events. **22/22 assertions pass.**

| Event | Buckhead | Duluth | Result |
|---|---|---|---|
| menu_view | N/A | N/A | **PASS** — fires once on /menu, not elsewhere |
| order_online_click | Tested | Tested | **PASS** — correct location on both |
| order_buckhead | Tested | N/A | **PASS** — and verified it does NOT fire on Duluth |
| order_duluth | N/A | Tested | **PASS** — and verified it does NOT fire on Buckhead |
| phone_click | Tested | Tested | **PASS** |
| directions_click | Tested | Tested | **PASS** |
| catering_lead | Tested | Tested | **PASS** — callback fires; click does NOT |
| franchise_lead | Tested | — | **PASS** — callback fires |
| gift_card_click | Tested | — | **PASS** |
| view_item | Tested | — | **PASS** — real item name and category |
| select_location | Tested | Tested | **PASS** |
| purchase | — | — | **NOT IMPLEMENTED** — asserted absent on order clicks |

Additional assertions that pass: rapid double-click fires once, not twice; every
`location` value is `buckhead`, `duluth`, `unknown` or `all` — no variants.

### One design decision worth flagging

The homepage **"Order Buckhead" / "Order Duluth"** buttons navigate to the location
pages, not to checkout — deliberate, so nobody orders from the wrong kitchen. They
are therefore **not** order clicks. They fire `select_location`, not
`order_online_click`. Counting them as order intent would have inflated the metric
by every visitor who simply chose a store. The real order CTA on each location page
fires the real event.

### Lead events — an honest limitation

The catering and franchise forms are currently **`mailto:` links with no submission
callback**. A successful submission cannot be confirmed client-side. Firing on click
would count every abandoned draft as a lead.

So they do not fire on click. The plumbing is built and tested:

```javascript
window.bmCateringLead('buckhead');   // call from a real success callback
window.bmFranchiseLead();
```

**To activate:** move the forms to a real backend (Jotform is already in your
connectors, or Netlify Forms) and call these on success. Until then:
`catering_lead` and `franchise_lead` are **implemented but will never fire in
production**, which is correct — better zero leads than fabricated ones.

---

## PURCHASE / REVENUE

```
purchase:  ORDER PLATFORM INTEGRATION REQUIRED
```

Checkout happens on `order.online` — a DoorDash domain we cannot tag. See
`ORDER_TRACKING_INTEGRATION_REPORT.md` for what was verified, what wasn't, and the
six questions to put to DoorDash.

---

## UTM AND CLICK-ID PRESERVATION

Audited. The site **strips nothing**: no JS rewrites `location.search`, no redirect
drops a query string. Netlify redirects use `:splat`, which preserves query
parameters through the host and legacy-path redirects.

`utm_*`, `gclid`, `gbraid`, `wbraid` and `fbclid` all survive to GTM.

**Caveat:** parameters are preserved *on our site*. They are not forwarded into the
`order.online` checkout, because the order link is static. If DoorDash supports
query-parameter passthrough, that is worth adding.

---

## PERFORMANCE AND SEO

- GTM loads async; no render blocking
- No npm packages, no tracking libraries; event layer is ~3KB unminified
- No interference with video autoplay, mobile nav or the sticky CTA — full SEO
  suite re-run after implementation: **GO FOR PRODUCTION**, all 20 checks pass
- Titles, descriptions, canonicals, schema, H1s, sitemap: unchanged

---

## EXTERNAL SETUP STILL REQUIRED

| Item | Status |
|---|---|
| GTM website installation | **COMPLETE** |
| GA4 tag inside GTM | **REQUIRES GTM ACCOUNT CONFIGURATION** |
| Google Ads | **CONVERSION ID + LABELS REQUIRED** |
| Meta | **PIXEL ID REQUIRED** |
| Purchase / revenue | **ORDER PLATFORM INTEGRATION REQUIRED** |
| Tag Assistant verification | **REQUIRED AFTER DEPLOYMENT** |

### What you must do inside GTM (I have no account access)

1. **Google Tag** → Tag ID `G-220KLBJVG4` → trigger **Initialization — All Pages**
2. Create **Custom Event triggers** for each event name below
3. Create **GA4 Event tags** for each, passing the dataLayer variables
4. Create **Data Layer Variables**: `location`, `order_type`, `page_type`,
   `item_name`, `item_category`, `lead_type`, `link_type`
5. **Preview** on: homepage, /menu, /buckhead, /duluth, /catering, one burger page,
   one pasta page
6. Confirm GTM loads once, GA4 loads once, no duplicate page_view
7. **Publish**, then check GA4 **DebugView**
8. Mark these as **Key Events** in GA4: `order_online_click`, `order_buckhead`,
   `order_duluth`, `catering_lead`, `phone_click`

Event names to register: `menu_view`, `view_item`, `select_location`,
`order_online_click`, `order_buckhead`, `order_duluth`, `phone_click`,
`directions_click`, `gift_card_click`, `catering_lead`, `franchise_lead`.

**GA4 is not yet collecting data.** The container is on the site; the tag inside it
is not configured. Both are required.

---

## FILES CHANGED

| File | Change |
|---|---|
| 108 × `*.html` | GTM head + noscript; body data attributes for page-level events |
| `assets/config.js` | GTM + GA4 IDs recorded; gtag loader removed; Pixel left empty |
| `assets/analytics.js` | Rewritten as a pure dataLayer layer — no Google tag loading |
| `analytics_check.py` | **New** — static installation verification |
| `test_analytics.js` | **New** — jsdom behavioural test suite, 22 assertions |
| `ANALYTICS_IMPLEMENTATION_REPORT.md` | **New** — this file |
| `ORDER_TRACKING_INTEGRATION_REPORT.md` | **New** |

Nothing was deployed. The build is packaged and waiting for your instruction.

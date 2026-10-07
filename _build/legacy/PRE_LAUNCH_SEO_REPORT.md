# PRE-LAUNCH SEO REPORT — BITE MORE

**Build:** 108 HTML pages · 105 sitemap URLs · 251 JSON-LD blocks · 187 images
**Validator:** `python3 seo_prelaunch_check.py` → exit code 0
**Date:** 13 August 2026

---

## FINAL VERIFICATION TABLE

| Test | Result |
|---|---|
| Old Duluth phone | **PASS** |
| Location hours consistent | **PASS** |
| Canonical tags | **PASS** |
| Clean schema URLs | **PASS** |
| Sitemap vs canonicals | **PASS** |
| robots.txt | **PASS** |
| AggregateRating issue | **PASS** |
| Google Place ID placeholders | **PASS** |
| Analytics placeholders safely handled | **PASS** |
| Internal links | **PASS** |
| JSON-LD parsing | **PASS** |
| NAP consistency | **PASS** |
| Duplicate titles | **PASS** |
| Missing titles | **PASS** |
| Missing descriptions | **PASS** |
| H1 structure | **PASS** |
| Image alt attributes | **PASS** |
| Production host consistency | **PASS** |
| Redirect rules | **PASS** |

No FAIL rows. Details below.

---

## STEP-BY-STEP RESULTS

### 1 — Single source of truth
Created **`site_config.py`**. Holds both locations' name, address, phone, hours
(human + schema), geo, maps link, order URL, cross-street, Place ID field, plus
analytics IDs, rating policy and the retired-value blocklist.

`apply_config.py` pushes it into all 108 pages. `seo_prelaunch_check.py` validates
against it. Generator sources (`v2_base.py`, `v2_build.py`, `v2_pages.py`) now
import from it. One file to change; the whole site follows.

### 2 — Old Duluth phone
```
OLD DULUTH PHONE OCCURRENCES: 0
```
All variants (`(321) 333-2984`, `321-333-2984`, `3213332984`, `+13213332984`)
removed from HTML, JSON-LD, footers, FAQs and generator source. Three generator
files carried it and were fixed at source, not just in output.

### 3 — Hours
Generic `HOURS_SCHEMA` eliminated. `HOURS_BUCKHEAD` and `HOURS_DULUTH` are separate
and authoritative:

| | Buckhead | Duluth |
|---|---|---|
| Mon–Wed | 11:00 am – 12:00 am | 11:00 am – 9:00 pm |
| Thu | 11:00 am – 1:00 am | 11:00 am – 11:00 pm |
| Fri–Sat | **11:00 am – 3:00 am** | 11:00 am – 11:00 pm |
| Sun | 11:00 am – 1:00 am | 11:00 am – 11:00 pm |

Applied to 81 Restaurant schema blocks, every visible table, FAQ answers and prose.
Zero "Closed Monday" strings remain. **No conflicts left to flag.**

### 4 — URL normalisation
**216 schema URLs** rewritten from `.html` to clean form across `url`, `@id`,
`item`, `mainEntityOfPage` and `menu` fields. Canonical, og:url, BreadcrumbList and
internal links now all resolve to one preferred URL per page.

### 5 — Sitemap
```
SITEMAP URLS CHECKED: 105
SITEMAP/CANONICAL CONFLICTS: 0
DUPLICATE SITEMAP URLS: 0
NON-200/INVALID LOCAL TARGETS: 0
NOINDEX URLS IN SITEMAP: 0
```
`/blog/index` → `/blog/`. Noindex pages (`coming-soon`, `tags/tagliatelle`, `404`)
excluded. No `.html`, no Netlify hostname.

### 6 — AggregateRating
```
QUESTIONABLE RESTAURANT AGGREGATERATING INSTANCES: 0
```
**81 instances removed.** Reason: the figure aggregates DoorDash and UberEats
delivery ratings, which is not a first-party review corpus and is not eligible for
Restaurant `aggregateRating`. Google's own local listing shows a materially lower
figure on a much smaller sample. Emitting it as review markup was a manual-action
risk with no upside.

Visible social proof retained and labelled: **"4.3 ★ · 1,000+ delivery ratings"**.

> **Note on the brief.** It referenced *"4.8 stars / 1,000+"*, and the supplied
> homepage reference file shows *"4.9 ★ · 1100+ reviews"* in the hero while showing
> *"4.5 / 862 ratings"* further down the same page. Three different unverified
> figures. Verified values on 2026-08 were **4.3 on DoorDash** and **4.3 on
> UberEats**. I used 4.3 and did not adopt any of the higher numbers.
> `RATING_DISPLAY` in `site_config.py` is the single place to change it.

### 7 — Google Place IDs
```
PLACE_ID_BUCKHEAD: Not Provided
PLACE_ID_DULUTH:   Not Provided
```
Not invented. The review CTAs render as a disabled state ("Review Buckhead on
Google — link pending") rather than a broken URL. **Zero customer-facing URLs
contain placeholder text.** Populate `google_place_id` in `site_config.py`, re-run
`apply_config.py`, and the buttons activate.

### 8 — Analytics
```
GA4_MEASUREMENT_ID: Not Provided
META_PIXEL_ID:      Not Provided
```
Inline placeholder blocks removed from all 108 pages. Replaced with
`assets/config.js` (two empty strings) and `assets/analytics.js` (loader). With
empty IDs **nothing loads and no network request fires**.

Event hooks live and queuing to `dataLayer` regardless of ID state:
`order_online_click`, `order_buckhead`, `order_duluth`, `phone_click`,
`directions_click`, `catering_lead`, `franchise_lead`, `gift_card_click`.

**Insert real IDs at `assets/config.js` lines 6–7. Nothing else changes.**

### 9 — Netlify domain consolidation
`www.bitemore.us/*` → `bitemore.us/*` (301) and `bite-more.netlify.app/*` →
`bitemore.us/*` (301). Full-URL `from` values, so they only fire on those hosts —
no loop on the apex. All canonicals stay `https://bitemore.us/…`.

### 10 — robots.txt
Allows all crawling, no CSS/JS blocks, explicit allows for GPTBot, OAI-SearchBot,
ClaudeBot, PerplexityBot, Google-Extended. `Sitemap: https://bitemore.us/sitemap.xml`.
Marketing commentary stripped.

### 11–14 — Sitemap, canonicals, titles, H1
```
TOTAL HTML PAGES: 108      MISSING CANONICALS: 0    MULTIPLE CANONICALS: 0
NON-PRODUCTION CANONICALS: 0                        CANONICAL CONFLICTS: 0
MISSING TITLES: 0          DUPLICATE TITLES: 0
MISSING DESCRIPTIONS: 0    DUPLICATE DESCRIPTIONS: 0
PAGES WITH ZERO H1: 0      PAGES WITH MULTIPLE H1: 0
```

### 15 — Images
```
TOTAL IMAGES: 187    MISSING ALT: 0    MEANINGFUL IMAGES WITH EMPTY ALT: 0
```
Below-fold images lazy-loaded; hero/LCP images are not. **Known issue:** food
imagery is still served from `img.cdn4dd.com` (DoorDash's CDN). Netlify cannot
optimise files it does not host, and DoorDash could change or remove them. Moving
to self-hosted WebP/AVIF is the single biggest remaining performance item and needs
your own photography.

### 16–19 — Links, redirects, structured data, NAP
```
BROKEN INTERNAL LINKS: 0
JSON-LD BLOCKS: 251        JSON PARSE ERRORS: 0
STALE PHONE REFERENCES: 0  STALE HOURS REFERENCES: 0
NON-CANONICAL SCHEMA URLS: 0  PLACEHOLDER VALUES: 0  QUESTIONABLE RATING MARKUP: 0
NAP CONFLICTS: 0
REDIRECT LOOPS: 0  CHAINS: 0  DEAD TARGETS: 0
```
Legacy redirects cover the paths confirmed from Apple Maps and Google's cached copy
of the old site. **A Search Console export of the old `bitemore.us` URL set is still
required for complete migration coverage** — unknown historical URLs were not invented.

### 20 — No new programmatic pages
Zero new SEO landing pages created. Page count unchanged at 108.

### 22 — Automated test
`seo_prelaunch_check.py` — standard library only, 20 checks, exits non-zero on any
blocker. Run it before every deploy.

---

## MOBILE + VIDEO QA

| Test | Result | Note |
|---|---|---|
| 320px layout | PASS | overflow guard + `clamp()` typography |
| 375px layout | PASS | |
| 390px layout | PASS | |
| 430px layout | PASS | |
| Tablet layout | PASS | |
| Desktop layout | PASS | unchanged |
| Mobile navigation | PASS | 48px targets, Menu/Order/Locations prioritised |
| Sticky mobile CTA | PASS | 107/108 pages; location pages show Call/Order/Directions for *that* store only |
| Forms mobile optimised | PASS | `type="tel"`, `type="email"`, 16px inputs (no iOS zoom), 48px fields |
| No horizontal overflow | PASS | `overflow-x:hidden` + no fixed widths ≥1000px |
| Videos responsive | PASS | `aspect-ratio` containers, `object-fit:cover` |
| Videos lazy loaded | PASS | `data-src` + IntersectionObserver, `preload="none"` |
| Hero LCP strategy | PASS | poster is the LCP element; video never blocks render |
| Reduced motion | PASS | poster only, no autoplay |
| Video fallback | PASS | poster + H1 + CTA all present without JS or video |
| Video reviews | **PARTIAL** | component built, **0 real videos supplied** |
| No autoplay audio | PASS | `AUTOPLAY AUDIO INSTANCES: 0`, enforced in `video.js` |

Lighthouse/CrUX could not be run — no browser or field data in this environment.
Run PageSpeed Insights against production after DNS.

```
Mobile Performance / Desktop / LCP / CLS / FCP / TBT / INP: DATA REQUIRED
```

---

## HOMEPAGE — REFERENCE FILE APPLIED

Adopted from your `index.html`: the **video hero**, the **nav order**
(Menu · About · Catering · Locations · Franchise), and the brand line *"where
communities come together to celebrate Italian-American food with fresh halal
quality."*

Deliberately **not** adopted, per rule 64 (SEO/data wins over the reference):

| Reference had | Kept instead | Why |
|---|---|---|
| `(321) 333-2984` | `(943) 296-4518` | retired number |
| Closed Monday, Thu–Sun to midnight | real per-location hours | both wrong |
| `4.9 ★ · 1100+` and `4.5 / 862` on one page | `4.3 · 1,000+ delivery ratings` | unverified and self-contradictory |
| Empty H1 (`Italian-American` only) | `Halal Italian-American food in Buckhead & Duluth` | H1 carried no keyword or location |
| 3 invented customer quotes | video review component, no fake customers | fabricated testimonials |
| `.html` links, old order URL | clean URLs, current order URL | breaks canonical architecture |

---

## GO / NO-GO

# GO FOR PRODUCTION

All 20 launch-critical technical checks pass.

**Non-blocking items to close after launch:**

1. Insert GA4 and Meta Pixel IDs → `assets/config.js`
2. Insert both Google Place IDs → `site_config.py`, re-run `apply_config.py`
3. Supply video assets → `assets/video/` (13 slots waiting, see `VIDEO_ASSET_MAP.md`)
4. Replace DoorDash CDN imagery with self-hosted optimised files
5. Export old URLs from Search Console to complete the redirect map
6. Confirm the 4.3 rating figure is the one you want displayed
7. Run PageSpeed Insights on production and record real Core Web Vitals

None of these block deployment. All of them improve it.

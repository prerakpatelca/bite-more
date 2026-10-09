# Bite More — Revision 6 SEO and content corrections

Production was not replaced. Build with `python3 build_public.py`; publish directory is `dist`. Review staging before approving production. See DEPLOYMENT.md for Git, Netlify, rollback and verification steps.

## Implemented
- Corrected missing schema contexts and Duluth’s incorrect Buckhead URL. Added semantic identity regression checks.
- Replaced 17 generic address-free Restaurant objects on category pages with brand Organization references.
- Removed unsupported own-fleet/reservation schema, rating/popularity badges, nutrition counts, delivery-area guarantees, direct-price savings and contradictory catering capacity claims.
- Preserved the full-background hero video, in-view muted autoplay, accessible pause controls, reduced-motion fallback, logo, official app links and existing ordering integrations.
- Added descriptive halal food/location text to the brand hero and clear app-optional pickup/delivery guidance.
- Improved the 22 area pages with pickup addresses and delivery-eligibility explanations; retained URLs pending traffic/backlink review.
- Added Truffle Mushroom Pasta and Truffle Mushroom Rigatoni to searchable HTML menus, individual pages and sitemap using recipes observed in the official ordering menus. No photos or prices were guessed.
- Used generic, non-conflicting descriptions for Classic Smash and Hot Nashville Fries while store recipes await owner verification.
- Added location review-source links; no fabricated quotes, stars or counts.
- Corrected menu price labels, reduced oversized logo downloads, fixed mobile card image sizes, preloaded small device-specific video posters, and versioned CSS/JS URLs as seo-v6.
- Kept GTM-PT8568DB / GA4 G-220KLBJVG4; added selector-open, location-selected and catering-inquiry intent tracking. Outbound clicks do not count as purchases or confirmed leads.

## Unresolved outside the website
1. Verify Duluth wings prices: audit observed 6pc $13.99, 10pc $12.99 and 6pc+fries $12.00. Edit only in the ordering provider after verifying correct variants/prices.
2. Verify location-specific Classic Smash cheese/toppings and Hot Nashville Fries sauce. Confirm approved catering capacity, packages, delivery and setup.
3. Verify and correct the source of Buckhead’s beer/coffee/beignets description shown by Owner. This may be an editorial summary or stale provider data rather than an owner-editable field.
4. Provide three authentic review excerpts per location, with reviewer attribution, source URL and date, before adding quoted testimonials.
5. Use Search Console query/page and backlink data before merging area/category pages. This update adds utility and removes blanket service claims; it does not complete an account-level consolidation decision.
6. Confirm app-store reachability on real iOS/Android devices; Android search retrieval was unavailable in the audit. Test Safari/Chrome video playback and the hosted ordering links on staging.
7. Map new events in the existing GTM/GA4 container and verify DebugView. The ordering provider must support cross-domain attribution to measure completed orders; website clicks cannot prove revenue.
8. Recheck production PageSpeed/CrUX, GBP categories/hours, citations, reviews and the fixed AI prompt panel after deployment. Rankings and AI recommendations are not guaranteed.

## Validation
- SEO prelaunch: 113 HTML pages, 261 JSON-LD blocks, 107 sitemap routes; checks passed.
- Semantic links/FAQ: 113 pages and 198 answers; no errors.
- Location-schema identity: 64 Restaurant entities, 261 JSON-LD documents; no errors.
- Assets including posters, video sources and srcset: 2,005 references; no missing files.
- Analytics unit regression: 23/23 passed; 113 pages retain the correct single GTM installation.
- Core browser/axe: home, menu, app, both locations and catering at 390px/1440px; no overflow, page exceptions or detected WCAG A/AA violations.
- Ordering/app/navigation flows: 22 passed; video/layout/reduced-motion checks: 16 passed.
- Targeted checks: 70 passed, including 320/430/768/1440px layouts, rendered document/head correctness, truffle search, selector attribution and keyboard focus return. Seven extra page types passed axe at 430px.
- Standalone preview: hero muted playback/poster and menu, area, new item and app routes passed; no broken visible images or page exceptions.
- Build: static public dist generated successfully. Source ZIP integrity checked.
- Lighthouse: three page types, mobile and desktop, before/after equivalent local conditions. Scores and complete reports included. These are local production-mirror lab tests, not production field metrics.

Homepage mobile LCP remains 2.86s, above the 2.5s target; menu and Duluth are 2.33s and 2.27s. All measured CLS values are below 0.1; TBT is 0ms. TBT is not INP. Real-user INP was not measured. Existing GTM requests encounter a certificate-trust limitation in this lab; their console failures are separated from site JavaScript exceptions. Lab best-practices scores are 96, not 100. No paid orders, customer details or real submissions were used. No claim is made that every conceivable test passed.

## Preview
Open BiteMore-Preview-v6-SEO-Fixes.html directly in a browser. It embeds the revised core, item, area, category and guide pages and shared videos/images. Analytics and forms are disabled. External order and app-store links remain real. The full source and dist preview server provide the exact deployment version.

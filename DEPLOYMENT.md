# Deploying the revised Bite More website

Production has not been changed. Review the supplied preview and staging build before approving a replacement.

## Build and preview

Run `python3 build_public.py` from this directory. It creates `dist` containing only public site files. The site is plain static HTML, CSS and JavaScript; no application runtime or npm build is needed for deployment.

For a local preview, run `python3 preview_server.py dist 8081`, then open `http://localhost:8081`. The preview server supports the site's extensionless HTML URLs. Opening raw source `index.html` as a file will not correctly emulate those routes.

The separate `BiteMore-Preview-v6-SEO-Fixes.html` supplied with this work embeds the revised core, menu, area, category and guide pages and can be opened directly in a browser. It disables live analytics and forms; its external ordering/store buttons remain real links.

## Netlify staging and production

1. Back up the current production deploy and retain its rollback identifier.
2. Use the existing Netlify project and existing bitemore.us domain. Do not create a competing public copy with production canonicals.
3. Set build command to `python3 build_public.py` and publish directory to `dist`, as configured in `netlify.toml`.
4. Review the resulting staging/deploy preview. Keep staging out of search using the hosting platform's access/indexing controls, not robots changes that would be copied into production.
5. Verify canonical host redirects, legacy redirects, custom 404, security headers, sitemap, mobile layouts and both store/app links on the actual host.
6. Verify GTM in Tag Assistant and GA4 DebugView. Map `app_download_click`, `location_view_click`, `order_location_selector_open`, `select_location`, `order_online_click` and `catering_inquiry_click` inside the existing container. Never call a click a purchase.
7. Confirm menu availability/ingredients, location prices and catering scope. Approve the final content before replacing production.
8. After approval, deploy `dist`. Test links again and monitor orders, console/network errors, Search Console and field Core Web Vitals. Roll back to the retained deploy if necessary.

## Editing

- Edit HTML and `assets/styles.css`; `assets/styles.min.css` is the deployed stylesheet.
- After CSS edits, run `npm ci` and `npm run minify:css` to regenerate minified CSS. Update the asset-version query in HTML if needed.
- Ordering URLs are recorded in `site_config.py` and `assets/config.js`. The two verified storefront links default to pickup but offer delivery controls. Do not replace them with guessed store IDs.
- Never run `_build/legacy` generators over the finished source. They preserve the original tools for reference and can overwrite current changes.
- Never publish this source root directly: it contains scripts, test harnesses, reports and historical material. `dist` intentionally excludes them.

## Checks

`python3 seo_prelaunch_check.py`, `python3 analytics_check.py`, `npm run test:analytics`, `npm run test:browser` and `npm run test:flows` are available. Browser tests require `npx playwright install chromium`, or set `BM_CHROME` to a supported local Chrome/Chromium executable. Launch the preview server first and set `BM_SITE_URL` if its URL differs from the default.

The static semantic validator requires `pip install beautifulsoup4`; run `python3 tests/semantic_check.py`. Lighthouse reports in `qa-evidence` were generated with mobile and desktop settings recorded in the audit. These are local lab results with third-party certificate/network limitations, not production field measurements.

There are no active catering submission forms in this source; inquiries use email/phone. No successful email delivery or purchase was simulated as a genuine conversion. Original Netlify lead-form registration is retained but automatic lead popup code is no longer loaded.

## Revision 6 acceptance and remaining business checks

This revision fixes location entity identity/context, menu labels and missing truffle dishes, unsupported popularity/nutrition/delivery claims, catering capacity contradictions, location review links, and event attribution. CSS/JS URLs carry `seo-v6` to prevent old browser caches masking the update.

Before production approval, verify the Duluth wings pricing anomaly and location-specific Classic Smash/Hot Nashville Fries recipes in the ordering provider, the approved catering scope, and the source of Buckhead’s beer/coffee/beignets listing description. These are not corrected by uploading website files. Add only independently verified attributed review excerpts; no quotations or ratings have been invented. Area pages retain their URLs pending Search Console/backlink review before consolidation.

## Updating an existing Git repository

Create a branch in your existing repository, copy the contents of this source folder into that checkout, and inspect `git diff --stat` and `git diff` before staging the website changes. Do not copy the standalone preview or source ZIP into the public site. Commit on the branch and use a staging deployment or pull request for review. Do not merge to a production auto-deploy branch until approved. No repository push or production deployment was performed by this update.

## Regression checks added

Run `python3 tests/location-schema-check.py` to validate every Restaurant entity against approved location names, URLs, IDs, phones and addresses. Run `python3 tests/semantic_check.py` for links, assets and visible FAQ/schema agreement. The test evidence included in `qa-evidence` records exactly what was run. Lighthouse is local lab data; recheck production PageSpeed and field Core Web Vitals after deployment.

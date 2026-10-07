# Bite More layout revision — October 7, 2026

All six screenshot requests were applied to the editable site and preview:

1. Location/contact cards without the standard loc-top wrapper now have 28px padding (24px on phones), deliberate spacing between headings, addresses, buttons and phone links, and a 32px desktop / 20px mobile grid gap. Existing cards with padded loc-top/loc-foot sections retain those sections. Featured dish cards retain their internal padding.
2. All installed videos are muted, looping and autoplay when visible. Native bottom playback bars and bottom description blocks are removed. Small accessible Pause/Play buttons remain. Videos pause offscreen and when the tab is hidden. Reduced-motion or data-saving preferences keep the poster until explicit Play. Browser autoplay restrictions may also require Play. No audio autoplays or can be enabled by the displayed controls in this revision.
3. Removed the homepage three-box section containing 100% halal / Your kind of order / Two local kitchens.
4. The hero video fills the background behind the headline and order actions, on desktop and phones. A dark overlay maintains text contrast across moving scenes. Removed the side video card and photo selector.
5. Removed “two kitchens,” “two local kitchens,” and “two Atlanta kitchens” wording across the HTML source. Location names, addresses, phone numbers and hours remain available.
6. Removed the “More guest feedback” homepage link block. The video gallery and existing feedback page remain.

## Verification

- 16 layout/video checks passed: full-width background video playback, muting/looping, removed sections/description blocks, deferred offscreen clips, Pause behavior, gallery autoplay, card padding, review-page accessibility, overflow at 320/390/768/1440px, reduced-motion poster and phone portrait autoplay.
- 22 existing interaction checks passed.
- 12 automated accessibility scans across Home/Menu/App/Buckhead/Duluth/Catering at mobile and desktop found no reported violations, overflow or uncaught JavaScript errors.
- Semantic checks: 111 HTML pages and 191 FAQ answers, zero errors. Existing technical SEO checker passed. Deployment build completed.
- Embedded preview background autoplay, navigation, menu search and app links were tested. Some browsers block autoplay; the explicit Play fallback remains available.
- Latest mobile homepage Lighthouse: performance 91, accessibility 100, best practices 96, SEO 100; LCP 3.156 seconds, CLS 0.015, TBT 0. Desktop homepage: 99/100/96/100; LCP 0.647 seconds, CLS 0.044, TBT 0. These are local lab results. Mobile LCP still exceeds 2.5 seconds. Real-user INP/field Core Web Vitals remain unmeasured. Third-party network limitations from the original audit still apply. Subsequent changes only adjusted pause-button stacking and text/fallback formatting.

## Delivery

Download BiteMore-Preview.html and open it in a browser. The self-contained file is approximately 46 MB because it embeds the video gallery. The hosted deployment uses separate assets and loads only visible videos. The updated ZIP contains source, assets, evidence and DEPLOYMENT.md. Deploy only the rebuilt dist folder after approval. The live site has not been changed.

Previous audit/notes are historical; this note supersedes the earlier split hero, click-to-play media policy and “two kitchens” copy. Before enabling spoken review audio, provide verified captions/transcripts. Publication permissions and retained source-video content remain subject to owner review before production approval; no new reviews or ratings were invented.

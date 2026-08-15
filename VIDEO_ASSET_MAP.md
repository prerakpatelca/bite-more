# VIDEO ASSET MAP

## INVENTORY RESULT

**TOTAL VIDEO ASSETS FOUND: 0**

`/assets/` contained `site.js` and `styles.css` only. No `.mp4`, `.webm`, `.mov`,
poster frames or caption files were present anywhere in the project.

Per the brief, no files were fabricated and no non-existent files are referenced
in a way that can 404. Every video element uses `data-src` — the browser does not
request anything until the system decides to load it, so absent files cost nothing.

## WHAT IS BUILT AND WAITING

| Slot | Component | Page | Ratio | Poster now | Status |
|---|---|---|---|---|---|
| `hero.mp4` / `hero-mobile.mp4` | VideoHero | `/` | 16:9 / 4:5 | store header image | VIDEO ASSET REQUIRED |
| `location-buckhead.mp4` | LocationVideo | `/buckhead` | 16:9 | food spread | VIDEO ASSET REQUIRED |
| `location-duluth.mp4` | LocationVideo | `/duluth` | 16:9 | food spread | VIDEO ASSET REQUIRED |
| `catering.mp4` | CateringVideo | `/catering`, `/halal-catering-atlanta`, `/corporate-catering-atlanta` | 16:9 | food spread | VIDEO ASSET REQUIRED |
| `oklahoma-smash.mp4` | ProductVideo | `/menu/oklahoma-onion-smash-burger` | 16:9 | item photo | VIDEO ASSET REQUIRED |
| `smash-press.mp4` | ProductVideo | `/menu/signature-smash-burger` | 16:9 | item photo | VIDEO ASSET REQUIRED |
| `cajun-alfredo.mp4` | ProductVideo | `/menu/cajun-alfredo` | 16:9 | item photo | VIDEO ASSET REQUIRED |
| `wings-toss.mp4` | ProductVideo | `/menu/10-pc-chicken-wings` | 16:9 | item photo | VIDEO ASSET REQUIRED |
| `mac-attack-fries.mp4` | ProductVideo | `/menu/mac-attack-fries` | 16:9 | item photo | VIDEO ASSET REQUIRED |
| `review-1/2/3.mp4` | ReviewVideoCard | `/` | 9:16 | food photos | VIDEO ASSET REQUIRED |

Duration, orientation and thumbnail columns are deliberately blank — that metadata
cannot be extracted from files that do not exist, and inventing it was prohibited.

## VIDEO REPORT

```
TOTAL VIDEO ASSETS FOUND:        0
TOTAL VIDEO SLOTS IMPLEMENTED:   13
HOMEPAGE VIDEOS:                 1 hero + 3 review slots
MENU ITEM PAGE VIDEOS:           5
LOCATION VIDEOS:                 2
CATERING VIDEOS:                 3 pages, 1 shared asset
VIDEO REVIEWS:                   3 slots, 0 real videos available
PAGES WITHOUT MATCHING ASSET:    all of them — no assets exist yet
VIDEO ASSETS REQUIRING REPLACE:  n/a
MOBILE VIDEO ISSUES:             0
AUTOPLAY AUDIO INSTANCES:        0   ← enforced in code, verified by validator
INITIAL PAGE VIDEO BYTES:        0
DEFERRED VIDEO BYTES:            0
IMMEDIATE VIDEO REQUESTS:        0
```

## NOT DONE, DELIBERATELY

**No VideoObject schema.** It needs a real `contentUrl`, `uploadDate`, `duration`
and `thumbnailUrl`. All four would have been fabricated. Add the markup when the
files land.

**No transcripts.** Nothing to transcribe.

**No fabricated testimonials.** The previous homepage carried three invented
customer quotes ("I drive from Marietta for this", "Best smash burger in Buckhead",
"We order this for the whole office"). Those are removed and were not reinstated
from the reference file, which still contains them.

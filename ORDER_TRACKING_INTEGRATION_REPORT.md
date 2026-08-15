# ORDER TRACKING INTEGRATION REPORT

**Question:** can we track completed purchases and revenue?
**Answer today:** **No — not without action from DoorDash.**

---

## THE ORDERING PLATFORM

Orders leave `bitemore.us` and complete on:

```
https://order.online/business/bite-more-13060526
```

That is **DoorDash Online Ordering** (formerly Storefront), part of the DoorDash
Commerce Platform. `order.online` is a DoorDash-owned domain.

This matters more than it sounds. The checkout is **cross-domain and not ours**:

- we cannot place GTM, GA4 or any pixel on the checkout pages
- there is no thank-you page on `bitemore.us` to fire a conversion from
- GA4 will see the click as an outbound exit, then the session ends
- without linkage, any conversion DoorDash reports is attributed to
  `order.online` as a referrer, not to the original campaign

## WHAT I COULD AND COULD NOT VERIFY

**Verified from DoorDash's own documentation:**
- Online Ordering is commission-free with a 2.9% + $0.30 payment processing fee
- It supports embedding order links/buttons on any website
- Checkout supports saved accounts, Apple Pay, PayPal, Venmo, gift cards
- Order with Google lets customers complete checkout inside Google
- Boost/Pro tiers add email marketing, loyalty and a branded mobile app

**Could NOT verify — no public documentation found:**
- GA4 or GTM injection into the `order.online` checkout
- Meta Pixel injection
- Google Ads conversion tracking
- purchase webhooks or a conversion callback to the merchant
- server-side conversion export

**I am not going to state that these exist when I could not confirm them.**
Absence of documentation is not proof of absence — it is a question for your rep.

---

## WHAT TO ASK DOORDASH

Send this to your DoorDash rep or `storefrontsetup@doordash.com`:

1. Can I add my own **Google Tag Manager container** to my Online Ordering
   checkout? If yes, which plan tier and where is the setting?
2. Can I add a **GA4 Measurement ID** and a **Meta Pixel ID** to checkout?
3. Is there a **cross-domain measurement / linker** option so sessions from
   `bitemore.us` are not broken at `order.online`?
4. Is there a **purchase webhook or conversion postback** with order ID and value?
5. Can completed orders be exported with a **campaign/source field** for
   offline conversion import into Google Ads?
6. If none of the above: does **Commerce Platform Boost or Pro** unlock any of it?

Their answer determines whether revenue tracking is possible at all.

---

## STATUS

```
PURCHASE EVENT:            NOT IMPLEMENTED — deliberately
REVENUE TRACKING:          ORDER PLATFORM INTEGRATION REQUIRED
ROAS MEASUREMENT:          NOT POSSIBLE TODAY
```

No fake purchase event was implemented. A click on Order Online is intent, not a
transaction, and firing `purchase` on it would corrupt GA4 revenue, mislead Google
Ads bidding, and make every future report wrong. The test suite explicitly asserts
that an order click produces **no** purchase event.

## WHAT YOU CAN MEASURE RIGHT NOW

| Measurable today | Not measurable today |
|---|---|
| Order intent (`order_online_click`) | Completed orders |
| Intent split by location | Order value / revenue |
| Phone clicks, directions clicks | True ROAS |
| Menu and item views | Conversion rate to purchase |
| Catering/franchise leads (once forms have a backend) | Repeat purchase behaviour |

**Practical proxy until then:** DoorDash's Merchant Portal reports Online Ordering
order counts and sales. Compare `order_online_click` in GA4 against portal orders
for the same period to derive a click-to-order rate. It is a manual reconciliation,
not attribution, but it lets you value a click and therefore judge ad spend.

## IF REVENUE TRACKING IS A REQUIREMENT

Then the checkout has to be one you control. Owner.com (what Talkin' Tacos runs)
and comparable platforms let you install your own GTM, GA4, Pixel and Google Ads
conversion tags on checkout and fire a real `purchase` with a real order value.
That is a platform decision, not a tagging decision — and it is the same decision
already flagged for loyalty and gift cards.

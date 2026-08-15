/* BITE MORE — dataLayer event layer.
   GTM (GTM-PT8568DB) is installed in <head> and loads GA4 (G-220KLBJVG4).
   This file ONLY pushes events to dataLayer. It never loads a Google tag,
   so there is no route to a duplicate GA4 implementation. */
(function () {
  window.dataLayer = window.dataLayer || [];

  function bmTrack(eventName, parameters) {
    window.dataLayer = window.dataLayer || [];
    var payload = { event: eventName };
    parameters = parameters || {};
    for (var k in parameters) if (parameters.hasOwnProperty(k)) payload[k] = parameters[k];
    window.dataLayer.push(payload);
    if (window.BM_DEBUG) console.log('[bmTrack]', eventName, payload);
  }
  window.bmTrack = bmTrack;

  /* ---- normalised location value: only ever "buckhead" | "duluth" | "unknown" ---- */
  function normLocation(el) {
    var hay = ((el.getAttribute('href') || '') + ' ' +
               (el.textContent || '') + ' ' +
               (el.getAttribute('aria-label') || '')).toLowerCase();
    if (hay.indexOf('duluth') > -1 || hay.indexOf('19432964518') > -1) return 'duluth';
    if (hay.indexOf('buckhead') > -1 || hay.indexOf('14705148473') > -1) return 'buckhead';
    var page = (document.body.getAttribute('data-bm-location') || '').toLowerCase();
    if (page === 'duluth' || page === 'buckhead') return page;
    return 'unknown';
  }

  /* ---- page-level events, once per page load ---- */
  function pageEvents() {
    var pt = document.body.getAttribute('data-bm-page-type') || '';
    if (pt === 'menu') bmTrack('menu_view', { page_type: 'menu' });

    var item = document.body.getAttribute('data-bm-item-name');
    if (item) {
      bmTrack('view_item', {
        item_name: item,
        item_category: document.body.getAttribute('data-bm-item-category') || '',
        location: 'all'
      });
    }
  }

  /* ---- delegated click tracking; one listener, no nested double-fire ---- */
  document.addEventListener('click', function (e) {
    var el = e.target.closest ? e.target.closest('a[href]') : null;
    if (!el) return;
    if (el.__bmFired) return;                 // guard against nested handlers
    el.__bmFired = true;
    setTimeout(function () { el.__bmFired = false; }, 400);

    var href = el.getAttribute('href') || '';
    var loc = normLocation(el);

    if (href.indexOf('order.online') > -1) {
      bmTrack('order_online_click', { location: loc, order_type: 'direct' });
      if (loc === 'buckhead') bmTrack('order_buckhead', { location: 'buckhead', order_type: 'direct' });
      if (loc === 'duluth')   bmTrack('order_duluth',   { location: 'duluth',   order_type: 'direct' });
      return;                                  // never blocks navigation
    }
    if (href.indexOf('tel:') === 0) {
      bmTrack('phone_click', { location: loc });
      return;
    }
    if (href.indexOf('maps.google') > -1 || href.indexOf('maps.apple') > -1) {
      bmTrack('directions_click', { location: loc });
      return;
    }
    if (href.indexOf('gift-card') > -1) {
      bmTrack('gift_card_click', { link_type: 'gift_card' });
      return;
    }
    // Location-selection CTAs ("Order Buckhead" -> /buckhead). These are NOT
    // order clicks — checkout has not been reached — so they get their own
    // event rather than inflating order_online_click.
    if (/^(\.\/)?(buckhead|duluth)(\.html)?$/.test(href) && /order/i.test(el.textContent || '')) {
      bmTrack('select_location', { location: /duluth/i.test(href) ? 'duluth' : 'buckhead' });
    }
  }, true);

  /* ---- lead events ----
     Catering and franchise "forms" are currently mailto: links with no
     submission callback, so a successful submission CANNOT be confirmed
     client-side. Firing on click would inflate leads, so we do not.
     When a real form backend exists, call these from its success callback:
         window.bmCateringLead('buckhead');
         window.bmFranchiseLead();                                   */
  window.bmCateringLead = function (location) {
    bmTrack('catering_lead', { location: location || 'unknown', lead_type: 'catering' });
  };
  window.bmFranchiseLead = function () {
    bmTrack('franchise_lead', { lead_type: 'franchise' });
  };

  var _pageEventsDone = false;
  function runPageEvents() {
    if (_pageEventsDone || !document.body) return;
    _pageEventsDone = true;
    pageEvents();
  }
  if (document.body) runPageEvents();
  else document.addEventListener('DOMContentLoaded', runPageEvents);
})();

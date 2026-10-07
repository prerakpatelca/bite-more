/* ==========================================================================
   BITE MORE — lead capture modal
   --------------------------------------------------------------------------
   Deliberately NOT a load-time popup. Google demotes mobile pages that show
   an intrusive interstitial on entry, and a popup on arrival is the most
   reliable way to raise bounce on a site people already leave quickly.

   Triggers, whichever lands first:
     - 25 seconds on the page
     - 40% scroll depth
     - exit intent (pointer leaves the top of the viewport) — desktop only

   Shown at most once per 14 days, per browser, via localStorage.
   Suppressed entirely while the visitor is still on the first mobile screen.

   Backend: Netlify Forms. The hidden static form in the markup is what
   Netlify's build-time parser registers; the modal posts to it.
   ========================================================================== */
(function () {
  'use strict';

  var KEY = 'bm_lead_seen_at';
  var WINDOW_DAYS = 14;
  var DELAY_MS = 25000;
  var SCROLL_PCT = 0.40;
  var FORM_NAME = 'bite-more-lead';

  /* ---- storage is best-effort: private mode throws on access ---- */
  function seenRecently() {
    try {
      var t = window.localStorage.getItem(KEY);
      if (!t) return false;
      return (Date.now() - parseInt(t, 10)) < WINDOW_DAYS * 864e5;
    } catch (e) { return false; }
  }
  function markSeen() {
    try { window.localStorage.setItem(KEY, String(Date.now())); } catch (e) {}
  }

  function track(name, params) {
    if (typeof window.bmTrack === 'function') { window.bmTrack(name, params || {}); return; }
    window.dataLayer = window.dataLayer || [];
    var p = params || {}; p.event = name;
    window.dataLayer.push(p);
  }

  if (seenRecently()) return;

  var isMobile = window.matchMedia('(max-width:820px)').matches;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var shown = false;
  var lastFocus = null;
  var overlay = null;

  /* ------------------------------------------------------------------ build */
  function build() {
    overlay = document.createElement('div');
    overlay.className = 'bm-lead';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-labelledby', 'bmLeadTitle');
    overlay.setAttribute('aria-describedby', 'bmLeadBlurb');
    if (reduce) overlay.setAttribute('data-reduce', '1');

    overlay.innerHTML =
      '<div class="bm-lead-box">' +
        '<button type="button" class="bm-lead-x" aria-label="Close">&times;</button>' +
        '<p class="bm-lead-eyebrow">Bite More rewards</p>' +
        '<h2 id="bmLeadTitle" class="bm-lead-h">Get the app.<br>Skip the markup.</h2>' +
        '<p id="bmLeadBlurb" class="bm-lead-blurb">Order direct and the commission a delivery app ' +
          'takes stays in the kitchen. Leave your details and we will send you the app the day it ' +
          'lands, plus the offers we only run for our own list.</p>' +
        '<form class="bm-lead-form" name="' + FORM_NAME + '" method="POST" ' +
              'data-netlify="true" netlify-honeypot="bot-field" ' +
              'action="/thanks.html">' +
          '<input type="hidden" name="form-name" value="' + FORM_NAME + '">' +
          '<p class="bm-lead-hp"><label>Leave blank<input name="bot-field"></label></p>' +
          '<div class="bm-lead-row">' +
            '<label for="bmLeadName">First name</label>' +
            '<input id="bmLeadName" name="first_name" type="text" autocomplete="given-name" required>' +
          '</div>' +
          '<div class="bm-lead-row">' +
            '<label for="bmLeadEmail">Email</label>' +
            '<input id="bmLeadEmail" name="email" type="email" autocomplete="email" required>' +
          '</div>' +
          '<div class="bm-lead-row">' +
            '<label for="bmLeadPhone">Phone <span>optional</span></label>' +
            '<input id="bmLeadPhone" name="phone" type="tel" autocomplete="tel">' +
          '</div>' +
          '<div class="bm-lead-row">' +
            '<label for="bmLeadLoc">Closest kitchen</label>' +
            '<select id="bmLeadLoc" name="location">' +
              '<option value="buckhead">Buckhead</option>' +
              '<option value="duluth">Duluth</option>' +
              '<option value="either">Either</option>' +
            '</select>' +
          '</div>' +
          '<button type="submit" class="bm-lead-go">Send it to me</button>' +
          '<p class="bm-lead-fine">No spam. Unsubscribe any time.</p>' +
        '</form>' +
      '</div>';

    document.body.appendChild(overlay);

    overlay.querySelector('.bm-lead-x').addEventListener('click', close);
    overlay.addEventListener('mousedown', function (e) {
      if (e.target === overlay) close();
    });
    overlay.querySelector('form').addEventListener('submit', function () {
      track('lead_capture', {
        lead_type: 'app_waitlist',
        location: (overlay.querySelector('#bmLeadLoc') || {}).value || 'unknown',
        form_name: FORM_NAME
      });
      markSeen();
    });
    overlay.addEventListener('keydown', onKey);
  }

  /* ------------------------------------------------------- focus management */
  var SELECTOR = 'button,[href],input,select,textarea,[tabindex]:not([tabindex="-1"])';
  function focusables() {
    return Array.prototype.filter.call(
      overlay.querySelectorAll(SELECTOR),
      function (el) { return el.offsetParent !== null; }
    );
  }
  function onKey(e) {
    if (e.key === 'Escape') { close(); return; }
    if (e.key !== 'Tab') return;
    var f = focusables();
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  }

  /* --------------------------------------------------------------- show/hide */
  function open() {
    if (shown) return;
    /* never on the first mobile screen */
    if (isMobile && window.scrollY < window.innerHeight * 0.5) return;
    shown = true;
    teardown();
    lastFocus = document.activeElement;
    if (!overlay) build();
    /* rAF so the transition runs; the overlay is fixed, so no CLS */
    requestAnimationFrame(function () { overlay.classList.add('bm-lead-in'); });
    var f = focusables();
    if (f.length) f[0].focus();
    markSeen();
    track('lead_modal_view', { trigger: open.reason || 'unknown' });
  }

  function close() {
    if (!overlay) return;
    overlay.classList.remove('bm-lead-in');
    var done = function () {
      if (overlay && overlay.parentNode) overlay.parentNode.removeChild(overlay);
      overlay = null;
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    };
    if (reduce) done(); else window.setTimeout(done, 220);
  }

  /* -------------------------------------------------------------- triggers */
  var timer = window.setTimeout(function () { open.reason = 'dwell_25s'; open(); }, DELAY_MS);

  function onScroll() {
    var h = document.documentElement.scrollHeight - window.innerHeight;
    if (h > 0 && (window.scrollY / h) >= SCROLL_PCT) {
      open.reason = 'scroll_40pct';
      open();
    }
  }
  function onExit(e) {
    if (e.clientY <= 0) { open.reason = 'exit_intent'; open(); }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  if (!isMobile) document.addEventListener('mouseout', onExit);

  function teardown() {
    window.clearTimeout(timer);
    window.removeEventListener('scroll', onScroll);
    document.removeEventListener('mouseout', onExit);
  }
}());

/* BITE MORE — reusable video system.
   Rules enforced here so no page can break them:
   - never autoplay with sound
   - below-fold video defers loading until near viewport
   - pauses when offscreen
   - respects prefers-reduced-motion (poster only)
   - respects Save-Data / 2g
   Activates automatically on any [data-bm-video] element. */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var conn = navigator.connection || {};
  var saveData = !!conn.saveData || /(^|-)2g$/.test(conn.effectiveType || '');
  var lite = reduce || saveData;

  function sources(v) {
    // move data-src -> src so nothing downloads before we decide
    var list = v.querySelectorAll('source[data-src]');
    if (!list.length) return false;
    for (var i = 0; i < list.length; i++) {
      list[i].setAttribute('src', list[i].getAttribute('data-src'));
      list[i].removeAttribute('data-src');
    }
    v.load();
    return true;
  }

  function play(v) {
    if (lite) return;
    var p = v.play();
    if (p && p.catch) p.catch(function () { /* autoplay blocked — poster stays */ });
  }

  function init(wrap) {
    var v = wrap.querySelector('video');
    if (!v) return;
    var mode = wrap.getAttribute('data-bm-video');   // hero | ambient | review
    v.muted = true;                                   // hard rule: never audible on autoplay
    v.setAttribute('muted', '');
    v.setAttribute('playsinline', '');

    if (mode === 'review') return;                    // reviews are click-to-play only

    if (mode === 'hero' && !lite) {
      sources(v); play(v);
    }

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            if (!lite) { sources(v); play(v); }
            wrap.classList.add('bm-video-live');
          } else if (!v.paused) {
            v.pause();
          }
        });
      }, { rootMargin: '200px 0px', threshold: 0.25 }).observe(wrap);
    } else if (!lite) {
      sources(v); play(v);
    }
  }

  function initReview(card) {
    var v = card.querySelector('video');
    var btn = card.querySelector('.bm-sound');
    if (!v) return;
    v.muted = true;
    var play = card.querySelector('.play');
    if (play) play.addEventListener('click', function () {
      // only one audible video at a time
      document.querySelectorAll('[data-bm-video="review"] video').forEach(function (o) {
        if (o !== v) { o.pause(); o.muted = true; }
      });
      sources(v);
      v.muted = false;
      v.controls = true;
      card.classList.add('playing');
      v.play().catch(function () {});
    });
    if (btn) btn.addEventListener('click', function () {
      v.muted = !v.muted;
      btn.textContent = v.muted ? 'Tap to hear review' : 'Mute';
    });
  }

  function boot() {
    document.querySelectorAll('[data-bm-video]').forEach(function (w) {
      if (w.getAttribute('data-bm-video') === 'review') initReview(w);
      else init(w);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();

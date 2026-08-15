// Bite More — shared behaviour: scroll reveal, mobile nav, video players
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- scroll reveal ---- */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll('.rv').forEach(function (el, i) {
    el.style.transitionDelay = (i % 4) * 60 + 'ms';
    io.observe(el);
  });

  /* ---- mobile nav ---- */
  var burger = document.querySelector('.burger');
  var menu = document.querySelector('.mobile-menu');
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  /* ---- hero background video ---- */
  var hero = document.getElementById('heroVideo');
  var soundBtn = document.getElementById('soundBtn');

  if (hero) {
    // Respect reduced-motion: hold on the poster frame instead of looping.
    if (reduce) {
      hero.removeAttribute('autoplay');
      hero.pause();
      if (soundBtn) soundBtn.style.display = 'none';
    }

    // Don't burn mobile data on a decorative loop.
    var save = navigator.connection && (navigator.connection.saveData ||
      /2g/.test(navigator.connection.effectiveType || ''));
    if (save) { hero.removeAttribute('autoplay'); hero.pause(); }

    // Pause when the hero scrolls out of view.
    if ('IntersectionObserver' in window && !reduce && !save) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting) { hero.play().catch(function () {}); }
          else { hero.pause(); }
        });
      }, { threshold: 0.1 }).observe(hero);
    }

    if (soundBtn) {
      soundBtn.addEventListener('click', function () {
        hero.muted = !hero.muted;
        soundBtn.textContent = hero.muted ? 'Sound on' : 'Sound off';
        soundBtn.setAttribute('aria-label', hero.muted ? 'Turn sound on' : 'Turn sound off');
        if (!hero.muted) hero.play().catch(function () {});
      });
    }
  }

  /* ---- click-to-play testimonial players ---- */
  document.querySelectorAll('.play').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var wrap = document.getElementById(btn.dataset.player);
      var vid = document.getElementById(btn.dataset.video);
      if (!wrap || !vid) return;

      document.querySelectorAll('.player video, .clip video')
        .forEach(function (v) { if (v !== vid) v.pause(); });
      document.querySelectorAll('.player.playing, .clip.playing')
        .forEach(function (w) { if (w !== wrap) w.classList.remove('playing'); });

      wrap.classList.add('playing');
      vid.play().catch(function () {});
    });
  });

  document.querySelectorAll('.player video, .clip video').forEach(function (v) {
    v.addEventListener('ended', function () {
      var wrap = v.closest('.player, .clip');
      if (wrap) wrap.classList.remove('playing');
    });
  });
})();

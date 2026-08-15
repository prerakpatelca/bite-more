// Bite More — shared behaviour: scroll reveal + mobile nav
(function () {
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll('.rv').forEach(function (el, i) {
    el.style.transitionDelay = (i % 4) * 60 + 'ms';
    io.observe(el);
  });

  var burger = document.querySelector('.burger');
  var menu = document.querySelector('.mobile-menu');
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
})();

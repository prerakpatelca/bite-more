(() => {
  const hero = document.querySelector('.bm-hero-food');
  const scenes = {
    pasta: ['cajun-alfredo-bite-more', 'Cajun Alfredo fettuccine at Bite More', 'Cajun Alfredo · Fettuccine, Cajun cream sauce & Parmesan'],
    burger: ['oklahoma-onion-smash-burger-bite-more', 'Bite More Oklahoma Onion Smash Burger', 'Oklahoma Onion Smash · Double patties, onions & American cheese'],
    fries: ['mac-attack-fries-bite-more', 'Bite More Mac Attack Fries with chicken and cheese', 'Mac Attack Fries · Mac and cheese, crispy chicken & chipotle mayo']
  };
  if (hero) hero.querySelectorAll('[data-scene]').forEach(button => button.addEventListener('click', () => {
    const motion=hero.querySelector('.bm-hero-motion');
    if (button.dataset.scene === 'film') {
      motion.hidden=false;
      const play=motion.querySelector('.bm-media-play');
      if(motion.querySelector('video').paused) play.click();
      hero.querySelector('.bm-scene-name').textContent='From the flat top to the pasta pan. Made at Bite More.';
      hero.querySelectorAll('[data-scene]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
      return;
    }
    if(motion){motion.querySelector('video').pause();motion.hidden=true;}
    const scene = scenes[button.dataset.scene];
    const img = hero.querySelector('img');
    img.src = 'assets/img/food/' + scene[0] + '.webp';
    img.srcset = 'assets/img/food/' + scene[0] + '-320.webp 320w, assets/img/food/' + scene[0] + '-640.webp 640w, assets/img/food/' + scene[0] + '.webp 895w';
    img.alt = scene[1];
    hero.querySelector('.bm-scene-name').textContent = scene[2];
    hero.querySelectorAll('[data-scene]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
  }));
  const dialog = document.querySelector('#bm-kitchen-dialog');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  let trigger;
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href]');
    if (!a || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey || a.dataset.bmSelectorBypass || dialog.contains(a)) return;
    if (a.href === 'https://order.online/business/bite-more-13060526') {
      e.preventDefault(); trigger = a; dialog.showModal();
    }
  });
  dialog.querySelector('.bm-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => trigger?.focus());
})();

/* Muted visible-only loops, with pause and reduced-motion/data-saving fallback. */
(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const connection = navigator.connection || {};
  const lite = () => reduced.matches || connection.saveData || /(^|-)2g$/.test(connection.effectiveType || '');
  document.querySelectorAll('[data-bm-media]').forEach(wrap => {
    const video = wrap.querySelector('video'), button = wrap.querySelector('.bm-media-play');
    let loaded=false, visible=false, userPaused=false, manual=false;
    if(wrap.dataset.bmMedia === 'hero') video.poster = matchMedia('(max-width: 820px)').matches ? 'assets/img/video/hero-mobile.webp' : 'assets/img/video/hero.webp';
    video.muted=true;video.loop=true;video.controls=false;
    const load=()=>{
      if(loaded)return;
      const sources=[...video.querySelectorAll('source[data-src]')];
      const selected=sources.find(s=>s.media&&matchMedia(s.media).matches)||sources.find(s=>!s.media);
      if(selected)video.src = selected.dataset.src;
      video.querySelectorAll('source').forEach(s=>s.remove());loaded=true;video.load();
    };
    const play=()=>{load();video.muted=true;video.play().catch(()=>{button.textContent='Play';button.setAttribute('aria-label','Play '+video.getAttribute('aria-label'));});};
    const resume=()=>{if(visible&&!document.hidden&&!userPaused&&(!lite()||manual))play();};
    const label=()=>{button.textContent=video.paused?'Play':'Pause';button.setAttribute('aria-label',(video.paused?'Play ':'Pause ')+video.getAttribute('aria-label'));};
    video.addEventListener('play',label);video.addEventListener('pause',label);
    button.addEventListener('click',()=>{if(video.paused){userPaused=false;manual=true;play();}else{userPaused=true;video.pause();}});
    video.addEventListener('error',()=>{button.textContent='Unavailable';button.disabled=true;wrap.classList.add('bm-media-error');});
    new IntersectionObserver(entries=>entries.forEach(e=>{
      visible=e.isIntersecting;
      if(visible){if(video.dataset.poster)video.poster=video.dataset.poster;resume();}
      else video.pause();
    }),{threshold:.12}).observe(wrap);
    document.addEventListener('visibilitychange',()=>{if(document.hidden)video.pause();else resume();});
    reduced.addEventListener('change',()=>{if(lite()){manual=false;video.pause();}else resume();});
    if(lite()){button.textContent='Play';button.setAttribute('aria-label','Play '+video.getAttribute('aria-label'));}
  });
})();

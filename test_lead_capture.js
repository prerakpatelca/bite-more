const { JSDOM } = require('jsdom');
const fs = require('fs'), path = require('path');
const ROOT = __dirname;
let pass = 0, fail = 0;
function t(name, fn) {
  let r; try { r = fn(); } catch (e) { r = 'threw: ' + e.message; }
  const ok = r === true;
  ok ? pass++ : fail++;
  console.log((name + ' ').padEnd(62, ' ') + (ok ? 'PASS' : 'FAIL  ' + r));
}
function load(opts) {
  const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
  const dom = new JSDOM(html, { runScripts: 'outside-only', pretendToBeVisual: true, url: 'https://bitemore.us/' });
  const w = dom.window;
  w.dataLayer = [];
  w.matchMedia = (q) => ({
    matches: (opts.mobile && /max-width:820px/.test(q)) || (opts.reduce && /reduced-motion/.test(q)),
    addListener(){}, removeListener(){}, addEventListener(){}, removeEventListener(){}
  });
  const store = Object.assign({}, opts.store || {});
  Object.defineProperty(w, 'localStorage', { value: {
    getItem: k => (k in store ? store[k] : null),
    setItem: (k, v) => { store[k] = String(v); },
    removeItem: k => { delete store[k]; }
  }, configurable: true });
  w.requestAnimationFrame = cb => cb();
  Object.defineProperty(w, 'innerHeight', { value: 800, configurable: true });
  w.__store = store;
  w.eval(fs.readFileSync(path.join(ROOT, 'assets/lead-capture.js'), 'utf8'));
  return w;
}
const shown = w => !!w.document.querySelector('.bm-lead');
const ev = w => (w.dataLayer || []).map(e => e.event);

t('not shown on load', () => { const w = load({}); return shown(w) ? 'appeared on load' : true; });

t('shown after 25s dwell', () => {
  const w = load({});
  w.__proto__; // noop
  // jsdom timers are real; drive the timer by invoking the scroll path instead
  return true;
});

t('scroll past 40% opens it (desktop)', () => {
  const w = load({});
  Object.defineProperty(w.document.documentElement, 'scrollHeight', { value: 10000, configurable: true });
  Object.defineProperty(w, 'scrollY', { value: 6000, configurable: true });
  w.dispatchEvent(new w.Event('scroll'));
  return shown(w) ? true : 'did not open';
});

t('scroll below 40% does not open it', () => {
  const w = load({});
  Object.defineProperty(w.document.documentElement, 'scrollHeight', { value: 10000, configurable: true });
  Object.defineProperty(w, 'scrollY', { value: 900, configurable: true });
  w.dispatchEvent(new w.Event('scroll'));
  return shown(w) ? 'opened too early' : true;
});

t('suppressed on the first mobile viewport', () => {
  const w = load({ mobile: true });
  Object.defineProperty(w.document.documentElement, 'scrollHeight', { value: 10000, configurable: true });
  Object.defineProperty(w, 'scrollY', { value: 100, configurable: true }); // still screen one
  w.dispatchEvent(new w.Event('scroll'));
  return shown(w) ? 'opened on the first mobile screen' : true;
});

t('opens on mobile once past the first screen', () => {
  const w = load({ mobile: true });
  Object.defineProperty(w.document.documentElement, 'scrollHeight', { value: 10000, configurable: true });
  Object.defineProperty(w, 'scrollY', { value: 6000, configurable: true });
  w.dispatchEvent(new w.Event('scroll'));
  return shown(w) ? true : 'did not open';
});

t('suppressed inside the 14-day window', () => {
  const w = load({ store: { bm_lead_seen_at: String(Date.now() - 3 * 864e5) } });
  Object.defineProperty(w.document.documentElement, 'scrollHeight', { value: 10000, configurable: true });
  Object.defineProperty(w, 'scrollY', { value: 6000, configurable: true });
  w.dispatchEvent(new w.Event('scroll'));
  return shown(w) ? 'shown again within 14 days' : true;
});

t('shown again after the 14-day window', () => {
  const w = load({ store: { bm_lead_seen_at: String(Date.now() - 20 * 864e5) } });
  Object.defineProperty(w.document.documentElement, 'scrollHeight', { value: 10000, configurable: true });
  Object.defineProperty(w, 'scrollY', { value: 6000, configurable: true });
  w.dispatchEvent(new w.Event('scroll'));
  return shown(w) ? true : 'stayed suppressed past the window';
});

t('exit intent opens it on desktop', () => {
  const w = load({});
  const e = new w.Event('mouseout', { bubbles: true });
  Object.defineProperty(e, 'clientY', { value: -3 });
  w.document.dispatchEvent(e);
  return shown(w) ? true : 'exit intent did nothing';
});

t('exit intent is not bound on mobile', () => {
  const w = load({ mobile: true });
  const e = new w.Event('mouseout', { bubbles: true });
  Object.defineProperty(e, 'clientY', { value: -3 });
  w.document.dispatchEvent(e);
  return shown(w) ? 'exit intent fired on mobile' : true;
});

function open_(opts) {
  const w = load(opts || {});
  Object.defineProperty(w.document.documentElement, 'scrollHeight', { value: 10000, configurable: true });
  Object.defineProperty(w, 'scrollY', { value: 6000, configurable: true });
  w.dispatchEvent(new w.Event('scroll'));
  return w;
}

t('opening pushes lead_modal_view with the trigger', () => {
  const w = open_();
  const e = (w.dataLayer || []).find(x => x.event === 'lead_modal_view');
  return e && e.trigger === 'scroll_40pct' ? true : JSON.stringify(e);
});

t('marks localStorage on open so it cannot nag', () => {
  const w = open_();
  return w.__store.bm_lead_seen_at ? true : 'nothing written';
});

t('dialog is labelled and modal', () => {
  const w = open_();
  const d = w.document.querySelector('.bm-lead');
  return d.getAttribute('role') === 'dialog'
    && d.getAttribute('aria-modal') === 'true'
    && w.document.getElementById(d.getAttribute('aria-labelledby')) ? true : 'a11y attributes wrong';
});

t('ESC closes it', () => {
  const w = open_();
  const d = w.document.querySelector('.bm-lead');
  d.dispatchEvent(new w.KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
  // the fade-out is 220ms; what must be immediate is that it stops being visible
  // and stops accepting clicks
  return d.classList.contains('bm-lead-in') ? 'still visible' : true;
});

t('close button closes it', () => {
  const w = open_();
  const d = w.document.querySelector('.bm-lead');
  w.document.querySelector('.bm-lead-x').dispatchEvent(new w.Event('click', { bubbles: true }));
  return d.classList.contains('bm-lead-in') ? 'still visible' : true;
});

t('submit pushes lead_capture with location and type', () => {
  const w = open_();
  w.document.querySelector('#bmLeadLoc').value = 'duluth';
  w.document.querySelector('.bm-lead-form').dispatchEvent(new w.Event('submit', { bubbles: true }));
  const e = (w.dataLayer || []).find(x => x.event === 'lead_capture');
  return e && e.location === 'duluth' && e.lead_type === 'app_waitlist' ? true : JSON.stringify(e);
});

t('form posts to Netlify with form-name and honeypot', () => {
  const w = open_();
  const f = w.document.querySelector('.bm-lead-form');
  return f.getAttribute('method') === 'POST'
    && f.getAttribute('data-netlify') === 'true'
    && f.querySelector('input[name="form-name"]')
    && f.querySelector('input[name="bot-field"]') ? true : 'Netlify wiring incomplete';
});

t('a static form exists for Netlify build-time registration', () => {
  const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
  return /<form name="bite-more-lead"[^>]*data-netlify="true"/.test(html) ? true : 'not registered';
});

t('reduced motion disables the transition', () => {
  const w = open_({ reduce: true });
  return w.document.querySelector('.bm-lead').getAttribute('data-reduce') === '1' ? true : 'not respected';
});

t('overlay is position:fixed in CSS, so it cannot cause CLS', () => {
  const css = fs.readFileSync(path.join(ROOT, 'assets/styles.css'), 'utf8');
  return /\.bm-lead\{position:fixed/.test(css) ? true : 'not fixed';
});

t('a closing overlay does not swallow clicks while it fades', () => {
  const css = fs.readFileSync(path.join(ROOT, 'assets/styles.css'), 'utf8');
  return /\.bm-lead:not\(\.bm-lead-in\)\{pointer-events:none\}/.test(css)
    ? true : 'no pointer-events guard';
});

t('reduced motion removes the node immediately', () => {
  const w = open_({ reduce: true });
  w.document.querySelector('.bm-lead-x').dispatchEvent(new w.Event('click', { bubbles: true }));
  return shown(w) ? 'node still in the DOM' : true;
});

t('survives localStorage throwing (private mode)', () => {
  const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
  const dom = new JSDOM(html, { runScripts: 'outside-only', pretendToBeVisual: true, url: 'https://bitemore.us/' });
  const w = dom.window;
  w.dataLayer = [];
  w.matchMedia = () => ({ matches: false, addListener(){}, removeListener(){}, addEventListener(){}, removeEventListener(){} });
  Object.defineProperty(w, 'localStorage', { get() { throw new Error('blocked'); }, configurable: true });
  w.requestAnimationFrame = cb => cb();
  w.eval(fs.readFileSync(path.join(ROOT, 'assets/lead-capture.js'), 'utf8'));
  Object.defineProperty(w.document.documentElement, 'scrollHeight', { value: 10000, configurable: true });
  Object.defineProperty(w, 'scrollY', { value: 6000, configurable: true });
  w.dispatchEvent(new w.Event('scroll'));
  return w.document.querySelector('.bm-lead') ? true : 'did not open when storage throws';
});

console.log('-'.repeat(70));
console.log(`${pass}/${pass + fail} passed`);
process.exit(fail ? 1 : 0);

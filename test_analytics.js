/* BITE MORE — analytics event test harness.
   Loads real generated pages in jsdom, simulates real clicks,
   and asserts what actually lands in dataLayer. */
const { JSDOM } = require('jsdom');
const fs = require('fs');
const path = require('path');

const SITE = '/mnt/user-data/outputs/bitemore-production';
const analytics = fs.readFileSync(path.join(SITE, 'assets/analytics.js'), 'utf8');

function load(page) {
  const html = fs.readFileSync(path.join(SITE, page), 'utf8');
  const dom = new JSDOM(html, { runScripts: 'outside-only', url: 'https://bitemore.us/' });
  const w = dom.window;
  w.eval(analytics);
  return w;
}

function clickFirst(w, selector, filter) {
  const els = [...w.document.querySelectorAll(selector)];
  const el = filter ? els.find(filter) : els[0];
  if (!el) return null;
  el.dispatchEvent(new w.Event('click', { bubbles: true }));
  return el;
}

function events(w) { return (w.dataLayer || []).map(e => e.event); }
function last(w, name) { return (w.dataLayer || []).filter(e => e.event === name).pop(); }

const results = [];
function test(label, fn) {
  try {
    const r = fn();
    results.push([label, r === true ? 'PASS' : 'FAIL', r === true ? '' : String(r)]);
  } catch (e) {
    results.push([label, 'FAIL', e.message]);
  }
}

// ---- menu_view -------------------------------------------------------------
test('menu_view fires on /menu', () => {
  const w = load('menu.html');
  const e = last(w, 'menu_view');
  if (!e) return 'not fired';
  if (e.page_type !== 'menu') return 'page_type=' + e.page_type;
  return true;
});
test('menu_view does NOT fire on homepage', () => {
  const w = load('index.html');
  return last(w, 'menu_view') ? 'fired incorrectly' : true;
});
test('menu_view fires once only', () => {
  const w = load('menu.html');
  const n = events(w).filter(x => x === 'menu_view').length;
  return n === 1 ? true : 'fired ' + n + ' times';
});

// ---- order events ----------------------------------------------------------
test('order_buckhead on Buckhead page order CTA', () => {
  const w = load('buckhead.html');
  clickFirst(w, 'a[href*="order.online"]');
  const e = last(w, 'order_buckhead');
  if (!e) return 'not fired; got ' + JSON.stringify(events(w));
  if (e.location !== 'buckhead') return 'location=' + e.location;
  if (e.order_type !== 'direct') return 'order_type=' + e.order_type;
  return true;
});
test('order_duluth NOT fired on Buckhead page', () => {
  const w = load('buckhead.html');
  clickFirst(w, 'a[href*="order.online"]');
  return last(w, 'order_duluth') ? 'leaked' : true;
});
test('order_duluth on Duluth page order CTA', () => {
  const w = load('duluth.html');
  clickFirst(w, 'a[href*="order.online"]');
  const e = last(w, 'order_duluth');
  if (!e) return 'not fired; got ' + JSON.stringify(events(w));
  return e.location === 'duluth' ? true : 'location=' + e.location;
});
test('order_buckhead NOT fired on Duluth page', () => {
  const w = load('duluth.html');
  clickFirst(w, 'a[href*="order.online"]');
  return last(w, 'order_buckhead') ? 'leaked' : true;
});
test('order_online_click accompanies location event', () => {
  const w = load('duluth.html');
  clickFirst(w, 'a[href*="order.online"]');
  const g = last(w, 'order_online_click');
  return g && g.location === 'duluth' ? true : 'missing or wrong: ' + JSON.stringify(g);
});
test('homepage location CTAs fire select_location, not a false order', () => {
  const w = load('index.html');
  const bh = [...w.document.querySelectorAll('a')].find(a => /order buckhead/i.test(a.textContent));
  const dl = [...w.document.querySelectorAll('a')].find(a => /order duluth/i.test(a.textContent));
  if (!bh || !dl) return 'CTAs not found';
  bh.dispatchEvent(new w.Event('click', { bubbles: true }));
  dl.dispatchEvent(new w.Event('click', { bubbles: true }));
  const evs = events(w);
  const sel = (w.dataLayer || []).filter(e => e.event === 'select_location').map(e => e.location);
  if (evs.includes('order_online_click')) return 'inflated order intent on a navigation click';
  return sel.includes('buckhead') && sel.includes('duluth') ? true : 'got ' + JSON.stringify(sel);
});

// ---- phone -----------------------------------------------------------------
test('phone_click Buckhead has location=buckhead', () => {
  const w = load('buckhead.html');
  clickFirst(w, 'a[href^="tel:"]');
  const e = last(w, 'phone_click');
  return e && e.location === 'buckhead' ? true : JSON.stringify(e);
});
test('phone_click Duluth has location=duluth', () => {
  const w = load('duluth.html');
  clickFirst(w, 'a[href^="tel:"]');
  const e = last(w, 'phone_click');
  return e && e.location === 'duluth' ? true : JSON.stringify(e);
});

// ---- directions ------------------------------------------------------------
test('directions_click Buckhead', () => {
  const w = load('buckhead.html');
  clickFirst(w, 'a[href*="maps.google"]');
  const e = last(w, 'directions_click');
  return e && e.location === 'buckhead' ? true : JSON.stringify(e);
});
test('directions_click Duluth', () => {
  const w = load('duluth.html');
  clickFirst(w, 'a[href*="maps.google"]');
  const e = last(w, 'directions_click');
  return e && e.location === 'duluth' ? true : JSON.stringify(e);
});

// ---- gift card -------------------------------------------------------------
test('gift_card_click fires', () => {
  const w = load('index.html');
  const el = clickFirst(w, 'a[href*="gift-card"]');
  if (!el) return 'no gift-card link on homepage';
  return last(w, 'gift_card_click') ? true : 'not fired';
});

// ---- view_item -------------------------------------------------------------
test('view_item fires on menu item page with real name', () => {
  const w = load('menu/cajun-alfredo.html');
  const e = last(w, 'view_item');
  if (!e) return 'not fired';
  if (!/Cajun Alfredo/i.test(e.item_name)) return 'item_name=' + e.item_name;
  return true;
});
test('view_item does NOT fire on non-item pages', () => {
  const w = load('catering.html');
  return last(w, 'view_item') ? 'fired incorrectly' : true;
});

// ---- purchase safety -------------------------------------------------------
test('no purchase event from order click', () => {
  const w = load('buckhead.html');
  clickFirst(w, 'a[href*="order.online"]');
  return events(w).includes('purchase') ? 'FAKE PURCHASE FIRED' : true;
});

// ---- lead events -----------------------------------------------------------
test('catering_lead NOT fired by clicking the mailto CTA', () => {
  const w = load('catering.html');
  clickFirst(w, 'a[href^="mailto:catering"]');
  return last(w, 'catering_lead') ? 'fired without confirmed submission' : true;
});
test('catering_lead fires from success callback', () => {
  const w = load('catering.html');
  w.bmCateringLead('buckhead');
  const e = last(w, 'catering_lead');
  return e && e.location === 'buckhead' && e.lead_type === 'catering' ? true : JSON.stringify(e);
});
test('franchise_lead fires from success callback', () => {
  const w = load('franchise.html');
  w.bmFranchiseLead();
  const e = last(w, 'franchise_lead');
  return e && e.lead_type === 'franchise' ? true : JSON.stringify(e);
});

// ---- dedupe ----------------------------------------------------------------
test('rapid double click does not double-fire', () => {
  const w = load('buckhead.html');
  const el = w.document.querySelector('a[href*="order.online"]');
  el.dispatchEvent(new w.Event('click', { bubbles: true }));
  el.dispatchEvent(new w.Event('click', { bubbles: true }));
  const n = events(w).filter(x => x === 'order_buckhead').length;
  return n === 1 ? true : 'fired ' + n + ' times';
});

// ---- location normalisation ------------------------------------------------
test('location values are only buckhead/duluth/unknown', () => {
  const pages = ['index.html', 'buckhead.html', 'duluth.html', 'menu.html', 'catering.html'];
  const bad = [];
  pages.forEach(p => {
    const w = load(p);
    w.document.querySelectorAll('a[href*="order.online"], a[href^="tel:"], a[href*="maps.google"]')
      .forEach(a => a.dispatchEvent(new w.Event('click', { bubbles: true })));
    (w.dataLayer || []).forEach(e => {
      if (e.location && !['buckhead', 'duluth', 'unknown', 'all'].includes(e.location)) bad.push(e.location);
    });
  });
  return bad.length === 0 ? true : 'bad values: ' + [...new Set(bad)].join(',');
});

// ---- output ----------------------------------------------------------------
console.log('='.repeat(70));
console.log('BITE MORE — ANALYTICS EVENT TESTS (jsdom, real pages, real clicks)');
console.log('='.repeat(70));
const w = Math.max(...results.map(r => r[0].length));
results.forEach(([n, r, d]) => console.log(n.padEnd(w) + '  ' + r + (d ? '  ' + d : '')));
const failed = results.filter(r => r[1] === 'FAIL');
console.log('-'.repeat(70));
console.log(`${results.length - failed.length}/${results.length} passed`);
process.exit(failed.length ? 1 : 0);

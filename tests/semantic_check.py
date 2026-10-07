from pathlib import Path
from bs4 import BeautifulSoup
import re,json,urllib.parse
root=Path(__file__).resolve().parents[1]; errors=[];count=0;faqs=0
for p in root.rglob('*.html'):
 if 'dist' in p.relative_to(root).parts:continue
 s=BeautifulSoup(p.read_text(),'html.parser');count+=1
 for a in s.select('a[href],script[src],link[href],img[src]'):
  u=a.get('href',a.get('src',''));v=urllib.parse.urlsplit(u)
  if v.scheme or u.startswith('//'):continue
  dest=(root/v.path.lstrip('/') if v.path.startswith('/') else p.parent/v.path).resolve()
  if not v.path:dest=p.resolve()
  if not dest.suffix and dest.with_suffix('.html').exists():dest=dest.with_suffix('.html')
  elif dest.is_dir():dest=dest/'index.html'
  if not dest.exists() and not dest.suffix:dest=dest.with_suffix('.html')
  if not dest.exists():errors.append(f'{p.name}: missing {u}')
  elif v.fragment and dest.suffix=='.html':
   target=BeautifulSoup(dest.read_text(),'html.parser')
   if not target.find(id=v.fragment):errors.append(f'{p.name}: missing anchor {u}')
 if 'branding' in p.parts:continue
 for sc in s.select('script[type="application/ld+json"]'):
  try:o=json.loads(sc.get_text())
  except Exception as e:errors.append(str(p)+': invalid JSON');continue
  if o.get('@type')=='FAQPage' and s.select('.faq details'):
   actual={d.summary.get_text(' ',strip=True):d.p.get_text(' ',strip=True) for d in s.select('.faq details') if d.summary and d.p}
   for q in o['mainEntity']:
    faqs+=1
    if q['name'] not in actual or q['acceptedAnswer']['text']!=actual[q['name']]:errors.append(str(p)+': schema/visible FAQ mismatch '+q['name'])
 if s.select_one('header.nav'):
  if len(s.select('main'))!=1:errors.append(str(p)+': missing/duplicate main')
  if not s.select_one('a.skip-link'):errors.append(str(p)+': missing skip link')
  if not s.select_one('header a[href$="app"]'):errors.append(str(p)+': missing app nav')
result={'htmlPages':count,'faqAnswersCompared':faqs,'errors':errors};(root/'qa-evidence/semantic-validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));raise SystemExit(bool(errors))

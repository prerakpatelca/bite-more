from pathlib import Path
from bs4 import BeautifulSoup
import json,sys
root=Path(__file__).resolve().parents[1];errors=[];restaurants=0;documents=0
facts={'buckhead':('Bite More Buckhead','+14705148473','3150 Roswell Rd NW, Suite A1','30305'),'duluth':('Bite More Duluth','+19432964518','2148 Duluth Hwy 120, Suite 117','30097')}
def walk(o,p):
 global restaurants
 if isinstance(o,dict):
  if o.get('@type')=='Restaurant':
   restaurants+=1;loc='duluth' if 'duluth' in str(o.get('name','')).lower() else 'buckhead';name,phone,address,zipc=facts[loc];url='https://bitemore.us/'+loc
   for field,expect in [('name',name),('url',url),('@id',url+'#restaurant'),('telephone',phone)]:
    if o.get(field)!=expect:errors.append(f'{p}: {field} mismatch {o.get(field)!r}')
   for field,expect in [('streetAddress',address),('postalCode',zipc)]:
    if o.get('address',{}).get(field)!=expect:errors.append(f'{p}: address {field} mismatch')
   if 'hasDeliveryMethod' in o or 'acceptsReservations' in o:errors.append(f'{p}: unsupported fulfillment/reservation fact')
  for v in o.values():walk(v,p)
 elif isinstance(o,list):
  for v in o:walk(v,p)
for p in root.rglob('*.html'):
 if 'dist' in p.parts or 'branding' in p.parts:continue
 s=BeautifulSoup(p.read_text(),'html.parser')
 for sc in s.select('script[type="application/ld+json"]'):
  documents+=1;o=json.loads(sc.get_text())
  if o.get('@context')!='https://schema.org':errors.append(f'{p}: missing/incorrect schema context')
  walk(o,p.relative_to(root))
result={'jsonLdDocuments':documents,'restaurantEntities':restaurants,'errors':errors};(root/'qa-evidence/location-schema.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));sys.exit(bool(errors))

from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import sys
ROOT=Path(sys.argv[1]).resolve()
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
 def do_GET(self):
  p=self.path.split('?')[0]
  if not Path(p).suffix and (ROOT/(p.lstrip('/')+'.html')).is_file(): self.path=p+'.html'
  super().do_GET()
ThreadingHTTPServer(('0.0.0.0',int(sys.argv[2])),Handler).serve_forever()

"""Build the static deployment directory without exposing source, tests or reports."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'dist'
if OUT.exists():shutil.rmtree(OUT)
OUT.mkdir()
for name in ['assets','branding','blog','menu','places','tags']:
 source=ROOT/name
 if source.exists():shutil.copytree(source,OUT/name)
for p in ROOT.iterdir():
 if p.is_file() and (p.suffix in {'.html','.ico','.xml','.webmanifest'} or p.name in {'robots.txt','llms.txt'}):shutil.copy2(p,OUT/p.name)
print('Built',OUT)

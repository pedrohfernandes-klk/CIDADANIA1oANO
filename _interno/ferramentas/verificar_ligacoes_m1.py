from pathlib import Path
from html.parser import HTMLParser
import json,re
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[2]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=[];self.writing=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='a' and 'href' in a:self.links.append(a['href'])
  if tag in ['textarea','input','form']:self.writing.append(tag)
errors=[];pages=[ROOT/'docs/index.html',*sorted((ROOT/'docs/m1').glob('*.html')),ROOT/'_interno/m1/professor.html']
for f in pages:
 s=f.read_text();p=Page();p.feed(s)
 if len(p.ids)!=len(set(p.ids)):errors.append(f'{f.name}: IDs repetidos')
 for url in p.links:
  u=urlsplit(url)
  if u.scheme or not u.path:continue
  target=(f.parent/unquote(u.path)).resolve()
  if not target.exists():errors.append(f'{f.relative_to(ROOT)} -> {url}')
 if re.match(r'passo-\d\d.html',f.name):
  if p.writing:errors.append(f'{f.name}: campos de escrita')
  for need in ['atividade','feedback','reiniciar','dados','estado']:
   if need not in p.ids:errors.append(f'{f.name}: falta {need}')
  cfg=json.loads(re.search(r'id="dados">(.*?)</script>',s,re.S)[1])
  for r in cfg['rounds']:
   if 'correct' in r and isinstance(r['correct'],int):assert 0<=r['correct']<len(r['options'])
assert len(list((ROOT/'docs/m1').glob('passo-*.html')))==10
assert not errors,'\n'.join(errors)
print(f'{len(pages)} páginas verificadas; ligações locais válidas; dez fichas sem campos de escrita.')

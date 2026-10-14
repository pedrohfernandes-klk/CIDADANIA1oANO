"""Obtém reproduções com domínio público declarado no registo de origem."""
from pathlib import Path
import urllib.request,urllib.parse,json,re,html,io,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/m1/imagens';OUT.mkdir(exist_ok=True)
FILES={
 'publico':'File:An Experiment on a Bird in an Air Pump by Joseph Wright of Derby, 1768.jpg',
 'caverna':'File:Platon Cave Sanraedam 1604.jpg',
 'shakespeare':'File:William Shakespeare Chandos Portrait.jpg',
 'stanislavski':'File:Konstantin Stanislavskiy 1912.jpg',
 'sisifo':'File:Punishment sisyph.jpg',
 'tchekhov':'File:Chekhov 1898 by Osip Braz.jpg',
 'juri':'File:The Jury by John Morgan.jpg',
 'leitura':'File:Johannes Vermeer - Girl Reading a Letter by an Open Window - Google Art Project.jpg',
}
def clean(s):return html.unescape(re.sub('<[^>]+>','',s)).strip()
def get(url):return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'EPI-Cidadania-educational/1.0 (educational resource)'}),timeout=25).read()
records={}
record_file=OUT/'creditos.json'
if record_file.exists():records=json.loads(record_file.read_text())
for key,name in FILES.items():
 if key in records and (OUT/(key+'.webp')).exists():continue
 try:
  url='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(dict(action='query',format='json',titles=name,prop='imageinfo',iiprop='url|extmetadata',iiurlwidth=1100))
  data=json.loads(get(url));page=next(iter(data['query']['pages'].values()));info=page['imageinfo'][0];meta=info['extmetadata']
  license=clean(meta.get('LicenseShortName',{}).get('value',''));copyright=meta.get('Copyrighted',{}).get('value','')
  if 'public domain' not in license.lower() and license.lower() not in ['cc0','pdm']:raise ValueError('Domínio público não confirmado: '+license)
  raw=get(info.get('thumburl',info['url']));im=Image.open(io.BytesIO(raw)).convert('RGB');im.thumbnail((1100,1000));im.save(OUT/(key+'.webp'),'WEBP',quality=83,method=6)
  records[key]={'file':key+'.webp','title':clean(meta.get('ObjectName',{}).get('value',name[5:])),'artist':clean(meta.get('Artist',{}).get('value','Autoria indicada no registo')),'date':clean(meta.get('DateTimeOriginal',{}).get('value','')),'source':info['descriptionurl'],'download':info.get('thumburl',info['url']),'license':license,'copyrighted':copyright,'retrieved':'2026-10-14','width':im.width,'height':im.height,'sha256':hashlib.sha256((OUT/(key+'.webp')).read_bytes()).hexdigest(),'modifications':'Redimensionamento e conversão para WebP, sem recorte.'}
  record_file.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');print(key,license,im.size,flush=True)
 except Exception as e:print(key,type(e).__name__,str(e),flush=True)
print('Imagens verificadas:',len(records),flush=True)

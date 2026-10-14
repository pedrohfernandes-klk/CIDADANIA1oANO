from pathlib import Path
import json,base64,html
from m1_contexto import CONTEXT
ROOT=Path(__file__).resolve().parents[2]
IMAGES=ROOT/'docs/m1/imagens'
def e(x):return html.escape(str(x))
def modes():
 return '''<section class="modo-uso nao-imprimir" aria-label="Forma de usar a página"><p>Como vais usar esta página?</p><div class="modos"><button type="button" class="modo-btn" data-set-mode="projecao" aria-pressed="false">Na aula</button><button type="button" class="modo-btn" data-set-mode="autonomo" aria-pressed="true">Ao meu ritmo</button><button type="button" class="modo-btn" data-set-mode="revisao" aria-pressed="false">Rever</button></div><p class="modo-explica" id="modo-explica"></p></section>'''
def image_uri(key,small=False):
 file=IMAGES/(key+('-mini.webp' if small else '.webp'))
 if not file.exists():raise FileNotFoundError(file)
 return 'data:image/webp;base64,'+base64.b64encode(file.read_bytes()).decode()
def model(c):
 labels=['O exemplo','O que permite perceber','A ligação ao argumento']
 return '<div class="modelo">'+''.join(f'<div><span>{label}</span><p>{e(text)}</p></div>' for label,text in zip(labels,c['essay']))+'</div>'
def terms(c):
 return '<dl class="termos">'+''.join(f'<div class="termo"><dt>{e(word)}</dt><dd>{e(meaning)}<span class="exemplo"><b>Por exemplo:</b> {e(example)}</span></dd></div>' for word,meaning,example in c['words'])+'</dl>'
def panel(key,label,title,content):
 return f'<section class="lesson-panel" id="{key}" data-panel="{key}" data-title="{e(label)}"><p class="panel-kicker">{e(label)}</p><h2>{e(title)}</h2>{content}</section>'
def step_page(step,head,refs,essays):
 c=CONTEXT[step['id']];records=json.loads((IMAGES/'creditos.json').read_text());credit=records[c['image']]
 nav='<nav class="context-toc" aria-label="Partes deste passo">'+''.join(f'<a href="#{key}" data-open-panel="{key}">{label}</a>' for key,label in [('observar','1 · Observar'),('conhecer','2 · Conhecer'),('perceber','3 · Relacionar'),('experimentar','4 · Experimentar'),('sala','5 · Na sala'),('rever','6 · Rever')])+'</nav>'
 body=head(step['title'],step['subtitle'])+modes()+nav
 visual=f'<p class="pergunta-guia">{e(c["hook"])}</p><figure class="imagem-obra"><img src="{image_uri(c["image"])}" alt="{e(c["alt"])}" width="{credit["width"]}" height="{credit["height"]}" decoding="async"><figcaption>{e(c["caption"])} <a href="{e(credit["source"])}" target="_blank" rel="noopener">Registo de origem · domínio público</a>.</figcaption></figure>'
 visual+='<div class="image-notes">'+''.join(f'<details><summary>{e(title)}</summary><p>{e(text)}</p></details>' for title,text in c['observe'])+'</div>'
 body+=panel('observar','1 · Observar','Começa por olhar',visual)
 chapters='<div class="context-body">'+''.join(f'<details class="context-chapter" open><summary>{e(title)}</summary><p>{e(text)}</p></details>' for title,text in c['chapters'])+'</div>'
 if c.get('reading'):
  label,excerpt,note=c['reading']
  chapters+=f'<section class="context-chapter"><h3>{e(label)}</h3><blockquote class="leitura-integral">{e(excerpt)}</blockquote><p class="credito">{e(note)}</p></section>'
 chapters+='<details><summary>Quero consultar as fontes</summary>'+refs(c['refs'])+'</details>'
 body+=panel('conhecer','2 · Conhecer','A obra e o problema',chapters)
 a,b,d,f,g=c['bridge']
 bridge='<p>Estas palavras ajudam a nomear o que estamos a observar.</p>'+terms(c)+f'<div class="ponte"><div><h3>{e(a)}</h3><p>{e(b)}</p></div><div><h3>{e(d)}</h3><p>{e(f)}</p></div></div><p class="ponte-conclusao">{e(g)}</p>'
 body+=panel('perceber','3 · Relacionar','Das palavras à situação',bridge)
 body+=panel('experimentar','4 · Experimentar','Escolher e perceber porquê','<p>Usa o que acabaste de conhecer. Escolhe, abre pistas e compara. Justifica oralmente antes de ler o comentário.</p><section class="exercicio"><div id="atividade"></div><aside class="feedback" id="feedback" role="status" aria-live="polite" hidden></aside></section><noscript><p>Ativa o JavaScript para usar as escolhas. O contexto, as imagens e os apoios à escrita continuam disponíveis.</p></noscript><div class="barra nao-imprimir"><span id="estado">Por explorar</span><button class="c-sec" id="reiniciar" type="button">Recomeçar o exercício</button></div>')
 room='<p>As propostas seguintes fazem-se oralmente e com o corpo. O professor escolhe a sequência adequada à aula.</p>'+''.join(f'<section class="atividade-oral"><h3>{e(name)}</h3><p>{e(text)}</p></section>' for name,text in c['oral'])
 room+='<p class="credito">As falas identificadas como texto original foram criadas para estas atividades. Não são excertos dos autores estudados.</p>'
 body+=panel('sala','5 · Na sala','Ler, representar, discutir',room)
 review='<ul>'+''.join(f'<li>{e(x)}</li>' for x in c['review'])+'</ul><h3>Do exemplo à explicação</h3><p>Repara na ligação entre as três partes. Usa este modo de construir o raciocínio com um exemplo teu.</p>'+model(c)
 review+=f'<details class="check-compreensao"><summary>{e(c["check"][0])}</summary><p>{e(c["check"][1])}</p></details>'
 review+='<p><a href="glossario.html">Consultar as palavras do módulo</a> · <a href="oficina-ensaio.html">Preparar um argumento para o ensaio</a></p>'
 body+=panel('rever','6 · Rever','O que levo deste passo',review)
 body+='<nav class="projection-nav nao-imprimir" aria-label="Momentos da aula"><button type="button" class="c-sec" id="panel-prev">← Anterior</button><span class="projection-label" id="projection-label"></span><button type="button" class="c-prim" id="panel-next">Seguinte →</button></nav>'
 body+='<section class="fichas-apoio">'+essays+'</section>' if essays else ''
 previous=f'passo-{int(step["id"])-1:02d}.html' if step['id']!='01' else 'index.html'
 following=f'passo-{int(step["id"])+1:02d}.html' if step['id']!='10' else 'ensaio-2.html'
 body+=f'<nav class="barra"><a class="c-sec" href="{previous}">← Voltar</a><a class="c-prim" href="{following}">'+('Próximo passo →' if step['id']!='10' else 'Preparar o segundo ensaio →')+'</a></nav>'
 return body

def index_page(steps,head):
 body=head('Ser-se humano','Quem conta como pessoa — e quem decide?',back='../index.html')
 body+='<p class="p-lead">Direitos humanos e democracia · Interpretação — Ator/atriz</p><div class="percurso-principal"><h2>Uma vida é mais do que um papel</h2><p>Um homem descobre que a sua vida é um espetáculo. Mais tarde, doze homens têm de decidir sobre alguém que não está na sala. Entre os dois filmes, vamos investigar liberdade, dignidade, informação e responsabilidade.</p><a class="c-prim" href="passo-01.html">Começar com Truman →</a></div>'
 for start,title,description in [(0,'I · Uma vida sob controlo','Conhecer Truman, perguntar pelo lugar do outro e construir o primeiro ensaio.'),(5,'II · Decidir com os outros','Entrar em Doze Homens em Fúria, investigar provas e preparar uma posição sobre democracia e responsabilidade.')]:
  body+=f'<section class="percurso-grupo"><p class="p-rot">Passos {start+1} a {start+5}</p><h2>{title}</h2><p>{description}</p><nav class="passos" aria-label="{e(title)}">'
  for s in steps[start:start+5]:
   c=CONTEXT[s['id']]
   body+=f'<a class="passo" href="passo-{s["id"]}.html"><span class="n">{s["id"]}</span><img class="thumb" src="{image_uri(c["image"],True)}" alt="" width="320" height="220" loading="lazy"><b>{e(s["title"])}</b><p class="p-nota">{e(s["subtitle"])}</p><p>{e(c["hook"])}</p><span class="badge" data-progresso="{s["id"]}">Por explorar</span></a>'
  body+='</nav></section>'
 body+='''<section class="materiais"><h2>Encontrar uma palavra, preparar uma ideia</h2><a href="glossario.html">Palavras explicadas com exemplos</a><a href="revisao.html">Rever os dez passos</a><a href="oficina-ensaio.html">Do exemplo ao argumento · oficina dos ensaios</a></section><section class="materiais"><h2>Investigar e escrever</h2><a href="guiao-1.html">Guião 1 · investigar Truman</a><a href="ensaio-1.html">Ficha 1 · primeiro ensaio</a><a href="guiao-2.html">Guião 2 · investigar Doze Homens em Fúria</a><a href="ensaio-2.html">Ficha 2 · segundo ensaio</a></section><section class="materiais"><h2>O que já trabalhámos</h2><a href="../aula-1.html">O que vemos · Platão, CHIROPTERA e This is Water</a><a href="../aula-2.html">O que somos · Sísifo e Abramović</a><a href="../projeto.html">Pergunta Humana · materiais anteriores</a><a href="anteriores/ficha-cd1.html">Primeira ficha de dignidade e investigação</a></section><details><summary>Como usar este percurso</summary><p>Em cada passo, começa pela imagem e conhece a obra antes de responder. Na aula, usa «Na aula» para mostrar um momento de cada vez. Em casa, escolhe «Ao meu ritmo». Antes dos ensaios, usa «Rever».</p><p>Os exercícios fazem-se com escolhas e justificações orais. A escrita fica nos guiões e fichas. O estado «Explorado» fica apenas neste aparelho e não é uma nota.</p></details><p class="credito"><a href="imagens.html">Imagens de domínio público · autores, datas e registos</a></p>'''
 return body

def write_support(out,shell,head):
 words={}
 for k,c in CONTEXT.items():
  for w,meaning,example in c['words']:words.setdefault(w,(meaning,example,k))
 body=head('Palavras que ajudam a pensar','Uma definição curta, um exemplo e um caminho de regresso')+'<p>Abre a palavra de que precisas. O exemplo ajuda a perceber como se usa numa situação.</p>'
 for w,(meaning,example,k) in sorted(words.items(),key=lambda x:x[0].lower()):body+=f'<details class="revisao-card"><summary>{e(w)}</summary><p>{e(meaning)}</p><p><b>Por exemplo:</b> {e(example)}</p><a href="passo-{k}.html#perceber">Voltar ao passo {k}</a></details>'
 (out/'glossario.html').write_text(shell('Palavras explicadas',body))
 body=head('Rever para compreender','Dez passos · relações, diferenças e exemplos')+'<p>Escolhe o passo que precisas de recuperar. Se uma referência ainda não é clara, regressa ao seu contexto antes de a usar no ensaio.</p>'
 for k,c in CONTEXT.items():body+=f'<section class="revisao-card"><p class="p-rot">Passo {k}</p><h2>{e(c["hook"])}</h2><ul>'+''.join(f'<li>{e(t)}</li>' for t in c['review'])+'</ul>'+model(c)+f'<a href="passo-{k}.html">Conhecer e explorar este passo →</a></section>'
 body+='<section class="materiais"><a href="oficina-ensaio.html">Construir a minha argumentação</a></section>'
 (out/'revisao.html').write_text(shell('Revisão dos dez passos',body))
 body=head('Do exemplo ao argumento','Uma oficina para os dois ensaios')+'''<p>Uma opinião ganha fundamento quando explicas o que a sustenta. Antes de escrever o texto completo, experimenta dizer estas ligações em voz alta.</p><div class="guiao-por-etapas"><section><h2>1 · Formula uma pergunta</h2><p>«A liberdade» é um tema. «Pode uma vida confortável não ser livre?» é uma pergunta que permite defender uma posição.</p><p class="frase-apoio">Quero investigar se… / O problema que encontro é…</p></section><section><h2>2 · Responde com uma tese</h2><p>A tese é a posição que vais procurar defender. Deve responder à pergunta. Pode ser limitada: «em certas condições», «quando», «desde que».</p><p class="frase-apoio">Defendo que… porque…</p></section><section><h2>3 · Escolhe uma cena e explica-a</h2><p>Indica uma ação concreta. Depois, explica o que permite perceber e como se relaciona com a tese. O leitor deve conseguir acompanhar o raciocínio mesmo que não se recorde de todos os pormenores do filme.</p>'''+model(CONTEXT['01'])+'''</section><section><h2>4 · Compara com rigor</h2><p>Encontra uma relação entre as obras e uma diferença. Explica por que razão essa diferença importa.</p><p class="frase-apoio">As duas situações aproximam-se porque… No entanto, diferem em… Esta diferença é importante porque…</p></section><section><h2>5 · Responde a uma objeção</h2><p>Apresenta uma dificuldade real da tua posição. Responde-lhe com razões. Se a dificuldade for forte, podes precisar de limitar ou reformular a tese.</p><p class="frase-apoio">Pode argumentar-se que… Essa dificuldade é relevante porque… Contudo… / Por isso, a minha posição precisa de reconhecer que…</p></section><section><h2>6 · Mostra de onde vem a informação</h2><p>Identifica autor ou instituição, título, data quando disponível e ligação. Distingue uma informação que retiras da fonte da interpretação que propões.</p><p class="frase-apoio">A fonte informa que… A partir desta informação, proponho que…</p></section></div><section class="materiais"><h2>Usar na ficha</h2><a href="ensaio-1.html">Primeiro ensaio · 250–350 palavras</a><a href="ensaio-2.html">Segundo ensaio · 400–600 palavras</a><a href="revisao.html">Rever exemplos dos dez passos</a></section>'''
 (out/'oficina-ensaio.html').write_text(shell('Oficina dos ensaios',body))
 body=head('Imagens para observar','Domínio público · a imagem também é uma fonte')+'<p>Estas imagens são objetos de observação, não fotografias dos filmes ou das performances. Cada legenda identifica a relação proposta. As reproduções foram redimensionadas e convertidas para WebP.</p>'
 records=json.loads((IMAGES/'creditos.json').read_text())
 for k,credit in records.items():
  captions=next(c for c in CONTEXT.values() if c['image']==k)
  body+=f'<figure class="imagem-obra revisao-card"><img src="{image_uri(k)}" alt="{e(captions["alt"])}" width="{credit["width"]}" height="{credit["height"]}" loading="lazy"><figcaption>{e(captions["caption"])}<br>Autoria no registo: {e(credit["artist"])}.<br>Direitos no registo: {e(credit["license"])}. Consulta: {e(credit["retrieved"])}.<br><a href="{e(credit["source"])}" target="_blank" rel="noopener">Consultar a proveniência e a declaração de direitos</a></figcaption></figure>'
 (out/'imagens.html').write_text(shell('Créditos das imagens',body))

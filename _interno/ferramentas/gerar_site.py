#!/usr/bin/env python3
"""Gera o site dos alunos de Cidadania I (pasta docs/, publicada com GitHub Pages).

Uso: python3 _interno/ferramentas/gerar_site.py

Só entra aqui material para os alunos: nada de planos do professor nem de chaves.
Cada página é autónoma (CSS e JS embutidos). As respostas dos alunos ficam
guardadas apenas no telemóvel ou computador de cada um (localStorage).
"""
from pathlib import Path
from html import escape

RAIZ = Path(__file__).resolve().parents[2]
DOCS = RAIZ / "docs"

CSS = """
:root{--fundo:#fff;--papel:#fff;--tinta:#000;--suave:#333;--cor:#2f6f7a;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--fundo:#000;--papel:#000;--tinta:#fff;--suave:#ccc;--cor:#7fc4cf;color-scheme:dark}}
:root[data-theme=dark]{--fundo:#000;--papel:#000;--tinta:#fff;--suave:#ccc;--cor:#7fc4cf;color-scheme:dark}
*{box-sizing:border-box}
html,body{margin:0;background:var(--fundo);color:var(--tinta)}
body{font:17px/1.5 Arial,Helvetica,sans-serif;-webkit-text-size-adjust:100%}
a{color:var(--tinta)}
.topo{position:sticky;top:0;z-index:5;background:var(--fundo);border-bottom:3px solid var(--tinta);padding:10px 16px 8px}
.topo .l1{display:flex;justify-content:space-between;align-items:baseline;gap:10px;max-width:720px;margin:auto}
.marca{font:900 11.5px/1.2 "Arial Black",Arial,sans-serif;text-transform:uppercase;letter-spacing:1px;text-decoration:none}
.topo nav{display:flex;gap:12px;flex-wrap:wrap;font:700 12.5px/1.2 Arial,sans-serif;text-transform:uppercase;letter-spacing:.6px}
.topo nav a{text-decoration:none;padding:4px 0}
.topo nav a[aria-current=page]{text-decoration:underline;text-decoration-thickness:3px;text-underline-offset:4px}
main{max-width:720px;margin:auto;padding:22px 16px 60px}
h1{font:900 34px/1 "Arial Black",Arial,sans-serif;text-transform:uppercase;border-top:10px solid var(--tinta);padding-top:12px;margin:0 0 6px;text-wrap:balance}
.sub{font-size:13px;text-transform:uppercase;letter-spacing:1px;margin:0 0 18px}
h2{font:900 13px/1 "Arial Black",Arial,sans-serif;letter-spacing:1px;text-transform:uppercase;background:var(--tinta);color:var(--fundo);padding:8px 9px;margin:34px 0 12px}
h3{font:900 16px/1.2 "Arial Black",Arial,sans-serif;text-transform:uppercase;margin:22px 0 8px;text-wrap:balance}
p{margin:0 0 12px;max-width:65ch}
ul,ol{margin:0 0 12px;padding-left:22px}li{margin-bottom:6px}
.citacao{border:2px solid var(--tinta);border-left:12px solid var(--tinta);padding:14px 16px;font-size:19px;line-height:1.4;margin:12px 0}
.citacao cite{display:block;font-size:12px;font-style:normal;font-weight:700;text-transform:uppercase;letter-spacing:.8px;margin-top:8px;color:var(--cor)}
.ret{margin:14px 0;padding:12px 14px;border:2px solid var(--tinta);border-left:12px solid var(--cor)}
.palavra{font:900 11.5px/1 "Arial Black",Arial,sans-serif;text-transform:uppercase;letter-spacing:1px;display:block;margin-bottom:6px}
.grelha{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(200px,100%),1fr));gap:10px;margin:12px 0}
.cartao{border:2px solid var(--tinta);padding:12px 14px;min-width:0}
.cartao b{display:block;font:900 11.5px/1.2 "Arial Black",Arial,sans-serif;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px}
.cartao.escuro{background:var(--tinta);color:var(--fundo)}
.lista{list-style:none;padding:0;margin:0}
.lista li{border-bottom:1px solid var(--tinta);margin:0}
.lista a{display:block;padding:14px 4px;min-height:48px;text-decoration:none}
.lista a b{display:block;font:900 20px/1.15 "Arial Black",Arial,sans-serif;text-transform:uppercase}
.lista a small{display:block;font-size:14px;color:var(--suave);margin-top:4px}
.passos{counter-reset:p;list-style:none;padding:0}
.passos li{counter-increment:p;position:relative;padding-left:48px;min-height:36px;margin-bottom:14px}
.passos li::before{content:counter(p);position:absolute;left:0;top:-2px;width:34px;height:34px;border-radius:50%;background:var(--tinta);color:var(--fundo);font:900 16px/34px "Arial Black",Arial,sans-serif;text-align:center}
table{width:100%;border-collapse:collapse;font-size:15px;margin:10px 0 14px}
th,td{border:2px solid var(--tinta);padding:8px 10px;text-align:left;vertical-align:top}
th{font:900 11.5px/1.2 "Arial Black",Arial,sans-serif;text-transform:uppercase;letter-spacing:.8px}
td.n{font-weight:700;font-variant-numeric:tabular-nums;white-space:nowrap}
.tabela{overflow-x:auto}
.ligacoes{list-style:none;padding:0}
.ligacoes li{border-left:4px solid var(--cor);padding:4px 0 4px 10px;margin-bottom:10px}
.ligacoes small{display:block;color:var(--suave);font-size:13.5px}
.aviso{font-size:14px;border:2px dashed var(--tinta);padding:10px 12px;margin:12px 0}
.campo{margin:12px 0 16px}
.campo label{display:block;font-weight:700;margin-bottom:6px}
textarea,input[type=text]{width:100%;font:inherit;padding:10px 12px;border:2px solid var(--tinta);background:var(--papel);color:var(--tinta);border-radius:0}
textarea{min-height:96px;resize:vertical}
.acoes{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}
.btn{min-height:48px;border:2px solid var(--tinta);background:var(--tinta);color:var(--fundo);font:700 14px/1 Arial,sans-serif;text-transform:uppercase;letter-spacing:.6px;padding:14px 18px;cursor:pointer}
.btn.sec{background:var(--fundo);color:var(--tinta)}
.estado{font-size:14px;min-height:20px;margin-top:8px}
.nota{font-size:13.5px;color:var(--suave)}
footer{max-width:720px;margin:0 auto;padding:16px 16px 40px;font-size:12.5px;border-top:2px solid var(--tinta)}
a:focus-visible,button:focus-visible,textarea:focus-visible,input:focus-visible{outline:3px solid var(--tinta);outline-offset:2px}
@media (max-width:480px){h1{font-size:27px}.topo .l1{flex-direction:column;gap:6px}}
@media print{.topo{position:static}.acoes,.topo nav{display:none}}
"""

JS = """
(function(){
  /* respostas guardadas só neste aparelho */
  function ler(k){try{return localStorage.getItem(k)}catch(e){return null}}
  function gravar(k,v){try{localStorage.setItem(k,v)}catch(e){}}
  var campos=[].slice.call(document.querySelectorAll('[data-guardar]'));
  campos.forEach(function(c){
    var k='cd1-'+c.dataset.guardar,v=ler(k);if(v!==null)c.value=v;
    c.addEventListener('input',function(){gravar(k,c.value)});
  });
  var copiar=document.getElementById('copiar'),estado=document.getElementById('estado');
  if(copiar)copiar.addEventListener('click',function(){
    var nome=(document.querySelector('[data-guardar=nome]')||{}).value||'';
    var txt=document.title+(nome?' · '+nome:'')+'\\n\\n'+campos.filter(function(c){return c.dataset.guardar!=='nome'}).map(function(c){
      var l=document.querySelector('label[for='+c.id+']');return (l?l.textContent:'')+'\\n'+(c.value||'(sem resposta)');
    }).join('\\n\\n');
    var ok=function(){estado.textContent='Copiado. Cola no e-mail ou na plataforma da turma.'};
    var falha=function(){var t=document.getElementById('texto-copia');t.hidden=false;t.value=txt;t.focus();t.select();estado.textContent='Não deu para copiar sozinho: o texto está selecionado em baixo, copia-o tu.'};
    if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(txt).then(ok,falha);else falha();
  });
})();
"""

NAV = [("index.html", "Início"), ("aula-1.html", "Aula 1"), ("aula-2.html", "Aula 2"), ("projeto.html", "Projeto")]


def pagina(ficheiro, titulo, corpo, diario=False):
    nav = "".join(
        f'<a href="{f}"{" aria-current=page" if f == ficheiro else ""}>{n}</a>' for f, n in NAV
    )
    script = f"<script>{JS}</script>" if diario else ""
    return f"""<!doctype html>
<html lang="pt-PT"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{escape(titulo)}</title>
<meta name="description" content="Cidadania e Desenvolvimento · Módulo 1 · Ser-se humano: investigação e informação · EPI 2026/2027">
<style>{CSS}</style></head><body>
<header class="topo"><div class="l1"><a class="marca" href="index.html">Cidadania I · INTP26</a><nav aria-label="Páginas do módulo">{nav}</nav></div></header>
<main>
{corpo}
</main>
<footer>Cidadania e Desenvolvimento · EPI – Escola Profissional de Imagem · 2026/2027 · turma INTP26. As respostas que escreves aqui ficam guardadas só no teu aparelho.</footer>
{script}
</body></html>
"""


def ligacoes(itens):
    out = '<ul class="ligacoes">'
    for t, url, nota in itens:
        alvo = f'<a href="{url}" target="_blank" rel="noopener">{t}</a>' if url else t
        out += f"<li>{alvo}{f'<small>{nota}</small>' if nota else ''}</li>"
    return out + "</ul>"


def diario(chave, perguntas):
    out = '<h2 id="diario">O teu diário de investigação</h2><p>Escreve aqui ou no teu caderno. Fica guardado só neste aparelho. No fim, copia e envia ao professor.</p>'
    out += '<div class="campo"><label for="nome">Nome</label><input type="text" id="nome" data-guardar="nome" autocomplete="name"></div>'
    for i, p in enumerate(perguntas, 1):
        out += f'<div class="campo"><label for="{chave}-{i}">{p}</label><textarea id="{chave}-{i}" data-guardar="{chave}-{i}"></textarea></div>'
    out += '<div class="acoes"><button class="btn" id="copiar" type="button">Copiar as minhas respostas</button></div><p class="estado" id="estado" role="status"></p><textarea id="texto-copia" hidden aria-label="Texto para copiar"></textarea>'
    return out


# ---------------------------------------------------------------- INÍCIO
INICIO = """
<h1>Ser-se humano</h1>
<p class="sub">Cidadania e Desenvolvimento · Módulo 1 · investigação e informação · 30 horas</p>
<p>Neste módulo fazemos duas perguntas ao mesmo tempo: <b>o que é ser humano?</b> e <b>como sabemos o que sabemos?</b> Partimos de filosofia, de arte e de performance, e acabamos com uma investigação vossa, apresentada em cena.</p>

<h2>As aulas</h2>
<ul class="lista">
<li><a href="aula-1.html"><b>Aula 1 · O que vemos</b><small>A caverna de Platão · CHIROPTERA, de JR, Damien Jalet e Thomas Bangalter · This is Water, de David Foster Wallace</small></a></li>
<li><a href="aula-2.html"><b>Aula 2 · O que somos</b><small>Sísifo e Albert Camus · Marina Abramović: Rhythm 0 e The Artist Is Present</small></a></li>
</ul>

<h2>O projeto</h2>
<ul class="lista">
<li><a href="projeto.html"><b>«Pergunta Humana»</b><small>Uma pergunta sobre ser-se humano, investigada a sério e transformada num teatro-documento de 5 a 8 minutos.</small></a></li>
</ul>

<h2>Como és avaliado</h2>
<p>Não há testes. Contam quatro trabalhos:</p>
<div class="tabela"><table>
<tr><th>Trabalho</th><th>Peso</th></tr>
<tr><td>Diário de investigação: duas ou três linhas no fim de cada aula</td><td class="n">20%</td></tr>
<tr><td>Laboratório de verificação: verificar afirmações com fontes</td><td class="n">20%</td></tr>
<tr><td>Dossiê de investigação do projeto (em grupo, com a tua parte identificada)</td><td class="n">30%</td></tr>
<tr><td>Teatro-documento: apresentação pública e defesa das escolhas</td><td class="n">30%</td></tr>
</table></div>
<p>Contam também a assiduidade, a pontualidade, o trabalho de equipa, o pensamento crítico, a autonomia e o respeito pelas regras. O limite de faltas do módulo é de 6 horas.</p>

<div class="ret"><span class="palavra">Diário</span>Cada aula tem, no fim da página, as perguntas do diário. Podes responder aqui, no telemóvel, e enviar ao professor com o botão «Copiar as minhas respostas».</div>
"""

# ---------------------------------------------------------------- AULA 1
AULA1 = """
<h1>O que vemos</h1>
<p class="sub">Aula 1 · Cidadania I · Ser-se humano</p>
<p>Três imagens de pessoas que não veem aquilo em que vivem: prisioneiros numa caverna, uma gruta pintada na fachada de uma ópera e dois peixes que não sabem o que é a água.</p>

<h2>1 · A caverna de Platão</h2>
<blockquote class="citacao">Suponhamos uns homens numa habitação subterrânea em forma de caverna, com uma entrada aberta para a luz. Estão lá dentro desde a infância, algemados de pernas e pescoços, de tal maneira que só lhes é dado permanecer no mesmo lugar e olhar em frente.<cite>Platão, A República, livro VII (c. 375 a.C.)</cite></blockquote>
<p>Atrás dos prisioneiros há um muro e um fogo. Pessoas passam por trás do muro com objetos, e o fogo projeta as sombras desses objetos na parede do fundo. Os prisioneiros só veem as sombras e julgam que são as próprias coisas.</p>
<h3>Sair da caverna, em quatro momentos</h3>
<ol class="passos">
<li><b>Sombras.</b> Toma-se a sombra pela coisa. Tudo parece claro.</li>
<li><b>Virar-se.</b> Um prisioneiro é solto e vê o fogo. A luz dói nos olhos.</li>
<li><b>Sair.</b> Sobe ao exterior e, aos poucos, vê as coisas e o sol.</li>
<li><b>Voltar.</b> Desce para contar o que viu. Os outros riem-se e não acreditam.</li>
</ol>
<h3>Que paredes temos hoje?</h3>
<div class="grelha">
<div class="cartao"><b>O feed</b>mostra o que um algoritmo escolheu para ti</div>
<div class="cartao"><b>A notícia partilhada</b>chega sem autor, sem data, sem contexto</div>
<div class="cartao"><b>A resposta da IA</b>soa segura, mesmo quando inventa</div>
<div class="cartao"><b>O grupo da turma</b>repete o que todos já pensam</div>
</div>
<div class="ret"><span class="palavra">A ideia a levar</span>Investigar é virar a cabeça: perguntar de onde vem a luz que faz a sombra.</div>

<h2>2 · CHIROPTERA</h2>
<p>Em 2023, o Palais Garnier, a Ópera de Paris, estava em obras. O artista <b>JR</b> cobriu os andaimes com uma enorme gruta pintada em trompe-l'œil: <i>Retour à la caverne</i> («Regresso à caverna»).</p>
<div class="grelha">
<div class="cartao"><b>Quando</b>12 de novembro de 2023, na Place de l'Opéra, à frente de milhares de pessoas.</div>
<div class="cartao"><b>Quem dança</b>Mais de 150 bailarinos na fachada, com coreografia de Damien Jalet.</div>
<div class="cartao"><b>A música</b>Thomas Bangalter (ex-Daft Punk): uma faixa de cerca de 17 minutos e uma versão de quase 6 horas.</div>
</div>
<p><i>Chiroptera</i> é o nome científico dos <b>morcegos</b>. Vivem nas grutas e orientam-se no escuro pelo eco: emitem um som e «ouvem» a forma das coisas. O prisioneiro de Platão só confia no que vê; o morcego confia noutra coisa.</p>
<div class="ret"><span class="palavra">Pergunta</span>A obra mostra-nos a caverna ou põe-nos dentro dela? E que «eco» podemos usar para nos orientarmos no meio de tanta informação?</div>

<h2>3 · This is Water</h2>
<blockquote class="citacao">Dois peixes jovens vão a nadar e cruzam-se com um peixe mais velho, que lhes acena e diz: «Bom dia, rapazes. Como está a água?» Os dois peixes nadam mais um bocado, até que um olha para o outro e pergunta: «Que raio é a água?»<cite>David Foster Wallace, discurso no Kenyon College, 21 de maio de 2005 · tradução livre</cite></blockquote>
<p>A <b>água</b> é aquilo que é tão constante que deixamos de ver. Wallace chama <i>default setting</i>, a configuração de fábrica, ao modo automático em que cada um se vê como o centro do mundo: a fila do supermercado, o trânsito e as outras pessoas parecem existir só para nos atrasar.</p>
<p>Para ele, pensar é escolher para onde olhar. A liberdade que conta faz-se de atenção, consciência e esforço, todos os dias.</p>

<h2>Juntar as três</h2>
<div class="grelha">
<div class="cartao"><b>Caverna · Platão</b>Tomamos sombras por coisas.</div>
<div class="cartao escuro"><b>Gruta na ópera · JR, Jalet, Bangalter</b>A arte põe a caverna à vista de milhares de pessoas de uma vez.</div>
<div class="cartao"><b>Água · Wallace</b>Não vemos aquilo em que vivemos.</div>
</div>
""" + diario("aula1", [
    "Qual é a tua água? Uma coisa que fazes em modo automático e que hoje viste pela primeira vez.",
    "Uma informação que aceitaste esta semana sem verificar. Onde a podias confirmar?",
]) + """
<h2>Para ir mais longe</h2>
<h3>Daqui, para onde?</h3>
<div class="grelha">
<div class="cartao"><b>De Platão</b>José Saramago, <i>A Caverna</i> (2000): um oleiro perde o trabalho para um centro comercial gigante, onde as obras descobrem uma gruta.<br><br>Peter Weir, <i>The Truman Show</i> (1998): um homem vive, sem saber, dentro de um programa de televisão.</div>
<div class="cartao"><b>De CHIROPTERA</b>Ai Weiwei, <i>Remembering</i> (Munique, 2009): 9 000 mochilas na fachada de um museu formam a frase de uma mãe: «Ela viveu feliz durante sete anos neste mundo.»<br><br>Ai Weiwei, <i>Citizens' Investigation</i> (2008–2011): sem números oficiais, voluntários apuraram os nomes de 5 196 alunos mortos no sismo de Sichuan.</div>
<div class="cartao"><b>De Wallace</b>Eli Pariser, <i>The Filter Bubble</i> (2011): a «água» do século XXI é o mundo que um algoritmo escolhe para cada um.<br><br>Ai Weiwei, <i>Rapture</i> (Lisboa, Cordoaria Nacional, 2021): obras sobre vigilância, refugiados e liberdade de expressão.</div>
</div>
<h3>Ligações</h3>
""" + ligacoes([
    ("Alegoria da caverna (Wikipédia)", "https://pt.wikipedia.org/wiki/Alegoria_da_caverna", "Platão, A República, livro VII. Tradução portuguesa: Maria Helena da Rocha Pereira, Fundação Calouste Gulbenkian."),
    ("JR, Retour à la caverne, Acte II: CHIROPTERA", "https://jr-art.net/projects/chiroptera", "Imagens e vídeo da performance, no site do artista."),
    ("Documentário «Dans la lumière», sobre CHIROPTERA", "https://ra.co/news/81822", "Realizado por Vincent Lorca, cerca de 30 minutos."),
    ("Thomas Bangalter, CHIROPTERA: a música", "https://musictech.com/news/music/thomas-bangalter-new-track-chiroptera/", ""),
    ("David Foster Wallace, This is Water: transcrição e áudio", "https://fs.blog/david-foster-wallace-this-is-water/", "O discurso completo, em inglês."),
    ("Ai Weiwei, Remembering (Britannica)", "https://www.britannica.com/topic/Remembering-art-installation-by-Ai-Weiwei", "Em inglês."),
    ("Ai Weiwei, Rapture, Lisboa 2021 (Lisson Gallery)", "https://lissongallery.com/news/rapture-a-major-exhibition-by-ai-weiwei-opens-at-cordoaria-nacional-in-lisbon", "Em inglês."),
])

# ---------------------------------------------------------------- AULA 2
AULA2 = """
<h1>O que somos</h1>
<p class="sub">Aula 2 · Cidadania I · Ser-se humano</p>
<p>Depois de «o que vemos», a pergunta muda: o que é isto de ser humano? Duas respostas: um mito grego lido por um escritor do século XX e uma artista que usa o próprio corpo como material.</p>

<h2>1 · Sísifo</h2>
<p>Sísifo, rei de Corinto, enganou os deuses e até a morte. O castigo: empurrar uma pedra até ao cimo de uma montanha. Mal chega lá acima, a pedra rola de volta, e ele recomeça. Para sempre. O mito aparece já na <i>Odisseia</i> de Homero (canto XI).</p>
<blockquote class="citacao">A própria luta para atingir os píncaros basta para encher um coração de homem. É preciso imaginar Sísifo feliz.<cite>Albert Camus, O Mito de Sísifo (1942), últimas linhas</cite></blockquote>
<div class="grelha">
<div class="cartao"><b>O absurdo</b>Queremos que a vida tenha sentido, e o mundo não nos responde.</div>
<div class="cartao"><b>A resposta de Camus</b>Não fugir: viver com lucidez e fazer da pedra a nossa coisa.</div>
</div>
<h3>Três Sísifos</h3>
<p>Em aula, empurrámos uma pedra imaginária de três maneiras: <b>desesperado</b> (a pedra é um castigo), <b>indiferente</b> (a pedra é só rotina) e <b>feliz</b> (a pedra é minha). A pedra era a mesma; o corpo mudou. É essa a ideia de Camus: o sentido que damos a uma tarefa muda a tarefa.</p>

<h2>2 · Marina Abramović</h2>
<p>Marina Abramović (Belgrado, 1946) é uma das artistas que definiram a <b>performance</b>, uma arte em que o material da obra é o corpo da própria artista.</p>
<h3>Rhythm 0 · Nápoles, 1974</h3>
<div class="grelha">
<div class="cartao"><b>6 horas</b>imóvel, numa galeria</div>
<div class="cartao"><b>72 objetos</b>numa mesa: de uma rosa e uma pena a uma tesoura e uma faca</div>
<div class="cartao"><b>1 instrução</b>o público podia usá-los nela como quisesse</div>
</div>
<p class="aviso">Ao longo das horas, parte do público passou de gestos inofensivos a gestos violentos, e houve quem a defendesse. As imagens e os relatos desta obra são fortes.</p>
<div class="ret"><span class="palavra">Pergunta</span>O que fazemos ao outro quando não há regras? A dignidade depende de a outra pessoa a respeitar? A Declaração Universal dos Direitos Humanos começa assim: «Todos os seres humanos nascem livres e iguais em dignidade e em direitos.» (artigo 1.º)</div>
<h3>The Artist Is Present · MoMA, Nova Iorque, 2010</h3>
<p>Durante quase três meses, mais de 736 horas no total, Abramović esteve sentada em silêncio no átrio do museu. Quem quisesse sentava-se à frente dela e olhava-a nos olhos o tempo que quisesse. Houve quem chorasse, quem risse e quem não aguentasse um minuto.</p>
<p>Em aula fizemos o mesmo, em pares, durante um minuto. Estar presente é o contrário do modo automático de que falava Wallace na aula 1.</p>

<h2>Ser humano é…</h2>
<div class="grelha">
<div class="cartao"><b>Sísifo</b>dar sentido a um esforço que não acaba</div>
<div class="cartao"><b>Rhythm 0</b>depender do modo como os outros nos tratam</div>
<div class="cartao"><b>The Artist Is Present</b>ser visto, e conseguir olhar o outro</div>
</div>
""" + diario("aula2", [
    "Qual é a tua pedra? Uma pedra que empurras todos os dias. Consegues imaginar-te feliz a empurrá-la?",
    "Uma palavra para o minuto em que olhaste o teu colega. Porquê essa?",
    "Uma pergunta sobre ser-se humano que gostavas de investigar no projeto.",
]) + """
<h2>Para ir mais longe</h2>
<h3>Daqui, para onde?</h3>
<div class="grelha">
<div class="cartao"><b>De Sísifo</b>Ticiano, <i>Sísifo</i> (1548–1549), no Museo del Prado, em Madrid: o corpo dobrado sob a pedra.<br><br>Albert Camus, <i>A Peste</i> (1947): uma cidade fechada por uma epidemia, onde a revolta deixa de ser de um e passa a ser de todos.</div>
<div class="cartao"><b>De Rhythm 0</b>Yoko Ono, <i>Cut Piece</i> (Tóquio, 1964): dez anos antes, sentada num palco, deixa o público cortar-lhe a roupa com uma tesoura.<br><br>O caso Kitty Genovese (Nova Iorque, 1964) deu origem à ideia de «efeito do espectador», mas em 2016 o <i>New York Times</i> admitiu que tinha exagerado o número de testemunhas. É um caso sobre quem só vê e também sobre informação errada.</div>
<div class="cartao"><b>De Abramović</b>Ai Weiwei, <i>Law of the Journey</i> (2016): um barco insuflável de 16 metros cheio de figuras humanas, os refugiados. Esteve em Lisboa em 2021.<br><br>Ai Weiwei, <i>Human Flow</i> (2017): documentário sobre refugiados em vários países do mundo.</div>
</div>
<h3>Ligações</h3>
""" + ligacoes([
    ("Sísifo (Wikipédia)", "https://pt.wikipedia.org/wiki/S%C3%ADsifo", "Homero, Odisseia, canto XI, tradução de Frederico Lourenço · Albert Camus, O Mito de Sísifo, 1942."),
    ("Marina Abramović, Rhythm 0 (Wikipédia)", "https://en.wikipedia.org/wiki/Rhythm_0", "Em inglês. Contém descrições de violência."),
    ("MoMA, Marina Abramović: The Artist Is Present (guia áudio)", "https://www.moma.org/audio/3118", "Em inglês."),
    ("Documentário «Marina Abramović: The Artist Is Present»", "", "Realizado por Matthew Akers, 2012."),
    ("MoMA, Yoko Ono: One Woman Show, 1960–1971 (inclui Cut Piece)", "https://www.moma.org/calendar/exhibitions/1494", "Em inglês."),
    ("O caso Kitty Genovese (Wikipédia)", "https://en.wikipedia.org/wiki/Murder_of_Kitty_Genovese", "Em inglês. Descreve um crime violento."),
    ("Ai Weiwei, Rapture, Lisboa 2021 (Lisson Gallery)", "https://lissongallery.com/news/rapture-a-major-exhibition-by-ai-weiwei-opens-at-cordoaria-nacional-in-lisbon", "Em inglês."),
])

# ---------------------------------------------------------------- PROJETO
PROJETO = """
<h1>Pergunta Humana</h1>
<p class="sub">Projeto do Módulo 1 · em grupo · teatro-documento</p>
<p>Cada grupo escolhe <b>uma pergunta sobre o que é ser humano</b>, investiga-a a sério e transforma o que encontrou num <b>teatro-documento</b> de 5 a 8 minutos, apresentado em público. No teatro-documento, o texto vem do que se investigou: entrevistas, documentos e dados, ditos em cena.</p>

<h2>Uma boa pergunta</h2>
<ul>
<li>Não se responde com «sim» ou «não».</li>
<li>Não se resolve com cinco minutos de pesquisa.</li>
<li>Pode ser investigada aqui: na escola, no bairro, na família, em fontes a que tens acesso.</li>
</ul>
<div class="grelha">
<div class="cartao"><b>Exemplo</b>Porque é que as pessoas assistem sem intervir quando alguém é humilhado?</div>
<div class="cartao"><b>Exemplo</b>O que muda numa pessoa quando muda de país?</div>
<div class="cartao"><b>Exemplo</b>Que pedra empurram todos os dias as pessoas da nossa rua?</div>
</div>

<h2>As fases</h2>
<ol class="passos">
<li><b>A pergunta.</b> Partir das perguntas do vosso diário e escolher uma em grupo.</li>
<li><b>O plano.</b> O que precisamos de saber? Quem vamos ouvir? Que fontes vamos procurar?</li>
<li><b>A recolha.</b> Entrevistas, inquéritos, observação, documentos, dados.</li>
<li><b>A verificação.</b> Cada informação importante tem de ter duas fontes independentes e credíveis.</li>
<li><b>O dossiê.</b> Pergunta, plano, fontes verificadas, entrevistas (com consentimento) e conclusões. Cada um identifica a sua parte.</li>
<li><b>O teatro-documento.</b> Escolher, montar e ensaiar 5 a 8 minutos a partir do material recolhido.</li>
<li><b>A apresentação.</b> Em público, seguida de debate. Têm de defender as vossas escolhas.</li>
</ol>

<h2>Verificar: leitura lateral</h2>
<ol class="passos">
<li><b>Sai da página.</b> Quem diz isto? Com que interesse?</li>
<li><b>Procura duas fontes independentes e credíveis:</b> universidade, revista científica, organismo oficial, verificação de factos. Duas páginas que se copiam uma à outra não contam.</li>
<li><b>Decide:</b> verdadeiro, falso, depende ou sem prova. E escreve porquê.</li>
</ol>
<p class="nota">Um assistente de inteligência artificial não é uma fonte: o que ele responde é mais uma afirmação a verificar.</p>

<h2>Ética: as pessoas que entrevistas</h2>
<ul>
<li><b>Consentimento.</b> Explica para que é a entrevista e pede autorização antes de gravar ou tomar notas. Se a pessoa for menor, é preciso também a autorização do encarregado de educação.</li>
<li><b>Anonimato.</b> Pergunta se a pessoa quer ser identificada. Em cena, podes mudar nomes e pormenores.</li>
<li><b>Dados pessoais.</b> Não publiques gravações, fotografias, moradas ou contactos de ninguém. Guarda o material só para o trabalho.</li>
<li><b>Respeito.</b> A pessoa pode desistir a qualquer momento, e o que disse sai do trabalho.</li>
</ul>

<h2>Avaliação</h2>
<div class="tabela"><table>
<tr><th>Trabalho</th><th>Peso</th></tr>
<tr><td>Diário de investigação (individual)</td><td class="n">20%</td></tr>
<tr><td>Laboratório de verificação</td><td class="n">20%</td></tr>
<tr><td>Dossiê de investigação (em grupo, com a tua parte identificada)</td><td class="n">30%</td></tr>
<tr><td>Teatro-documento: apresentação pública e defesa das escolhas</td><td class="n">30%</td></tr>
</table></div>
"""

PAGINAS = [
    ("index.html", "Cidadania I · Ser-se humano", INICIO, False),
    ("aula-1.html", "Aula 1 · O que vemos", AULA1, True),
    ("aula-2.html", "Aula 2 · O que somos", AULA2, True),
    ("projeto.html", "Projeto · Pergunta Humana", PROJETO, False),
]

if __name__ == "__main__":
    DOCS.mkdir(exist_ok=True)
    (DOCS / ".nojekyll").write_text("")
    for f, t, corpo, d in PAGINAS:
        (DOCS / f).write_text(pagina(f, t, corpo, d), encoding="utf-8")
        print(DOCS / f)

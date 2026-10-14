from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/m1/materiais';OUT.mkdir(parents=True,exist_ok=True)
for name,file in [('Sans','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Serif','DejaVuSerif.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
pdfmetrics.registerFont(TTFont('Bebas',str(Path(__file__).parent/'identidade/BebasNeue-Regular.ttf')))
W,H=A4;M=47;CW=W-2*M;INK=colors.HexColor('#171717');RED=colors.HexColor('#c8232c');GRAY=colors.HexColor('#555555')
ST={k:ParagraphStyle(k,fontName=font,fontSize=size,leading=leading,textColor=INK) for k,font,size,leading in [('body','Serif',10,14),('q','Sans',10.5,15),('small','Sans',8.5,12),('guide','Sans',10,14)]}
def p(c,text,y,style='q',width=CW,x=M):
 obj=Paragraph(text,ST[style]);_,h=obj.wrap(width,800);assert y-h>47,(text[:70],y,h);obj.drawOn(c,x,y-h);return y-h
def header(c,num,label):
 # O contorno e as letras do logótipo são os vetores do site oficial da EPI.
 from reportlab.graphics.shapes import Drawing,Path as RPath
 # SVG conservado na versão HTML; a versão PDF usa o mesmo logótipo rasterizado.
 from reportlab.lib.utils import ImageReader
 import io,base64
 logo=Path(__file__).parent/'identidade/epi-pdf.png'
 if logo.exists():c.drawImage(str(logo),M,H-61,width=91,height=36,mask='auto')
 else:
  c.setStrokeColor(INK);c.rect(M,H-58,32,32);c.setFont('Sans',12);c.drawString(M+8,H-47,'epi');c.setFont('Bold',5);c.drawString(M+38,H-38,'ESCOLA PROFISSIONAL');c.drawString(M+38,H-46,'DE IMAGEM')
 c.setFillColor(RED);c.setFont('Bold',8);c.drawRightString(W-M,H-35,'CIDADANIA E DESENVOLVIMENTO')
 c.setFillColor(GRAY);c.setFont('Sans',8);c.drawRightString(W-M,H-49,'Módulo 1 · Interpretação — Ator/atriz · INTP26')
 c.setStrokeColor(colors.HexColor('#dddddd'));c.line(M,38,W-M,38);c.setFont('Sans',7.5);c.drawString(M,25,'Direitos Humanos e Democracia · EPI · Pedro Fernandes');c.drawRightString(W-M,25,f'{label} | {num}')
def title(c,label,heading,sub=''):
 c.setFillColor(INK);c.setFont('Bold',8);c.drawString(M,H-71,label);c.setStrokeColor(INK);c.rect(M-5,H-77,pdfmetrics.stringWidth(label,'Bold',8)+10,17)
 c.setFont('Bebas',26);c.drawString(M,H-102,heading.upper());y=H-117
 if sub:y=p(c,sub,y,'small')-12
 return y-6
def lines(c,y,n,gap=20):
 c.setStrokeColor(colors.HexColor('#b7c0c4'));c.setLineWidth(.45)
 for i in range(n):y-=gap;assert y>48;c.line(M,y,W-M,y)
 return y-18
def q(c,n,text,y,count=4):
 y=p(c,f'<font name="Bold">{n}.</font> '+text,y);return lines(c,y,count)

f=OUT/'Doze_Homens_Guiao_Investigacao.pdf';c=canvas.Canvas(str(f),pagesize=A4);c.setTitle('Antes de decidir | Guião de investigação');c.setAuthor('Pedro Fernandes')
header(c,1,'Investigação');y=title(c,'PREPARAÇÃO DO SEGUNDO FILME','Antes de decidir','Doze Homens em Fúria · Sidney Lumet, 1957')
y=p(c,'Na aula, veremos <i>Doze Homens em Fúria</i>. Observa como os jurados falam, escutam, ocupam o espaço e mudam — ou mantêm — as suas posições. A investigação prepara o segundo ensaio, em que relacionarás este filme com <i>The Truman Show</i>.',y,'guide')-14
y=p(c,'<font name="Bold">Escolhe dois caminhos de investigação</font>',y)-10
items=[
 ('PROVA E INTERPRETAÇÃO','O que é apresentado como evidência? Que conclusões vão além do que se pode demonstrar? Distingue uma observação da interpretação que uma personagem faz dela.'),
 ('PRECONCEITO E IGUALDADE','Que ideias sobre a origem, a pertença ou a condição de uma pessoa influenciam a decisão? Relaciona com a dignidade e com a igualdade de direitos.'),
 ('MAIORIA E DISCORDÂNCIA','Quando ajuda uma discordância a decidir melhor? Observa a diferença entre contar votos e discutir razões.'),
 ('O TRABALHO DO ATOR','Escolhe uma personagem: o que quer, que ação usa e como reage à resistência? Relaciona com Stanislavski e com a tradição do Actors Studio. Compreender uma ação significa justificá-la?'),
 ('A PESSOA AUSENTE','Quem é discutido sem estar na sala? Relaciona com Truman e com a intervenção de Sylvia. Pergunta quem fala, de quem se fala e quem não consegue responder.'),
 ('UMA TERCEIRA REFERÊNCIA','Escolhe Shakespeare, Pinter, Sarah Kane, Tchékhov, Abramović, Platão, Sísifo, The Egg ou CHIROPTERA. Procura uma relação com o filme e uma diferença que não devas apagar.'),
]
for i,(h,t) in enumerate(items,1):y=p(c,f'<font name="Bold" color="#c8232c">{i:02d} / {h}</font> — '+t,y,'guide')-9
y=p(c,'<font name="Bold">Traz para a próxima aula</font>',y)-7
y=p(c,'Duas fontes identificadas; uma cena de cada filme; uma ligação a outra referência estudada; uma objeção à tua posição; e uma pergunta de investigação. Regista por palavras tuas e separa a informação da tua interpretação.',y,'guide')-13
y=p(c,'<font name="Bold">Contexto e fontes de partida</font>',y,'small')-5
y=p(c,'O filme apresenta um júri dos Estados Unidos. Não descreve o sistema judicial português. A presunção de inocência não equivale a uma certeza sobre o que aconteceu.',y,'small')-8
p(c,'<link href="https://www.loc.gov/item/96513458/" color="#c8232c">Library of Congress · ficha do filme</link> · <link href="https://unric.org/pt/declaracao-universal-dos-direitos-humanos/" color="#c8232c">ONU / UNRIC · direitos humanos</link><br/><link href="https://theactorsstudio.org/who-we-are/our-history/" color="#c8232c">Actors Studio · história</link> · <link href="https://livingarchive.royalcourttheatre.com/" color="#c8232c">Royal Court · arquivo de teatro</link><br/>As ligações são clicáveis. Recupera também os materiais das aulas anteriores.',y,'small');c.save()

TEXT=[
 'Em The Truman Show, muitas pessoas conhecem a verdade sobre a vida de Truman, mas só ele é impedido de a conhecer. Em Doze Homens em Fúria, um grupo tem de avaliar informação antes de decidir sobre outra pessoa. Nos dois filmes, o problema não se limita ao que alguém sabe: importa perceber como usa esse conhecimento e quem suporta as consequências.',
 'Truman acredita que escolhe a sua vida. Porém, o programa prepara obstáculos, explora os seus medos e controla as relações em que confia. O conforto de Seahaven não lhe permite aceitar ou recusar a situação, porque desconhece a sua verdadeira natureza. A liberdade exige informação e uma possibilidade real de agir.',
 'No segundo filme, a discussão entre os jurados mostra como uma primeira impressão pode parecer uma certeza. Uma prova precisa de ser examinada: o que demonstra, que interpretação admite e que condições podem limitar o seu valor? Discordar pode abrir uma investigação mais rigorosa. Isso não significa que qualquer dúvida tenha o mesmo fundamento ou que todas as opiniões sejam igualmente sustentadas.',
 'A igualdade também está em causa quando uma decisão depende de ideias feitas sobre o grupo a que uma pessoa pertence. A dignidade não pode depender da origem, da condição social ou da popularidade. Os artigos 1.º, 7.º, 10.º e 11.º da Declaração Universal dos Direitos Humanos permitem relacionar igual dignidade, igualdade perante a lei, julgamento justo e presunção de inocência.',
 'Há uma diferença importante entre votar e deliberar. Votar regista escolhas; deliberar envolve ouvir razões, examinar informação e considerar objeções. Uma maioria pode decidir com base em preconceitos ou em dados insuficientes. Por isso, uma sociedade democrática precisa de procedimentos justos, proteção dos direitos e possibilidades de contestação.',
 'A turma de Interpretação pode observar como os atores tornam visíveis objetivos, resistências e mudanças de posição. Stanislavski e a tradição desenvolvida no Actors Studio ajudam a investigar o trabalho do ator, mas compreender uma personagem não significa aprovar as suas ações. Marlon mantém o papel para conservar o engano; Sylvia rompe com ele para devolver informação a Truman.',
 'As outras referências estudadas abrem perguntas diferentes. Shakespeare permite investigar quem precisa de reclamar reconhecimento; Pinter, como uma autoridade se torna difícil de questionar; Sarah Kane, como escutamos vozes que não compreendemos inteiramente. Tchékhov e Abramović ajudam a distinguir expectativa dramática, consentimento e responsabilidade perante um perigo.',
 'Comparar obras não exige torná-las equivalentes. Um júri, um programa de televisão e uma performance têm condições diferentes. A comparação ganha rigor quando explica essas diferenças e identifica um problema comum. Antes de decidir sobre alguém, importa perguntar: ouvi essa pessoa, verifiquei a informação e posso responder pelos efeitos da minha decisão?'
]
f=OUT/'Doze_Homens_Ficha_Ensaio.pdf';c=canvas.Canvas(str(f),pagesize=A4);c.setTitle('Decidir sobre o outro | Ficha para o ensaio 2');c.setAuthor('Pedro Fernandes')
header(c,1,'Leitura');y=title(c,'TEXTO DE APOIO','Decidir sobre o outro','Dois filmes · informação, dignidade e democracia')
for i,t in enumerate(TEXT,1):y=p(c,f'<font name="Bold" color="#c8232c">{i}.</font> '+t,y,'body')-7
p(c,'Texto original de apoio. Referências: The Truman Show (Peter Weir, 1998); 12 Angry Men (Sidney Lumet, 1957); Declaração Universal dos Direitos Humanos; história institucional do Actors Studio. Os artigos são sintetizados, sem transcrição.',y,'small');c.showPage()
header(c,2,'Interpretação');y=title(c,'COMPREENDER E COMPARAR','Da informação à decisão')
y=p(c,'Nome: __________________________________ N.º: _____ Turma: __________<br/>Data: ____ / ____ / ______',y)-14
y=p(c,'Responde em papel, por frases completas e por palavras tuas. Usa o texto e cenas dos filmes para fundamentar as respostas.',y,'small')-18
y=q(c,1,'Explica a diferença entre a situação de Truman e a dos jurados perante a informação (parágrafos 1 a 3).',y,4)
y=q(c,2,'Explica por que razão uma primeira impressão não deve ser tratada como uma certeza. Usa um exemplo do segundo filme (parágrafo 3).',y,5)
y=q(c,3,'Distingue votar de deliberar e explica como uma maioria pode tomar uma decisão injusta (parágrafo 5).',y,5)
y=q(c,4,'Compara Marlon e Sylvia. Que relação existe entre o papel que representam e a responsabilidade que assumem (parágrafo 6)?',y,4);c.showPage()
header(c,3,'Planificação');y=title(c,'INVESTIGAR E PLANEAR','Uma tese que possa ser defendida')
y=p(c,'<font name="Bold">5.</font> Escolhe uma pergunta para o ensaio: proteção e controlo; maioria e justiça; responsabilidade de quem assiste; ou compreensão e responsabilidade do ator. Podes propor outra pergunta ao professor.',y)-15
for label,n in [
 ('A pergunta que vou investigar e a tese que vou defender:',3),
 ('Dois argumentos e uma cena de cada filme que os sustente:',5),
 ('Dois direitos ou princípios democráticos e a ligação aos exemplos:',3),
 ('Uma terceira referência: relação e diferença em comparação com os filmes:',3),
 ('Uma objeção à tese e a minha resposta:',3),
]:y=p(c,'<font name="Bold">'+label+'</font>',y);y=lines(c,y,n,18)
p(c,'Fontes: identifica pelo menos duas. Seleciona-as pela relação com a pergunta, pela autoria e pela possibilidade de verificar a informação.',y,'small');c.showPage()
header(c,4,'Ensaio 2');y=title(c,'ESCREVER E FUNDAMENTAR','O meu ensaio')
y=p(c,'<font name="Bold">6.</font> Escreve um ensaio de <font name="Bold">400 a 600 palavras</font>. Apresenta uma tese, dois argumentos, uma cena de cada filme, uma terceira referência estudada, uma objeção e uma conclusão. Relaciona os exemplos com direitos humanos e democracia.',y,'small')-10
y=p(c,'Título: ___________________________________________________________',y)-2
lines(c,y,27,19);c.showPage()
header(c,5,'Ensaio 2');y=title(c,'CONTINUAR E REVER','Do argumento à conclusão')
y=lines(c,y,18,19)
y=p(c,'<font name="Bold">Fontes consultadas</font> — autor ou instituição, título e ligação. A lista de referências não entra na contagem de palavras.',y,'small')-3
y=lines(c,y,4,19)
p(c,'Revisão: tese clara • argumentos explicados • exemplos dos dois filmes analisados • relação e diferença entre referências • direitos e democracia • objeção enfrentada • fontes identificadas • linguagem revista',y,'small');c.save()

INTERNAL=ROOT/'_interno/m1';INTERNAL.mkdir(parents=True,exist_ok=True)
f=INTERNAL/'Doze_Homens_Guia_Professor.pdf';c=canvas.Canvas(str(f),pagesize=A4);c.setTitle('Professor | Respostas e critérios do ensaio 2');c.setAuthor('Pedro Fernandes')
header(c,1,'Professor');y=title(c,'RESPOSTAS ORIENTADORAS','Informação e responsabilidade','Aceitar formulações equivalentes e interpretações fundamentadas.')
answers=[
 ('1. Situações perante a informação','Truman é impedido de conhecer a realidade que organiza a sua vida. Os jurados recebem informação que têm de avaliar criticamente antes de decidir. Em ambos os casos, importa analisar a relação entre conhecimento, poder e efeitos sobre outra pessoa.'),
 ('2. Primeira impressão e certeza','Uma impressão pode assentar em informação incompleta, preconceitos ou interpretações não verificadas. Aceitar um exemplo do filme que identifique o dado, a interpretação inicial e a razão da sua revisão. Não confundir dúvida fundamentada com recusa de toda a evidência.'),
 ('3. Votação e deliberação','Votar regista as escolhas; deliberar exige discutir razões, avaliar informação e considerar objeções. Uma maioria pode tomar uma decisão injusta quando usa dados insuficientes, preconceitos ou impede a pessoa afetada de ser ouvida. A igualdade de participação não elimina a exigência de fundamento.'),
 ('4. Marlon e Sylvia','Marlon usa a representação de uma amizade para manter Truman enganado. Sylvia interrompe o papel para lhe revelar a verdade, aceitando o risco de ser afastada. A diferença mostra que cumprir o papel não elimina a responsabilidade pelos efeitos sobre uma pessoa real.'),
 ('5. Planificação','Verificar se a tese responde à pergunta; se os argumentos são distintos; se há uma cena de cada filme; se os direitos são explicados; se a terceira referência inclui uma relação e uma diferença; e se a objeção enfrenta uma dificuldade real. As fontes devem ser adequadas à pergunta, identificadas e verificáveis.'),
 ('6. Ensaio','Avaliar a posição e a fundamentação, sem exigir uma opinião predeterminada. O aluno deve explicar as relações entre as obras e os princípios de cidadania. Um resumo extenso do enredo não substitui a análise. A referência ao ator pode partir da ação, do objetivo, do papel e da consciência profissional.'),
]
for h,t in answers:y=p(c,'<font name="Bold" color="#c8232c">'+h+'</font>',y)-5;y=p(c,t,y,'guide')-17
c.showPage();header(c,2,'Professor');y=title(c,'AVALIAÇÃO E ACOMPANHAMENTO','Do primeiro ao segundo ensaio')
y=p(c,'O primeiro ensaio, centrado em Truman, fornece feedback sobre tese, argumento e objeção. O segundo alarga a análise aos dois filmes e a uma terceira referência. As fichas interativas trabalham reconhecimento, decisão e revisão, sem produção textual.',y,'guide')-18
y=p(c,'<font name="Bold">Grelha sugerida: 20 pontos</font>',y)-10
for h,t in [
 ('Tese · 3','Posição clara que responde à pergunta escolhida.'),
 ('Argumentos e cidadania · 5','Dois argumentos explicados, com relação pertinente a direitos humanos e princípios democráticos.'),
 ('Exemplos e comparação · 4','Uma cena de cada filme analisada e uma terceira referência relacionada, incluindo uma diferença relevante.'),
 ('Objeção e resposta · 3','Dificuldade real reconhecida e enfrentada com fundamento.'),
 ('Organização e linguagem · 3','Progressão das ideias, conclusão, clareza e correção linguística. Considerar a extensão pedida sem aplicar uma dupla penalização.'),
 ('Fontes · 2','Pelo menos duas fontes identificadas, adequadas e usadas de forma verificável.'),
]:y=p(c,'<font name="Bold">'+h+'</font> — '+t,y,'guide')-11
y-=8
y=p(c,'<font name="Bold">Precisão conceptual</font>',y)-9
y=p(c,'O segundo filme apresenta um júri dos Estados Unidos. A presunção de inocência não exige demonstrar com certeza o que ocorreu. Não equiparar maiorias a injustiça automática, sistema de Stanislavski ao Método, autora a voz dramática ou participação consentida a autorização ilimitada.',y,'guide')-16
y=p(c,'<font name="Bold">Referências e continuidade</font>',y)-9
y=p(c,'A ficha oficial do módulo e os materiais anteriores foram conservados no repositório. Esta grelha e os ensaios são a proposta do novo percurso; não substituem administrativamente os parâmetros da ficha oficial.',y,'small')-10
p(c,'<link href="https://www.loc.gov/item/96513458/" color="#c8232c">Library of Congress · 12 Angry Men</link><br/><link href="https://unric.org/pt/declaracao-universal-dos-direitos-humanos/" color="#c8232c">ONU / UNRIC · Declaração Universal dos Direitos Humanos</link><br/><link href="https://theactorsstudio.org/who-we-are/our-history/" color="#c8232c">Actors Studio · história</link><br/>Textos e casos da ficha: elaboração original para INTP26. Fontes adicionais nos passos interativos.',y,'small');c.save()
print('Criados três PDFs em',OUT)

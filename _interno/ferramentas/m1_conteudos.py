"""Conteúdos originais do percurso. As situações inventadas são identificadas."""
SOURCES={
 'direitos':('ONU / UNRIC · Declaração Universal dos Direitos Humanos','https://unric.org/pt/declaracao-universal-dos-direitos-humanos/'),
 'egg':('Andy Weir · The Egg · original em inglês','https://galactanet.com/oneoff/theegg_mod.html'),
 'shakespeare':('Folger Shakespeare Library · O Mercador de Veneza · III, 1','https://www.folger.edu/explore/shakespeares-works/the-merchant-of-venice/read/3/1/'),
 'abramovic':('MoMA · Marina Abramović fala sobre Rhythm 0','https://www.moma.org/audio/playlist/243/3118'),
 'studio':('Actors Studio · história e raízes do trabalho','https://theactorsstudio.org/who-we-are/our-history/'),
 'chekhov':('Anton Tchékhov · carta a Lazarev, 1 de novembro de 1889 · original russo','https://predanie.ru/book/221237-pisma-1888-1889/?chapter=chapter_224'),
 'pinter':('Royal Court · The Dumb Waiter / O Monta-Cargas','https://livingarchive.royalcourttheatre.com/plays/the-dumb-waiter/'),
 'kane':('Royal Court · Crave, de Sarah Kane','https://livingarchive.royalcourttheatre.com/plays/crave/'),
 'chiroptera':('Damien Jalet · CHIROPTERA · JR, Damien Jalet e Thomas Bangalter','https://damienjalet.com/project/chiroptera/'),
 'filme2':('Library of Congress · 12 Angry Men · Sidney Lumet, 1957','https://www.loc.gov/item/96513458/'),
 'lumet':('BFI · Doze Homens em Fúria: espaço, atores e deliberação','https://www.bfi.org.uk/features/sidney-lumets-first-last-films-12-angry-men-before-devil-knows-youre-dead'),
}

def close(title,text,discuss):return dict(title=title,text=text,discuss=discuss)
def option(label,feedback):return dict(label=label,feedback=feedback)
def quiz(title,scene,question,options,correct,feedback,type='classify'):
 return dict(title=title,scene=scene,question=question,options=options,correct=correct,feedback=feedback,type=type)

STEPS=[
dict(id='01',title='Uma vida em direto',subtitle='The Truman Show entra aqui.',type='perspective',icon='camera',refs=['direitos'],
 intro='Vê o filme na aula. Depois, abre as posições. Truman acredita viver uma vida comum; o programa organiza aquilo que ele pode conhecer e escolher.',
 aim='Reconhecer o que cada interveniente sabe, o poder de que dispõe e a responsabilidade que assume.',
 previous='As páginas «O que vemos» e «O que somos» ajudam a recuperar a caverna, CHIROPTERA, Sísifo e Abramović.',
 rounds=[
 dict(title='Quem sabe o quê?',question='Abre as quatro posições antes de tomar partido.',roles=[
 dict(label='Truman',text='Vive as relações como reais. Ignora as câmaras e o guião. As suas decisões assentam numa informação que lhe foi preparada.'),
 dict(label='Christof',text='Conhece a estrutura do programa. Decide acontecimentos, controla informação e apresenta o seu domínio como proteção.'),
 dict(label='Marlon',text='Sabe que representa um amigo. Recebe palavras de Christof e usa a confiança de Truman para manter o engano.'),
 dict(label='Sylvia',text='Sabe que o mundo de Truman é encenado. Procura revelar-lhe a verdade e é afastada. Recusa subordinar a pessoa ao papel.')],
 feedback='Saber mais e poder intervir altera a responsabilidade. Truman suporta os efeitos de decisões em que não pode participar.'),
 dict(title='A tempestade',scene='Truman tenta sair de barco. Christof provoca uma tempestade que o põe em perigo.',question='Como lês esta decisão?',type='branch',options=[
 option('É uma forma de proteção.','A proteção alegada entra em conflito com o perigo criado. Que interesse está Christof a proteger neste momento?'),
 option('É uma tentativa de manter o controlo.','A fuga ameaça o programa. A tempestade torna visível o poder exercido sobre Truman e o risco que esse poder aceita impor-lhe.'),
 option('A responsabilidade é apenas de Truman, porque decidiu sair.','Escolher sair não autoriza outra pessoa a criar deliberadamente um perigo. Distingue o risco da viagem do risco imposto pelo programa.')]),
 ],close=close('A pessoa antes do programa','O filme fornece o primeiro caso do módulo: uma pessoa é usada para sustentar um espetáculo sem poder aceitar ou recusar a situação.','Debate: quem tinha condições para intervir antes da tempestade?')),

dict(id='02',title='Abrir a caverna',subtitle='Aparência, informação e evidência.',type='reveal',icon='cave',refs=['chiroptera'],
 intro='Abre as pistas uma a uma. Distingue aquilo que observas da explicação que propões. Relaciona Seahaven com a caverna de Platão.',
 aim='Distinguir observação, hipótese e conclusão; reconhecer os limites da informação disponível.',
 rounds=[
 dict(title='Uma falha no cenário',question='Que conclusão é sustentada pelas três pistas?',clues=['Um objeto de iluminação cai perto de Truman.','Uma emissão de rádio parece acompanhar os seus movimentos.','Algumas pessoas repetem percursos de forma invulgar.'],options=['Existe motivo para investigar uma realidade organizada à sua volta.','Todos os seus conhecidos querem matá-lo.','Qualquer vida repetitiva é um programa de televisão.'],correct=0,feedback='As pistas sustentam uma suspeita que precisa de ser investigada. Não demonstram as outras duas afirmações.'),
 dict(title='O que não sabemos',question='Qual é a diferença entre hipótese e prova?',clues=['Uma pessoa observa padrões.','Encontra uma possível explicação.','Procura informações que confirmem ou contrariem essa explicação.'],options=['Uma hipótese é uma explicação a testar; a evidência permite avaliá-la.','Uma hipótese torna-se prova quando é repetida muitas vezes.','Uma prova é aquilo em que a maioria acredita.'],correct=0,feedback='Investigar inclui procurar dados que possam contrariar a nossa hipótese. A frequência e a popularidade de uma afirmação não a tornam verdadeira.'),
 ],close=close('O familiar também se questiona','Platão e Truman permitem discutir a relação entre aquilo que vemos e aquilo que sabemos. CHIROPTERA abre outras possibilidades de perceber a caverna através do corpo, da luz e do som.','Debate: que informação poderia levar-te a abandonar uma certeza?')),

dict(id='03',title='O lugar do outro',subtitle='The Egg, Shakespeare e direitos humanos.',type='match',icon='mirror',refs=['egg','shakespeare','direitos'],
 intro='Relaciona cada situação com o princípio mais diretamente afetado. Depois, troca de posição. Recupera The Egg e o discurso de Shylock em O Mercador de Veneza.',
 aim='Relacionar igualdade e dignidade com situações concretas, sem reduzir uma pessoa à sua utilidade ou pertença.',
 rounds=[
 dict(title='Direitos em cena',question='Seleciona um par de cada vez.',pairs=[
 ['Filmar e transmitir a intimidade de Truman sem o seu conhecimento.','Vida privada · artigo 12.º','A exposição permanente impede Truman de decidir sobre a sua intimidade.'],
 ['Ocultar a realidade do programa e afastar quem tenta revelá-la.','Liberdade de informação · artigo 19.º','Sem acesso à informação, Truman não consegue avaliar a sua situação.'],
 ['Tratar uma vida como um produto subordinado às audiências.','Igual dignidade · artigo 1.º','A dignidade da pessoa não depende do lucro ou do interesse do público.']]),
 dict(type='perspective',title='Quem está do outro lado?',question='Situação inventada: um vídeo embaraçoso de um colega circula entre pessoas da escola.',roles=[
 dict(label='Quem partilha',text='Acha graça ao vídeo e não pensa no efeito da circulação. O facto de já existir não resolve a questão do consentimento.'),
 dict(label='Quem aparece',text='Não autorizou a publicação e teme que o vídeo passe a definir a forma como os outros o veem.'),
 dict(label='Quem assiste',text='Pode continuar a circulação, recusar partilhar ou procurar apoiar a pessoa exposta.')],feedback='The Egg convida a imaginar o lugar do outro. Shakespeare permite perguntar por que razão alguém precisa de reclamar o reconhecimento da sua humanidade.'),
 ],close=close('Reconhecer não é idealizar','Uma pessoa pode merecer reconhecimento e, ao mesmo tempo, ter ações que devemos criticar. A discriminação sofrida por Shylock não torna automaticamente justa a vingança.','Debate: a empatia muda apenas o que sentimos ou também aquilo que fazemos?')),

dict(id='04',title='Querer, agir, responder',subtitle='De Stanislavski ao Actors Studio.',type='order',icon='mask',refs=['studio'],
 intro='Reconstrói uma linha de influência. Depois, distingue o objetivo de uma personagem da ação que escolhe. Entender um motivo não elimina a responsabilidade.',
 aim='Investigar a preparação do ator e relacioná-la com a compreensão do outro e a avaliação das suas ações.',
 rounds=[
 dict(title='Uma tradição que se transforma',question='Ordena esta linha de influência. Não é uma equivalência entre todas as propostas.',items=['O trabalho de Stanislavski e a sua receção nos Estados Unidos.','O Group Theatre desenvolve experiências de formação e representação.','No Actors Studio, Strasberg aprofunda a sua abordagem ao trabalho do ator.','Hoje, investigamos essas propostas e discutimos escolhas e limites.'],order=[0,1,2,3],feedback='O Actors Studio situa as suas raízes no Group Theatre e no trabalho de Stanislavski e Vakhtangov. Strasberg desenvolveu uma abordagem própria: sistema e Método não são nomes perfeitamente intercambiáveis.'),
 quiz('Objetivo ou ação?','Christof quer manter Truman em Seahaven. Para isso, controla informação e provoca obstáculos.','Qual das opções distingue o que pretende daquilo que faz?',['Objetivo: manter Truman. Ação: controlar o que ele pode saber e fazer.','Objetivo: provocar uma tempestade. Ação: querer manter Truman.','Objetivo e ação são sempre a mesma coisa.'],0,'O objetivo indica aquilo que procura alcançar. A ação é uma forma concreta de o tentar alcançar. A existência de um objetivo não torna aceitável qualquer ação.'),
 dict(type='branch',title='Marlon e Sylvia',question='Que diferença pesa mais na análise da responsabilidade dos dois?',options=[
 option('A qualidade da representação.','Uma representação convincente pode aumentar o efeito do engano. A qualidade técnica não resolve a responsabilidade ética.'),
 option('A forma como usam aquilo que sabem.','Marlon conserva o engano; Sylvia tenta revelá-lo. A decisão de continuar ou romper o papel altera o efeito sobre Truman.'),
 option('O número de falas.','Ter mais ou menos falas não determina o valor ético de uma intervenção. É preciso analisar o que ela permite ou impede.')]),
 ],close=close('Compreender e avaliar','As circunstâncias ajudam a compreender uma ação. A cidadania exige também perguntar pelos seus efeitos, pela liberdade dos envolvidos e pela possibilidade de agir de outra forma.','Debate: onde termina o trabalho do ator e começa a sua responsabilidade pessoal?')),

dict(id='05',title='Uma posição com fundamento',subtitle='Sísifo, Truman e o primeiro ensaio.',type='build',icon='stone',refs=['direitos'],
 intro='Escolhe ligações que sustentem uma tese. Recupera Sísifo: a repetição de uma vida não determina, por si só, se essa vida tem sentido ou se é livre.',
 aim='Reconhecer tese, argumento, exemplo e objeção antes de escrever o primeiro ensaio na ficha própria.',
 rounds=[
 dict(title='O conforto basta?',scene='Tese proposta: ter uma vida confortável não basta para ser livre.',question='Seleciona dois elementos que fundamentam diretamente esta tese.',options=[
 dict(label='Sem conhecer a sua situação, Truman não consegue aceitá-la ou recusá-la.'),
 dict(label='A cidade de Seahaven tem ruas agradáveis.'),
 dict(label='Marlon é uma personagem do filme.'),
 dict(label='Os obstáculos preparados pela produção tornam a saída quase impossível.')],correct=[0,3],hint='Procura razões ligadas à informação e à possibilidade real de escolher. Um detalhe do filme não é automaticamente um argumento.',feedback='Os dois elementos relacionam liberdade com informação e possibilidade de agir. Explicar esta ligação é diferente de resumir o filme.'),
 quiz('Uma objeção útil','Alguém responde: sair pode expor Truman a perigos reais.','Qual é a resposta que enfrenta a objeção?',['A liberdade envolve riscos, mas isso não autoriza controlar toda a vida de outra pessoa.','Não gosto de Christof.','Quem discorda não percebe o filme.'],0,'Uma resposta fundamentada reconhece a dificuldade e explica por que razão ela não destrói a tese. Atacar quem discorda não responde ao argumento.'),
 ],close=close('Ensaio 1','Abre a ficha de Truman. Usa o texto, a interpretação e a planificação para escrever o primeiro ensaio de 250 a 350 palavras. A produção escrita fica na ficha e em papel, fora deste exercício.','Pergunta do ensaio: uma vida confortável é necessariamente uma vida livre?')),

dict(id='06',title='A pistola e a prova',subtitle='Tchékhov, Abramović e o segundo filme.',type='branch',icon='prop',refs=['chekhov','abramovic','filme2'],
 intro='Vê Doze Homens em Fúria na aula. Depois, distingue o efeito de um objeto numa narrativa, o perigo real numa performance e o valor de um objeto como prova.',
 aim='Distinguir expectativa dramática, consentimento e evidência. O filme decorre num júri dos Estados Unidos; não apresenta o funcionamento dos tribunais portugueses.',
 rounds=[
 dict(title='Tem de acontecer?',scene='Situação inventada: uma arma é apresentada como elemento importante numa cena. O público começa a esperar um disparo.',question='Que desenvolvimento escolherias para explorar a responsabilidade?',options=[
 option('A personagem dispara.','A expectativa pode cumprir-se. Mas o efeito dramático não torna a violência inevitável nem moralmente justificada. Que consequências mostra a cena?'),
 option('Outra personagem retira a arma.','A intervenção interrompe uma possibilidade anunciada. Também pode ter força dramática: transforma a prevenção numa ação visível.'),
 option('A personagem decide não disparar.','A recusa pode contrariar a expectativa e revelar uma escolha. A análise deve explicar como a preparação da cena dá sentido a essa recusa.')]),
 quiz('Pistola e consentimento','Em Rhythm 0, Abramović colocou objetos à disposição do público, incluindo uma pistola e uma bala. Na tempestade, Truman corre um perigo criado por Christof.','Que diferença deve entrar na comparação?',['Abramović definiu uma situação de participação; Truman desconhece o programa. Isso não elimina a responsabilidade de quem presencia perigo.','Aceitar participar elimina qualquer responsabilidade do público.','As duas situações têm exatamente o mesmo consentimento.'],0,'A comparação permite discutir consentimento e intervenção, sem equiparar as duas situações. A presença de uma arma não impõe a obrigação moral de a usar.'),
 quiz('Um objeto prova tudo?','Em Doze Homens em Fúria, o júri analisa objetos, depoimentos e interpretações.','Qual é a atitude mais rigorosa perante uma prova aparentemente decisiva?',['Examinar o que mostra, o que não mostra e as condições da sua interpretação.','Concluir que um objeto nunca serve de prova.','Aceitar a primeira explicação porque parece convincente.'],0,'O valor de uma prova depende da relação que estabelece com o facto em causa. Questionar essa relação não equivale a negar toda a evidência.'),
 ],close=close('Três objetos, três problemas','Tchékhov permite discutir a preparação narrativa; Abramović, os limites da participação; Lumet, a avaliação de provas. São relações a investigar, não situações equivalentes.','Debate: quando confundimos o que esperamos com aquilo que sabemos?')),

dict(id='07',title='A ordem chegou',subtitle='Pinter, obediência e limites ao poder.',type='power',icon='hatch',refs=['pinter','direitos'],
 intro='Lê as ordens e escolhe como responder. As situações seguintes foram criadas para a ficha; não são falas de Pinter. Relaciona-as com O Monta-Cargas, também traduzido como O Serviço.',
 aim='Reconhecer a responsabilidade de quem dá, transmite e executa uma ordem; discutir mecanismos de contestação.',
 rounds=[
 dict(title='Primeira ordem',scene='Situação inventada: chega uma instrução sem assinatura. Um colega deve ser excluído de uma apresentação. Não é indicado qualquer motivo.',question='Qual é a tua primeira ação?',options=[
 option('Executar, porque alguém com autoridade terá decidido.','Presumir que a ordem é legítima não esclarece quem a deu nem porquê. A execução pode produzir uma injustiça que ninguém assume.'),
 option('Pedir a identificação de quem decidiu e o fundamento.','A identificação e a justificação permitem questionar a decisão e avaliar se existe um procedimento justo.'),
 option('Excluir outra pessoa em vez dele.','Trocar a pessoa afetada não resolve a falta de fundamento nem de possibilidade de contestação.')]),
 dict(title='A responsabilidade desaparece?',scene='A resposta é: «Cumpre. A decisão veio de cima.»',question='Como respondes?',options=[
 option('Isso basta para executar.','A origem hierárquica de uma ordem não demonstra a sua justiça. Quem a executa continua a ter de avaliar os efeitos e os meios de contestação.'),
 option('Peço um procedimento em que o colega possa ser ouvido.','Uma decisão que afeta alguém deve poder ser fundamentada e contestada. Dar voz à pessoa não significa garantir-lhe qualquer resultado.'),
 option('Publico acusações sobre todos os envolvidos.','A publicidade sem verificação pode criar novas injustiças. Questionar o poder exige também rigor na informação que divulgamos.')]),
 ],close=close('A autoridade responde','Pinter permite analisar ordens, silêncios e uma autoridade fora de vista. A democracia exige que o poder possa ser identificado, questionado e responsabilizado.','Debate: como pode uma pessoa recusar uma ordem sem deixar de agir de forma responsável?')),

dict(id='08',title='Escutar sem inventar',subtitle='Sarah Kane, voz e interpretação.',type='listen',icon='voice',refs=['kane'],
 intro='Consulta a apresentação de Crave. Depois, distingue o que uma voz diz daquilo que projetamos sobre ela. As frases dos casos foram criadas para a ficha; não são excertos de Sarah Kane.',
 aim='Respeitar a voz do outro, reconhecer incertezas e evitar transformar uma interpretação num diagnóstico ou numa identidade.',
 rounds=[
 quiz('Uma frase não é uma biografia','Situação inventada: uma personagem diz «Não consigo falar disto agora».','Que conclusão é sustentada pela frase?',['A personagem não consegue falar desse assunto naquele momento.','A personagem nunca quer falar com ninguém.','A personagem tem uma condição clínica determinada.'],0,'A frase permite reconhecer uma dificuldade situada. Não fornece uma biografia nem permite um diagnóstico. A interpretação deve respeitar o que o material efetivamente mostra.','listen'),
 quiz('Quem ficou sem voz?','Situação inventada: numa reunião, três pessoas interpretam o comportamento de uma quarta, que ainda não foi ouvida.','Qual é a informação que faz mais falta?',['A perspetiva da pessoa de quem se fala.','O número de pessoas que concordam entre si.','Uma etiqueta rápida para explicar o comportamento.'],0,'Concordar entre si não substitui ouvir a pessoa afetada. Escutar pode confirmar ou alterar uma interpretação.','listen'),
 dict(type='branch',title='Ler uma voz',question='Ao trabalhar uma voz dramática, que atitude favorece uma interpretação responsável?',options=[
 option('Escolher uma explicação e apresentá-la como a única possível.','Uma interpretação pode ser coerente sem esgotar o texto. Explica as pistas que a sustentam e reconhece o que permanece aberto.'),
 option('Relacionar as escolhas de leitura com pistas do texto.','As escolhas ganham fundamento quando se pode mostrar o que as sustenta. Isso permite debate entre interpretações.'),
 option('Usar a vida da autora para explicar automaticamente todas as vozes.','Autora e voz dramática não são identidades equivalentes. A biografia pode ser contexto, mas não substitui a leitura da obra.')]),
 ],close=close('A pessoa não cabe numa etiqueta','Sarah Kane entra como objeto de leitura e investigação, não como diagnóstico da autora ou dos alunos. A cidadania exige reconhecer quem fala e quem é interpretado sem ter voz.','Debate: o que muda quando deixamos a pessoa responder à interpretação que fizeram dela?')),

dict(id='09',title='Uma decisão entre muitos',subtitle='Doze Homens em Fúria, Sylvia e CHIROPTERA.',type='vote',icon='table',refs=['filme2','chiroptera','direitos'],
 intro='Escolhe uma posição, conhece nova informação e decide se a manténs. A situação é inventada e não constitui uma simulação jurídica. Relaciona-a com o debate entre os jurados do filme.',
 aim='Distinguir votação de deliberação; reconhecer o valor da discordância fundamentada, da igualdade e da revisão de uma decisão.',
 rounds=[
 dict(title='A maioria já decidiu',scene='Situação inventada: um grupo quer excluir um colega de um projeto. Quase todos acreditam que ele divulgou informação privada.',question='O que propões?',initial=['Acompanhar a maioria.','Pedir verificação e ouvir o colega.','Defender o colega sem verificar nada.'],newInfo='A acusação assenta numa captura de ecrã cortada. A pessoa acusada ainda não foi ouvida e existe outra explicação possível.',final=[
 option('Suspender a decisão para verificar a informação.','A revisão reconhece limites na evidência. Não declara automaticamente a pessoa inocente; procura um procedimento mais justo.'),
 option('Manter a exclusão porque a maioria continua a concordar.','A quantidade de votos não corrige a fragilidade da informação nem a ausência da voz de quem é afetado.'),
 option('Concluir imediatamente que a acusação foi uma mentira deliberada.','Uma acusação pouco sustentada não prova, por si só, intenção de mentir. Também essa conclusão precisa de evidência.')]),
 dict(type='perspective',title='Quem interrompe o espetáculo?',question='Regressa à tempestade de Truman e à intervenção de Sylvia.',roles=[
 dict(label='Ator',text='Pode continuar o papel, questionar o guião ou recusar uma ação que prejudica uma pessoa. Sylvia procura devolver informação a Truman.'),
 dict(label='Equipa',text='Dispõe de informação e meios técnicos. Deve perguntar pelo perigo real e pela possibilidade de interromper uma decisão.'),
 dict(label='Público',text='Pode consumir o espetáculo, recusar alimentá-lo ou exigir a defesa da pessoa. O prazer de assistir não resolve a responsabilidade.')],feedback='Em CHIROPTERA, muitos corpos constroem uma experiência comum. No debate cívico, uma ação coletiva também exige perguntar quem participa, quem fica de fora e como se tratam as diferenças.'),
 ],close=close('Discordar também participa','Uma democracia exige participação, informação, direitos e limites ao poder. Uma maioria pode tomar decisões e, ainda assim, ter de rever o modo como tratou uma pessoa.','Debate: que condições tornam uma decisão coletiva mais justa?')),

dict(id='10',title='Pôr o argumento à prova',subtitle='Investigar antes do segundo ensaio.',type='audit',icon='evidence',refs=['filme2','studio','direitos'],
 intro='Abre as fontes, reconhece o que cada uma permite saber e avalia as ligações de um argumento. A escrita fica para o guião e a ficha do segundo ensaio.',
 aim='Selecionar fontes adequadas, distinguir informação de interpretação e responder a uma objeção.',
 rounds=[
 dict(title='Que fonte serve esta pergunta?',scene='Pergunta de investigação: como se relaciona a formação do ator no Actors Studio com Stanislavski?',question='Abre as três fontes e escolhe uma estratégia.',sources=[
 dict(label='História institucional',author='Actors Studio · página oficial',description='Identifica raízes, intervenientes e propostas de trabalho. É uma fonte diretamente ligada à instituição.',limit='É também a forma como a instituição apresenta a sua história. Pode ser comparada com investigação histórica independente.'),
 dict(label='Comentário sem autoria',author='Publicação anónima · caso inventado',description='Afirma que sistema e Método são exatamente a mesma coisa. Não apresenta bibliografia.',limit='Sem autoria nem fontes, é difícil verificar a origem e o fundamento da afirmação.'),
 dict(label='Uma cena de um filme',author='Obra cinematográfica',description='Permite observar escolhas de representação e discutir os seus efeitos.',limit='Uma cena não demonstra, por si só, a genealogia de uma técnica nem a formação de um ator.')],options=[
 option('Começar pela história institucional e confrontá-la com outra fonte identificada.','A fonte responde à pergunta e a comparação permite reconhecer perspetivas e verificar informação.'),
 option('Escolher o comentário que confirma aquilo em que já acredito.','Isso favorece o viés de confirmação. A adequação e a verificação da fonte devem pesar mais do que a concordância.'),
 option('Usar apenas a cena para reconstruir a história da formação.','A cena pode apoiar uma análise de representação, mas não substitui fontes sobre a história da formação.')]),
 dict(type='build',title='Uma tese que resiste',scene='Tese proposta: uma decisão coletiva só é justa quando a participação se apoia em informação e respeita a dignidade das pessoas.',question='Seleciona uma razão e uma objeção que merecem entrar no ensaio.',options=[
 dict(label='Sem ouvir a pessoa afetada e verificar a informação, o grupo pode decidir com base em preconceitos.'),
 dict(label='As maiorias nunca podem tomar decisões.'),
 dict(label='Objeção: verificar tudo pode atrasar uma decisão necessária; é preciso explicar como agir com rigor e oportunidade.'),
 dict(label='O filme é antigo, por isso não tem relação com a cidadania.')],correct=[0,2],hint='Escolhe uma razão ligada à tese e uma dificuldade real a que ela tenha de responder. Evita generalizações absolutas.',feedback='Um argumento ganha força quando enfrenta uma dificuldade real. O segundo ensaio deve relacionar os filmes, uma referência estudada e os princípios de cidadania.'),
 ],close=close('Ensaio 2','Abre o guião de investigação e a ficha «Decidir sobre o outro». Escolhe uma questão e escreve o segundo ensaio de 400 a 600 palavras em papel ou no formato indicado pelo professor.','Debate: que posição mudaste durante este módulo, e porquê?')),
]

# DIÁRIO

## 2026-09-27 · Arranque de Cidadania e Desenvolvimento (INTP26)

**Feito**
- Criado o repositório: `_interno/` (LEIA-ME, sistema, diário, índice, ferramentas) e `10-ano/Cidadania/`.
- Fichas de módulo M1 e M2 (`.docx`) geradas sobre a ficha de Português ANI26 (logótipo, cabeçalho, tabelas e formatação do modelo). Aprendizagens de referência: ENEC e Perfil dos Alunos. Avaliação só por projeto, também nas recuperações.
- Aula 1 de M1 («O que nos torna humanos?»): plano, 18 diapositivos, ficha do aluno.
- Aula 1 de M2 («Quem escolheu o que viste hoje?»): plano, 17 diapositivos, ficha do aluno, 24 cartões para o «feed de papel».
- Projetos: «Pergunta Humana» (M1, teatro-documento) e «Contra-feed» (M2, performance ou vídeo-performance e manifesto de uso), pensados para uma turma de Interpretação.

**Decisões tomadas por falta de informação** (rever)
- `_interno/01-sistema` não existia: reconstruído a partir dos materiais Terra Firme e das fichas de Português. Tudo o que não se confirmou está marcado com A CONFIRMAR.
- A ficha modelo MM26 não estava no Drive; usou-se a ANI26, com a mesma estrutura.
- Curso «Interpretação» deduzido do código INT (ficha INT25 de Português).
- Professor: «Pedro Fernandes».
- Aulas de 100 min (2 × 50), com versão de 50 min em cada plano.
- Limite de faltas: 6 h por módulo (20%, como nas fichas de Português).

**Por decidir**
- Horário da turma, e daí as datas de início e de conclusão de cada módulo.
- Ordem dos módulos (em paralelo ou em sequência) e em que período arranca cada um.
- Se os domínios da ENEC de 2017 continuam a ser a referência depois da revisão de 2025.
- Fichas de módulo para outras turmas (o gerador aceita qualquer código de turma).

**Nota**
- O PDF «MM26» do Drive é o processo individual dos alunos (dados pessoais). Não foi usado nem copiado para aqui.

## 2026-10-07 · Widget do feed de papel (M2, aula 1)

**Feito**
- `M2-Expressao-algoritmos/aula-01/feed.html`: o algoritmo do «feed de papel» corre no ecrã (projetor ou telemóvel). 3 rondas de 6 cartões; versão 1 (gostos) e versão 2 (tempo de leitura medido em segredo). No fim, revela a regra e a tabela de cada tema, ronda a ronda, com os temas que desapareceram. Não guarda nem envia dados.
- A atividade passou a ter 3 rondas nas duas versões: plano, diapositivos e ficha do aluno atualizados. Os cartões em papel ficam como alternativa sem ecrã.

## 2026-10-07 · Páginas que não abriam

**Problema:** as páginas HTML dependiam de ficheiros partilhados (`terra-firme.css`, `diapositivos.css/.js`, `ficha.js`). Abertas sozinhas (descarregadas, enviadas, no telemóvel) ficavam sem estilo e sem funcionamento; o widget do feed ficava em branco. No GitHub só se vê o código. Além disso, `confirm()` e `window.print()` não funcionam dentro do visualizador de artefactos.

**Feito**
- Cada página passou a ser autónoma (CSS e JavaScript dentro do ficheiro); os ficheiros partilhados foram apagados.
- «Sair» (widget) e «Apagar respostas» (fichas) passaram a pedir um segundo toque, em vez de `confirm()`. O botão de imprimir esconde-se quando a página está embutida.
- Publicado um artefacto privado com as 7 páginas: https://claude.ai/artifact/6pJxKPQAgrEiCJCe2KR6Fh (para os alunos o abrirem, é preciso partilhá-lo no menu Partilhar).

## 2026-10-07 · PowerPoint das aulas 1 e 2 de Cidadania I

**Feito**
- Dois PowerPoint com o que foi efetivamente dado, organizados assim: aula 1 «O que vemos» (caverna de Platão; CHIROPTERA, que é o 2.º ato de «Retour à la caverne», do JR, na Ópera de Paris, 2023; This is Water) e aula 2 «O que somos» (Sísifo e Camus; Marina Abramović: Rhythm 0 e The Artist Is Present).
- Cada um tem um diapositivo de desdobramentos («Daqui, para onde?»), com Ai Weiwei (Remembering, Citizens' Investigation, Rapture em Lisboa, Law of the Journey, Human Flow), Saramago, The Truman Show, Pariser, Ticiano, A Peste, Yoko Ono (Cut Piece) e o caso Kitty Genovese, e as referências com ligações.
- Guião, tempos e cuidados nas notas do orador.

**Por verificar**
- Não consegui ver os diapositivos renderizados (o LibreOffice deste ambiente não abre ficheiros); verifiquei a estrutura, o texto que cabe em cada caixa e uma pré-visualização aproximada.
- As ligações foram tiradas de resultados de pesquisa; não as consegui abrir uma a uma (a rede deste ambiente bloqueia esses sites).
- Os HTML da aula 1 ficaram desatualizados em relação ao que foi dado.

## 2026-10-07 · Feed de papel: cartões repetidos

**Problema:** na versão «gostos», o mesmo cartão podia aparecer duas vezes. Havia 4 cartões por tema, mas o tema favorito aparece até 7 vezes em 3 rondas (e até 9 quando o cartão «ao acaso» calhava no mesmo tema); quando o monte acabava, era baralhado e reutilizado.

**Feito**
- 8 cartões por tema (48 no total), no widget e no anexo do plano para imprimir.
- O cartão ao acaso vem sempre de outro tema (nem o 1.º nem o 2.º do ranking). Máximo por tema numa sessão: 1 + 3 + 3 = 7 < 8, por isso nenhum cartão se repete.
- Testado: 10 000 sessões simuladas com o código da página, zero repetições. Regra atualizada no plano, nos diapositivos e no próprio widget.

## 2026-10-07 · Site dos alunos, Módulo 1

**Feito**
- `docs/`: site para os alunos, só com material para eles (sem planos nem chaves). Páginas: início (módulo, aulas, avaliação), aula 1 «O que vemos», aula 2 «O que somos», projeto «Pergunta Humana» (fases, leitura lateral, ética das entrevistas, avaliação). Cada aula tem o diário com as perguntas de saída, guardado no aparelho do aluno, e um botão para copiar as respostas e enviar ao professor.
- Gerado por `_interno/ferramentas/gerar_site.py`.
- Publicado também como artefacto: https://claude.ai/artifact/UkG9oY2VZvBcuefaXqk9yL (privado até ser partilhado no menu Partilhar).

**Por fazer (professor)**
- Ligar o GitHub Pages: no repositório, Settings → Pages → «Deploy from a branch» → ramo `claude/cidadania-desenvolvimento-modulos-rv1e4q`, pasta `/docs`. Endereço previsto: https://pedrohfernandes-klk.github.io/CIDADANIA1oANO/

## 2026-10-07 · Site publicado no GitHub Pages

- O Pages não ficou ativo pelas definições. A solução foi publicar o conteúdo de `docs/` num ramo `gh-pages`: o GitHub ativou o Pages sozinho e a publicação («pages build and deployment») terminou com sucesso às 13:51.
- **Endereço para os alunos: https://pedrohfernandes-klk.github.io/CIDADANIA1oANO/**
- O ramo `gh-pages` só tem o site dos alunos (4 páginas). Planos, chaves e `_interno` não são publicados.
- Para atualizar o site: editar `_interno/ferramentas/gerar_site.py` e correr `bash _interno/ferramentas/publicar_site.sh`.

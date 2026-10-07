# Cidadania e Desenvolvimento · 10.º ano · 2026/2027 · LEIA-ME

Repositório de trabalho da disciplina de Cidadania e Desenvolvimento, turma **INTP26** (1.º ano, Interpretação), EPI – Escola Profissional de Imagem.

## Antes de escrever qualquer material

1. Ler este ficheiro.
2. Ler `01-sistema/`: `VOZ.md`, `PLANO.md`, `HORARIO.md`, `TEMPOS.md` e `CALENDARIO.md`.
3. Criar o material na pasta do módulo (`10-ano/Cidadania/…`), com a identidade visual Terra Firme. **Cada página HTML é autónoma**: CSS e JavaScript ficam dentro do próprio ficheiro, para abrir sozinha no telemóvel, no Drive ou num artefacto. Partir de uma página existente.
   - Não usar `confirm()`, `alert()` nem `window.print()` sem alternativa: não funcionam dentro do visualizador de artefactos.
4. Acrescentá-lo ao índice (`INDICE-MATERIAIS.md` e `10-ano/Cidadania/index.html`).
5. Registar no `DIARIO.md` o que foi feito e o que ficou por decidir.

## Estado deste sistema (27/09/2026)

Os ficheiros `_interno/` e `01-sistema/` **não existiam neste repositório** quando foi criado. Foram reconstruídos a partir do que havia noutras fontes:

- os materiais de Português publicados (repositório `pt`, identidade Terra Firme);
- o *Guia de preparação, ensino e produção de provas Terra Firme · Português 639* (Drive);
- as fichas de módulo de Português de 2026/2027 (Drive; modelo usado: `PT_MOD_1_Literatura_Medieval_ANI26_2026_2027.docx`).

Tudo o que não foi possível confirmar está marcado com **A CONFIRMAR**. Se existir uma versão original destes ficheiros, é ela que manda: substitui-os.

## Estrutura

```
_interno/
  00-LEIA-ME.md            este ficheiro
  01-sistema/              regras (voz, plano, horário, tempos, calendário)
  DIARIO.md                registo de trabalho
  INDICE-MATERIAIS.md      índice de tudo o que existe
  ferramentas/             gerador das fichas de módulo (.docx)
10-ano/Cidadania/
  index.html               índice público dos materiais
  Fichas de modulo/        fichas de módulo oficiais (.docx)
  M1-Ser-se-humano/aula-NN/            plano.html · diapositivos.html · ficha.html
  M2-Expressao-algoritmos/aula-NN/     idem
```

## Fichas de módulo

São geradas por `ferramentas/gerar_fichas.py` a partir de uma ficha de módulo de Português da escola, que serve de modelo: mantém o logótipo, o cabeçalho, as tabelas e a formatação e troca só o conteúdo (em `ferramentas/fichas_conteudo.py`).

```
pip install python-docx
python3 _interno/ferramentas/gerar_fichas.py CAMINHO/PT_MOD_1_Literatura_Medieval_MM26_2026_2027.docx INTP26
```

O modelo **não** está no repositório, porque tem dados de outra docente e o repositório é público. Descarrega-o do Drive (pasta das fichas de módulo de Português) antes de correr o script.

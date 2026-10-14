# Módulo 1 — Ser-se humano: novo percurso

## Abrir

Página dos alunos: `docs/index.html`, com entrada em `docs/m1/index.html`.
Cada ficha nova é um HTML autónomo: estilos, fonte Bebas Neue, logótipo e JavaScript estão incluídos. Não precisa de servidor nem de bibliotecas externas para as interações.

## Percurso

- Dez passos, com uma proposta de três horas por passo: visionamento, leitura, investigação, debate e escrita. Total: 30 horas.
- The Truman Show entra no passo 1; Ensaio 1 no passo 5 (250–350 palavras).
- Doze Homens em Fúria (Sidney Lumet, 1957) entra no passo 6; Ensaio 2 no passo 10 (400–600 palavras).
- Dez fichas interativas, com 23 rondas. Não há campos de produção textual nas fichas novas. A justificação é oral; a investigação e os ensaios ficam em papel ou no formato indicado pelo professor.
- Guiões e fichas HTML/PDF na pasta `docs/m1/`; respostas e orientações do professor nesta pasta interna.
- As aulas anteriores estão ligadas ao novo percurso. A antiga entrada está em `docs/arquivo-m1.html`.

## Design

CSS de base recuperado de `pedrohfernandes-klk/pt`, `index.html`, em 14/10/2026, blob `9ae6b4ff51ee00d7b502b5504b28ab7310eb46e0`: cores, largura de leitura, tipografia, botões, estados e acessibilidade. Extensões em `gerar_percurso_m1.py` para as novas interações.

Logótipo: vetores da página oficial `https://www.epi.edu.pt/`. Fonte Bebas Neue: Google Fonts, licença SIL OFL conservada em `ferramentas/identidade/Bebas-OFL.txt`. Os desenhos das fichas são SVG originais em código.

## Gerar e verificar

```bash
python3 _interno/ferramentas/gerar_percurso_m1.py
python3 _interno/ferramentas/gerar_pdfs_m1.py
node --check _interno/ferramentas/cidadania-m1.js
node _interno/ferramentas/verificar_interacoes_m1.cjs
python3 _interno/ferramentas/verificar_ligacoes_m1.py
```

Os PDFs usam ReportLab e fontes DejaVu instaladas no sistema. Os PDFs existentes de Truman foram integrados a partir dos materiais preparados nesta conversa.

O publicador existente chama o novo gerador depois do gerador das aulas anteriores, para conservar o novo índice. Os PDFs já estão versionados e não precisam de ser regenerados para publicar. Esta proposta não executa o publicador nem altera o ramo `gh-pages`.

## Avaliação

A ficha oficial do módulo foi conservada. O percurso e a grelha dos dois ensaios constituem a proposta atual, sem substituir administrativamente os parâmetros dessa ficha. Não há recolha de nomes ou respostas na página. «Explorado» é um marcador local, não uma nota.

## Verificação

O teste do motor percorre todas as fichas e as três alternativas nas decisões abertas, verifica tentativas erradas, reinício e armazenamento indisponível. É um teste de DOM mínimo, não um teste num navegador real. Neste ambiente não estava disponível a capacidade de controlo de navegador exigida pelo fluxo Sites; por isso não foi iniciada uma pré-visualização de navegador. Os PDFs foram renderizados e inspecionados visualmente.

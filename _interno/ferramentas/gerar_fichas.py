#!/usr/bin/env python3
"""Gera as fichas de módulo de Cidadania e Desenvolvimento a partir do modelo da escola.

Uso:
    python3 gerar_fichas.py MODELO.docx [TURMA]

MODELO.docx é uma ficha de módulo de Português da EPI (por exemplo,
PT_MOD_1_Literatura_Medieval_MM26_2026_2027.docx). O script mantém o logótipo,
o cabeçalho, as tabelas e a formatação do modelo e troca apenas o conteúdo.
O conteúdo dos módulos está em fichas_conteudo.py.

Convenção das linhas de texto:
    "**Texto"  -> parágrafo a negrito
    "~Texto"   -> parágrafo com o estilo List Paragraph (como no modelo)
    ""         -> linha em branco
"""
import copy
import sys
from pathlib import Path

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH

from fichas_conteudo import COMUM, MODULOS

AQUI = Path(__file__).resolve().parent
DESTINO = AQUI.parent.parent / "10-ano" / "Cidadania" / "Fichas de modulo"


def celulas(linha):
    """Células únicas de uma linha (as fundidas aparecem uma só vez)."""
    vistas, out = set(), []
    for c in linha.cells:
        if id(c._tc) not in vistas:
            vistas.add(id(c._tc))
            out.append(c)
    return out


def escrever(celula, linhas, alinhar=None):
    """Substitui o texto da célula mantendo a formatação do primeiro parágrafo."""
    if isinstance(linhas, str):
        linhas = [linhas]
    paras = celula.paragraphs
    modelo_p = copy.deepcopy(paras[0]._p)
    modelo_r = None
    for p in paras:
        if p.runs:
            modelo_r = copy.deepcopy(p.runs[0]._r)
            break
    for p in paras[1:]:
        p._p.getparent().remove(p._p)
    primeiro = paras[0]
    for r in list(primeiro._p):
        if r.tag.endswith("}r") or r.tag.endswith("}hyperlink"):
            primeiro._p.remove(r)
    alvo = primeiro
    for i, linha in enumerate(linhas):
        if i > 0:
            novo = copy.deepcopy(modelo_p)
            for r in list(novo):
                if r.tag.endswith("}r") or r.tag.endswith("}hyperlink"):
                    novo.remove(r)
            alvo._p.addnext(novo)
            alvo = docx.text.paragraph.Paragraph(novo, celula)
        negrito = linha.startswith("**")
        lista = linha.startswith("~")
        texto = linha[2:] if negrito else linha[1:] if lista else linha
        alvo.style = celula.part.document.styles["List Paragraph" if lista else "Normal"]
        if alinhar is not None:
            alvo.alignment = alinhar
        if texto:
            if modelo_r is not None:
                r = copy.deepcopy(modelo_r)
                for t in r.findall(docx.oxml.ns.qn("w:t")):
                    r.remove(t)
                alvo._p.append(r)
                run = docx.text.run.Run(r, alvo)
                run.text = texto
            else:
                run = alvo.add_run(texto)
                run.font.name = "Arial"
                run.font.size = docx.shared.Pt(10)
            run.bold = True if negrito else None


def ajustar_linhas(tabela, inicio, n_atual, n_novo, molde=None):
    """Garante n_novo linhas de dados a partir de `inicio` (clonando a linha molde)."""
    molde = inicio + (molde or 0)
    while n_atual < n_novo:
        nova = copy.deepcopy(tabela.rows[molde]._tr)
        tabela.rows[inicio + n_atual - 1]._tr.addnext(nova)
        n_atual += 1
    while n_atual > n_novo:
        tr = tabela.rows[inicio + n_atual - 1]._tr
        tr.getparent().remove(tr)
        n_atual -= 1


def cabecalho(tabela, m, turma):
    l = [celulas(r) for r in tabela.rows]
    escrever(l[0][2], COMUM["curso"])
    escrever(l[0][4], turma)
    escrever(l[1][2], COMUM["professor"])
    escrever(l[1][4], COMUM["ano_letivo"])
    escrever(l[2][2], COMUM["disciplina"])
    escrever(l[3][2], m["titulo"])
    escrever(l[4][2], m["horas"])
    escrever(l[4][4], m["inicio"])
    escrever(l[4][6], m["fim"])
    escrever(l[4][8], m["faltas"])


def gerar(modelo, m, turma):
    d = docx.Document(modelo)
    T = d.tables

    # I · ficha da escola
    cabecalho(T[0], m, turma)

    t = T[1]  # 2. Conteúdos (linha 0 = cabeçalho; linha 1 = molde com título a negrito)
    ajustar_linhas(t, 1, len(t.rows) - 1, len(m["conteudos"]), molde=1)
    for linha, (texto, horas, recursos) in zip(t.rows[1:], m["conteudos"]):
        c = celulas(linha)
        escrever(c[1], texto, WD_ALIGN_PARAGRAPH.JUSTIFY)
        escrever(c[2], horas, WD_ALIGN_PARAGRAPH.CENTER)
        escrever(c[3], recursos)
        escrever(c[4], "")

    t = T[2]  # 3. Atividades
    ajustar_linhas(t, 1, len(t.rows) - 1, len(m["atividades"]))
    for linha, (texto, horas) in zip(t.rows[1:], m["atividades"]):
        c = celulas(linha)
        escrever(c[1], texto)
        escrever(c[2], horas)

    c = celulas(T[3].rows[2])  # 4. Projetos
    escrever(c[1], m["projeto"][0])
    escrever(c[2], m["projeto"][1])

    # II · ficha do aluno
    cabecalho(T[4], m, turma)
    escrever(celulas(T[5].rows[1])[1], m["programa"])
    escrever(celulas(T[6].rows[1])[1], m["objetivos"])

    t = T[7]  # 4. Perfil
    escrever(celulas(t.rows[1])[1], ["Aprendizagens de referência", "(ENEC · Perfil dos Alunos) / Competências"])
    c = celulas(t.rows[2])
    escrever(c[1], m["perfil"][0], WD_ALIGN_PARAGRAPH.JUSTIFY)
    escrever(c[2], m["perfil"][1], WD_ALIGN_PARAGRAPH.JUSTIFY)
    escrever(c[3], m["perfil"][2], WD_ALIGN_PARAGRAPH.JUSTIFY)

    t = T[8]  # 5. Avaliação: linhas 4.. são as atividades ponderadas
    n_quant = next(i for i, r in enumerate(t.rows) if celulas(r)[1].text.strip().startswith("Qualitativa")) - 4
    ajustar_linhas(t, 4, n_quant, len(m["ponderacao"]))
    for linha, (texto, peso) in zip(t.rows[4:], m["ponderacao"]):
        c = celulas(linha)
        escrever(c[1], texto)
        escrever(c[2], peso, WD_ALIGN_PARAGRAPH.CENTER)
    facult = False
    for r in t.rows:
        c = celulas(r)
        nome = c[1].text.strip()
        if nome.startswith("Facultativos"):
            facult = True
            continue
        if facult and len(c) > 2:
            escrever(c[2], "X" if any(nome.startswith(f) for f in m["facultativos"]) else "",
                     WD_ALIGN_PARAGRAPH.CENTER)

    escrever(celulas(T[9].rows[2])[1], COMUM["recuperacao"], WD_ALIGN_PARAGRAPH.JUSTIFY)
    escrever(celulas(T[10].rows[1])[1], m["recursos"], WD_ALIGN_PARAGRAPH.JUSTIFY)

    d.core_properties.title = m["titulo"]
    d.core_properties.author = COMUM["professor"]
    DESTINO.mkdir(parents=True, exist_ok=True)
    saida = DESTINO / m["ficheiro"].format(turma=turma)
    d.save(saida)
    return saida


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    turma = sys.argv[2] if len(sys.argv) > 2 else COMUM["turma"]
    for m in MODULOS:
        print(gerar(sys.argv[1], m, turma))

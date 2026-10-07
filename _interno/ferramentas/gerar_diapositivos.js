#!/usr/bin/env node
/*
 * Gera os PowerPoint de Cidadania I, aulas 1 e 2 (identidade Terra Firme).
 *
 * Uso:
 *   npm install pptxgenjs          (numa pasta qualquer; depois NODE_PATH=…/node_modules)
 *   node gerar_diapositivos.js
 *
 * Saída: 10-ano/Cidadania/M1-Ser-se-humano/aula-0N/CD_I_Aula_0N_INTP26.pptx
 * As notas do orador de cada diapositivo têm o guião do professor.
 */
const path = require("path");
const pptxgen = require("pptxgenjs");

const RAIZ = path.resolve(__dirname, "..", "..", "10-ano", "Cidadania", "M1-Ser-se-humano");

/* Terra Firme: preto e branco, Arial Black nos títulos, um verde-azulado só para destaques */
const THEME = {
  name: "Terra Firme",
  headFontFace: "Arial Black",
  bodyFontFace: "Arial",
  colors: {
    dk1: "000000", lt1: "FFFFFF", dk2: "1A1A1A", lt2: "EDEFEF",
    accent1: "2F6F7A", accent2: "7FC4CF", accent3: "595959", accent4: "BFBFBF",
    accent5: "000000", accent6: "FFFFFF", hlink: "2F6F7A", folHlink: "595959",
  },
};
const PRETO = "000000", BRANCO = "FFFFFF", COR = "2F6F7A", COR_CLARA = "7FC4CF", CINZA = "595959", FUNDO2 = "EDEFEF";
const W = 10, H = 5.625, M = 0.5;

function novoDeck(rodape) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.author = "Pedro Fernandes";
  pres.company = "EPI - Escola Profissional de Imagem";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };

  const rod = (cor) => [
    { text: { text: rodape, options: { x: M, y: H - 0.38, w: 6, h: 0.25, fontFace: "Arial", fontSize: 9, bold: true, color: cor, charSpacing: 1, margin: 0 } } },
  ];
  pres.defineSlideMaster({
    title: "ESCURO",
    background: { color: PRETO },
    objects: rod(BRANCO),
    slideNumber: { x: W - M - 0.6, y: H - 0.38, w: 0.6, h: 0.25, fontFace: "Arial", fontSize: 9, bold: true, color: BRANCO, align: "right", margin: 0 },
    placeholders: [],
  });
  pres.defineSlideMaster({
    title: "CONTEUDO",
    background: { color: BRANCO },
    objects: rod(PRETO),
    slideNumber: { x: W - M - 0.6, y: H - 0.38, w: 0.6, h: 0.25, fontFace: "Arial", fontSize: 9, bold: true, color: PRETO, align: "right", margin: 0 },
    placeholders: [],
  });
  return pres;
}

/* etiqueta preta com texto branco (a .rot do Terra Firme): diz que momento da aula é */
function etiqueta(s, texto, escuro) {
  const w = 0.32 + texto.length * 0.095;
  s.addShape("rect", { x: M, y: 0.35, w, h: 0.3, fill: { color: escuro ? BRANCO : PRETO }, line: { color: escuro ? BRANCO : PRETO, width: 0 }, objectName: "etiqueta" });
  s.addText(texto.toUpperCase(), { x: M, y: 0.35, w, h: 0.3, fontFace: "Arial", fontSize: 10, bold: true, charSpacing: 1.5, color: escuro ? PRETO : BRANCO, align: "center", valign: "middle", margin: 0, isTextBox: true });
}
function titulo(s, texto, escuro, opts = {}) {
  s.addText(texto.toUpperCase(), { x: M, y: 0.75, w: W - 2 * M, h: opts.h || 0.75, fontFace: "Arial Black", fontSize: opts.size || 26, color: escuro ? BRANCO : PRETO, valign: "top", margin: 0, isTextBox: true, fit: "none" });
}
function texto(s, runs, o) {
  s.addText(runs, Object.assign({ fontFace: "Arial", fontSize: 16, color: PRETO, valign: "top", margin: 0, isTextBox: true, paraSpaceAfter: 6 }, o));
}
function bullets(itens, o = {}) {
  return itens.map((t, i) => {
    const runs = typeof t === "string" ? { text: t } : t;
    return Object.assign({}, runs, { options: Object.assign({ bullet: { indent: 14 }, breakLine: i < itens.length - 1 }, runs.options || {}, o) });
  });
}
/* caixa de citação: filete grosso à esquerda é a marca Terra Firme das citações */
function citacao(s, txt, fonte, o) {
  const { x, y, w, h, escuro, size } = Object.assign({ size: 18 }, o);
  s.addShape("rect", { x, y, w, h, fill: { color: escuro ? PRETO : BRANCO }, line: { color: escuro ? BRANCO : PRETO, width: 2 } });
  s.addShape("rect", { x, y, w: 0.14, h, fill: { color: escuro ? BRANCO : PRETO }, line: { color: escuro ? BRANCO : PRETO, width: 0 } });
  s.addText([
    { text: txt, options: { fontSize: size, color: escuro ? BRANCO : PRETO, breakLine: true } },
    { text: fonte.toUpperCase(), options: { fontSize: 10, bold: true, charSpacing: 1, color: escuro ? COR_CLARA : COR } },
  ], { x: x + 0.35, y: y + 0.18, w: w - 0.55, h: h - 0.3, fontFace: "Arial", valign: "middle", margin: 0, paraSpaceAfter: 10, isTextBox: true });
}
/* cartão com contorno: rótulo pequeno + texto */
function cartao(s, x, y, w, h, rot, corpo, o = {}) {
  s.addShape("rect", { x, y, w, h, fill: { color: o.fill || BRANCO }, line: { color: PRETO, width: o.grosso ? 3 : 2 } });
  s.addText([
    { text: rot.toUpperCase(), options: { fontSize: 10, bold: true, charSpacing: 1.5, color: o.corRot || PRETO, breakLine: true } },
    { text: corpo, options: { fontSize: o.size || 14, color: PRETO } },
  ], { x: x + 0.15, y: y + 0.12, w: w - 0.3, h: h - 0.24, fontFace: "Arial", valign: "top", margin: 0, paraSpaceAfter: 6, isTextBox: true });
}
function circuloNum(s, x, y, n, d = 0.5, escuro) {
  s.addShape("ellipse", { x, y, w: d, h: d, fill: { color: escuro ? BRANCO : PRETO }, line: { color: escuro ? BRANCO : PRETO, width: 0 } });
  s.addText(String(n), { x, y, w: d, h: d, fontFace: "Arial Black", fontSize: 16, color: escuro ? PRETO : BRANCO, align: "center", valign: "middle", margin: 0, isTextBox: true });
}
function capa(pres, sec, eyebrow, tit, sub, nota) {
  const s = pres.addSlide({ masterName: "ESCURO", sectionTitle: sec });
  s.addText(eyebrow.toUpperCase(), { x: M, y: 0.6, w: 9, h: 0.3, fontFace: "Arial", fontSize: 11, bold: true, charSpacing: 2, color: COR_CLARA, margin: 0, isTextBox: true });
  s.addText(tit.toUpperCase(), { x: M, y: 1.2, w: 9, h: 2.2, fontFace: "Arial Black", fontSize: 44, color: BRANCO, valign: "top", margin: 0, isTextBox: true });
  s.addText(sub, { x: M, y: 3.75, w: 8, h: 0.8, fontFace: "Arial", fontSize: 16, color: BRANCO, valign: "top", margin: 0, isTextBox: true });
  s.addNotes(nota);
  return s;
}
function referencias(pres, sec, refs, nota) {
  const POR = 7, paginas = Math.ceil(refs.length / POR);
  for (let pg = 0; pg < paginas; pg++) {
    const parte = refs.slice(pg * POR, (pg + 1) * POR);
    const s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: sec });
    etiqueta(s, "Para ir mais longe");
    titulo(s, "Referências e ligações" + (paginas > 1 ? ` (${pg + 1}/${paginas})` : ""));
    const linhas = [];
    parte.forEach(([obra, url], i) => {
      const ultimo = i === parte.length - 1;
      linhas.push({ text: obra, options: { fontSize: 11, color: PRETO, breakLine: !!url || !ultimo, bullet: { indent: 12 } } });
      if (url) linhas.push({ text: url.replace(/^https?:\/\//, ""), options: { fontSize: 10, color: COR, hyperlink: { url }, breakLine: !ultimo, indentLevel: 1 } });
    });
    s.addText(linhas, { x: M, y: 1.45, w: W - 2 * M, h: 3.6, fontFace: "Arial", valign: "top", margin: 0, paraSpaceAfter: 3, isTextBox: true });
    s.addNotes(nota);
  }
}
/* desdobramentos: de cada referência da aula, para onde se pode ir a seguir */
function desdobramentos(pres, sec, colunas, nota) {
  const s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: sec });
  etiqueta(s, "Desdobramentos");
  titulo(s, "Daqui, para onde?");
  const cw = (W - 2 * M - 0.4) / 3;
  colunas.forEach(([origem, itens], i) => {
    const x = M + i * (cw + 0.2);
    s.addShape("rect", { x, y: 1.5, w: cw, h: 0.42, fill: { color: PRETO }, line: { color: PRETO, width: 0 } });
    s.addText("DE " + origem.toUpperCase() + "  →", { x: x + 0.12, y: 1.5, w: cw - 0.24, h: 0.42, fontFace: "Arial", fontSize: 10.5, bold: true, charSpacing: 1, color: BRANCO, valign: "middle", margin: 0, isTextBox: true });
    const runs = [];
    itens.forEach(([t, d], k) => {
      runs.push({ text: t, options: { bold: true, fontSize: 12.5, breakLine: true } });
      runs.push({ text: d, options: { fontSize: 11.5, breakLine: k < itens.length - 1, paraSpaceAfter: 12 } });
    });
    s.addShape("rect", { x, y: 1.92, w: cw, h: 2.95, fill: { color: BRANCO }, line: { color: PRETO, width: 2 } });
    s.addText(runs, { x: x + 0.12, y: 2.04, w: cw - 0.24, h: 2.75, fontFace: "Arial", color: PRETO, valign: "top", margin: 0, paraSpaceAfter: 2, isTextBox: true });
  });
  s.addNotes(nota);
}

/* ===================================================================== AULA 1 */
async function aula1() {
  const pres = newDeck("CIDADANIA I · AULA 1 · O QUE VEMOS · INTP26");
  pres.title = "Cidadania I · Aula 1 · O que vemos";

  pres.addSection({ title: "Abertura" });
  capa(pres, "Abertura", "Cidadania I · Ser-se humano: investigação e informação · Aula 1",
    "O que vemos", "Platão · JR, Damien Jalet e Thomas Bangalter · David Foster Wallace",
    "100 min. Fio da aula: três imagens de pessoas que não veem aquilo em que vivem (prisioneiros numa caverna, uma gruta pintada numa ópera, peixes que não sabem o que é a água). No fim, cada aluno nomeia a sua «água» e uma informação que aceitou sem verificar.");

  let s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: "Abertura" });
  etiqueta(s, "Mesa · 3 min");
  titulo(s, "Como sabes que o que vês é verdade?", false, { size: 30, h: 1.4 });
  texto(s, "Escreve uma coisa que tens a certeza de que é verdade e que nunca viste com os teus olhos.", { x: M, y: 2.4, w: 6, h: 1.2, fontSize: 18 });
  s.addShape("ellipse", { x: 7.3, y: 2.2, w: 1.9, h: 1.9, fill: { color: BRANCO }, line: { color: PRETO, width: 3 } });
  s.addText("3:00", { x: 7.3, y: 2.2, w: 1.9, h: 1.9, fontFace: "Arial Black", fontSize: 30, align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addNotes("0–5 min. Escrita individual, sem conversa. Recolher três ou quatro exemplos em voz alta (que a Terra é redonda, que o avô nasceu numa certa aldeia, uma notícia). Perguntar a um aluno: «Como sabes?» Guardar duas respostas no quadro; voltam na saída.");

  /* --- Platão --- */
  pres.addSection({ title: "A caverna" });
  s = pres.addSlide({ masterName: "ESCURO", sectionTitle: "A caverna" });
  etiqueta(s, "Objeto", true);
  citacao(s,
    "Suponhamos uns homens numa habitação subterrânea em forma de caverna, com uma entrada aberta para a luz. Estão lá dentro desde a infância, algemados de pernas e pescoços, de tal maneira que só lhes é dado permanecer no mesmo lugar e olhar em frente.",
    "Platão, A República, livro VII (c. 375 a.C.)", { x: M, y: 1.0, w: W - 2 * M, h: 3.6, escuro: true, size: 20 });
  s.addNotes("5–12 min. Ler em voz alta, devagar. Antes de explicar, perguntar: «O que é que estes homens veem?» Deixar a turma chegar sozinha às sombras. Tradução portuguesa de referência: Maria Helena da Rocha Pereira (Fundação Calouste Gulbenkian). O texto é um diálogo entre Sócrates e Glauco.");

  s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: "A caverna" });
  etiqueta(s, "A alegoria");
  titulo(s, "Dentro da caverna");
  // esquema: parede do fundo · prisioneiros · muro com objetos · fogo · saída
  const yb = 4.35;
  s.addShape("rect", { x: 0.6, y: 1.55, w: 0.22, h: 2.8, fill: { color: PRETO }, line: { color: PRETO, width: 0 }, objectName: "parede" });
  [1.75, 2.55].forEach((yy) => s.addShape("ellipse", { x: 0.95, y: yy, w: 0.55, h: 0.7, fill: { color: "BFBFBF" }, line: { color: "BFBFBF", width: 0 } }));
  [1.9, 2.5, 3.1].forEach((xx) => s.addShape("ellipse", { x: xx, y: 3.55, w: 0.42, h: 0.42, fill: { color: PRETO }, line: { color: PRETO, width: 0 } }));
  s.addShape("rect", { x: 4.1, y: 3.75, w: 1.7, h: 0.35, fill: { color: BRANCO }, line: { color: PRETO, width: 2 } });
  s.addShape("triangle", { x: 4.3, y: 3.3, w: 0.4, h: 0.42, fill: { color: PRETO }, line: { color: PRETO, width: 0 } });
  s.addShape("rect", { x: 5.05, y: 3.35, w: 0.36, h: 0.38, fill: { color: PRETO }, line: { color: PRETO, width: 0 } });
  s.addShape("ellipse", { x: 6.35, y: 3.2, w: 0.6, h: 0.8, fill: { color: COR }, line: { color: COR, width: 0 } });
  s.addShape("rect", { x: 7.6, y: 1.55, w: 1.9, h: 2.8, fill: { color: FUNDO2 }, line: { color: PRETO, width: 2 } });
  s.addShape("line", { x: 7.0, y: 2.95, w: 0.55, h: 0, line: { color: PRETO, width: 2, endArrowType: "triangle" } });
  s.addShape("line", { x: 0.6, y: yb, w: 8.9, h: 0, line: { color: PRETO, width: 1.5 } });
  const lab = (t, x, y, w, al) => s.addText(t, { x, y, w, h: 0.5, fontFace: "Arial", fontSize: 11, bold: true, color: PRETO, align: al || "left", valign: "top", margin: 0, isTextBox: true });
  lab("SOMBRAS NA PAREDE", 0.6, 1.2, 2.2);
  lab("PRISIONEIROS · só veem a parede", 1.8, 4.45, 2.2);
  lab("MURO E OBJETOS", 4.0, 4.45, 1.9);
  lab("FOGO", 6.2, 4.45, 0.9, "center");
  s.addText([{ text: "SAÍDA", options: { bold: true, fontSize: 11, breakLine: true } }, { text: "a luz do sol: as coisas como são", options: { fontSize: 12 } }],
    { x: 7.75, y: 1.7, w: 1.6, h: 1.4, fontFace: "Arial", color: PRETO, valign: "top", margin: 0, isTextBox: true });
  s.addNotes("12–17 min. Desenhar este esquema no quadro enquanto se explica (ou mostrar este diapositivo). Atrás dos prisioneiros há um muro; por trás dele passam pessoas que transportam objetos; um fogo projeta as sombras desses objetos na parede. Os prisioneiros dão nomes às sombras e julgam que são as próprias coisas. Pergunta: «Se sempre só viste sombras, como saberias que são sombras?»");

  s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: "A caverna" });
  etiqueta(s, "A alegoria");
  titulo(s, "Quatro momentos");
  const passos = [["Sombras", "Toma-se a sombra pela coisa. Tudo parece claro."], ["Virar-se", "Um prisioneiro é solto e vê o fogo. A luz dói nos olhos."], ["Sair", "Sobe ao exterior e, aos poucos, vê as coisas e o sol."], ["Voltar", "Desce para contar. Os outros riem-se e não acreditam."]];
  passos.forEach(([t, d], i) => {
    const x = M + i * 2.3;
    circuloNum(s, x, 1.75, i + 1);
    if (i < 3) s.addShape("line", { x: x + 0.6, y: 2.0, w: 1.6, h: 0, line: { color: PRETO, width: 1.5, endArrowType: "triangle" } });
    s.addText([{ text: t.toUpperCase(), options: { fontFace: "Arial Black", fontSize: 14, breakLine: true } }, { text: d, options: { fontSize: 13 } }],
      { x, y: 2.45, w: 2.05, h: 1.9, fontFace: "Arial", color: PRETO, valign: "top", margin: 0, paraSpaceAfter: 6, isTextBox: true });
  });
  s.addNotes("17–22 min. Insistir no 2.º e no 4.º momentos: conhecer custa (a luz dói) e quem volta com outra versão é ridicularizado. Pedir exemplos atuais de «voltar à caverna»: contar à família que uma notícia era falsa, corrigir um amigo num grupo.");

  s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: "A caverna" });
  etiqueta(s, "Ligação · 10 min");
  titulo(s, "Que paredes temos hoje?");
  const paredes = [["O feed", "mostra o que um algoritmo escolheu para ti"], ["A notícia partilhada", "chega sem autor, sem data, sem contexto"], ["A resposta da IA", "soa segura, mesmo quando inventa"], ["O grupo da turma", "repete o que todos já pensam"]];
  paredes.forEach(([r, c], i) => cartao(s, M + (i % 2) * 4.55, 1.55 + Math.floor(i / 2) * 1.3, 4.35, 1.1, r, c));
  texto(s, [{ text: "Investigar é virar a cabeça: ", options: { bold: true } }, { text: "perguntar de onde vem a luz que faz a sombra." }], { x: M, y: 4.25, w: 9, h: 0.5, fontSize: 15 });
  s.addNotes("22–32 min. Pares: escolher uma das quatro paredes e dar um exemplo real (sem nomes de pessoas). Este é o fio do módulo: a segunda metade é sobre investigar e verificar. A pergunta de saída da aula volta a isto.");

  /* --- CHIROPTERA --- */
  pres.addSection({ title: "CHIROPTERA" });
  s = pres.addSlide({ masterName: "ESCURO", sectionTitle: "CHIROPTERA" });
  etiqueta(s, "Objeto · Paris, 2023", true);
  titulo(s, "Uma caverna na Ópera", true, { size: 28 });
  const fatos = [["Retour à la caverne", "JR cobre os andaimes do Palais Garnier com uma gruta em trompe-l'œil (setembro a novembro de 2023)."], ["CHIROPTERA", "12 de novembro de 2023: mais de 150 bailarinos dançam na fachada, na Place de l'Opéra. Coreografia de Damien Jalet."], ["Música", "Thomas Bangalter (ex-Daft Punk). Uma faixa de cerca de 17 minutos e uma versão de quase 6 horas."]];
  fatos.forEach(([r, c], i) => {
    s.addText([{ text: r.toUpperCase(), options: { fontSize: 11, bold: true, charSpacing: 1.5, color: COR_CLARA, breakLine: true } }, { text: c, options: { fontSize: 14, color: BRANCO } }],
      { x: M + i * 3.05, y: 1.85, w: 2.8, h: 2.4, fontFace: "Arial", valign: "top", margin: 0, paraSpaceAfter: 8, isTextBox: true });
  });
  s.addNotes("32–40 min. Mostrar imagens e um excerto do vídeo da performance (ligações no último diapositivo; o documentário «Dans la lumière», de Vincent Lorca, tem cerca de 30 minutos: escolher 3 a 4). Ouvir 1 a 2 minutos da música de olhos fechados antes de mostrar a imagem.");

  s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: "CHIROPTERA" });
  etiqueta(s, "Pergunta");
  titulo(s, "Chiroptera = morcegos");
  cartao(s, M, 1.6, 4.35, 1.6, "O morcego", "Vive na caverna e orienta-se no escuro pelo eco: emite um som e «ouve» a forma das coisas.");
  cartao(s, 5.15, 1.6, 4.35, 1.6, "O prisioneiro de Platão", "Vive na caverna e só confia no que vê. Toma as sombras pela realidade.");
  texto(s, [{ text: "Para discutir: ", options: { bold: true } }, { text: "a obra mostra-nos a caverna ou põe-nos dentro dela? E que «eco» podemos usar para nos orientarmos no meio de tanta informação?" }], { x: M, y: 3.5, w: 9, h: 1.0, fontSize: 16 });
  s.addNotes("40–50 min. Ninguém sabe a intenção dos autores ao certo: aceitar leituras justificadas. O «eco» pode ser: perguntar a uma segunda fonte, falar com quem viveu a situação, medir, testar. É a ponte para a investigação do projeto «Pergunta Humana». Corte possível aqui se a aula tiver 50 minutos.");

  /* --- This is Water --- */
  pres.addSection({ title: "This is Water" });
  s = pres.addSlide({ masterName: "ESCURO", sectionTitle: "This is Water" });
  etiqueta(s, "Objeto", true);
  citacao(s,
    "Dois peixes jovens vão a nadar e cruzam-se com um peixe mais velho, que lhes acena e diz: «Bom dia, rapazes. Como está a água?» Os dois peixes nadam mais um bocado, até que um olha para o outro e pergunta: «Que raio é a água?»",
    "David Foster Wallace, This is Water · Kenyon College, 21 de maio de 2005 · tradução livre", { x: M, y: 1.0, w: W - 2 * M, h: 3.6, escuro: true, size: 19 });
  s.addNotes("50–55 min. Ler em português; se a turma acompanhar, ouvir o início do discurso original (ligação no fim). Perguntar só: «O que é a água?» Não explicar ainda.");

  s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: "This is Water" });
  etiqueta(s, "A ideia");
  titulo(s, "O modo automático");
  s.addText("ÁGUA", { x: M, y: 1.55, w: 3.6, h: 1.4, fontFace: "Arial Black", fontSize: 60, color: COR, margin: 0, valign: "top", isTextBox: true });
  texto(s, "aquilo que é tão constante que deixamos de ver.", { x: M, y: 2.85, w: 3.6, h: 0.9, fontSize: 15 });
  texto(s, bullets([
    "Wallace chama-lhe «default setting»: a configuração de fábrica.",
    "Nela, sou o centro do mundo: a fila, o trânsito e as outras pessoas existem para me atrasar.",
    "Pensar é escolher para onde olhar. A liberdade que conta, diz ele, faz-se de atenção, consciência e esforço, todos os dias.",
  ]), { x: 4.5, y: 1.6, w: 5.0, h: 3.0, fontSize: 15, paraSpaceAfter: 10 });
  s.addNotes("55–65 min. O discurso usa o exemplo da fila do supermercado ao fim do dia: podemos ver os outros como obstáculos ou imaginar a vida deles. Ligar ao artigo 1.º da Declaração Universal dos Direitos Humanos: «dotados de razão e de consciência». Consciência, aqui, é dar conta da água.");

  s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: "This is Water" });
  etiqueta(s, "Juntar · 15 min");
  titulo(s, "Três imagens, uma pergunta");
  const tres = [["Caverna", "Platão", "Tomamos sombras por coisas."], ["Gruta na ópera", "JR · Jalet · Bangalter", "A arte mostra a caverna a milhares de pessoas de uma vez."], ["Água", "Wallace", "Não vemos aquilo em que vivemos."]];
  tres.forEach(([r, a, c], i) => {
    const x = M + i * 3.05;
    s.addShape("rect", { x, y: 1.55, w: 2.85, h: 2.2, fill: { color: i === 1 ? PRETO : BRANCO }, line: { color: PRETO, width: 2 } });
    s.addText([{ text: r.toUpperCase(), options: { fontFace: "Arial Black", fontSize: 16, breakLine: true } }, { text: a, options: { fontSize: 11, bold: true, color: i === 1 ? COR_CLARA : COR, breakLine: true } }, { text: c, options: { fontSize: 14 } }],
      { x: x + 0.18, y: 1.7, w: 2.5, h: 1.95, fontFace: "Arial", color: i === 1 ? BRANCO : PRETO, valign: "top", margin: 0, paraSpaceAfter: 8, isTextBox: true });
  });
  texto(s, [{ text: "Em grupo: ", options: { bold: true } }, { text: "uma imagem fixa de 10 segundos que mostre a vossa «caverna» ou a vossa «água». A turma adivinha qual é." }], { x: M, y: 4.05, w: 9, h: 0.7, fontSize: 15 });
  s.addNotes("65–85 min. Grupos de 3–4: 8 minutos para preparar a imagem fixa, depois apresentações. É uma turma de Interpretação: o corpo é a forma de resposta. A turma tem de dizer qual é a caverna ou a água e porquê.");

  pres.addSection({ title: "Fecho" });
  s = pres.addSlide({ masterName: "ESCURO", sectionTitle: "Fecho" });
  etiqueta(s, "Saída · diário de investigação", true);
  titulo(s, "Qual é a tua água?", true, { size: 34 });
  texto(s, bullets([
    "Uma coisa que fazes em modo automático e que hoje viste pela primeira vez.",
    "Uma informação que aceitaste esta semana sem verificar. Onde a podias confirmar?",
  ]), { x: M, y: 1.85, w: 8.5, h: 2.2, fontSize: 18, color: BRANCO, paraSpaceAfter: 14 });
  s.addNotes("85–100 min. Escrita individual no diário de investigação (conta para os 20% do diário). Voltar às duas certezas escritas no quadro no início: como as poderíamos verificar? Próxima aula: Sísifo e Marina Abramović.");

  desdobramentos(pres, "Fecho", [
    ["Platão", [
      ["José Saramago, A Caverna (2000)", "Um oleiro perde o trabalho para um centro comercial gigante, onde as obras descobrem uma gruta."],
      ["The Truman Show (Peter Weir, 1998)", "Um homem vive, sem saber, dentro de um programa de televisão."],
    ]],
    ["CHIROPTERA", [
      ["Ai Weiwei, Remembering (Munique, 2009)", "9 000 mochilas na fachada da Haus der Kunst formam a frase de uma mãe: «Ela viveu feliz durante sete anos neste mundo.»"],
      ["Ai Weiwei, Citizens' Investigation (2008–2011)", "Sem nomes oficiais, voluntários apuram os de 5 196 alunos mortos no sismo de Sichuan."],
    ]],
    ["Wallace", [
      ["Eli Pariser, a bolha de filtro (2011)", "A água do século XXI: cada um vê o mundo que um algoritmo escolheu. Ponte para Cidadania II."],
      ["Ai Weiwei, Rapture (Lisboa, 2021)", "Na Cordoaria Nacional: obras sobre vigilância, refugiados e liberdade de expressão."],
    ]],
  ], "Usar como menu para o diário ou para escolher o tema do projeto. A ligação mais forte é o Ai Weiwei: a Citizens' Investigation é exatamente o que o módulo pede, uma investigação feita por cidadãos quando a informação oficial falta. Remembering repete o gesto da gruta do JR: usar a fachada de um edifício para obrigar a ver.");

  referencias(pres, "Fecho", [
    ["Platão, A República, livro VII, 514a–517a. Tradução de Maria Helena da Rocha Pereira, Fundação Calouste Gulbenkian.", ""],
    ["Alegoria da caverna (Wikipédia)", "https://pt.wikipedia.org/wiki/Alegoria_da_caverna"],
    ["JR, Retour à la caverne, Acte II: CHIROPTERA (Palais Garnier, 2023)", "https://jr-art.net/projects/chiroptera"],
    ["Documentário «Dans la lumière», de Vincent Lorca, sobre CHIROPTERA (Resident Advisor)", "https://ra.co/news/81822"],
    ["Thomas Bangalter, CHIROPTERA: a música (MusicTech)", "https://musictech.com/news/music/thomas-bangalter-new-track-chiroptera/"],
    ["David Foster Wallace, This is Water: transcrição e áudio do discurso (Farnam Street)", "https://fs.blog/david-foster-wallace-this-is-water/"],
    ["This Is Water: contexto e publicação em livro, 2009 (Wikipédia)", "https://en.wikipedia.org/wiki/This_Is_Water"],
    ["José Saramago, A Caverna, 2000.", ""],
    ["Ai Weiwei, Remembering, Haus der Kunst, Munique, 2009 (Britannica)", "https://www.britannica.com/topic/Remembering-art-installation-by-Ai-Weiwei"],
    ["Pais chineses procuram respostas sobre as mortes de alunos no sismo (NPR, 2009)", "https://www.npr.org/2009/05/04/103727282/chinese-seek-answers-in-student-quake-deaths"],
    ["Ai Weiwei, Rapture, Cordoaria Nacional, Lisboa, 4 jun.–28 nov. 2021 (Lisson Gallery)", "https://lissongallery.com/news/rapture-a-major-exhibition-by-ai-weiwei-opens-at-cordoaria-nacional-in-lisbon"],
    ["Eli Pariser, The Filter Bubble, 2011.", ""],
  ], "As ligações abrem a partir do modo de apresentação. Verificar antes da aula se o vídeo do documentário está disponível em Portugal.");

  const f = path.join(RAIZ, "aula-01", "CD_I_Aula_01_INTP26.pptx");
  await pres.writeFile({ fileName: f });
  return f;
}

/* ===================================================================== AULA 2 */
async function aula2() {
  const pres = newDeck("CIDADANIA I · AULA 2 · O QUE SOMOS · INTP26");
  pres.title = "Cidadania I · Aula 2 · O que somos";

  pres.addSection({ title: "Abertura" });
  capa(pres, "Abertura", "Cidadania I · Ser-se humano: investigação e informação · Aula 2",
    "O que somos", "Sísifo e Camus · Marina Abramović",
    "100 min. Fio da aula: depois de «o que vemos», agora «o que somos». Sísifo mostra o ser humano a dar sentido a um esforço sem fim; Marina Abramović mostra o que acontece quando um corpo fica nas mãos dos outros e quando duas pessoas apenas se olham. Termina na dignidade (artigo 1.º da DUDH) e nas perguntas para o projeto.");

  let s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: "Abertura" });
  etiqueta(s, "Retoma · 5 min");
  titulo(s, "Qual era a tua água?", false, { size: 30 });
  cartao(s, M, 1.65, 2.85, 1.7, "Caverna", "Tomamos sombras por coisas.");
  cartao(s, 3.575, 1.65, 2.85, 1.7, "Gruta na ópera", "A arte põe a caverna à vista de todos.");
  cartao(s, 6.65, 1.65, 2.85, 1.7, "Água", "Não vemos aquilo em que vivemos.");
  texto(s, "Três alunos leem a saída da aula passada. A turma diz se aquilo é mesmo «água».", { x: M, y: 3.7, w: 9, h: 0.8, fontSize: 16 });
  s.addNotes("0–5 min. Ler três entradas do diário (com autorização). Hoje muda a pergunta: já não «como sabemos», mas «o que é isto de ser humano», com duas figuras: um mito grego e uma artista viva.");

  /* --- Sísifo --- */
  pres.addSection({ title: "Sísifo" });
  s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: "Sísifo" });
  etiqueta(s, "Objeto · o mito");
  titulo(s, "Sísifo");
  // encosta e pedra
  s.addShape("rtTriangle", { x: 5.4, y: 1.6, w: 4.1, h: 2.8, flipH: true, fill: { color: FUNDO2 }, line: { color: PRETO, width: 2 } });
  s.addShape("ellipse", { x: 7.25, y: 1.95, w: 0.85, h: 0.85, fill: { color: PRETO }, line: { color: PRETO, width: 0 } });
  s.addShape("line", { x: 6.05, y: 2.75, w: 0.85, h: 0.55, flipV: true, line: { color: COR, width: 2.5, endArrowType: "triangle" } });
  texto(s, bullets([
    "Rei de Corinto, enganou os deuses e até a morte.",
    "Castigo: empurrar uma pedra até ao cimo de uma montanha.",
    "Mal chega lá acima, a pedra rola de volta. E ele recomeça. Para sempre.",
  ]), { x: M, y: 1.6, w: 4.6, h: 2.6, fontSize: 16, paraSpaceAfter: 12 });
  texto(s, "Aparece já na Odisseia de Homero, canto XI.", { x: M, y: 4.3, w: 4.6, h: 0.4, fontSize: 11, color: CINZA });
  s.addNotes("5–10 min. Contar o mito, não ler. Perguntar: «Qual é a pior parte do castigo: o peso, ou saber que nunca acaba?» A maioria escolhe a segunda: é aí que entra Camus.");

  s = pres.addSlide({ masterName: "ESCURO", sectionTitle: "Sísifo" });
  etiqueta(s, "Camus · 1942", true);
  citacao(s,
    "A própria luta para atingir os píncaros basta para encher um coração de homem. É preciso imaginar Sísifo feliz.",
    "Albert Camus, O Mito de Sísifo (1942), últimas linhas", { x: M, y: 1.0, w: W - 2 * M, h: 2.3, escuro: true, size: 22 });
  texto(s, ([
    { text: "Absurdo: ", options: { bold: true, color: COR_CLARA } }, { text: "queremos sentido e o mundo não responde.", options: { breakLine: true } },
    { text: "Resposta de Camus: ", options: { bold: true, color: COR_CLARA } }, { text: "não fugir, viver com lucidez e fazer da pedra a nossa coisa." },
  ]), { x: M, y: 3.55, w: 9, h: 1.2, fontSize: 16, color: BRANCO, paraSpaceAfter: 8 });
  s.addNotes("10–18 min. Camus escreve durante a Segunda Guerra Mundial. Feliz não quer dizer contente: quer dizer que Sísifo, ao descer para ir buscar a pedra, sabe exatamente o que lhe acontece e, mesmo assim, não desiste. Perguntar: «Que pedras empurramos todos os dias?» (escola, trabalho, cuidar de alguém, treinar um papel).");

  s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: "Sísifo" });
  etiqueta(s, "Em cena · 15 min");
  titulo(s, "Três Sísifos");
  [["Desesperado", "a pedra é um castigo"], ["Indiferente", "a pedra é só rotina"], ["Feliz", "a pedra é minha"]].forEach(([t, d], i) => {
    const x = M + i * 3.05;
    circuloNum(s, x, 1.65, i + 1, 0.55);
    s.addText([{ text: t.toUpperCase(), options: { fontFace: "Arial Black", fontSize: 18, breakLine: true } }, { text: d, options: { fontSize: 14 } }],
      { x: x + 0.7, y: 1.6, w: 2.2, h: 1.0, fontFace: "Arial", color: PRETO, valign: "top", margin: 0, isTextBox: true });
  });
  texto(s, bullets([
    "Em silêncio, cada um empurra uma pedra imaginária durante 30 segundos, três vezes, uma por versão.",
    "Depois, em pares: o que mudou no corpo de uma versão para a outra? A pedra era a mesma.",
  ]), { x: M, y: 2.95, w: 9, h: 1.5, fontSize: 16, paraSpaceAfter: 10 });
  s.addNotes("18–33 min. Espaço livre. O professor marca os 30 segundos. O objetivo é sentir que a mesma tarefa muda com o sentido que lhe damos, que é a tese de Camus. Fechar com a linha (sim / depende / não) na sala: «É possível imaginar Sísifo feliz?» Pedir uma justificação por zona.");

  /* --- Abramović --- */
  pres.addSection({ title: "Marina Abramović" });
  s = pres.addSlide({ masterName: "ESCURO", sectionTitle: "Marina Abramović" });
  etiqueta(s, "Objeto · Nápoles, 1974", true);
  titulo(s, "Rhythm 0", true, { size: 34 });
  [["6 horas", "imóvel, no Studio Morra"], ["72 objetos", "em cima de uma mesa"], ["1 instrução", "usem-nos em mim como quiserem"]].forEach(([n, l], i) => {
    s.addText([{ text: n, options: { fontFace: "Arial Black", fontSize: 30, color: COR_CLARA, breakLine: true } }, { text: l, options: { fontSize: 14, color: BRANCO } }],
      { x: M + i * 3.05, y: 1.7, w: 2.85, h: 1.6, fontFace: "Arial", valign: "top", margin: 0, isTextBox: true });
  });
  texto(s, "Entre os objetos havia uma rosa, uma pena, perfume, pão e vinho, mas também uma tesoura, uma faca e uma pistola com uma bala.", { x: M, y: 3.5, w: 9, h: 0.9, fontSize: 15, color: BRANCO });
  s.addNotes("33–43 min. Marina Abramović (Belgrado, 1946) é uma das artistas que definiram a performance: o corpo da artista é o material da obra. Contar com cuidado o que aconteceu: ao longo das horas, o público passou de gestos inofensivos a gestos agressivos (cortaram-lhe a roupa, feriram-na) e houve quem a defendesse. Quando ela se mexeu no fim, as pessoas afastaram-se. Não mostrar imagens fortes sem avisar a turma.");

  s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: "Marina Abramović" });
  etiqueta(s, "Pergunta");
  titulo(s, "O que fazemos ao outro quando não há regras?", false, { size: 24, h: 0.9 });
  cartao(s, M, 1.85, 4.35, 1.9, "O que a obra mostrou", "Quando alguém se torna objeto, há quem o proteja e há quem abuse. E muitos limitam-se a ver.");
  cartao(s, 5.15, 1.85, 4.35, 1.9, "O que a lei diz", "«Todos os seres humanos nascem livres e iguais em dignidade e em direitos.» (DUDH, art. 1.º)", { corRot: COR });
  texto(s, [{ text: "Para discutir: ", options: { bold: true } }, { text: "a dignidade depende de a outra pessoa a respeitar? E tu, em que grupo estarias: os que protegem, os que abusam ou os que veem?" }], { x: M, y: 3.95, w: 9, h: 0.8, fontSize: 15 });
  s.addNotes("43–50 min. Discussão em plenário. Ligar ao artigo 1.º da DUDH, que vem da aula de apresentação. Os que «só veem» são a parte mais interessante da discussão: o espetador também é responsável? Corte possível aqui se a aula tiver 50 minutos.");

  s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: "Marina Abramović" });
  etiqueta(s, "Objeto · MoMA, Nova Iorque, 2010");
  titulo(s, "The Artist Is Present");
  // duas cadeiras e uma mesa, vistas de cima
  s.addShape("rect", { x: 6.0, y: 2.0, w: 0.7, h: 0.7, fill: { color: PRETO }, line: { color: PRETO, width: 0 } });
  s.addShape("rect", { x: 6.95, y: 1.95, w: 1.0, h: 0.8, fill: { color: BRANCO }, line: { color: PRETO, width: 2 } });
  s.addShape("rect", { x: 8.2, y: 2.0, w: 0.7, h: 0.7, fill: { color: BRANCO }, line: { color: PRETO, width: 2 } });
  s.addText("ARTISTA", { x: 5.75, y: 2.85, w: 1.2, h: 0.3, fontFace: "Arial", fontSize: 10, bold: true, align: "center", margin: 0, isTextBox: true });
  s.addText("QUALQUER PESSOA", { x: 7.8, y: 2.85, w: 1.5, h: 0.3, fontFace: "Arial", fontSize: 10, bold: true, align: "center", margin: 0, isTextBox: true });
  texto(s, bullets([
    "Durante quase três meses, Abramović esteve sentada, em silêncio, no átrio do museu.",
    "Quem quisesse sentava-se à frente dela e olhava-a nos olhos o tempo que quisesse.",
    "Ao todo, mais de 736 horas. Houve quem chorasse, quem risse, quem não aguentasse um minuto.",
  ]), { x: M, y: 1.6, w: 5.0, h: 3.0, fontSize: 15, paraSpaceAfter: 10 });
  s.addNotes("50–57 min. Se houver tempo, mostrar um excerto do documentário «Marina Abramović: The Artist Is Present» (Matthew Akers, 2012), por exemplo o momento em que Ulay, o ex-companheiro e parceiro de trabalho, se senta à frente dela. Contraste com Rhythm 0: aqui ela não está à mercê de ninguém, está apenas presente. Pergunta: «Porque é que olhar alguém nos olhos, em silêncio, é tão difícil?»");

  s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: "Marina Abramović" });
  etiqueta(s, "Em cena · 10 min");
  titulo(s, "Um minuto presente");
  texto(s, bullets([
    "Pares, frente a frente, em duas cadeiras. Um minuto de silêncio, a olhar o outro nos olhos.",
    "Quem não quiser olhar pode ser o guarda do tempo, ou olhar para as mãos do colega.",
    "Depois, cada um escreve uma palavra para o que sentiu. Só uma.",
  ]), { x: M, y: 1.6, w: 5.6, h: 2.6, fontSize: 16, paraSpaceAfter: 12 });
  s.addShape("ellipse", { x: 7.1, y: 1.7, w: 2.1, h: 2.1, fill: { color: BRANCO }, line: { color: PRETO, width: 3 } });
  s.addText("1:00", { x: 7.1, y: 1.7, w: 2.1, h: 2.1, fontFace: "Arial Black", fontSize: 32, align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addNotes("57–67 min. Atividade voluntária: ninguém é obrigado a olhar. Fazer duas rondas, trocando de par. Recolher as palavras no quadro (desconforto, riso, calma, vergonha, ligação). Ligar a This is Water: estar presente é o contrário do modo automático.");

  /* --- Fecho --- */
  pres.addSection({ title: "Fecho" });
  s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: "Fecho" });
  etiqueta(s, "Juntar · 15 min");
  titulo(s, "Ser humano é…");
  [["Sísifo", "dar sentido a um esforço que não acaba"], ["Rhythm 0", "depender do modo como os outros nos tratam"], ["The Artist Is Present", "ser visto, e conseguir olhar o outro"]].forEach(([r, c], i) => {
    cartao(s, M + i * 3.05, 1.6, 2.85, 1.5, r, c, { size: 15 });
  });
  texto(s, [{ text: "Projeto «Pergunta Humana»: ", options: { bold: true } }, { text: "em grupos, transformem uma destas ideias numa pergunta que se possa investigar. Exemplo: «Porque é que as pessoas assistem sem intervir quando alguém é humilhado?»" }], { x: M, y: 3.4, w: 9, h: 1.2, fontSize: 15 });
  s.addNotes("67–85 min. Cada grupo escreve uma ou duas perguntas e lê-as. Critério: a pergunta não se responde com sim ou não nem com cinco minutos de pesquisa. As perguntas ficam registadas: são candidatas ao projeto.");

  s = pres.addSlide({ masterName: "ESCURO", sectionTitle: "Fecho" });
  etiqueta(s, "Saída · diário de investigação", true);
  titulo(s, "Qual é a tua pedra?", true, { size: 34 });
  texto(s, bullets([
    "Uma pedra que empurras todos os dias. Consegues imaginar-te feliz a empurrá-la?",
    "Uma pergunta sobre ser-se humano que gostavas de investigar no projeto.",
  ]), { x: M, y: 1.85, w: 8.5, h: 2.2, fontSize: 18, color: BRANCO, paraSpaceAfter: 14 });
  s.addNotes("85–100 min. Escrita individual no diário de investigação. Recolher as perguntas do projeto: na próxima aula formam-se os grupos a partir delas.");

  desdobramentos(pres, "Fecho", [
    ["Sísifo", [
      ["Ticiano, Sísifo (1548–1549)", "No Museo del Prado, em Madrid: o corpo dobrado sob a pedra."],
      ["Albert Camus, A Peste (1947)", "Uma cidade fechada por uma epidemia: a revolta deixa de ser de um e passa a ser de todos."],
    ]],
    ["Rhythm 0", [
      ["Yoko Ono, Cut Piece (Tóquio, 1964)", "Dez anos antes: sentada no palco, deixa o público cortar-lhe a roupa com uma tesoura."],
      ["O caso Kitty Genovese (Nova Iorque, 1964)", "Deu origem ao «efeito do espectador». Em 2016, o New York Times admitiu que tinha exagerado o número de testemunhas."],
    ]],
    ["Abramović", [
      ["Ai Weiwei, Law of the Journey (2016)", "Um barco insuflável de 16 metros cheio de figuras humanas: os refugiados. Esteve em Lisboa em 2021."],
      ["Ai Weiwei, Human Flow (2017)", "Documentário sobre refugiados em 23 países: estar presente diante de quem perdeu tudo."],
    ]],
  ], "Kitty Genovese liga as duas aulas: é uma história sobre quem só vê (como em Rhythm 0) e também um caso de informação errada, corrigida 52 anos depois. O caso envolve violência sexual e homicídio: contar com cuidado. Ai Weiwei leva a dignidade para fora da sala: Law of the Journey esteve na Cordoaria Nacional, em Lisboa, na exposição Rapture (2021).");

  referencias(pres, "Fecho", [
    ["Homero, Odisseia, canto XI. Tradução de Frederico Lourenço.", ""],
    ["Albert Camus, O Mito de Sísifo (Le Mythe de Sisyphe), 1942.", ""],
    ["Sísifo (Wikipédia)", "https://pt.wikipedia.org/wiki/S%C3%ADsifo"],
    ["Marina Abramović, Rhythm 0, 1974 (Wikipédia)", "https://en.wikipedia.org/wiki/Rhythm_0"],
    ["MoMA, Marina Abramović: The Artist Is Present (2010): guia áudio", "https://www.moma.org/audio/3118"],
    ["MoMA, comunicado de imprensa da exposição (PDF)", "https://www.moma.org/documents/moma_press-release_387201.pdf"],
    ["Documentário «Marina Abramović: The Artist Is Present», de Matthew Akers (2012).", ""],
    ["Declaração Universal dos Direitos Humanos, artigo 1.º (versão portuguesa).", ""],
    ["Ticiano, Sísifo, 1548–1549. Museo del Prado, Madrid.", ""],
    ["Albert Camus, A Peste, 1947.", ""],
    ["MoMA, Yoko Ono: One Woman Show, 1960–1971 (inclui Cut Piece)", "https://www.moma.org/calendar/exhibitions/1494"],
    ["O caso Kitty Genovese e a correção do New York Times (Wikipédia)", "https://en.wikipedia.org/wiki/Murder_of_Kitty_Genovese"],
    ["Ai Weiwei, Rapture, Cordoaria Nacional, Lisboa, 2021 (Lisson Gallery)", "https://lissongallery.com/news/rapture-a-major-exhibition-by-ai-weiwei-opens-at-cordoaria-nacional-in-lisbon"],
    ["Ai Weiwei, Human Flow, documentário, 2017.", ""],
  ], "Rhythm 0 tem imagens fortes; ver o material antes de o mostrar e avisar a turma.");

  const f = path.join(RAIZ, "aula-02", "CD_I_Aula_02_INTP26.pptx");
  await pres.writeFile({ fileName: f });
  return f;
}

const newDeck = novoDeck;

(async () => {
  let applyTheme = null;
  try { ({ applyTheme } = require(process.env.APPLY_THEME || "./apply_theme.js")); } catch (e) { /* opcional */ }
  for (const fn of [aula1, aula2]) {
    const f = await fn();
    if (applyTheme) await applyTheme(f, THEME);
    console.log(f);
  }
})();

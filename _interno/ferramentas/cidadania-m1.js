/* Motor das fichas: sem campos de escrita, sem recolha de dados pessoais. */
(() => {
  'use strict';
  const root=document.getElementById('atividade');
  if(!root)return;
  const cfg=JSON.parse(document.getElementById('dados').textContent);
  let round=0,selected=[],finished=false;
  const key='epi-cd-m1-v1-'+cfg.id;
  const el=(tag,text,cls)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;};
  const button=(text,fn,cls='opcao')=>{const b=el('button',text,cls);b.type='button';b.addEventListener('click',fn);return b;};
  const feedback=document.getElementById('feedback');
  const announce=text=>{feedback.replaceChildren(el('p',text));feedback.hidden=false;};
  const save=value=>{try{localStorage.setItem(key,value);}catch{};};
  const clear=()=>{root.replaceChildren();feedback.hidden=true;feedback.replaceChildren();selected=[];};
  function finish(){
    finished=true;save('explorado');clear();
    root.append(el('p','Percurso explorado','p-rot'),el('h2',cfg.close.title),el('p',cfg.close.text,'ler'));
    root.append(el('p',cfg.close.discuss,'debate'));
    root.append(button('Voltar a explorar',reset,'c-prim'));
    document.getElementById('estado').textContent='Explorado';
  }
  function next(){round++;if(round>=cfg.rounds.length)finish();else render();}
  function after(text){announce(text);root.querySelectorAll('button').forEach(b=>b.disabled=true);root.append(button(round+1===cfg.rounds.length?'Concluir':'Continuar',next,'c-prim seguir'));}
  function reset(){round=0;finished=false;save('');render();}
  function heading(r){root.append(el('p',`${round+1} / ${cfg.rounds.length}`,'p-rot'),el('h2',r.title||cfg.title));if(r.scene)root.append(el('p',r.scene,'cena ler'));if(r.question)root.append(el('p',r.question,'pergunta'));}
  function classify(r){
    const grid=el('div',undefined,'escolhas');
    r.options.forEach((o,i)=>grid.append(button(o,()=>{
      if(i===r.correct){after(r.feedback);}else{announce(r.wrong?.[i]||'Volta ao caso e procura uma pista. Podes tentar outra vez.');}
    })));
    root.append(grid);
  }
  function choices(r){
    const grid=el('div',undefined,'escolhas');
    r.options.forEach(o=>grid.append(button(o.label,()=>after(o.feedback))));
    root.append(grid);
    root.append(el('p','Escolhe uma posição. Explica-a oralmente antes de avançar.','p-nota'));
  }
  function match(r){
    let left=null;const done=new Set();
    const grid=el('div',undefined,'pares');const a=el('div'),b=el('div');
    const leftButtons=[],rightButtons=[];
    r.pairs.forEach((p,i)=>{
      const btn=button(p[0],()=>{left=i;leftButtons.forEach((x,j)=>{x.setAttribute('aria-pressed',String(i===j));});announce('Agora escolhe o direito ou princípio correspondente.');});
      btn.setAttribute('aria-pressed','false');a.append(btn);leftButtons.push(btn);
    });
    const indexes=r.pairs.map((_,i)=>i).reverse();
    indexes.forEach(i=>{
      const btn=button(r.pairs[i][1],()=>{
        if(left===null){announce('Escolhe primeiro uma situação na primeira coluna.');return;}
        if(left!==i){announce('Essa ligação precisa de ser revista. Procura o direito diretamente afetado.');return;}
        done.add(i);leftButtons[i].disabled=true;btn.disabled=true;leftButtons[i].setAttribute('aria-pressed','false');left=null;
        announce(r.pairs[i][2]);
        if(done.size===r.pairs.length){root.append(button('Continuar',next,'c-prim seguir'));}
      });b.append(btn);rightButtons.push(btn);
    });
    grid.append(a,b);root.append(grid,el('p','Seleciona uma situação e depois o princípio que lhe corresponde. Há outras relações possíveis; aqui procuramos a mais direta.','p-nota'));
  }
  function perspective(r){
    const seen=new Set();const box=el('div',undefined,'perspetiva');const grid=el('div',undefined,'escolhas');
    r.roles.forEach((role,i)=>grid.append(button(role.label,()=>{
      seen.add(i);box.replaceChildren(el('h3',role.label),el('p',role.text,'ler'));
      grid.children[i].setAttribute('aria-pressed','true');
      if(seen.size===r.roles.length&&!root.querySelector('.seguir'))root.append(button('Comparar as posições',()=>after(r.feedback),'c-prim seguir'));
    })));
    [...grid.children].forEach(b=>b.setAttribute('aria-pressed','false'));
    root.append(grid,box,el('p','Abre todas as posições. Procura o que cada pessoa sabe e o que pode decidir.','p-nota'));
  }
  function order(r){
    const pool=el('div',undefined,'escolhas');const list=el('ol',undefined,'sequencia');const ids=[...r.order].reverse();
    ids.forEach(i=>pool.append(button(r.items[i],e=>{})));
    [...pool.children].forEach((b,j)=>{b.onclick=()=>{selected.push(ids[j]);list.append(el('li',r.items[ids[j]]));b.disabled=true;};});
    root.append(pool,list);
    root.append(button('Verificar a sequência',()=>{
      if(selected.length!==r.order.length){announce('Seleciona todos os elementos pela ordem que propões.');return;}
      if(selected.every((x,i)=>x===r.order[i]))after(r.feedback);else announce('A sequência ainda precisa de revisão. Limpa-a e observa as relações entre os elementos.');
    },'c-prim'));
    root.append(button('Limpar a sequência',()=>{selected=[];list.replaceChildren();[...pool.children].forEach(b=>b.disabled=false);feedback.hidden=true;},'c-sec'));
  }
  function build(r){
    const grid=el('div',undefined,'escolhas');
    r.options.forEach((o,i)=>{
      const b=button(o.label,()=>{if(selected.includes(i))selected=selected.filter(x=>x!==i);else selected.push(i);b.setAttribute('aria-pressed',String(selected.includes(i)));});
      b.setAttribute('aria-pressed','false');grid.append(b);
    });root.append(grid);
    root.append(button('Verificar as ligações',()=>{
      const good=selected.length===r.correct.length&&r.correct.every(i=>selected.includes(i));
      if(good)after(r.feedback);else announce(r.hint);
    },'c-prim seguir'));
  }
  function reveal(r){
    let i=0;const board=el('div',undefined,'pistas');root.append(board);
    const b=button('Abrir a primeira pista',()=>{
      board.append(el('p',r.clues[i],'cena'));i++;
      b.textContent='Abrir a próxima pista';
      if(i===r.clues.length){b.remove();classify(r);}
    },'c-prim');root.append(b);
  }
  function audit(r){
    let seen=new Set();const pane=el('div',undefined,'perspetiva');const grid=el('div',undefined,'escolhas');
    r.sources.forEach((s,i)=>grid.append(button(s.label,()=>{seen.add(i);pane.replaceChildren(el('h3',s.author),el('p',s.description,'ler'),el('p',s.limit,'p-nota'));if(seen.size===r.sources.length&&!root.querySelector('.avaliar')){const box=el('div',undefined,'avaliar');root.append(box);r.options.forEach(o=>box.append(button(o.label,()=>after(o.feedback))));}})));
    root.append(grid,pane,el('p','Abre as fichas das fontes antes de escolher.','p-nota'));
  }
  function vote(r){
    let chosen=null;const first=el('div',undefined,'escolhas');const box=el('div',undefined,'pistas');
    r.initial.forEach((label,i)=>first.append(button(label,()=>{
      chosen=i;first.querySelectorAll('button').forEach(b=>b.disabled=true);
      box.append(el('p','A tua posição inicial: '+label,'p-rot'),el('p',r.newInfo,'cena ler'),el('p','Manténs ou revês a posição?','pergunta'));
      r.final.forEach(o=>box.append(button(o.label,()=>after(o.feedback))));
    })));
    root.append(first,box,el('p','Esta escolha representa a posição de quem está a usar o ecrã. Não simula uma votação real da turma.','p-nota'));
  }
  function render(){
    clear();document.getElementById('estado').textContent=`Ronda ${round+1}`;const r=cfg.rounds[round];heading(r);
    const types={classify,listen:classify,match,perspective,order,build,branch:choices,power:choices,reveal,audit,vote};
    (types[r.type||cfg.type]||choices)(r);
  }
  document.getElementById('reiniciar').addEventListener('click',reset);
  render();
  window.CidadaniaExercise={restart:reset,getState:()=>({round,finished,selected:[...selected]})};
})();

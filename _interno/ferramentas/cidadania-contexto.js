/* Três modos de leitura. As escolhas dos exercícios continuam sem escrita. */
(() => {
 'use strict';
 const body=document.body;
 const buttons=[...document.querySelectorAll('[data-set-mode]')];
 const panels=[...document.querySelectorAll('.lesson-panel')];
 const description=document.getElementById('modo-explica');
 const label=document.getElementById('projection-label');
 const previous=document.getElementById('panel-prev'),next=document.getElementById('panel-next');
 let panel=0,mode='autonomo';
 const descriptions={autonomo:'Lê ao teu ritmo. As seis partes estão abertas e podes regressar a uma palavra ou a uma imagem.',projecao:'Um momento de cada vez, para observar, ler e discutir em conjunto. Usa os botões no fundo da página.',revisao:'Recupera a ideia central, as palavras e um exemplo de argumentação antes de preparar o ensaio.'};
 function show(){
  panels.forEach((p,i)=>p.hidden=mode==='projecao'?i!==panel:mode==='revisao'&&p.dataset.panel!=='rever');
  if(label&&panels.length)label.textContent=`${panel+1} / ${panels.length} · ${panels[panel].dataset.title}`;
  if(previous)previous.disabled=panel===0;
  if(next)next.disabled=panel===panels.length-1;
 }
 function setMode(value){
  mode=Object.hasOwn(descriptions,value)?value:'autonomo';body.dataset.mode=mode;
  buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.setMode===mode)));
  document.querySelectorAll('details.context-chapter').forEach((chapter,i)=>chapter.open=mode!=='projecao'||i===0);
  if(description)description.textContent=descriptions[mode];
  try{localStorage.setItem('epi-cd-mode-v2',mode);}catch{}
  show();
 }
 buttons.forEach(b=>b.addEventListener('click',()=>setMode(b.dataset.setMode)));
 function change(delta){
  panel=Math.max(0,Math.min(panels.length-1,panel+delta));show();
  const title=panels[panel]?.querySelector('h2');
  if(title){title.setAttribute('tabindex','-1');title.focus({preventScroll:true});panels[panel].scrollIntoView({block:'start',behavior:'auto'});}
 }
 previous?.addEventListener('click',()=>change(-1));next?.addEventListener('click',()=>change(1));
 document.querySelectorAll('[data-open-panel]').forEach(a=>a.addEventListener('click',()=>{const i=panels.findIndex(p=>p.id===a.dataset.openPanel);if(i>=0){panel=i;show();}}));
 let stored;try{stored=localStorage.getItem('epi-cd-mode-v2');}catch{}
 const hash=window.location?.hash||'';
 const target=panels.findIndex(p=>'#'+p.id===hash);
 if(target>=0){panel=target;if(stored==='revisao'&&panels[target].dataset.panel!=='rever')stored='autonomo';}
 setMode(stored||'autonomo');
 window.CidadaniaReading={setMode,change,getState:()=>({mode,panel,panels:panels.length})};
})();

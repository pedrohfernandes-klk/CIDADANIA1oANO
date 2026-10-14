/* Exercita o motor real num DOM mínimo, sem arrancar servidor ou navegador. */
const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
class Element{
 constructor(tag){this.tagName=tag.toLowerCase();this.children=[];this.className='';this.attributes={};this.events={};this.disabled=false;this.hidden=false;this._text='';}
 set textContent(v){this._text=String(v);this.children=[];} get textContent(){return this._text+this.children.map(x=>x.textContent).join(' ');}
 append(...nodes){for(const n of nodes){n.parent=this;this.children.push(n);}}
 replaceChildren(...n){this.children=[];this._text='';this.append(...n);}
 addEventListener(type,fn){(this.events[type]??=[]).push(fn);}
 setAttribute(k,v){this.attributes[k]=v;} getAttribute(k){return this.attributes[k];}
 remove(){if(this.parent)this.parent.children=this.parent.children.filter(n=>n!==this);}
 querySelectorAll(q){const res=[];const match=n=>q.startsWith('.')?n.className.split(' ').includes(q.slice(1)):n.tagName===q;const walk=n=>{n.children.forEach(c=>{if(match(c))res.push(c);walk(c);});};walk(this);return res;}
 querySelector(q){return this.querySelectorAll(q)[0]??null;}
 click(){if(this.disabled)return;for(const fn of this.events.click??[])fn({target:this});if(this.onclick)this.onclick({target:this});}
}
const dir=path.join(__dirname,'../../docs/m1');const engine=fs.readFileSync(path.join(__dirname,'cidadania-m1.js'),'utf8');let total=0;
function run(file,fault=false,branch=0){
 const html=fs.readFileSync(path.join(dir,file),'utf8');const cfg=JSON.parse(html.match(/id="dados">([\s\S]*?)<\/script>/)[1]);
 const ids={};for(const id of ['atividade','feedback','dados','estado','reiniciar'])ids[id]=new Element('div');ids.dados.textContent=JSON.stringify(cfg);
 const records={};const context={document:{getElementById:id=>ids[id],createElement:tag=>new Element(tag)},localStorage:{setItem:(k,v)=>{if(fault)throw Error('blocked');records[k]=v;}},window:{}};
 vm.createContext(context);vm.runInContext(engine,context);const root=ids.atividade;
 const buttons=()=>root.querySelectorAll('button');const clickText=text=>{const b=buttons().find(b=>b.textContent===text&&!b.disabled);assert(b,'Botão em falta: '+text+' em '+file);b.click();};
 for(let ri=0;ri<cfg.rounds.length;ri++){
  const r=cfg.rounds[ri],type=r.type??cfg.type;
  assert.equal(context.window.CidadaniaExercise.getState().round,ri);
  if(['classify','listen'].includes(type)){
   const wrong=(r.correct+1)%r.options.length;clickText(r.options[wrong]);assert(!ids.feedback.hidden);assert.equal(context.window.CidadaniaExercise.getState().round,ri);clickText(r.options[r.correct]);
  }else if(['branch','power'].includes(type)){clickText(r.options[branch%r.options.length].label);
  }else if(type==='match'){
   clickText(r.pairs[0][1]);assert(!ids.feedback.hidden);
   for(const pair of r.pairs){clickText(pair[0]);clickText(pair[1]);}
  }else if(type==='perspective'){
   for(const role of r.roles)clickText(role.label);clickText('Comparar as posições');
  }else if(type==='order'){
   clickText('Verificar a sequência');assert(!ids.feedback.hidden);
   clickText(r.items[r.order.at(-1)]);clickText('Limpar a sequência');
   for(const i of r.order)clickText(r.items[i]);clickText('Verificar a sequência');
  }else if(type==='build'){
   clickText('Verificar as ligações');assert(!ids.feedback.hidden);
   for(const i of r.correct)clickText(r.options[i].label);clickText('Verificar as ligações');
  }else if(type==='reveal'){
   for(let i=0;i<r.clues.length;i++)clickText(i?'Abrir a próxima pista':'Abrir a primeira pista');clickText(r.options[r.correct]);
  }else if(type==='audit'){
   for(const source of r.sources)clickText(source.label);clickText(r.options[branch%r.options.length].label);
  }else if(type==='vote'){
   clickText(r.initial[branch%r.initial.length]);clickText(r.final[branch%r.final.length].label);
  }else throw Error('Tipo desconhecido: '+type);
  clickText(ri+1===cfg.rounds.length&&type!=='match'?'Concluir':'Continuar');
 }
 assert(context.window.CidadaniaExercise.getState().finished,file+' não terminou');
 if(!fault)assert.equal(records['epi-cd-m1-v1-'+cfg.id],'explorado');
 ids.reiniciar.click();assert.equal(context.window.CidadaniaExercise.getState().round,0);assert(!context.window.CidadaniaExercise.getState().finished);
 total++;
}
for(const file of fs.readdirSync(dir).filter(x=>/^passo-\d\d\.html$/.test(x))){for(let branch=0;branch<3;branch++)run(file,false,branch);run(file,true);}
console.log(total+' percursos completos verificados, incluindo escolhas, tentativas, recomeço e armazenamento indisponível.');

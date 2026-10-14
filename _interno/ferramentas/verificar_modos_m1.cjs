const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
class E{
 constructor(id=''){this.id=id;this.dataset={};this.attributes={};this.events={};this.hidden=false;this.disabled=false;this.open=false;}
 setAttribute(k,v){this.attributes[k]=v;}addEventListener(t,f){this.events[t]=f;}focus(){this.focused=true;}scrollIntoView(){}querySelector(){return new E();}
}
const names=['observar','conhecer','perceber','experimentar','sala','rever'];
const code=fs.readFileSync(path.join(__dirname,'cidadania-contexto.js'),'utf8');
function test(stored=null,blocked=false,hash=''){
 const panels=names.map(n=>{const p=new E(n);p.dataset={panel:n,title:n};return p;});
 const buttons=['projecao','autonomo','revisao'].map(n=>{const b=new E();b.dataset.setMode=n;return b;});
 const chapters=[new E(),new E(),new E()],ids={};for(const n of ['modo-explica','projection-label','panel-prev','panel-next'])ids[n]=new E(n);
 const body={dataset:{}};let data=stored;
 const context={window:{location:{hash}},document:{body,getElementById:id=>ids[id],querySelectorAll:q=>({'[data-set-mode]':buttons,'.lesson-panel':panels,'details.context-chapter':chapters,'[data-open-panel]':[]}[q]??[])},localStorage:{getItem:()=>{if(blocked)throw Error('blocked');return data;},setItem:(k,v)=>{if(blocked)throw Error('blocked');data=v;}}};
 vm.createContext(context);vm.runInContext(code,context);const api=context.window.CidadaniaReading;
 if(stored==='revisao'&&hash==='#conhecer'){assert.equal(api.getState().mode,'autonomo');assert.equal(api.getState().panel,1);}
 api.setMode('projecao');assert.equal(panels.filter(p=>!p.hidden).length,1);assert(chapters[0].open&&!chapters[1].open);
 for(let i=0;i<10;i++)api.change(1);assert.equal(api.getState().panel,5);assert(ids['panel-next'].disabled);
 for(let i=0;i<10;i++)api.change(-1);assert.equal(api.getState().panel,0);assert(ids['panel-prev'].disabled);
 api.setMode('revisao');assert.deepEqual(panels.filter(p=>!p.hidden).map(p=>p.id),['rever']);
 api.setMode('autonomo');assert(panels.every(p=>!p.hidden));assert(chapters.every(p=>p.open));
 assert.equal(buttons[1].attributes['aria-pressed'],'true');
}
test();test('projecao');test('revisao');test(null,true);test('revisao',false,'#conhecer');
console.log('Modos verificados: projeção, leitura autónoma, revisão, limites de navegação, âncora e armazenamento bloqueado.');

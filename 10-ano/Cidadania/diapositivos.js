/* Navegação: setas, espaço, PageUp/PageDown, toque, #n no endereço. «F» = ecrã inteiro. */
(function(){
  var ds=[].slice.call(document.querySelectorAll('.d')),i=0,barra=document.getElementById('barra'),cont=document.getElementById('cont');
  ds.forEach(function(){var s=document.createElement('span');barra&&barra.appendChild(s)});
  function ir(n){
    i=Math.max(0,Math.min(ds.length-1,n));
    ds.forEach(function(d,k){d.classList.toggle('ativo',k===i)});
    if(barra)[].forEach.call(barra.children,function(s,k){s.classList.toggle('f',k<=i)});
    if(cont)cont.textContent=(i+1)+' / '+ds.length;
    try{history.replaceState(null,'','#'+(i+1))}catch(e){}
  }
  document.addEventListener('keydown',function(e){
    if(/INPUT|TEXTAREA/.test(e.target.tagName))return;
    if(['ArrowRight','PageDown',' '].indexOf(e.key)>-1){e.preventDefault();ir(i+1)}
    else if(['ArrowLeft','PageUp'].indexOf(e.key)>-1){e.preventDefault();ir(i-1)}
    else if(e.key==='Home')ir(0);else if(e.key==='End')ir(ds.length-1);
    else if(e.key==='f'||e.key==='F'){var el=document.documentElement;if(!document.fullscreenElement&&el.requestFullscreen)el.requestFullscreen();else if(document.exitFullscreen)document.exitFullscreen()}
  });
  var x0=null;
  document.addEventListener('touchstart',function(e){x0=e.touches[0].clientX},{passive:true});
  document.addEventListener('touchend',function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>50)ir(i+(dx<0?1:-1));x0=null});
  var ant=document.getElementById('ant'),seg=document.getElementById('seg');
  ant&&ant.addEventListener('click',function(){ir(i-1)});seg&&seg.addEventListener('click',function(){ir(i+1)});
  /* Cronómetros: <button class="relogio" data-min="3">3:00</button>; clicar inicia/para. */
  [].forEach.call(document.querySelectorAll('.relogio'),function(b){
    var total=+b.dataset.min*60,rest=total,t=null;
    function mostra(){b.textContent=Math.floor(rest/60)+':'+('0'+rest%60).slice(-2)}
    b.addEventListener('click',function(){
      if(t){clearInterval(t);t=null;return}
      if(rest<=0)rest=total;
      t=setInterval(function(){rest--;mostra();if(rest<=0){clearInterval(t);t=null}},1000);
    });mostra();
  });
  var h=parseInt((location.hash||'').slice(1),10);ir(isNaN(h)?0:h-1);
})();

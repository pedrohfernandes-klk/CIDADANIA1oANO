/* Guarda as respostas neste dispositivo enquanto o aluno escreve (se o navegador deixar). */
(function(){
  var chave='cd-'+(document.body.dataset.ficha||location.pathname);
  var dados={};
  try{dados=JSON.parse(localStorage.getItem(chave)||'{}')||{}}catch(e){dados={}}
  var campos=[].slice.call(document.querySelectorAll('textarea[name],input[name]'));
  campos.forEach(function(c){
    if(dados[c.name]!=null){if(c.type==='radio'||c.type==='checkbox')c.checked=dados[c.name]===c.value||dados[c.name]===true;else c.value=dados[c.name]}
    c.addEventListener('input',guardar);c.addEventListener('change',guardar);
  });
  function guardar(){
    campos.forEach(function(c){
      if(c.type==='radio'){if(c.checked)dados[c.name]=c.value}
      else if(c.type==='checkbox')dados[c.name]=c.checked;
      else dados[c.name]=c.value;
    });
    try{localStorage.setItem(chave,JSON.stringify(dados))}catch(e){}
  }
  var imp=document.getElementById('imprimir');
  imp&&imp.addEventListener('click',function(){window.print()});
  var limpar=document.getElementById('limpar');
  limpar&&limpar.addEventListener('click',function(){
    if(!confirm('Apagar todas as respostas desta ficha neste dispositivo?'))return;
    try{localStorage.removeItem(chave)}catch(e){}
    campos.forEach(function(c){if(c.type==='radio'||c.type==='checkbox')c.checked=false;else c.value=''});dados={};
  });
})();

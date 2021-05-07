
window.attempted = [];
function hint_func(a){
  console.log(window.attempted.length);
  for(var i=0;i<window.attempted.length;i++){
    if(window.attempted[i].split(',')[1] == String(a)){
      alert(window.attempted[i].split(',')[2]);

    }
  }
}
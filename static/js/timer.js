
var interval = setInterval(function(){
  time--;
  document.getElementById('timer').innerHTML=time;

  if (time === 0){
    setTimeout( function(){clearInterval(interval);
    $("#submit").click()
    },0)

  }
}, 1000);
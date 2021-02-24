// 4,6,5,m,w,c
function show(result,remove,status,pass_status)
{
    if(remove == 6){
        document.getElementsByClassName('container1')[0].style.display = 'none';
        document.getElementsByClassName('container1')[2].style.display = 'none';
    }
    if(remove==4){
        document.getElementsByClassName('container1')[1].style.display = 'none';
        document.getElementsByClassName('container1')[2].style.display = 'none';
    }
    if(remove==5){
        document.getElementsByClassName('container1')[0].style.display = 'none';
        document.getElementsByClassName('container1')[1].style.display = 'none';
    }

    if(pass_status=='True'){
        var status = 'Status : PASS';
        document.getElementById("result1").innerHTML =  status ;
        document.getElementById("result2").innerHTML =  status ;
        document.getElementById("result3").innerHTML =  status ;
    }
    else{
        document.getElementById("result1").innerHTML =  status ;
        document.getElementById("result2").innerHTML =  status ;
        document.getElementById("result3").innerHTML =  status ;
    }
}
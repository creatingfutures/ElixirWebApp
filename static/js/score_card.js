function show(result,remove,status,pass_status)
{
    if(remove == 11){
        document.getElementsByClassName('container1')[0].style.display = 'none';
    }
    if(remove==1){
        document.getElementsByClassName('container1')[1].style.display = 'none';
    }
    if(pass_status=='True'){
        var status = 'Status : PASS';
        document.getElementById("result1").innerHTML =  status ;
        document.getElementById("result2").innerHTML =  status ;
    }
    else{
        document.getElementById("result1").innerHTML =  status ;
        document.getElementById("result2").innerHTML =  status ;
    }
}
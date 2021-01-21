//1,11,10
function show(result,remove,status,pass_status)
{
    console.log(question_type);
    if(question_type == "Word search"){
        document.getElementsByClassName('container1')[0].style.display = 'none';
        document.getElementsByClassName('container1')[2].style.display = 'none';
    }
    if(question_type== "Match the following"){
        document.getElementsByClassName('container1')[1].style.display = 'none';
        document.getElementsByClassName('container1')[2].style.display = 'none';
    }
    if(question_type=="Crossword"){
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
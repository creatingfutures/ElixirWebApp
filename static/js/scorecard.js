// m0,w1,c2
function show(result,remove,status,pass_status,question_type)

{
    if(question_type == 'word search'){
        document.getElementsByClassName('container1')[0].style.display = 'none';
        document.getElementsByClassName('container1')[2].style.display = 'none';
    }
    if(question_type== 'match the following' ){
        document.getElementsByClassName('container1')[1].style.display = 'none';
        document.getElementsByClassName('container1')[2].style.display = 'none';
    }
    if(question_type=='crossword' ){
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
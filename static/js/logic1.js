var score = 0
myfun = {
    res: function (ans) {
        var er = 0;
        var len = ans.length;
        console.log(len);
        var num = [];
        for (i = 1, j = 0; i <= len; i++, j++) {
            if (document.getElementById("r" + i).value == "") {
                ++er;
            }
            else {
                num[j] = document.getElementById("r" + i).value;
            }

        }
        if (er != 0) {
            if(time <= 0)alert("Time up!");
            else
            alert("Please fill all the answers");
         for (i = 1; i <= len; i++) {
                if (document.getElementById("r" + i).value == "") {
                    document.getElementById("r" + i).style.borderColor = "red";
                }
            }
            return;
        }
        var count = 0;
        for (i = 0; i < len; i++) {
            if (num[i] == ans[i]) {
                ++count;
            }
        }
        var res1;
        if (count == len) {
            res1 = "Correct Answer!"
            document.getElementById("demo").innerHTML = '<font style="color:black">' + res1  + '</font>';
            score = 1;
            return score;
            

        }
        else {
            res1 = "Wrong Answer!";
            document.getElementById("demo").innerHTML = '<font style="color:red">' + res1 + '</font>';
            score = 0;
            return score;
        }
        
    }
}

console.log('hi');


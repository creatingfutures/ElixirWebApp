var currentTextInput;
var puzzleArrayData;
//Loads the Crossword
function initializeScreen(questions,across_or_down){
	var puzzleTable = document.getElementById("puzzle");
	puzzleArrayData = preparePuzzleArray();
	for ( var i = 0; i < puzzleArrayData.length ; i++ ) {
		var row = puzzleTable.insertRow(-1);
		var rowData = puzzleArrayData[i];
		for(var j = 0 ; j < rowData.length ; j++){
			var cell = row.insertCell(-1);
			if(rowData[j] != 0){
				var txtID = String('txt' + '_' +i+'_'+j);
				//console.log(txtID);
				cell.innerHTML = '<input type="text" onClick="setCurrent(this);" class="inputBox" maxlength="1" style="text-transform: lowercase" ' + 'id="' + txtID + '" onfocus="textInputFocus(' + "'" + txtID + "'"+ ')">';
			}else{
				cell.style.backgroundColor  = "black";
			}
		}
	}
	
	addHint();
	clueClicked(questions,across_or_down);	
	//if(window.check_clue==0){show_words();}	
}

window.check_clue = 0;
var col = 13; //number of 'cells' in a row
var current;
var score;
var next;
document.onkeydown = check;
function movement(current,col,direction){
	var token = current.split("_");
	var row = token[1];
	var column = token[2];
	if(direction=='up'){
		row = row-1;
		return 'txt'+'_'+row+'_'+column;
	}
	if(direction=='down'){
		row = parseInt(row)+1;
		//console.log(row);
		return 'txt'+'_'+row+'_'+column;
	}
	if(direction=='left'){
		column = column-1;
		return 'txt'+'_'+row+'_'+column;
	}
	if(direction=='right'){
		column = parseInt(column)+1;
		//console.log(column);
		return 'txt'+'_'+row+'_'+column;
	}
}
function check(e){
	if (!e) var e = window.event;
		(e.keyCode) ? key = e.keyCode : key = e.which;
	var num = document.getElementsByTagName("input").length;
	try{
		switch(key){
			case 37: next = movement(current,col,'left'); break; 		//left
			case 38: next = movement(current,col,'up'); break; 		//up
			case 39: next = movement(current,col,'right'); break; 	//right
			case 40: next = movement(current,col,'down'); break; 	//down
		}
		if (key==37|key==38|key==39|key==40){
			//console.log(current,next);
			var code=document.getElementById(current).value;
			document.getElementById(next).focus();
			current = next;
		}		
	}catch(Exception){}
}
function setCurrent(element){
	var string = element.id;
	current = string.slice(0,string.length);
} 

function clueClicked(questions,across_or_down){
	var table = document.getElementById('wordbox');
	row_length = table.rows.length
	if(row_length==0){
	for(var i=0;i<questions.length;i++){
		var row = table.insertRow(i);
		var cell1 = row.insertCell(0);
		cell1.innerHTML = (i+1)+'.'+'&nbsp'+questions[i]+'&nbsp'+'&nbsp'+'('+'<strong>'+across_or_down[i]+'</strong>'+')';		
		}
	}
}

function answerblueprint(new_cells_allowed,answers,across_or_down){
	console.log(answers);
	score = checkClicked(new_cells_allowed,answers,across_or_down);
	return score; 
}


function textInputFocus(txtID123){
	currentTextInput = txtID123;
}
function clearAllClicked(questions,across_or_down){
	window.check_clue = 1;
	currentTextInput = '';
	var puzzleTable = document.getElementById("puzzle");
	puzzleTable.innerHTML = '';
    initializeScreen(questions,across_or_down);
}
//Check button
function checkClicked(new_cells_allowed,answers,across_or_down){
	var score = 0;
	console.log('hi prends',answers.length);
	for ( var i = 0; i < puzzleArrayData.length ; i++ ) {
		var rowData = puzzleArrayData[i];
		for(var j = 0 ; j < rowData.length ; j++){
			if(rowData[j] != 0){
				var selectedInputTextElement = document.getElementById('txt' + '_' +i+'_'+j);
				if(selectedInputTextElement.value != puzzleArrayData[i][j]){
					selectedInputTextElement.style.backgroundColor = 'red';
				}else{
					selectedInputTextElement.style.backgroundColor = 'green';
				}
			}
		}
	}

	for(var i=0;i<answers.length;i++)
	{
		var check_answer = '';
		var selectedInputTextElement = '';
		if(across_or_down[i]=='across'){
				for(var k=new_cells_allowed[i][0][1];k<new_cells_allowed[i][0][1]+answers[i].length;k++){
					//console.log(new_cells_allowed[i][0][0],k);
					check_answer = check_answer+ puzzleArrayData[new_cells_allowed[i][0][0]][k];
					selectedInputTextElement = selectedInputTextElement+document.getElementById('txt' + '_' +new_cells_allowed[i][0][0]+'_'+k).value;
				}	
			}	
		if(across_or_down[i]=='down'){
			for(var k=new_cells_allowed[i][0][0];k<new_cells_allowed[i][0][0]+answers[i].length;k++){
				//console.log(k,new_cells_allowed[i][0][1]);
				check_answer = check_answer+ puzzleArrayData[k][new_cells_allowed[i][0][1]];
				selectedInputTextElement = selectedInputTextElement+document.getElementById('txt' + '_' +k+'_'+new_cells_allowed[i][0][1]).value;
			}
		}
		//console.log(check_answer,selectedInputTextElement)
		if(check_answer==selectedInputTextElement){
			score = score+1;
		}
	}

	if(across_or_down.length == score){
		score = 1;	
	}
	else{
		score = 0
	}
	return score;
}
		

//Clue Button


/*

clueClicked

if (currentTextInput != null){
		var temp1 = currentTextInput;
		var token = temp1.split("_");
		var row = token[1];
		var column = token[2];
		document.getElementById(temp1).value = puzzleArrayData[row][column];
	}

for ( var i = 0; i < puzzleArrayData.length ; i++ ) {
		var rowData = puzzleArrayData[i];
		for(var j = 0 ; j < rowData.length ; j++){
			if(rowData[j] != 0){
				var selectedInputTextElement = document.getElementById('txt' + '_' +i+'_'+j);
				if(selectedInputTextElement.value != puzzleArrayData[i][j]){
					selectedInputTextElement.style.backgroundColor = 'red';
				}else{
					selectedInputTextElement.style.backgroundColor = 'green';
				}
			}
		}
	}

for(var i=0;i<answers.length;i++){
		var check_answer = '';
		var selectedInputTextElement = '';
		for(var j=new_cells_allowed[0][0][0];j<answers[i].length;j++){
			for(var k=new_cells_allowed[0][0][1];k<answers[i].length;k++){
				check_answer = check_answer+puzzleArrayData[j][k];
				selectedInputTextElement = selectedInputTextElement+document.getElementById('txt' + '_' +j+'_'+k);
			}	
		}
	console.log(check_answer,selectedInputTextElement);
	if(check_answer==selectedInputTextElement)
	{
		score = score+1;
		console.log(score);
	}
	}
	*/ 
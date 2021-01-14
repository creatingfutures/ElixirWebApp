var currentTextInput;
var puzzleArrayData;
//Loads the Crossword
function initializeScreen(){
	var puzzleTable = document.getElementById("puzzle");
	puzzleArrayData = preparePuzzleArray();
    
	for ( var i = 0; i < puzzleArrayData.length ; i++ ) {
		var row = puzzleTable.insertRow(-1);
		var rowData = puzzleArrayData[i];
		for(var j = 0 ; j < rowData.length ; j++){
			var cell = row.insertCell(-1);
			if(rowData[j] != 0){
				var txtID = String('txt' + '_' + i + '_' + j);
				cell.innerHTML = '<input type="text" class="inputBox" maxlength="1" style="text-transform: lowercase" ' + 'id="' + txtID + '" onfocus="textInputFocus(' + "'" + txtID + "'"+ ')">';
			}else{
				cell.style.backgroundColor  = "black";
			}
		}
	}
	addHint();
}
function textInputFocus(txtID123){
	currentTextInput = txtID123;
}
function clearAllClicked(){
	currentTextInput = '';
	var puzzleTable = document.getElementById("puzzle");
	puzzleTable.innerHTML = '';
    initializeScreen();
}
//Check button
function checkClicked(){
    
	for ( var i = 0; i < puzzleArrayData.length ; i++ ) {
		var rowData = puzzleArrayData[i];
		for(var j = 0 ; j < rowData.length ; j++){
			if(rowData[j] != 0){
				var selectedInputTextElement = document.getElementById('txt' + '_' + i + '_' + j);
				if(selectedInputTextElement.value != puzzleArrayData[i][j]){
					selectedInputTextElement.style.backgroundColor = 'red';

				}else{
					selectedInputTextElement.style.backgroundColor = 'green';
				}
			}
		}
	}
}
//Clue Button
function clueClicked(){
    
    	if (currentTextInput != null){
		var temp1 = currentTextInput;
        
		var token = temp1.split("_");
		var row = token[1];
		var column = token[2];
		document.getElementById(temp1).value = puzzleArrayData[row][column];
        
		//checkClicked();
	}
}

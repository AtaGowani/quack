var globalv;

function check(){
	var answer = document.getElementById('answer').value.toLowerCase();
	if (answer == globalv){
		document.getElementById("feedback").innerHTML = 'Correct!'
		var x = background();
		setInterval(function normal() {
		document.getElementById("feedback").innerHTML = '';
		}, 1000);
	}
	else{
		document.getElementById("feedback").innerHTML = 'Try Again!'
		setInterval(function normal() {
		document.getElementById("feedback").innerHTML = '';
		}, 5000);
	}
}

function normal() {
	document.getElementById("feedback").innerHTML = '';
}
	
function background(){
	var char = 'abcdefghijklmnopqrstuvwxyz';

   	var randomChar = char[Math.floor(Math.random() * char.length)];
   	globalv = randomChar;
    document.getElementById("myPicture").style.background = "url(" + "asl/" + randomChar + ".gif" + ") no-repeat";

    $(document).ready(function(){
    $('submit').keypress(function(e){
      if(e.keyCode==13)
      $('submit').click();
    });
});


}
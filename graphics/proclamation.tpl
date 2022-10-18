% rebase("graphics/base.tpl")
	<style>
		div {
			width: 100%;
			text-align: center;
			font-size: 10vw;
			color: rgb(255, 255, 255);
			justify-content: center;
			position: global;
			top: 50%;
			left: 50%;
		}
	</style>
	
	<div id="proclamation"></div>
	
	<script>
		/*Dobim spremenljivko v katero bi rada vpisovala tekst.*/
		var proclamation = document.getElementById('proclamation');
		
		/*S pomočjo rezultata dobim tekst, ki bi ga rada prikazala.*/
		var result = "";
		if({{zmage_runde1}} > {{zmage_runde2}})result = "You won!";
		else if({{zmage_runde1}} < {{zmage_runde2}})result = "You lost!";
		else result = "It's a draw!";
		
		/*Na strani prikažem ta tekst.*/
		proclamation.innerHTML = result;
		
		/*Po sekundi in pol kličem funkcijo reset_game.*/
		setTimeout(reset_game, 1500);
		
		function reset_game(){
			/*Funkcija stran preusmeri na originalno stran.*/
			let form = document.createElement('form');
			
			form.action = '/';
			form.method = 'GET';
			
			document.body.append(form);
			
			form.submit();
		}
	</script>
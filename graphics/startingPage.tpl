% rebase("graphics/base.tpl")
	
	<style>
	blockquote {
		text-align: center;
		font-size: 1vw;
	}
	
	.images-container {
		width: 100%;
		display: flex;
		justify-content: center;
	}
	
	.images-container img {
		margin-left: 5px;
		margin-right: 5px;
		width: 14%;
		height: 14%;
	}
	
	.new_game_button {
		position: absolute;
		width: 5%;
		height: 3%;
		top: 60%;
		left: 80%;
	}
	.replay_button {
		position: absolute;
		width: 5%;
		height: 3%;
		top:60%;
		left: 72%;
	}
	</style>
	
	<div class="images-container">
		<img src="/images/rock.png">
		<img src="/images/paper.png">
		<img src="/images/scissors.png">
		<img src="/images/lizard.png">
		<img src="/images/spock.png">
	</div>
	
	<blockquote>
	"Scissors cuts Paper, Paper covers Rock, Rock crushes Lizard, <br>
	Lizard poisons Spock, Spock smashes Scissors, Scissors decapitates Lizard, <br>
	Lizard eats Paper, Paper disproves Spock, Spock vaporizes Rock, <br>
	(and as it always has) Rock crushes Scissors." <br><br>
	<small>- Dr. Sheldon Lee Cooper, B.S., M.S., M.A., Ph.D., Sc.D..</small>
	</blockquote>

	<form action="/nova_igra/" method="post">
		<button class="new_game_button" type="submit">New Game</button>
	</form>
	<form action="/do_konca/" method="post">
		<button class="replay_button" type="submit" id="replay">Continue</button>
	</form>
	
	<script>
		/*Nastavim, ali je gumb za nadaljevanje prejšnje igre viden ali ne s pomočjo poslane spremenljivke.*/
		if("{{lahko_nadaljuje}}" == "False"){
			document.getElementById("replay").style.display="none";
		}
	</script>
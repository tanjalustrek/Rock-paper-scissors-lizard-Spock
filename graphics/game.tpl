% rebase("graphics/base.tpl")
	<style>
	
	.images-container {
		width: 99%;
		height: 60%;
		display: flex;
		position: absolute;
	}
	.images-container img {
		position: absolute;
		width: 14%;
		height: auto;
	}
	.images-container button {
		position: absolute;
		border: none;
		border-radius: 50%;
		width: 14%;
		height: 46.2%;
	}
	.images-container span {
		position: absolute;
		color: rgb(255, 255, 255);
		text-align: center;
	}
	
	.rock {left: 43%; top: 0%;}
	.paper {left: 60%; top: 37%;}
	.scissors {left: 53%; top: 100%;}
	.lizard {left: 32%; top: 100%;}
	.spock {left: 26%; top: 37%;}
	.counter {left: 48%; top: 55%; font-size: 10vw;}
	.num_of_rounds {left: 70%; top: 5%; font-size: 3vw;}
	.num_of_games {left: 70%; top: 15%; font-size: 3vw;}
	
	.NORMALEN {background-color: rgb(0, 0, 0, 0);}
	.IZBRAN {background-color: rgb(255, 255, 0, 0.5);}
	.NI_NA_VOLJO {background-color: rgb(180, 180, 180, 0.5);}
	</style>
	
	<div class="images-container">
		<img src="/images/rock.png" class="rock">
		<img src="/images/paper.png" class="paper">
		<img src="/images/scissors.png" class="scissors">
		<img src="/images/lizard.png" class="lizard">
		<img src="/images/spock.png" class="spock">
		
		<form action="/igra/" method="post" enctype="multipart/form-data" id="form">
			<button type="submit" class="rock {{statusi['rock']}}" name="rock"}></button>
			<button type="submit" class="paper {{statusi['paper']}}" name="paper"}></button>
			<button type="submit" class="scissors {{statusi['scissors']}}" name="scissors"></button>
			<button type="submit" class="lizard {{statusi['lizard']}}" name="lizard"></button>
			<button type="submit" class="spock {{statusi['spock']}}" name="spock"></button>
		</form>
		
		<span class="num_of_rounds">Round: {{trenutna_runda}}/{{stevilo_rund}}    {{zmage_runde1}}:{{zmage_runde2}}</span>
		<span class="num_of_games">Game: {{trenutna_igra}}/{{stevilo_iger}}    {{zmage_igre1}}:{{zmage_igre2}}</span>
		<span id="counter" class="counter">{{zacetni_prikaz}}</span>
	</div>
	
	<script>
		/*Dobim vse spremenljivke, ki jih uporabljam za pravilen prikaz igre.*/
		let buttons = document.getElementById('form').children;
		let counter = document.getElementById('counter');
		let time = {{preostali_cas}};
		
		/*Začnem ponovljiv klic metode update_counter na vsakih deset milisekund.*/
		timer = setInterval(update_counter, 10);
		
		function update_counter(){
			/*Preostali čas zmanjšam za deset milisekund, oziroma 0.01 sekunde.*/
			time -= 0.01;
			
			
			if(time <= 0){
				/*Če je čas manjši ali enak nič, končam ponovni klic funkcije in kličem funkcijo show_winner.*/
				show_winner();
				clearInterval(timer);
			} else {
				/*Če ima igralec še čas za izbiro, spremenim vrednost value vseh gumbov na preostali čas.*/
				/*Tako lahko z vsakim pritiskom gumba ugovotovim, koliko časa ima igralec še na voljo za izbiro.*/
				for(const child of buttons){
					child.setAttribute("value", time);
				}
				
				/*Izpis števca na sredini strani nastavim na navzgor zaokroženo vrednost preostalega časa.*/
				counter.innerHTML = Math.ceil(time);
			}
		}
		
		function show_winner(){
			/*Funkcija stran preusmeri na /prikazi_zmagovalca/*/
			let form = document.createElement('form');
			
			form.action = '/prikazi_zmagovalca/';
			form.method = 'GET';
			
			document.body.append(form);
			
			form.submit();
		}
	</script>
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
		
		.result {
			left: 50%;
			text-align: center;
			width: 100vw;
			font-size: 5vw;
			color: rgb(255, 255, 255);
		}
		.first_player {
			left: 23%;
			top: 50%;
		}
		.second_player {
			left: 63%;
			top: 50%;
		}
	</style>
	
	<div class="images-container">
		<img src="/images/{{prvi_igralec}}.png" class="first_player" id="first_player">
		<img src="/images/{{drugi_igralec}}.png" class="second_player" id="second_player">
		
		<div class="result" id="izpis"></div>
	</div>
	
	<script>
		/*Dobim vse spremenljivke, ki jih uporabim za prikaz izbir igralca in računalnika.*/
		var slika_prvi = document.getElementById('first_player');
		var slika_drugi = document.getElementById('second_player');
		
		/*Dobim vse spremenljivke, ki jih potrebujem za prikaz premikov slik izbir.*/
		var linearni_odmik = 0;
		var linearni_pospesek = 0.1;
		
		var zguba;
		var vektorska_pozicija_x;
		var vektorska_pozicija_y = 50;
		var vektorska_hitrost_x;
		var vektorska_hitrost_y = Math.random() - 0.5;
		var vektorski_pospesek = 0.95;
		
		/*Ker so vrednosti spremenljivk za prikaz odvisne od rezultata, jih nastavim glede na le tega.*/
		switch({{rezultat}}){
			case -1:
				/*Nastavim, da je zguba prva slika, ter hitrost_x nastavim na negativno, pozicijo pa na originalno pozicijo slike.*/
				/*To naredim, ker se mora slika premakniti levo in od svoje originalne pozicije.*/
				zguba = slika_prvi;
				vektorska_hitrost_x = -1.8;
				vektorska_pozicija_x = 35.5;
				break;
			case 1:
				/*Podobno naredim, če je zguba druga slika, samo da je hitrost_x pozitivna in da je druga tudi originalna pozicija.*/
				zguba = slika_drugi;
				vektorska_hitrost_x = 1.8;
				vektorska_pozicija_x = 50.5;
				break;
			case 0:
				/*Če ne zmaga nihče zgubo nastavim na null.*/
				zguba = null;
		}
		
		/*Začnem ponovljiv klic metode zacetni_premik na vsakih deset milisekund.*/
		var timer = setInterval(zacetni_premik, 10);
		
		function zacetni_premik(){
			/*Vrednosti, ki opisuje odmik, ki ga je slika naredila od originalne pozicije, prištejem pospesek (v resnici hitrost).*/
			linearni_odmik += linearni_pospesek;
			/*Nato tej spremenljivki dodam neko vrednost da slika čez čas pospešuje.*/
			linearni_pospesek += 0.01;
			
			/*Nastavim pozicijo slik glede na izračunani odmik.*/
			slika_prvi.style.left = 8 + linearni_odmik + "%";
			slika_drugi.style.left = 78 - linearni_odmik + "%";
			
			/*Ko odmik preseže neko vrednost, prekinem ponovljiv klic te funkcije in ocenim kaj mora program še narediti.*/
			if((8 + linearni_odmik) >= 35.5){
				clearInterval(timer);
				
				if({{rezultat}} == 0){
					/*Če ni zmagal nihče, na strani to tudi izpišem in po eni sekundi direktno kličem funkcijo zakljuci_prikaz.*/
					document.getElementById('izpis').innerHTML = "Draw";
					setTimeout(zakljuci_prikaz, 1000);
				} else {
					/*Če je nekdo zmagal sestavim izpis iz izbir igralca in računalnika ter rezultata.*/
					var izpis;
					
					var prvi_igralec = "{{prvi_igralec}}";
					var drugi_igralec = "{{drugi_igralec}}";
					
					/*Izbiro, ki je beseda iz samo malih črk, spremenim v besedo s veliko začetnico.*/
					prvi_igralec = prvi_igralec[0].toUpperCase() + prvi_igralec.slice(1);
					drugi_igralec = drugi_igralec[0].toUpperCase() + drugi_igralec.slice(1);
					
					/*Vrstni red besed je odvisen od tega kdo je zmagal (npr. namesto Scissors beats Rock želim Rock beats Scissors).*/
					if({{rezultat}} == 1){
						izpis = prvi_igralec+ " beats " + drugi_igralec; 
					} else {
						izpis = drugi_igralec + " beats " + prvi_igralec;
					}
					
					/*Na strani izpišem izpis in začnem še ponovljiv klic funkcije koncni_premik na vsake deset milisekund.*/
					document.getElementById('izpis').innerHTML = izpis;
					timer = setInterval(koncni_premik, 10);
				}
			}
		}
		
		function koncni_premik(){
			/*Prvo pomnožim hitrosti s pospeškom, ki je vrednost med nič in ena, da se hitrost eksponentno zmanjšuje.*/
			vektorska_hitrost_x *= vektorski_pospesek;
			vektorska_hitrost_y *= vektorski_pospesek;
			
			/*Nato poziciji prištejem hitrost in pozicijo zgube nastavim na novo izračunano pozicijo.*/
			vektorska_pozicija_x += vektorska_hitrost_x;
			vektorska_pozicija_y += vektorska_hitrost_y;
			zguba.style.left = vektorska_pozicija_x + "%";
			zguba.style.top = vektorska_pozicija_y + "%";
			
			/*Ko je hitrost_x manjša od neke količine, prekinem ponovljiv klic te funkcije in po osemstotih milisekundah kličem funkcijo zakljuci_prikaz.*/
			if(Math.abs(vektorska_hitrost_x) <= 0.1){
				clearInterval(timer);
				setTimeout(zakljuci_prikaz, 800);
			}
		}
		
		function zakljuci_prikaz(){
			/*Funkcija pošlje v program, da bi rada zaključila prikaz, kjer program spremeni vrednosti igre, preden preusmeri naprej.*/
			let form = document.createElement('form');
			
			form.action = '/zakljuci_prikaz/';
			form.method = 'POST';
			
			document.body.append(form);
			
			form.submit();
		}
		</script>
import json
import os
import io
import igra

datoteka = "stanje.json"

#Preveri če datoteka obstaja in če je berljiva. Če karkoli od tega ni, naredi novo datoteko v katero zapiše osnovni zapis {}.
def preveri_datoteko():
    global datoteka

    if not (os.path.isfile(datoteka) and os.access(datoteka, os.R_OK)):
        with io.open(datoteka, "w") as nova_datoteka:
            nova_datoteka.write(json.dumps({}))

#Vrne zadnjo igro, prebrano iz datoteke, kot nov objekt tipa Igra.
def vrni_zadnjo_igro():
    prebrano = open(datoteka)
    vrednosti = json.load(prebrano)

    #Če je datoteka prazna zadnja igra ne mora obstajati, zato vrne None.
    if len(vrednosti) == 0:
        return None
    
    zadnji_indeks = len(vrednosti) - 1
    zadnja_igra = vrednosti[str(zadnji_indeks)]
    zadnja_igra = igra.Igra(zadnji_indeks, zadnja_igra)
    return zadnja_igra

#Preveri, če se zadnjo igro da nadaljevati.
def preveri_zadnjo_igro():
    zadnja_igra = vrni_zadnjo_igro()

    #Če zadnja igra ne obstaja, je seveda ne moremo nadaljevati.
    if zadnja_igra == None:
        return False

    #Igre ne moremo nadaljevati, če je igra že zaključena.
    nekdo_zmagal = zadnja_igra.trenutna_runda >= igra.STEVILO_RUND + 1 and zadnja_igra.zmage_runde1 != zadnja_igra.zmage_runde2
    nekdo_zmagal = nekdo_zmagal or zadnja_igra.zmage_runde1 >= igra.STEVILO_RUND / 2
    nekdo_zmagal = nekdo_zmagal or zadnja_igra.zmage_runde2 >= igra.STEVILO_RUND / 2
    presega_maksimalno = zadnja_igra.trenutna_runda >= igra.MAKSIMALNO_RUND + 1
    if nekdo_zmagal or presega_maksimalno:
        return False
    
    return True

#Vrne naslednji ključ v datoteki. Ker so ključi zaporedne številke, lahko preprosto vrnemo število vrednosti, ker se ključi začnejo z 0.
def naslednji_id_igre():
    prebrano = open(datoteka)
    vrednosti = json.load(prebrano)
    return len(vrednosti)

#V datoteko shrani objekt tipa Igra.
def shrani_igro(igra):
    #Shrani vrednosti iz datoteke.
    vrednosti = None
    with open(datoteka, "r") as f:
        vrednosti = json.load(f)
    
    #Spremeni vrednosti iz datoteke. Če id igre obstaja, spremeni njegove lastnosti, če ne naredi nov ključ z idjem igre.
    vrednosti[str(igra.id)] = {
        "trenutna_igra": igra.trenutna_igra,
        "trenutna_runda": igra.trenutna_runda,
        "zmage_igre1": igra.zmage_igre1,
        "zmage_igre2": igra.zmage_igre2,
        "zmage_runde1": igra.zmage_runde1,
        "zmage_runde2": igra.zmage_runde2,
        "izbrani1": igra.izbrani1,
        "izbrani2": igra.izbrani2,
        "statusi": igra.statusi
    }
    
    #Zapiši spremenjene vrednosti.
    with open(datoteka, "w") as f:
        json.dump(vrednosti, f, indent=4)
        
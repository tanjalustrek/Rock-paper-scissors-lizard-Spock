from random import randint
from math import ceil
import bottle
import igra
import shranjevanje

moja_igra = None
preostali_cas = igra.CAS_ZA_IZBIRO
trenutni_izbrani = ""

#Kaj naj se prikaže na osnovni strani.
@bottle.get("/")
def index():
    #Preverim datoteko.
    shranjevanje.preveri_datoteko()

    #Preverim, če lahko nadaljujem zadnjo igro.
    lahko_nadaljuje = shranjevanje.preveri_zadnjo_igro()

    #Prikažem prvo stran in do nje pošljem, če igro lahko nadaljujem ali ne (ali naj se prikaže gumb za nadaljevanje igre ali ne).
    return bottle.template("graphics/startingPage.tpl", lahko_nadaljuje=lahko_nadaljuje)

#Kaj naj se zgodi, če igralec želi odigrati novo igro.
@bottle.post("/nova_igra/")
def nova_igra():
    #Kreiram novo igro in jo shranim, če igralec pred prvo izbiro prekine povezavo do strežnika.
    global moja_igra
    moja_igra = igra.Igra(shranjevanje.naslednji_id_igre())
    shranjevanje.shrani_igro(moja_igra)

    #Prikažem stran za igro.
    bottle.redirect("/igra/")

#Kaj naj se zgodi, če igralec želi zadnjo igro odigrati do konca.
@bottle.post("/do_konca/")
def nalozi_prejsnjo():
    #Mojo igro nastavim na zadnjo igro in jo preprosto odigram do konca.
    global moja_igra
    moja_igra = shranjevanje.vrni_zadnjo_igro()
    bottle.redirect("/igra/")

#Kaj naj se prikaže, ko igralec igra igro.
@bottle.get("/igra/")
def pokazi_igro():
    #Prikažem stran za igro in do nje pošljem vse spremenljivke, ki so potrebne za pravilni prikaz igre.
    global moja_igra
    return bottle.template(
        "graphics/game.tpl",
        statusi=moja_igra.statusi,
        trenutna_runda=moja_igra.trenutna_runda,
        trenutna_igra=moja_igra.trenutna_igra,
        preostali_cas=preostali_cas,
        zacetni_prikaz=ceil(preostali_cas),
        stevilo_rund=igra.STEVILO_RUND,
        stevilo_iger=igra.STEVILO_IGER_V_RUNDI,
        zmage_igre1=moja_igra.zmage_igre1,
        zmage_igre2=moja_igra.zmage_igre2,
        zmage_runde1=moja_igra.zmage_runde1,
        zmage_runde2=moja_igra.zmage_runde2
    )

#Kaj naj se zgodi, ko program želi končati prikaz rezultata med izbirami.
@bottle.post("/zakljuci_prikaz/")
def zakljuci_prikaz():
    global moja_igra
    global trenutni_izbrani

    #Izbrani gumb označim kot uporabljenega (ga ni mogoče več izbrati), izbiro ponastavim na nič in števec igre povečam za ena.
    moja_igra.statusi[trenutni_izbrani] = "NI_NA_VOLJO"
    trenutni_izbrani = ""
    moja_igra.trenutna_igra = moja_igra.trenutna_igra + 1

    #Shranim igro, ker je možno, da se trenutna runda še ni končala.
    shranjevanje.shrani_igro(moja_igra)

    #Preverim, če je nekdo zmagal že toliko iger da drugi ne more več zmagati, tudi če zmaga vse od zdaj naprej.
    logicna_zmaga_iger = moja_igra.zmage_igre1 >= igra.STEVILO_IGER_V_RUNDI / 2
    logicna_zmaga_iger = logicna_zmaga_iger or moja_igra.zmage_igre2 >= igra.STEVILO_IGER_V_RUNDI / 2

    if moja_igra.trenutna_igra >= igra.STEVILO_IGER_V_RUNDI + 1 or logicna_zmaga_iger:
        #Če se je runda končala, preverim če je kdo zmagal in to shranim.
        if(moja_igra.zmage_igre1 > moja_igra.zmage_igre2):
            moja_igra.zmage_runde1 = moja_igra.zmage_runde1 + 1
        elif(moja_igra.zmage_igre2 > moja_igra.zmage_igre1):
            moja_igra.zmage_runde2 = moja_igra.zmage_runde2 + 1
        
        #Resetiram spremenljivke, ki jih uporabljam za igranje posamezne runde.
        moja_igra.trenutna_igra = 1
        moja_igra.zmage_igre1 = 0
        moja_igra.zmage_igre2 = 0
        moja_igra.izbrani1 = []
        moja_igra.izbrani2 = []

        for kljuc in moja_igra.statusi:
            moja_igra.statusi[kljuc] = "NORMALEN"

        #Povečam število rund in shranim igro
        moja_igra.trenutna_runda = moja_igra.trenutna_runda + 1
        shranjevanje.shrani_igro(moja_igra)

        #Če je nekdo že zmagal, ali pa če je število rund večje od maksimalnega števila rund, prikažemo rezultate igre.
        nekdo_zmagal = moja_igra.trenutna_runda >= igra.STEVILO_RUND + 1 and moja_igra.zmage_runde1 != moja_igra.zmage_runde2
        nekdo_zmagal = nekdo_zmagal or moja_igra.zmage_runde1 >= igra.STEVILO_RUND / 2
        nekdo_zmagal = nekdo_zmagal or moja_igra.zmage_runde2 >= igra.STEVILO_RUND / 2
        presega_maksimalno = moja_igra.trenutna_runda >= igra.MAKSIMALNO_RUND + 1
        if nekdo_zmagal or presega_maksimalno:
            bottle.redirect("/razglasi_konec/")

    #Če se igra še ni končala jo nadaljujemo.
    bottle.redirect("/igra/")

#Kaj naj se prikaže ob razglasitvi konca.
@bottle.get("/razglasi_konec/")
def razglasi_konec():
    #Prikažemo stran za razglasitev in do nje pošljemo zmage rund igralca in računalnika.
    return bottle.template("graphics/proclamation.tpl", zmage_runde1=moja_igra.zmage_runde1, zmage_runde2=moja_igra.zmage_runde2)

#Kaj naj se prikaže, ko program želi prikazati kdo je zmagal igro.
@bottle.get("/prikazi_zmagovalca/")
def prikazi_zmagovalca():
    global preostali_cas
    global trenutni_izbrani
    global moja_igra

    #Preostali čas za izbiro nastavimo na originalnega.
    preostali_cas = igra.CAS_ZA_IZBIRO

    #Zagotovimo, da igralčeva izbira ni prazna (če je jo nastavimo na naključno iz še možnih).
    if trenutni_izbrani == "":
        trenutni_izbrani = nakljucni_normalni(moja_igra.statusi)

    #Ugotovimo kakšno izbiro je izbral računalnik in rezultat med izbirami igralca in računalnika.
    prvi_igralec = trenutni_izbrani
    drugi_igralec = igra.predvidevaj(moja_igra)
    rezultat = igra.oceniIzbora(prvi_igralec, drugi_igralec)

    #V igro shranimo izbire igralca in računalnika.
    moja_igra.izbrani1.append(prvi_igralec)
    moja_igra.izbrani2.append(drugi_igralec)

    #Preverimo, če je kdo zmagal in spremenimo število zmag zmagovalca.
    if rezultat == 1:
        moja_igra.zmage_igre1 = moja_igra.zmage_igre1 + 1
    elif(rezultat == -1):
        moja_igra.zmage_igre2 = moja_igra.zmage_igre2 + 1

    #Ponovno shranimo igro.
    shranjevanje.shrani_igro(moja_igra)

    #Prikažemo stran za prikaz zmagovalca in do nje pošljemo izbiri igralca in računalnika ter rezultat njunih izbir.
    return bottle.template("graphics/showWinner.tpl", prvi_igralec=prvi_igralec, drugi_igralec=drugi_igralec, rezultat=rezultat)

#Kaj naj se zgodi, ko program želi poslati, kaj se je zgodilo v igri (ko igralec pritisne na gumb).
@bottle.post("/igra/")
def spremeni_izbor():
    forms = bottle.request.forms
    global trenutni_izbrani
    global preostali_cas
    izbrani_status = ""

    #Preverimo kateri gumb je igralec pritisnil in vrednost izbrani_status nastavimo nanj.
    #Kateri gumb je igralec pritisnil ugotovimo tako, da probavamo dobiti vrednost vseh gumbov, saj bo vrednost vrnil le tisti, ki je originalno klical funkcijo.
    for kljuc in moja_igra.statusi:
        if forms.get(kljuc) != None:
            izbrani_status = kljuc
            preostali_cas = float(forms.get(kljuc))
            break
    
    #Če je igralec pritisnil na gumb, katerega je možno izbrati, ga nastavimo za izbranega.
    if moja_igra.statusi[izbrani_status] == "NORMALEN":
        moja_igra.statusi[izbrani_status] = "IZBRAN"

        #Če je prej že bil kakšen gumb izbran, ga nastavimo nazaj na možnega za izbiro, predenj trenutnega izbranega nastavimo na novega izbranega.
        if trenutni_izbrani != "":
            moja_igra.statusi[trenutni_izbrani] = "NORMALEN"
        trenutni_izbrani = izbrani_status
    
    #Ponovno prikažemo stran za igro, vendar je zdaj izbran drug gumb.
    bottle.redirect("/igra/")

#Kako naj stran dobi željeno sliko.
@bottle.get("/images/<picture>")
def serve_picture(picture):
    return bottle.static_file(picture, root="images")

#Funkcija, ki vrne naključno normalno vrednost iz poslanega izbora.
def nakljucni_normalni(izbor):
    mozni = []

    for kljuc in izbor:
        if izbor[kljuc] == "NORMALEN":
            mozni.append(kljuc)
    
    return mozni[randint(0, len(mozni)-1)]

#Zagon strežnika.
if __name__ == "__main__":
    bottle.run(reloader=True, debug=True)
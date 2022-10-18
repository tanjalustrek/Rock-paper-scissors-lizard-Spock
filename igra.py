from random import randint

STEVILO_RUND = 5
MAKSIMALNO_RUND = 10
STEVILO_IGER_V_RUNDI = 3
CAS_ZA_IZBIRO = 7

#Definirani razred Igra. Vsebuje vse spremenljivke, ki so potrebne za pravilni prikaz igre.
class Igra:
    #Igro se lahko kreira z vnaprej določenimi vrednostmi, ali pa se jo kreira s spremenljivkami iz dictionaryja (če bi jo radi kreirali iz datoteke za shranjevanje).
    def __init__(self, id, dict=None):
        self.id = id
        if dict == None:
            self.trenutna_igra = 1
            self.trenutna_runda = 1
            self.zmage_igre1 = 0
            self.zmage_igre2 = 0
            self.zmage_runde1 = 0
            self.zmage_runde2 = 0
            self.izbrani1 = []
            self.izbrani2 = []
            self.statusi = {
                "rock": "NORMALEN",
                "paper": "NORMALEN",
                "scissors": "NORMALEN",
                "lizard": "NORMALEN",
                "spock": "NORMALEN"
            }
        else:
            self.trenutna_igra = dict["trenutna_igra"]
            self.trenutna_runda = dict["trenutna_runda"]
            self.zmage_igre1 = dict["zmage_igre1"]
            self.zmage_igre2 = dict["zmage_igre2"]
            self.zmage_runde1 = dict["zmage_runde1"]
            self.zmage_runde2 = dict["zmage_runde2"]
            self.izbrani1 = dict["izbrani1"]
            self.izbrani2 = dict["izbrani2"]
            self.statusi = dict["statusi"]

#Funkcija, ki iz izborov ugotovi kdo zmaga, in vrne številko glede na rezultat (1 za igralca, -1 za računalnik in 0 za neizenačeno).
def oceniIzbora(izbor1, izbor2):
    if izbor1 == izbor2:
        return 0
    if izbor1 == "rock" and (izbor2 == "scissors" or izbor2 == "lizard"):
        return 1
    if izbor1 == "paper" and (izbor2 == "rock" or izbor2 == "spock"):
        return 1
    if izbor1 == "scissors" and (izbor2 == "paper" or izbor2 == "lizard"):
        return 1
    if izbor1 == "lizard" and (izbor2 == "paper" or izbor2 == "spock"):
        return 1
    if izbor1 == "spock" and (izbor2 == "rock" or izbor2 == "scissors"):
        return 1
    return -1

#Funkcija, ki predvideva najboljši možni izbor glede na prejšnje izbore igralca in računalnika.
def predvidevaj(igra):
    stevilo_izbir = len(igra.izbrani2)

    match(stevilo_izbir):
        case 0:
            #Vrne naključno izbiro.
            return dobi_zeljenega(igra.izbrani2, ["rock", "paper", "scissors", "lizard", "spock"])
        case 1:
            #Vrne naključno izmed dveh željenih. Če ena ni na voljo, preprosto vrne drugo.
            match(igra.izbrani1[0]):
                case "rock":
                    return dobi_zeljenega(igra.izbrani2, ["scissors", "lizard"])
                case "paper":
                    return dobi_zeljenega(igra.izbrani2, ["rock", "spock"])
                case "scissors":
                    return dobi_zeljenega(igra.izbrani2, ["paper", "lizard"])
                case "lizard":
                    return dobi_zeljenega(igra.izbrani2, ["paper", "spock"])
                case "spock":
                    return dobi_zeljenega(igra.izbrani2, ["rock", "scissors"])
        case 2:
            #Najprej prejšnji izbiri igralca uredi po vrsti, nato preveri katera izbira bi bila glede na njiju najboljša.
            #Prvo preveri bolj željene izbire in izmed njih vrne naključno. Če te niso na voljo, vrne naključno med manj željenimi.
            match(uredi_izbiri(igra.izbrani1)):
                case ["rock", "paper"]:
                    return dobi_zeljenega(igra.izbrani2, ["rock", "paper", "scissors", "spock"])
                
                case ["rock", "scissors"]:
                    zeljeni = dobi_zeljenega(igra.izbrani2, ["lizard"])
                    if zeljeni != None:
                        return zeljeni
                    
                    return dobi_zeljenega(igra.izbrani2, ["paper", "scissors"])
                
                case ["rock", "lizard"]:
                    return dobi_zeljenega(igra.izbrani2, ["paper", "scissors", "lizard", "spock"])
                
                case ["rock", "spock"]:
                    zeljeni = dobi_zeljenega(igra.izbrani2, ["scissors"])
                    if zeljeni != None:
                        return zeljeni
                    
                    return dobi_zeljenega(igra.izbrani2, ["rock", "lizard"])
                
                case ["paper", "scissors"]:
                    return dobi_zeljenega(igra.izbrani2, ["rock", "paper", "lizard", "spock"])
                
                case ["paper", "lizard"]:
                    zeljeni = dobi_zeljenega(igra.izbrani2, ["spock"])
                    if zeljeni != None:
                        return zeljeni
                    
                    return dobi_zeljenega(igra.izbrani2, ["rock", "paper"])
                
                case ["paper", "spock"]:
                    zeljeni = dobi_zeljenega(igra.izbrani2, ["rock"])
                    if zeljeni != None:
                        return zeljeni
                    
                    return dobi_zeljenega(igra.izbrani2, ["scissors", "spock"])
                
                case ["scissors", "lizard"]:
                    zeljeni = dobi_zeljenega(igra.izbrani2, ["paper"])
                    if zeljeni != None:
                        return zeljeni
                    
                    return dobi_zeljenega(igra.izbrani2, ["lizard", "spock"])
                
                case ["scissors", "spock"]:
                    return dobi_zeljenega(igra.izbrani2, ["rock", "paper", "scissors", "lizard"])
                
                case ["lizard", "spock"]:
                    return dobi_zeljenega(igra.izbrani2, ["rock", "paper", "scissors", "spock"])

#Funkcija, ki poskrbi, da sta dve izbiri urejeni po vrsti.      
def uredi_izbiri(izbiri):
    #Vrednosti izbir, da lahko preverimo če sta urejeni po vrsti.
    vrednosti = {
        "rock": 1,
        "paper": 2,
        "scissors": 3,
        "lizard": 4,
        "spock": 5
    }

    vrednost1 = vrednosti[izbiri[0]]
    vrednost2 = vrednosti[izbiri[1]]

    #Če je vrednost druge izbire manjša od prve, ju zamenjamo.
    if vrednost1 > vrednost2:
        temp = izbiri[0]
        izbiri[0] = izbiri[1]
        izbiri[1] = temp
    
    return izbiri

#Funkcija, ki vrne naključen izbor iz željenih izbir. Če so vse že porabljene vrne None.
def dobi_zeljenega(ze_izbrani, zeljeni):
    for izbrani in ze_izbrani:
        if izbrani in zeljeni:
            zeljeni.remove(izbrani)
    
    if len(zeljeni) == 0:
        return None
    
    return zeljeni[randint(0, len(zeljeni)-1)]
import pygame

SEMMI = 0
KICSI = 1
NAGY = 2
INSTANT = 10

SCREEN = (1600, 900)
ELHELYEZKEDESEK={
    "Felso_szakasz_magassag": 120,
    "Also_szakasz_magassag": 150,
    "Kep_meret": 320,
    "Valasztas_ervenyes_tavolsag": 200,
    "Valasz_megjelenitesi_tavolsag": 50,
    "Ikonok_merete": 64,
    "Kartya_gorbulet": 20,
    "kartya_keret_vastagsag": 15,
}

SZINEK={
    "fekete": (0,0,0),
    "sotet_szurke": (30,30,30),
    "feher": (255,255,255),
    "zold": (0,255,0),
    "piros": (255,0,0),
    "papir_normal": (232, 220, 184),
    "papir_sotetebb": (212, 200, 164),
    "papir_sotet": (152, 140, 104),
    "sotet_kek": (0, 20, 120),
    "kek_normal": (0, 140, 200),
    "kek_sotetebb": (0, 120, 180),
    "kek_sotet": (0, 100, 160),
    "vilagos_szurke": (200, 200, 200),
    "nagyon_vilagos_szurke": (230, 230, 230),
    "szurke": (150, 150, 150),
}

TEMA_ALAP={
    "valasz": SZINEK['feher'],
    "parbeszed": SZINEK['fekete'],
    "nev": SZINEK['fekete'],
    "felso_szakasz": SZINEK['fekete'],
    "also_szakasz": SZINEK['sotet_szurke'],
    "datum": SZINEK['feher'],
    "hatter": SZINEK['papir_normal'],
    "keret": SZINEK['papir_sotetebb'],
    "kartya_helye": SZINEK['papir_sotet'],
    "sima_potty": SZINEK['feher'],
    "jo_potty": SZINEK['zold'],
    "rossz_potty": SZINEK['piros'],
}

TEMA_KEK={
    "valasz": SZINEK['feher'],
    "parbeszed": SZINEK['feher'],
    "nev": SZINEK['feher'],
    "felso_szakasz": SZINEK['sotet_kek'],
    "also_szakasz": SZINEK['sotet_kek'],
    "datum": SZINEK['feher'],
    "hatter": SZINEK['kek_normal'],
    "keret": SZINEK['kek_sotetebb'],
    "kartya_helye": SZINEK['kek_sotet'],
    "sima_potty": SZINEK['feher'],
    "jo_potty": SZINEK['zold'],
    "rossz_potty": SZINEK['piros'],
}

TEMA_VILAGOS={
    "valasz": SZINEK['feher'],
    "parbeszed": SZINEK['fekete'],
    "nev": SZINEK['fekete'],
    "felso_szakasz": SZINEK['vilagos_szurke'],
    "also_szakasz": SZINEK['vilagos_szurke'],
    "datum": SZINEK['fekete'],
    "hatter": SZINEK['szurke'],
    "keret": SZINEK['nagyon_vilagos_szurke'],
    "kartya_helye": SZINEK['vilagos_szurke'],
    "sima_potty": SZINEK['feher'],
    "jo_potty": SZINEK['zold'],
    "rossz_potty": SZINEK['piros'],
}

SZINEK_HASZNALATA=TEMA_ALAP



PLAYER_MODE = {
    "Háború": False,
    "Járvány": False,
    "Infláció": False,
    "Radioaktivitás": False,
    "Jós": True,
    "Róka": False,  # Magas gazdaság, vagy magas hadsereg miatti halál megelőzése
    "Szerető": False,  # Alacsony boldogság miatti halál megelőzése
    "Templom": False,  # Alacsony boldogság miatti halál megelőzése
    "Euró": False,  # Alacsony gazdaság miatti halál megelőzése
    "Radar": False,  # Alacsony hadsereg miatti halál megelőzése
    "Atombunker": False  # Alacsony környezet miatti halál megelőzése
}


class Ability:
    def __init__(self, name, place):
        self.img = pygame.image.load(f"../Images/Icons/{name}.webp")
        self.place = place
        self.name = name


class Card:
    def __init__(self, name, parbeszed):
        self.eleres = f"../Images/Charachter/{name}.webp"  # Elérési útvonal
        self.name = name  # Karakter neve
        self.img = pygame.image.load(self.eleres)  # Kép
        self.szovegek = parbeszed


class PlayerStats:
    def __init__(self):
        # Játékos kezdőértékei 0 és 10 között. 5 az alap
        self.kornyezet = 5
        self.boldogsag = 5
        self.hadsereg = 5
        self.gazdasag = 5


Kumiyo_parbeszed = {
            "xyz1": [["Szoszi", "Bal: Gazdaság(+1)", "Jobb: Környezet(-1)"], [0, 0, 0, 1], [-1, 0, 0, 0]],
}
K_parbeszed = {
            "xyz1": [["Szoszi", "Bal: Boldogság(+1)", "Jobb: Hadsereg(+2)"], [0, 1, 0, 0], [0, 0, 2, 0]],
        }
President_Nakato_parbeszed = {
            "xyz1": [["Szoszi", "Bal: Hadsereg(-1)", "Jobb: Környezet(+2)"], [0, 0, -1, 0], [2, 0, 0, 0]],
        }
Crazy_jeffry_parbeszed = {
            "xyz1": [["Szoszi", "Bal: Környezet(-1)", "Jobb: Minden(-2)"], [-1, 0, 0, 0], [-2, -2, -2, -2]],
        }
Governor_Alien_parbeszed = {
            "xyz1": [["Szoszi", "Bal: Környezet(-1)", "Jobb: Minden(-2)"], [-KICSI, SEMMI, SEMMI, SEMMI], [-NAGY, -NAGY, -NAGY, -NAGY]],
        }

Alysha_Hall_parbeszed = {
    "xyz1": [["Édes, nem láttad a házvezetőnőt? Nem lehet igaz, sosem találom sehol amikor szükségem lenne rá. Néha úgy tűnik, mintha szándékosan kerülne engem"], [SEMMI, KICSI, SEMMI, SEMMI, "De láttam"], [SEMMI, SEMMI, KICSI, SEMMI, "Nem láttam"]],
}
Chef_parbeszed = {
            "xyz1": [["A biztonsági tisztje idegesítő, mint ananász a pizzán. Elkobozta az összes késemet"], [SEMMI, KICSI, SEMMI, SEMMI, "Beszélek vele"], [SEMMI, SEMMI, KICSI, SEMMI, "Biztonsági okokból teszi"]],
            "xyz1": [["Az étel amink van, már nem olyan jó, mint régen. Más beszállító után kéne néznünk, még ha drágább is lenne."], [SEMMI, KICSI, SEMMI, -KICSI, "Igen"], [SEMMI, -KICSI, SEMMI, KICSI, "Nem"]],
        }
Father_parbeszed = {
            "xyz1": [["Szoszi", "Bal: Környezet(-1)", "Jobb: Minden(-2)"], [-KICSI, SEMMI, SEMMI, SEMMI], [-NAGY, -NAGY, -NAGY, -NAGY]],
        }
Gardener_parbeszed = {
            "xyz1": [["Egy m-magánvállalat engedélyt kapott arra, hogy kivágjon 70 hektár fát! Ez hogyan l-lehetséges?"], [KICSI, SEMMI, SEMMI, -KICSI, "Valami tévedés történhetett"], [-KICSI, SEMMI, SEMMI, KICSI, "Fizetnek nekünk érte"]],
            "xyz2": [["N-nem hiszem el, még a város k-közepén is lehet érezni a gyárak füstjét. És még a növényeket is t-tönkreteszi. Be kell záratni!"], [KICSI, SEMMI, SEMMI, -KICSI, "Meglátom mit tehetek"], [-KICSI, SEMMI, SEMMI, SEMMI, "A növények kibírják"]],
        }
General_Ramsey_parbeszed = {
            "xyz1": [["A jelenlegi fegyverzetünk nyílt háborúban hasztalan lenne. Kapunk engedélyt nukleáris fegyverkezésre?"], [-NAGY, -KICSI, 2, -KICSI, "Igen"], [SEMMI, KICSI, -KICSI, SEMMI, "Nem"]],
            "xyz2": [["A nyugati országok fegyverkezésbe fektetik a pénzüket. Meg kell támadnunk őket, mielőtt ők támadnak meg minket!"], [SEMMI, -NAGY, -NAGY, SEMMI, "Fegyverbe"], [SEMMI, KICSI, -KICSI, SEMMI, "Nincs ok a pánikra"]],
            "xyz3": [["A kutatási részleg nem teszi a dolgát. Több munkaerőt és erőforrást kell fordítaniuk fegyverekre!"], [SEMMI, SEMMI, KICSI, -NAGY, "Igen"], [SEMMI, SEMMI, -KICSI, KICSI, "Nem"]],
            "xyz4": [["A seregünk gyenge, és a katonáink száma egyre csak fogy. Támogatnunk kéne a fiatalok toborzását."], [SEMMI, SEMMI, KICSI, -KICSI, "Egyetértek"], [SEMMI, KICSI, -KICSI, SEMMI, "Nincs rá szükség"]],
            "xyz5": [["Az emberek boldogtalanok, de a migránsok jó bűnbakok lennének. Őket kellene hibáztatni mindenért."], [SEMMI, KICSI, -KICSI, -KICSI, "Jó ötlet"], [SEMMI, -KICSI, KICSI, SEMMI, "Biztos nem"]],
        }
Gibson_parbeszed = {
            "xyz1": [["A farmokon a tehenek vért adnak tej helyett. Ez az újságokban fog kikötni!"], [-KICSI, SEMMI, SEMMI, -KICSI, "Ne hagyja, hogy ez megtörténjen"], [-KICSI, -NAGY, SEMMI, SEMMI, "Nem érdekel"]],
            "xyz3": [["A tenyészállatok életkörülményei az ország néhány pontján siralmasak. Közbe kellene lépnünk."], [SEMMI, KICSI, -KICSI, -KICSI, "Rendben"], [-KICSI, -KICSI, SEMMI, SEMMI, "Nem"]],
        }
Governor_parbeszed = {
            "xyz1": [["Sürgős hívást kaptunk, tűz ütött ki a városi ligetben. Minden lángokban áll!"], [SEMMI, -NAGY, -KICSI, SEMMI, "Állítsák meg a tüzet"], [SEMMI, SEMMI, -KICSI, -NAGY, "Segítsenek a civileknek"]],
            "xyz2": [["A lakosság elégedetlen, több pénzt követelnek rekreációs lehetőségekre"], [SEMMI, KICSI, SEMMI, SEMMI, "Úgy lesz"], [KICSI, SEMMI, SEMMI, SEMMI, "Felesleges"]],
            "xyz3": [["Falkába verődött kóbor kutyák terrorizálják a lakosokat néhány peremvidéken. Tenni kellene az ügy érdekében"], [SEMMI, KICSI, SEMMI, -KICSI, "Igen"], [-KICSI, -KICSI, SEMMI, KICSI, "Nem"]],
            "xyz4": [["Úgy néz ki, hajléktalanok élnek egy atomerőmű romjai között. Néhányukat eltorzította a sugárzás. Az emberek félnek tőlük"], [-KICSI, -KICSI, -KICSI, SEMMI, "Küldjék el őket"], [SEMMI, -NAGY, SEMMI, SEMMI, "Maradhatnak"]],
            "xyz5": [["Az emberek nem elégedettek a jelenlegi katonai döntéshozatalunkkal. Összeesküvésekről, korrupcióról, és közelgő háborúról beszélnek."], [SEMMI, KICSI, -KICSI, -KICSI, "Változtatunk a terveinken"], [SEMMI, -NAGY, KICSI, SEMMI, "Pletykáljanak csak"]],
            "xyz6": [["Vallási fanatisták kifosztottak egy kórházat. Azt állítják, hogy csak Isten lépes megmenteni az embereket."], [SEMMI, KICSI, -KICSI, SEMMI, "Lépjenek fel ellenük"], [SEMMI, KICSI, KICSI, -NAGY, "Ürítsék ki az épületet"]],
}
Housekeeper_parbeszed = {
            "xyz1": [["Hangyák, Hangyák mindenhol! Ez biztos a kertész hibája,", "lesz egy-két szavam hozzá!"], [SEMMI, SEMMI, SEMMI, SEMMI, "Csak nyugodtan"], [SEMMI, SEMMI, SEMMI, SEMMI, "Hagyja"]],
            "xyz2": [["Tudja mit találtam a lepedőjén ma reggel? Egy olajfoltot. Vicces, nem? Kíváncsi lennék, hogy kerülhetett oda."], [SEMMI, SEMMI, SEMMI, SEMMI, "Igen"], [SEMMI, SEMMI, SEMMI, SEMMI, "Nem"]],
        }
Moore_parbeszed={
    "xyz1": [["Egy névtelen bejelentés szerint veszélyben lehet az élete. Szigorítsunk a biztonsági előírásokon?"], [SEMMI, SEMMI, SEMMI, SEMMI, "Csak nyugodtan"], [SEMMI, SEMMI, SEMMI, SEMMI, "Hagyja"]],
    "Róka": [["Az ország erős, de belső fenyegetések mindig megjelenhetnek. Egy speciális osztagot kellene felállítanunk ilyen célra."], [SEMMI, SEMMI, SEMMI, -KICSI, "Részemről rendben"], [SEMMI, SEMMI, SEMMI, SEMMI, "Szó sem lehet róla"]],
}
Ross_parbeszed = {
    "xyz1": [["Az idei tél kifejezetten fagyos, és a termések mennyisége megcsappant. Segítséget kérhetnénk a nyugati országoktól."], [SEMMI, SEMMI, KICSI, -KICSI, "Igen"], [SEMMI, SEMMI, SEMMI, SEMMI, "Nem"]],
    "xyz2": [["Követséget kellene építenünk a szomszédos országokban, a háborúk elkerülése érdekében."], [SEMMI, SEMMI, -NAGY, KICSI, "Jó ötlet"], [SEMMI, SEMMI, KICSI, -NAGY, "Nincs rá szükség"]],
}
The_Creator_parbeszed = {
            "xyz1": [["Szoszi", "Bal: Környezet(-1)", "Jobb: Minden(-2)"], [-KICSI, SEMMI, SEMMI, SEMMI], [-NAGY, -NAGY, -NAGY, -NAGY]],
        }
Time_parbeszed = {
            "xyz1": [["Szoszi", "Bal: Környezet(-1)", "Jobb: Minden(-2)"], [-KICSI, SEMMI, SEMMI, SEMMI], [-NAGY, -NAGY, -NAGY, -NAGY]],
        }
Torres_parbeszed = {
    "xyz1": [["Engedélyezi az atomenergia használatát a kísérleteinkhez? Kutatási szempontból rendkívül hasznos lenne."], [-NAGY, -KICSI, SEMMI, NAGY, "Szabad kezet adok"], [KICSI, KICSI, SEMMI, -KICSI, "Ez túl veszélyes"]],
}
Vice_President_Orville_parbeszed = {
            "xyz1": [["Néhány gyógyszeripari vállalat engedélyre vár a kormánytól, hogy tesztelhessék a termékeiket állatokon"], [-KICSI, SEMMI, SEMMI, KICSI, "Megtehetik"], [KICSI, KICSI, SEMMI, -KICSI, "Abszolút nem"]],
        }


# Objektumok meghívása
cards = [Card("Séf", Chef_parbeszed), Card("Kertész", Gardener_parbeszed), Card("Tábornok", General_Ramsey_parbeszed), Card("Egészségügyi miniszter", Gibson_parbeszed), Card("Kormányzó", Governor_parbeszed), Card("Házvezetőnő", Housekeeper_parbeszed), Card("Alelnök", Vice_President_Orville_parbeszed), Card("Alysha Hall", Alysha_Hall_parbeszed), Card("Ross nagykövet", Ross_parbeszed), Card("Torres kutatótiszt", Torres_parbeszed), Card("Moore hírszerzési igazgató", Moore_parbeszed)]
#cards = [Card("Moore hírszerzési igazgató", Moore_parbeszed)]
Player = PlayerStats()

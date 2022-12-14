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
    "H??bor??": False,
    "J??rv??ny": False,
    "Infl??ci??": False,
    "Radioaktivit??s": False,
    "J??s": True,
    "R??ka": False,  # Magas gazdas??g, vagy magas hadsereg miatti hal??l megel??z??se
    "Szeret??": False,  # Alacsony boldogs??g miatti hal??l megel??z??se
    "Templom": False,  # Alacsony boldogs??g miatti hal??l megel??z??se
    "Eur??": False,  # Alacsony gazdas??g miatti hal??l megel??z??se
    "Radar": False,  # Alacsony hadsereg miatti hal??l megel??z??se
    "Atombunker": False  # Alacsony k??rnyezet miatti hal??l megel??z??se
}


class Ability:
    def __init__(self, name, place):
        self.img = pygame.image.load(f"../Images/Icons/{name}.webp")
        self.place = place
        self.name = name


class Card:
    def __init__(self, name, parbeszed):
        self.eleres = f"../Images/Charachter/{name}.webp"  # El??r??si ??tvonal
        self.name = name  # Karakter neve
        self.img = pygame.image.load(self.eleres)  # K??p
        self.szovegek = parbeszed


class PlayerStats:
    def __init__(self):
        # J??t??kos kezd????rt??kei 0 ??s 10 k??z??tt. 5 az alap
        self.kornyezet = 5
        self.boldogsag = 5
        self.hadsereg = 5
        self.gazdasag = 5


Kumiyo_parbeszed = {
            "xyz1": [["Szoszi", "Bal: Gazdas??g(+1)", "Jobb: K??rnyezet(-1)"], [0, 0, 0, 1], [-1, 0, 0, 0]],
}
K_parbeszed = {
            "xyz1": [["Szoszi", "Bal: Boldogs??g(+1)", "Jobb: Hadsereg(+2)"], [0, 1, 0, 0], [0, 0, 2, 0]],
        }
President_Nakato_parbeszed = {
            "xyz1": [["Szoszi", "Bal: Hadsereg(-1)", "Jobb: K??rnyezet(+2)"], [0, 0, -1, 0], [2, 0, 0, 0]],
        }
Crazy_jeffry_parbeszed = {
            "xyz1": [["Szoszi", "Bal: K??rnyezet(-1)", "Jobb: Minden(-2)"], [-1, 0, 0, 0], [-2, -2, -2, -2]],
        }
Governor_Alien_parbeszed = {
            "xyz1": [["Szoszi", "Bal: K??rnyezet(-1)", "Jobb: Minden(-2)"], [-KICSI, SEMMI, SEMMI, SEMMI], [-NAGY, -NAGY, -NAGY, -NAGY]],
        }

Alysha_Hall_parbeszed = {
    "xyz1": [["??des, nem l??ttad a h??zvezet??n??t? Nem lehet igaz, sosem tal??lom sehol amikor sz??ks??gem lenne r??. N??ha ??gy t??nik, mintha sz??nd??kosan ker??lne engem"], [SEMMI, KICSI, SEMMI, SEMMI, "De l??ttam"], [SEMMI, SEMMI, KICSI, SEMMI, "Nem l??ttam"]],
}
Chef_parbeszed = {
            "xyz1": [["A biztons??gi tisztje ideges??t??, mint anan??sz a pizz??n. Elkobozta az ??sszes k??semet"], [SEMMI, KICSI, SEMMI, SEMMI, "Besz??lek vele"], [SEMMI, SEMMI, KICSI, SEMMI, "Biztons??gi okokb??l teszi"]],
            "xyz1": [["Az ??tel amink van, m??r nem olyan j??, mint r??gen. M??s besz??ll??t?? ut??n k??ne n??zn??nk, m??g ha dr??g??bb is lenne."], [SEMMI, KICSI, SEMMI, -KICSI, "Igen"], [SEMMI, -KICSI, SEMMI, KICSI, "Nem"]],
        }
Father_parbeszed = {
            "xyz1": [["Szoszi", "Bal: K??rnyezet(-1)", "Jobb: Minden(-2)"], [-KICSI, SEMMI, SEMMI, SEMMI], [-NAGY, -NAGY, -NAGY, -NAGY]],
        }
Gardener_parbeszed = {
            "xyz1": [["Egy m-mag??nv??llalat enged??lyt kapott arra, hogy kiv??gjon 70 hekt??r f??t! Ez hogyan l-lehets??ges?"], [KICSI, SEMMI, SEMMI, -KICSI, "Valami t??ved??s t??rt??nhetett"], [-KICSI, SEMMI, SEMMI, KICSI, "Fizetnek nek??nk ??rte"]],
            "xyz2": [["N-nem hiszem el, m??g a v??ros k-k??zep??n is lehet ??rezni a gy??rak f??stj??t. ??s m??g a n??v??nyeket is t-t??nkreteszi. Be kell z??ratni!"], [KICSI, SEMMI, SEMMI, -KICSI, "Megl??tom mit tehetek"], [-KICSI, SEMMI, SEMMI, SEMMI, "A n??v??nyek kib??rj??k"]],
        }
General_Ramsey_parbeszed = {
            "xyz1": [["A jelenlegi fegyverzet??nk ny??lt h??bor??ban hasztalan lenne. Kapunk enged??lyt nukle??ris fegyverkez??sre?"], [-NAGY, -KICSI, 2, -KICSI, "Igen"], [SEMMI, KICSI, -KICSI, SEMMI, "Nem"]],
            "xyz2": [["A nyugati orsz??gok fegyverkez??sbe fektetik a p??nz??ket. Meg kell t??madnunk ??ket, miel??tt ??k t??madnak meg minket!"], [SEMMI, -NAGY, -NAGY, SEMMI, "Fegyverbe"], [SEMMI, KICSI, -KICSI, SEMMI, "Nincs ok a p??nikra"]],
            "xyz3": [["A kutat??si r??szleg nem teszi a dolg??t. T??bb munkaer??t ??s er??forr??st kell ford??taniuk fegyverekre!"], [SEMMI, SEMMI, KICSI, -NAGY, "Igen"], [SEMMI, SEMMI, -KICSI, KICSI, "Nem"]],
            "xyz4": [["A sereg??nk gyenge, ??s a katon??ink sz??ma egyre csak fogy. T??mogatnunk k??ne a fiatalok toborz??s??t."], [SEMMI, SEMMI, KICSI, -KICSI, "Egyet??rtek"], [SEMMI, KICSI, -KICSI, SEMMI, "Nincs r?? sz??ks??g"]],
            "xyz5": [["Az emberek boldogtalanok, de a migr??nsok j?? b??nbakok lenn??nek. ??ket kellene hib??ztatni minden??rt."], [SEMMI, KICSI, -KICSI, -KICSI, "J?? ??tlet"], [SEMMI, -KICSI, KICSI, SEMMI, "Biztos nem"]],
        }
Gibson_parbeszed = {
            "xyz1": [["A farmokon a tehenek v??rt adnak tej helyett. Ez az ??js??gokban fog kik??tni!"], [-KICSI, SEMMI, SEMMI, -KICSI, "Ne hagyja, hogy ez megt??rt??njen"], [-KICSI, -NAGY, SEMMI, SEMMI, "Nem ??rdekel"]],
            "xyz3": [["A teny??sz??llatok ??letk??r??lm??nyei az orsz??g n??h??ny pontj??n siralmasak. K??zbe kellene l??pn??nk."], [SEMMI, KICSI, -KICSI, -KICSI, "Rendben"], [-KICSI, -KICSI, SEMMI, SEMMI, "Nem"]],
        }
Governor_parbeszed = {
            "xyz1": [["S??rg??s h??v??st kaptunk, t??z ??t??tt ki a v??rosi ligetben. Minden l??ngokban ??ll!"], [SEMMI, -NAGY, -KICSI, SEMMI, "??ll??ts??k meg a t??zet"], [SEMMI, SEMMI, -KICSI, -NAGY, "Seg??tsenek a civileknek"]],
            "xyz2": [["A lakoss??g el??gedetlen, t??bb p??nzt k??vetelnek rekre??ci??s lehet??s??gekre"], [SEMMI, KICSI, SEMMI, SEMMI, "??gy lesz"], [KICSI, SEMMI, SEMMI, SEMMI, "Felesleges"]],
            "xyz3": [["Falk??ba ver??d??tt k??bor kuty??k terroriz??lj??k a lakosokat n??h??ny peremvid??ken. Tenni kellene az ??gy ??rdek??ben"], [SEMMI, KICSI, SEMMI, -KICSI, "Igen"], [-KICSI, -KICSI, SEMMI, KICSI, "Nem"]],
            "xyz4": [["??gy n??z ki, hajl??ktalanok ??lnek egy atomer??m?? romjai k??z??tt. N??h??nyukat eltorz??totta a sug??rz??s. Az emberek f??lnek t??l??k"], [-KICSI, -KICSI, -KICSI, SEMMI, "K??ldj??k el ??ket"], [SEMMI, -NAGY, SEMMI, SEMMI, "Maradhatnak"]],
            "xyz5": [["Az emberek nem el??gedettek a jelenlegi katonai d??nt??shozatalunkkal. ??sszeesk??v??sekr??l, korrupci??r??l, ??s k??zelg?? h??bor??r??l besz??lnek."], [SEMMI, KICSI, -KICSI, -KICSI, "V??ltoztatunk a terveinken"], [SEMMI, -NAGY, KICSI, SEMMI, "Pletyk??ljanak csak"]],
            "xyz6": [["Vall??si fanatist??k kifosztottak egy k??rh??zat. Azt ??ll??tj??k, hogy csak Isten l??pes megmenteni az embereket."], [SEMMI, KICSI, -KICSI, SEMMI, "L??pjenek fel ellen??k"], [SEMMI, KICSI, KICSI, -NAGY, "??r??ts??k ki az ??p??letet"]],
}
Housekeeper_parbeszed = {
            "xyz1": [["Hangy??k, Hangy??k mindenhol! Ez biztos a kert??sz hib??ja,", "lesz egy-k??t szavam hozz??!"], [SEMMI, SEMMI, SEMMI, SEMMI, "Csak nyugodtan"], [SEMMI, SEMMI, SEMMI, SEMMI, "Hagyja"]],
            "xyz2": [["Tudja mit tal??ltam a leped??j??n ma reggel? Egy olajfoltot. Vicces, nem? K??v??ncsi lenn??k, hogy ker??lhetett oda."], [SEMMI, SEMMI, SEMMI, SEMMI, "Igen"], [SEMMI, SEMMI, SEMMI, SEMMI, "Nem"]],
        }
Moore_parbeszed={
    "xyz1": [["Egy n??vtelen bejelent??s szerint vesz??lyben lehet az ??lete. Szigor??tsunk a biztons??gi el????r??sokon?"], [SEMMI, SEMMI, SEMMI, SEMMI, "Csak nyugodtan"], [SEMMI, SEMMI, SEMMI, SEMMI, "Hagyja"]],
    "R??ka": [["Az orsz??g er??s, de bels?? fenyeget??sek mindig megjelenhetnek. Egy speci??lis osztagot kellene fel??ll??tanunk ilyen c??lra."], [SEMMI, SEMMI, SEMMI, -KICSI, "R??szemr??l rendben"], [SEMMI, SEMMI, SEMMI, SEMMI, "Sz?? sem lehet r??la"]],
}
Ross_parbeszed = {
    "xyz1": [["Az idei t??l kifejezetten fagyos, ??s a term??sek mennyis??ge megcsappant. Seg??ts??get k??rhetn??nk a nyugati orsz??gokt??l."], [SEMMI, SEMMI, KICSI, -KICSI, "Igen"], [SEMMI, SEMMI, SEMMI, SEMMI, "Nem"]],
    "xyz2": [["K??vets??get kellene ??p??ten??nk a szomsz??dos orsz??gokban, a h??bor??k elker??l??se ??rdek??ben."], [SEMMI, SEMMI, -NAGY, KICSI, "J?? ??tlet"], [SEMMI, SEMMI, KICSI, -NAGY, "Nincs r?? sz??ks??g"]],
}
The_Creator_parbeszed = {
            "xyz1": [["Szoszi", "Bal: K??rnyezet(-1)", "Jobb: Minden(-2)"], [-KICSI, SEMMI, SEMMI, SEMMI], [-NAGY, -NAGY, -NAGY, -NAGY]],
        }
Time_parbeszed = {
            "xyz1": [["Szoszi", "Bal: K??rnyezet(-1)", "Jobb: Minden(-2)"], [-KICSI, SEMMI, SEMMI, SEMMI], [-NAGY, -NAGY, -NAGY, -NAGY]],
        }
Torres_parbeszed = {
    "xyz1": [["Enged??lyezi az atomenergia haszn??lat??t a k??s??rleteinkhez? Kutat??si szempontb??l rendk??v??l hasznos lenne."], [-NAGY, -KICSI, SEMMI, NAGY, "Szabad kezet adok"], [KICSI, KICSI, SEMMI, -KICSI, "Ez t??l vesz??lyes"]],
}
Vice_President_Orville_parbeszed = {
            "xyz1": [["N??h??ny gy??gyszeripari v??llalat enged??lyre v??r a korm??nyt??l, hogy tesztelhess??k a term??keiket ??llatokon"], [-KICSI, SEMMI, SEMMI, KICSI, "Megtehetik"], [KICSI, KICSI, SEMMI, -KICSI, "Abszol??t nem"]],
        }


# Objektumok megh??v??sa
cards = [Card("S??f", Chef_parbeszed), Card("Kert??sz", Gardener_parbeszed), Card("T??bornok", General_Ramsey_parbeszed), Card("Eg??szs??g??gyi miniszter", Gibson_parbeszed), Card("Korm??nyz??", Governor_parbeszed), Card("H??zvezet??n??", Housekeeper_parbeszed), Card("Aleln??k", Vice_President_Orville_parbeszed), Card("Alysha Hall", Alysha_Hall_parbeszed), Card("Ross nagyk??vet", Ross_parbeszed), Card("Torres kutat??tiszt", Torres_parbeszed), Card("Moore h??rszerz??si igazgat??", Moore_parbeszed)]
#cards = [Card("Moore h??rszerz??si igazgat??", Moore_parbeszed)]
Player = PlayerStats()

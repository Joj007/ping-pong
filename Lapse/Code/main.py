import pygame
import Classes
import Chain_messeages
import datetime
import random


def rad_szamitas(szoveg, index, valasz):
    rad = 0
    # Kör sugarának mérete
    if abs(szoveg[valasz][index]):
        if abs(szoveg[valasz][index]) == Classes.SEMMI:
            rad = 0
        elif abs(szoveg[valasz][index]) == Classes.KICSI:
            rad = 3
        elif abs(szoveg[valasz][index]) == Classes.NAGY or abs(szoveg[valasz][index]) == Classes.INSTANT:
            rad = 5
    return rad


def negativ_ertekek_visszaallitasa():
    Classes.PLAYER_MODE['Radioaktivitás'] = False
    Classes.PLAYER_MODE['Járvány'] = False
    Classes.PLAYER_MODE['Háború'] = False
    Classes.PLAYER_MODE['Infláció'] = False


def halal():
    global last_death_date
    global halal_bool
    if len(halal_tipus) == 2:
        negativ_ertekek_visszaallitasa()
        Classes.Player.kornyezet = 5
        Classes.Player.boldogsag = 5
        Classes.Player.hadsereg = 5
        Classes.Player.gazdasag = 5
    halal_bool = True


def halal_utani_uzenet():
    global szoveg
    global halal_bool
    global random_karakter
    szoveg = Chain_messeages.halalok[halal_tipus][0:-1]
    random_karakter = Chain_messeages.halalok[halal_tipus][-1]
    halal_bool = False





# Alap dolgok
pygame.init()
pygame.display.set_caption('A játék elkezdődött')
screen = pygame.display.set_mode((Classes.SCREEN[0], Classes.SCREEN[1]))

# Láncolt párbeszédhez változók
halal_bool = False
halal_tipus = ""


# Ikonok betöltése
kornyezet = pygame.image.load("../Images/Icons/tree.png")
boldogsag = pygame.image.load("../Images/Icons/person.png")
hadsereg = pygame.image.load("../Images/Icons/gun.png")
gazdasag = pygame.image.load("../Images/Icons/money.png")
csakfelfele = pygame.image.load("../Images/Icons/csakfelfelé.png")
csaklefele = pygame.image.load("../Images/Icons/csaklefelé.png")
shield_red = pygame.image.load('../Images/Icons/shield_red.png')
shield_green = pygame.image.load('../Images/Icons/shield_green.png')
szereto = pygame.image.load("../Images/Icons/Lover.webp")
Euro = pygame.image.load("../Images/Icons/Euro.webp")
Fox = pygame.image.load("../Images/Icons/Fox.webp")
Radar = pygame.image.load("../Images/Icons/Radar.webp")
Church = pygame.image.load("../Images/Icons/Church.webp")
Antiradiation = pygame.image.load("../Images/Icons/Antiradiation.webp")

# Betűtípusok betöltése
myfont = pygame.font.Font("../Fonts/Merriweather-Regular.ttf", 40)
parbeszed_font = pygame.font.Font("../Fonts/Merriweather-Regular.ttf", 20)
valasz_font = pygame.font.Font("../Fonts/Merriweather-Regular.ttf", 15)

# Kártyával kapcsolatos konstansok és változók
card_pos = [Classes.SCREEN[0]/2 - Classes.ELHELYEZKEDESEK['Kep_meret']/2, Classes.SCREEN[1]/2 - Classes.ELHELYEZKEDESEK['Kep_meret']/2]
CARD_START_X = Classes.SCREEN[0]/2 - Classes.ELHELYEZKEDESEK['Kep_meret']/2
CARD_START_Y = Classes.SCREEN[1]/2 - Classes.ELHELYEZKEDESEK['Kep_meret']/2
CARD_END_X = Classes.SCREEN[0]/2 + Classes.ELHELYEZKEDESEK['Kep_meret']/2
CARD_END_Y = Classes.SCREEN[1]/2 + Classes.ELHELYEZKEDESEK['Kep_meret']/2

last_death_date = datetime.datetime(2075, 7, 5)
date = datetime.datetime(2075, 7, 5) + datetime.timedelta(days=random.randint(10, 32))

random_karakter = Classes.cards[random.randint(0, len(Classes.cards)-1)]
szoveg = random.choice(list(random_karakter.szovegek.values()))
valasz_bal = szoveg[1]
valasz_jobb = szoveg[2]

# Képességek_lista
ability_list = []
# ability_list = [Classes.Ability("Lover", 0), Classes.Ability("Fox", 1), Classes.Ability("Radar", 2), Classes.Ability("Church", 3), Classes.Ability("Euro", 4), Classes.Ability("Antiradiation", 5)]

running = True
dragging = False

tarolo_hossz = 110 * 3 + 10
while running:
    # Egér koordináták
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Háttér
    screen.fill(Classes.SZINEK_HASZNALATA['hatter'])

    # Képességek megrajtolása és görgetése
    if 4 > len(ability_list) > 0:
        tarolo_hossz = 110 * len(ability_list) + 10
        pygame.draw.rect(screen, (100, 100, 100), (0, 225, tarolo_hossz, 50), 3, 25)
        for index in range(len(ability_list)):
            screen.blit(ability_list[index].img, (ability_list[index].place * 110 + 10, 200))
    elif len(ability_list) > 3:
        if tarolo_hossz > mouse_x > 0 and 200 < mouse_y < 300 and not dragging:
            tarolo_hossz = 110 * len(ability_list) + 10
            pygame.draw.rect(screen, (100, 100, 100), (0, 225, tarolo_hossz, 50), 3, 25)
            for index in range(len(ability_list)):
                screen.blit(ability_list[index].img, (ability_list[index].place * 110 + 10, 200))
        else:
            tarolo_hossz = 110 * 3 + 10
            pygame.draw.rect(screen, (100, 100, 100), (0, 225, tarolo_hossz, 50), 3, 25)
            for index in range(3):
                screen.blit(ability_list[index].img, (ability_list[index].place * 110 + 10, 200))

    # Alsó és felső szakaszok megrajzolása
    pygame.draw.rect(screen, Classes.SZINEK_HASZNALATA['felso_szakasz'], (0, 0, Classes.SCREEN[0], Classes.ELHELYEZKEDESEK['Felso_szakasz_magassag']))
    pygame.draw.rect(screen, Classes.SZINEK_HASZNALATA['also_szakasz'], (0, Classes.SCREEN[1]-Classes.ELHELYEZKEDESEK['Also_szakasz_magassag'], Classes.SCREEN[0], Classes.ELHELYEZKEDESEK['Also_szakasz_magassag']))


    # Értékek ikonjának megjelenítése
    screen.blit(kornyezet, (Classes.SCREEN[0]/5-Classes.ELHELYEZKEDESEK['Ikonok_merete']/2, Classes.ELHELYEZKEDESEK["Felso_szakasz_magassag"]/2-Classes.ELHELYEZKEDESEK['Ikonok_merete']/2))
    screen.blit(boldogsag, (Classes.SCREEN[0]/5*2-Classes.ELHELYEZKEDESEK['Ikonok_merete']/2, Classes.ELHELYEZKEDESEK["Felso_szakasz_magassag"]/2-Classes.ELHELYEZKEDESEK['Ikonok_merete']/2))
    screen.blit(hadsereg, (Classes.SCREEN[0]/5*3-Classes.ELHELYEZKEDESEK['Ikonok_merete']/2, Classes.ELHELYEZKEDESEK["Felso_szakasz_magassag"]/2-Classes.ELHELYEZKEDESEK['Ikonok_merete']/2))
    screen.blit(gazdasag, (Classes.SCREEN[0]/5*4-Classes.ELHELYEZKEDESEK['Ikonok_merete']/2, Classes.ELHELYEZKEDESEK["Felso_szakasz_magassag"]/2-Classes.ELHELYEZKEDESEK['Ikonok_merete']/2))


    # Átlátszó felület az értékek kijelzéséhez
    kornyezet_surf = pygame.Surface((128, abs((10-Classes.Player.kornyezet)*6.4)))
    kornyezet_surf.set_alpha(200)
    kornyezet_surf.fill(Classes.SZINEK_HASZNALATA['felso_szakasz'])
    screen.blit(kornyezet_surf, (Classes.SCREEN[0]//5-64, 120//2-32))

    boldogsag_surf = pygame.Surface((128, abs((10-Classes.Player.boldogsag)*6.4)))
    boldogsag_surf.set_alpha(200)
    boldogsag_surf.fill(Classes.SZINEK_HASZNALATA['felso_szakasz'])
    screen.blit(boldogsag_surf, (Classes.SCREEN[0]//5*2-64, 120//2-32))

    hadsereg_surf = pygame.Surface((128, abs((10-Classes.Player.hadsereg)*6.4)))
    hadsereg_surf.set_alpha(200)
    hadsereg_surf.fill(Classes.SZINEK_HASZNALATA['felso_szakasz'])
    screen.blit(hadsereg_surf, (Classes.SCREEN[0]//5*3-64, 120//2-32))

    gazdasag_surf = pygame.Surface((128, abs((10-Classes.Player.gazdasag)*6.4)))
    gazdasag_surf.set_alpha(200)
    gazdasag_surf.fill(Classes.SZINEK_HASZNALATA['felso_szakasz'])
    screen.blit(gazdasag_surf, (Classes.SCREEN[0]//5*4-64, 120//2-32))


    # Bal válasz
    valasz_szin = Classes.SZINEK_HASZNALATA['sima_potty']
    if Classes.SCREEN[0]/2-Classes.ELHELYEZKEDESEK['Valasz_megjelenitesi_tavolsag'] > card_pos[0] + Classes.ELHELYEZKEDESEK['Kep_meret'] / 2:
        for index in range(4):
            if Classes.PLAYER_MODE['Jós']:
                if szoveg[1][index] > 0:
                    valasz_szin = Classes.SZINEK_HASZNALATA['jo_potty']
                else:
                    valasz_szin = Classes.SZINEK_HASZNALATA['rossz_potty']
            pygame.draw.circle(screen, valasz_szin, (Classes.SCREEN[0] / 5 * (index + 1), 15), rad_szamitas(szoveg, index, 1))
    # Jobb válasz
    elif card_pos[0] + Classes.ELHELYEZKEDESEK['Kep_meret'] / 2 > Classes.SCREEN[0]/2+Classes.ELHELYEZKEDESEK['Valasz_megjelenitesi_tavolsag']:
        for index in range(4):
            if Classes.PLAYER_MODE['Jós']:
                if szoveg[2][index] > 0:
                    valasz_szin = (0, 255, 0)
                else:
                    valasz_szin = (255, 0, 0)
            pygame.draw.circle(screen, valasz_szin, (Classes.SCREEN[0] / 5 * (index + 1), 15), rad_szamitas(szoveg, index, 2))


    # Állapotok jelzése
    if Classes.PLAYER_MODE['Radioaktivitás']:
        screen.blit(csaklefele, (Classes.SCREEN[0] / 5 * 1 - 64 / 2 - 15, 120 / 2 - 64 / 2 - 10))
    if Classes.PLAYER_MODE['Járvány']:
        screen.blit(csaklefele, (Classes.SCREEN[0] / 5 * 2 - 64 / 2 - 10, 120 / 2 - 64 / 2 - 10))
    if Classes.PLAYER_MODE['Háború']:
        screen.blit(csaklefele, (Classes.SCREEN[0] / 5 * 3 - 64 / 2 - 10, 120 / 2 - 64 / 2 - 10))
    if Classes.PLAYER_MODE['Infláció']:
        screen.blit(csaklefele, (Classes.SCREEN[0] / 5 * 4 - 64 / 2 - 10, 120 / 2 - 64 / 2 - 10))
    if Classes.PLAYER_MODE['Euró']:
        screen.blit(shield_red, (Classes.SCREEN[0] / 5 * 4 + 64 / 2 - 10, 120 / 2 + 15))
    if Classes.PLAYER_MODE['Róka']:
        screen.blit(shield_green, (Classes.SCREEN[0] / 5 * 3 + 64 / 2 - 15, 120 / 2 - 50))
        screen.blit(shield_green, (Classes.SCREEN[0] / 5 * 4 + 64 / 2 - 15, 120 / 2 - 50))
    if Classes.PLAYER_MODE['Atombunker']:
        screen.blit(shield_red, (Classes.SCREEN[0] / 5 * 1 + 64 / 2 - 15, 120 / 2 + 15))
    if Classes.PLAYER_MODE['Radar']:
        screen.blit(shield_red, (Classes.SCREEN[0] / 5 * 3 + 64 / 2 - 15, 120 / 2 + 15))
    if Classes.PLAYER_MODE['Templom'] or Classes.PLAYER_MODE['Szerető']:
        screen.blit(shield_red, (Classes.SCREEN[0] / 5 * 2 + 64 / 2 - 15, 120 / 2 + 15))

    # Név
    name = myfont.render(random_karakter.name, True, Classes.SZINEK_HASZNALATA['nev'])
    name_rect = name.get_rect(center=(Classes.SCREEN[0] / 2, Classes.SCREEN[1] / 2 + Classes.ELHELYEZKEDESEK['Kep_meret']/2 + 50))
    screen.blit(name, name_rect)

    # Év
    date_label = myfont.render(str(date.year), True, Classes.SZINEK_HASZNALATA['datum'])
    date_rect = date_label.get_rect(center=(Classes.SCREEN[0] / 2, Classes.SCREEN[1] / 2 + Classes.ELHELYEZKEDESEK['Kep_meret'] / 2 + 170))
    screen.blit(date_label, date_rect)

    # Napja a hivatalban
    napja = abs(date-last_death_date).days
    day_label = myfont.render(str(napja) + " napot a hivatalban", True, Classes.SZINEK_HASZNALATA['datum'])
    day_rect = day_label.get_rect(center=(Classes.SCREEN[0] / 2, Classes.SCREEN[1] / 2 + Classes.ELHELYEZKEDESEK['Kep_meret'] / 2 + 230))
    screen.blit(day_label, day_rect)

    # Parbeszéd
    szoveg_y = 170
    for sor in szoveg[0]:
        szoveg_label = parbeszed_font.render(sor, True, Classes.SZINEK_HASZNALATA['parbeszed'])
        szoveg_rect = szoveg_label.get_rect(center=(Classes.SCREEN[0] / 2 - 15, szoveg_y))
        screen.blit(szoveg_label, szoveg_rect)
        szoveg_y += 25

    # Kártya helye
    pygame.draw.rect(screen, Classes.SZINEK_HASZNALATA['kartya_helye'], (int(CARD_START_X)-10, int(CARD_START_Y)-10, 340, 340), 0, Classes.ELHELYEZKEDESEK['Kartya_gorbulet'])
    # Karakter képe
    screen.blit(random_karakter.img, card_pos)
    # Kártya kerete
    pygame.draw.rect(screen, Classes.SZINEK_HASZNALATA['keret'], (int(card_pos[0]-10), int(card_pos[1]-10), 340, 340), Classes.ELHELYEZKEDESEK['kartya_keret_vastagsag'], Classes.ELHELYEZKEDESEK['Kartya_gorbulet'])


    # Bal válasz megjelenítése a kártyán
    valasz_szin = Classes.SZINEK_HASZNALATA['sima_potty']
    if Classes.SCREEN[0]/2-Classes.ELHELYEZKEDESEK['Valasz_megjelenitesi_tavolsag'] > card_pos[0] + Classes.ELHELYEZKEDESEK['Kep_meret'] / 2:
        bal_valasz = valasz_font.render(szoveg[1][4], True, Classes.SZINEK_HASZNALATA['valasz'])
        bal_valasz_rect = bal_valasz.get_rect(topleft=(card_pos[0] + 10, card_pos[1] + 10))
        screen.blit(bal_valasz, bal_valasz_rect)
    # Jobb válasz megjelenítése a kártyán
    elif card_pos[0] + Classes.ELHELYEZKEDESEK['Kep_meret'] / 2 > Classes.SCREEN[0]/2+Classes.ELHELYEZKEDESEK['Valasz_megjelenitesi_tavolsag']:
        jobb_valasz = valasz_font.render(szoveg[2][4], True, Classes.SZINEK_HASZNALATA['valasz'])
        jobb_valasz_rect = jobb_valasz.get_rect(topright=(card_pos[0] + 310, card_pos[1] + 10))
        screen.blit(jobb_valasz, jobb_valasz_rect)



    # Kártya pozíciója húzáskor
    if dragging:
        card_pos = [mouse_x-x_kulonbseg, mouse_y-y_kulonbseg]
    else:
        card_pos = [CARD_START_X, CARD_START_Y]

    # Ha túl nagy vagy túl kicsi az egyik érték, vége
    if Classes.Player.kornyezet <= 0:
        szoveg = [["Elnök úr, a sugárzásszint az egeket veri. Nem tudjuk többé garantálni a nép egészségét"], [0, 0, 0, 0, "Mi a..."], [0, 0, 0, 0, "Mi a..."]]
        random_karakter = Classes.Card("Torres kutatótiszt", Classes.Gardener_parbeszed)
        if Classes.PLAYER_MODE['Atombunker']:
            halal_tipus = "k-+"
            Classes.Player.kornyezet = 5
        else:
            halal_tipus = "k-"
        Classes.PLAYER_MODE['Atombunker'] = False
        halal()
    if Classes.Player.kornyezet >= 10:
        Classes.Player.kornyezet = 10
    if Classes.Player.boldogsag <= 0:
        szoveg = [["Elnök úr, terjed az elégedetlenség, és a nép a kormány ellen fordul."], [0, 0, 0, 0, "Mi a..."], [0, 0, 0, 0, "Mi a..."]]
        random_karakter = Classes.Card("Ross nagykövet", Classes.Gardener_parbeszed)
        if Classes.PLAYER_MODE['Templom'] or Classes.PLAYER_MODE['Szerető']:
            halal_tipus = "b-+"
            Classes.Player.boldogsag = 5
        else:
            halal_tipus = "b-"
        Classes.PLAYER_MODE['Templom'] = False
        Classes.PLAYER_MODE['Szerető'] = False
        halal()
    if Classes.Player.boldogsag >= 10:
        Classes.Player.boldogsag = 10
    if Classes.Player.hadsereg <= 0:
        szoveg = [["Szomszédos országok támadnak minket. A seregünk többé nem képes megvédeni magát a megszállóktól!"], [0, 0, 0, 0, "Mi a..."], [0, 0, 0, 0, "Mi a..."]]
        random_karakter = Classes.Card("Tábornok", Classes.Gardener_parbeszed)
        if Classes.PLAYER_MODE['Radar']:
            halal_tipus = "h-+"
            Classes.Player.hadsereg = 5
        else:
            halal_tipus = "h-"
        halal()
        Classes.PLAYER_MODE['Radar'] = False
    if Classes.Player.hadsereg >= 10:
        szoveg = [["Ne mozduljon, elnök úr! Ez egy katonai puccs."], [0, 0, 0, 0, "Mi a..."], [0, 0, 0, 0, "Mi a..."]]
        random_karakter = Classes.Card("Tábornok", Classes.Gardener_parbeszed)
        if Classes.PLAYER_MODE['Róka']:
            halal_tipus = "h++"
            Classes.Player.hadsereg = 5
        else:
            halal_tipus = "h+"
        halal()
        Classes.PLAYER_MODE['Róka'] = False
    if Classes.Player.gazdasag <= 0:
        szoveg = [["Elnök úr, az állam szegény, és az államadósság csődbe visz minket"], [0, 0, 0, 0, "Mi a..."], [0, 0, 0, 0, "Mi a..."]]
        random_karakter = Classes.Card("Ross nagykövet", Classes.Gardener_parbeszed)
        if Classes.PLAYER_MODE['Euró']:
            halal_tipus = "g-+"
            Classes.Player.gazdasag = 5
        else:
            halal_tipus = "g-"
        halal()
        Classes.PLAYER_MODE['Euró'] = False
    if Classes.Player.gazdasag >= 10:
        szoveg = [["Elnök úr, a bankok totális hatalommal bírnak. Egy felkelést vezetnek ön és a jelenlegi kormány ellen!"], [0, 0, 0, 0, "Mi a..."], [0, 0, 0, 0, "Mi a"]]
        random_karakter = Classes.Card("Ross nagykövet", Classes.Gardener_parbeszed)
        if Classes.PLAYER_MODE['Róka']:
            halal_tipus = "g++"
            Classes.Player.gazdasag = 5
        else:
            halal_tipus = "g+"
        halal()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
        # Kártya mozgatás
        if event.type == pygame.MOUSEBUTTONDOWN and CARD_START_X < mouse_x < CARD_END_X and CARD_START_Y < mouse_y < CARD_END_Y:
            dragging = True
            x_kulonbseg = mouse_x - card_pos[0]
            y_kulonbseg = mouse_y - card_pos[1]


        # Képesség használat
        if event.type == pygame.MOUSEBUTTONUP and not dragging:
            if tarolo_hossz > mouse_x > 0 and 200 < mouse_y < 300 and not dragging:
                for index in range(len(ability_list)):
                    if 110 * (index + 1) > mouse_x > 110 * index + 10:
                        if ability_list[index].name == "Fox":
                            Classes.PLAYER_MODE['Róka'] = True
                        if ability_list[index].name == "Radar":
                            Classes.PLAYER_MODE['Radar'] = True
                        if ability_list[index].name == "Antiradiation":
                            Classes.PLAYER_MODE['Atombunker'] = True
                        if ability_list[index].name == "Church":
                            Classes.PLAYER_MODE['Templom'] = True
                        if ability_list[index].name == "Lover":
                            Classes.PLAYER_MODE['Szerető'] = True
                        if ability_list[index].name == "Euro":
                            Classes.PLAYER_MODE['Euró'] = True
                        ability_list.pop(index)
                        for index_al in range(len(ability_list)):
                            if ability_list[index_al].place != index_al:
                                ability_list[index_al].place -= 1

        # Kártya elengedés
        if event.type == pygame.MOUSEBUTTONUP:
            # Elengedés bal oldalon
            if Classes.SCREEN[0]/2 - Classes.ELHELYEZKEDESEK['Valasztas_ervenyes_tavolsag'] > card_pos[0] + Classes.ELHELYEZKEDESEK['Kep_meret'] / 2:

                # Folyamatos képességek
                if Classes.PLAYER_MODE['Háború']:
                    Classes.Player.hadsereg -= Classes.KICSI
                if Classes.PLAYER_MODE['Járvány']:
                    Classes.Player.boldogsag -= Classes.KICSI
                if Classes.PLAYER_MODE['Infláció']:
                    Classes.Player.gazdasag -= Classes.KICSI
                if Classes.PLAYER_MODE['Radioaktivitás']:
                    Classes.Player.kornyezet -= Classes.KICSI

                date += datetime.timedelta(days=random.randint(10, 32))  # Dátum növelése
                # Értékek módosítása válasznak megfelelően
                Classes.Player.kornyezet += valasz_bal[0]
                Classes.Player.boldogsag += valasz_bal[1]
                Classes.Player.hadsereg += valasz_bal[2]
                Classes.Player.gazdasag += valasz_bal[3]

                if szoveg[1][4] == "Részemről rendben":
                    ability_list.append(Classes.Ability("Fox", len(ability_list)))

                # Következő kártya kihúzása
                random_karakter = Classes.cards[random.randint(0, len(Classes.cards)-1)]
                szoveg = random.choice(list(random_karakter.szovegek.values()))

                # Halál
                if halal_bool:
                    halal_utani_uzenet()
                    last_death_date = date + datetime.timedelta(random.randint(10, 32))

                # Válaszok megadása
                valasz_bal = szoveg[1]
                valasz_jobb = szoveg[2]

            # Elengedés jobb oldalon
            elif card_pos[0] + Classes.ELHELYEZKEDESEK['Kep_meret'] / 2 > Classes.SCREEN[0]/2 + Classes.ELHELYEZKEDESEK['Valasztas_ervenyes_tavolsag']:

                # Folyamatos képességek
                if Classes.PLAYER_MODE['Háború']:
                    Classes.Player.hadsereg -= Classes.KICSI
                if Classes.PLAYER_MODE['Járvány']:
                    Classes.Player.boldogsag -= Classes.KICSI
                if Classes.PLAYER_MODE['Infláció']:
                    Classes.Player.gazdasag -= Classes.KICSI
                if Classes.PLAYER_MODE['Radioaktivitás']:
                    Classes.Player.kornyezet -= Classes.KICSI

                date += datetime.timedelta(days=random.randint(10, 32)) # Dátum növelése
                # Értékek módosítása válasznak megfelelően
                Classes.Player.kornyezet += valasz_jobb[0]
                Classes.Player.boldogsag += valasz_jobb[1]
                Classes.Player.hadsereg += valasz_jobb[2]
                Classes.Player.gazdasag += valasz_jobb[3]

                # Következő kártya kihúzása
                random_karakter = Classes.cards[random.randint(0, len(Classes.cards)-1)]
                szoveg = random.choice(list(random_karakter.szovegek.values()))

                # Halál
                if halal_bool:
                    halal_utani_uzenet()
                    last_death_date = date + datetime.timedelta(random.randint(10, 32))

                # Válaszok megadása
                valasz_bal = szoveg[1]
                valasz_jobb = szoveg[2]


            dragging = False







    pygame.display.update()

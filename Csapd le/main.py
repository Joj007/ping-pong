import pygame, time

vege = False

a_jatekos_pontszam = 0
b_jatekos_pontszam = 0

screen_x = 800
screen_y = 700

pygame.init()
pygame.display.set_caption('A játék elkezdődött')
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((screen_x, screen_y))
green_x_img = pygame.image.load('green_x.png')
red_x_img = pygame.image.load('red_x.png')
a_jatekos_img = pygame.image.load('red_hand.png')
b_jatekos_img = pygame.image.load('blue_hand.png')
kezek_lista = [a_jatekos_img, b_jatekos_img]

a_jatekos_aktiv = False
b_jatekos_aktiv = False

a_jatekos_pos_alap = (250, 420)
b_jatekos_pos_alap = (a_jatekos_pos_alap[0]+50, a_jatekos_pos_alap[1]-400)
a_jatekos_pos_aktiv = (a_jatekos_pos_alap[0], a_jatekos_pos_alap[1]-120)
b_jatekos_pos_aktiv = (a_jatekos_pos_aktiv[0]+50, a_jatekos_pos_aktiv[1]-180)
a_jatekos_pos = a_jatekos_pos_alap
b_jatekos_pos = b_jatekos_pos_alap
kezek_lista_pos = [a_jatekos_pos, b_jatekos_pos]

a_jatekos_inaktiv = time.time()
b_jatekos_inaktiv = time.time()

x_tengely = [10, 50, 90]
y_tengely = [10, screen_y - 40]

runnig = True
while runnig:
    kezek_lista = [a_jatekos_img, b_jatekos_img]
    kezek_lista_pos = [a_jatekos_pos, b_jatekos_pos]
    screen.fill((200, 50, 200))
    for (kez, pos) in zip(kezek_lista, kezek_lista_pos):
        screen.blit(kez, pos)

    for x in x_tengely:
        screen.blit(green_x_img, (x, y_tengely[0]))
        screen.blit(green_x_img, (x, y_tengely[1]))

    if a_jatekos_pontszam >= 3:
        for x in x_tengely:
            screen.blit(red_x_img, (x, y_tengely[0]))
        if not vege:
            pygame.display.set_caption('A piros játékos nyert')
        vege = True
    elif a_jatekos_pontszam >= 2:
        screen.blit(red_x_img, (x_tengely[1], y_tengely[0]))
        screen.blit(red_x_img, (x_tengely[0], y_tengely[0]))
    elif a_jatekos_pontszam >= 1:
        screen.blit(red_x_img, (x_tengely[0], y_tengely[0]))

    if b_jatekos_pontszam >= 3:
        for x in x_tengely:
            screen.blit(red_x_img, (x, y_tengely[1]))
        if not vege:
            pygame.display.set_caption('A kék játékos nyert')
        vege = True
    elif b_jatekos_pontszam >= 2:
        screen.blit(red_x_img, (x_tengely[1], y_tengely[1]))
        screen.blit(red_x_img, (x_tengely[0], y_tengely[1]))
    elif b_jatekos_pontszam >= 1:
        screen.blit(red_x_img, (x_tengely[0], y_tengely[1]))

    if time.time() - a_jatekos_inaktiv > 10 and not vege:
        b_jatekos_pontszam += 1
        a_jatekos_inaktiv = time.time()
        pygame.display.set_caption('A piros játékos túl sokáig volt inaktív')
    if time.time() - b_jatekos_inaktiv > 10 and not vege:
        a_jatekos_pontszam += 1
        b_jatekos_inaktiv = time.time()
        pygame.display.set_caption('A kék játékos túl sokáig volt inaktív')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()

        if event.type == pygame.KEYDOWN and not vege:
            if event.key == pygame.K_RETURN:
                a_jatekos_inaktiv = time.time()
                try:
                    if time.time() - start_a < 0.3:
                        b_jatekos_pontszam += 1
                        pygame.display.set_caption('A piros játékos túl gyakran ütött')
                    start_a = time.time()
                    a_jatekos_aktiv = True
                    a_jatekos_pos = a_jatekos_pos_aktiv
                    if b_jatekos_aktiv:
                        a_jatekos_pontszam += 1
                        pygame.display.set_caption('A piros játékos találatot szerzett')
                except:
                    start_a = time.time()
                    a_jatekos_aktiv = True
                    a_jatekos_pos = a_jatekos_pos_aktiv
                    if b_jatekos_aktiv:
                        a_jatekos_pontszam += 1
                        pygame.display.set_caption('A piros játékos találatot szerzett')

            if event.key == pygame.K_SPACE:
                b_jatekos_inaktiv = time.time()
                try:
                    if time.time() - start_b < 0.3:
                        a_jatekos_pontszam += 1
                        pygame.display.set_caption('A kék játékos túl gyakran ütött')
                    start_b = time.time()
                    b_jatekos_aktiv = True
                    b_jatekos_pos = b_jatekos_pos_aktiv
                    if a_jatekos_aktiv:
                        b_jatekos_pontszam += 1
                        pygame.display.set_caption('A kék játékos találatot szerzett')
                except:
                    start_b = time.time()
                    b_jatekos_aktiv = True
                    b_jatekos_pos = b_jatekos_pos_aktiv
                    if a_jatekos_aktiv:
                        b_jatekos_pontszam += 1
                        pygame.display.set_caption('A kék játékos találatot szerzett')
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                a_jatekos_aktiv = False
                a_jatekos_pos = a_jatekos_pos_alap

            if event.key == pygame.K_SPACE:
                b_jatekos_aktiv = False
                b_jatekos_pos = b_jatekos_pos_alap

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                vege = False
                a_jatekos_pontszam, b_jatekos_pontszam = 0, 0
                for x in x_tengely:
                    screen.blit(green_x_img, (x, y_tengely[0]))
                    screen.blit(green_x_img, (x, y_tengely[1]))
                pygame.display.set_caption('A játék elkezdődött')
                a_jatekos_inaktiv = time.time()
                b_jatekos_inaktiv = time.time()

    pygame.display.update()
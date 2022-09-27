import random

from img_loader import *
pygame.init()
pygame.display.set_caption('A játék elkezdődött')
screen = pygame.display.set_mode((1600, 900))

control_1 = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "left": pygame.K_a,
    "right": pygame.K_d,
}
control_2 = {
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
}
control_3 = {
    "up": pygame.K_u,
    "down": pygame.K_j,
    "left": pygame.K_h,
    "right": pygame.K_k,
}
myfont = pygame.font.Font("../font/VT323-Regular.ttf", 60)


class Player:
    def __init__(self, control):
        self.color = (255, 255, 255)
        self.size = 50
        self.control = control
        if self.control == control_1:
            self.img_copy = pygame.transform.scale(player_1, (self.size*1.5, self.size))
        elif self.control == control_2:
            self.img_copy = pygame.transform.scale(player_2, (self.size * 1.5, self.size))
        else:
            self.img_copy = pygame.transform.scale(player_3, (self.size * 1.5, self.size))
        self.img = self.img_copy
        self.pos = self.x, self.y = 300, 300
        self.pressed = pygame.key.get_pressed()
        self.dead = False
        self.score = myfont.render(str(self.size * 10), True, (200, 200, 200))
        self.score_rect = self.score.get_rect(topleft=(0, 0))
        self.facing = "right"

    def draw(self):
        self.facing_test()
        if not self.dead:
            screen.blit(self.img, (self.x, self.y))
            self.moving()

    def facing_test(self):
        if self.facing == "right":
            self.img = pygame.transform.scale(pygame.transform.flip(self.img_copy, True, False), (self.size*1.5, self.size))
        else:
            self.img = pygame.transform.scale(pygame.transform.flip(self.img_copy, False, False),(self.size * 1.5, self.size))

    def moving(self):
        self.pressed = pygame.key.get_pressed()
        if self.pressed[self.control["left"]] and self.x > 0:
            self.x -= 3
            self.facing = "left"
        if self.pressed[self.control["right"]] and self.x < 1600 - self.size:
            self.x += 3
            self.facing = "right"
        if self.pressed[self.control["up"]] and self.y > 0:
            self.y -= 3
        if self.pressed[self.control["down"]] and self.y < 900 - self.size:
            self.y += 3
        if self.pressed[pygame.K_r]:
            player_1.x, player_2.x, player_3.x, player_1.y, player_2.y, player_3.y = 300, 300, 300, 300, 300, 300
            player_1.size, player_2.size, player_3.size = 50, 50, 50
            player_1.color, player_2.color, player_3.color = (255, 255, 255), (255, 255, 255), (255, 255, 255)
            player_1.dead, player_2.dead, player_3.dead = False, False, False


        self.coll()

    def coll(self):
        for fish in fish_list:
            if abs((fish.x+(fish.size*1.5//2))-(self.x+(self.size*1.5//2))) < self.size//2 + fish.size//2 and abs((fish.y+(fish.size//2))-(self.y+(self.size//2))) < self.size//2 + fish.size//2:
                if self.size > fish.size + 1:
                    fish_list.remove(fish)
                    self.facing_test()
                    self.size += fish.size // 30 + 1
                    self.moving()
                elif fish.size > self.size + 10:
                    self.dead = True
                    self.color = (200, 200, 200)
                else:
                    pass


class Fish:
    def __init__(self):
        if player_3.size < player_1.size > player_2.size:
            self.size_max = player_1.size + 50
        elif player_3.size < player_2.size > player_1.size:
            self.size_max = player_2.size + 50
        else:
            self.size_max = player_3.size + 50
        self.size = random.randint(20, self.size_max)
        self.speed = random.randint(1, 2)
        self.img = pygame.transform.scale(random.choice(fish_img), (self.size*1.5, self.size))
        self.random_num = random.randint(1, 2)
        self.y = random.randint(100, 800)
        fish_list.append(self)
        if self.random_num == 1:
            self.x = -100
            self.move_x = self.speed
            self.img = pygame.transform.flip(self.img, True, False)
        else:
            self.x = 1700
            self.move_x = -self.speed


    def draw(self):
        screen.blit(self.img, (self.x, self.y))
        self.moving()

    def moving(self):
        self.x += self.move_x
        self.out_of_zone()

    def out_of_zone(self):
        if (self.x > 1800 or -200 > self.x) and fish_list.count(self) >= 1:
            fish_list.remove(self)


class FishHorizontal:
    def __init__(self):
        if player_3.size < player_1.size > player_2.size:
            self.size_max = player_1.size + 100
        elif player_3.size < player_2.size > player_1.size:
            self.size_max = player_2.size + 100
        else:
            self.size_max = player_3.size + 50
        self.size = random.randint(50, self.size_max)
        self.speed = random.randint(1, 2)
        if self.speed == 1:
            self.img = pygame.transform.scale(meduza_img, (self.size, self.size*2))
            self.y = 1000
            self.move_y = -self.speed / 3
        else:
            self.img = pygame.transform.scale(octopus_img, (self.size, self.size))
            self.y = -100
            self.move_y = self.speed / 3
        self.x = random.randint(100, 1500)
        fish_hor_list.append(self)


    def draw(self):
        screen.blit(self.img, (self.x, self.y))
        self.moving()

    def moving(self):
        self.y += self.move_y
        self.out_of_zone()

    def out_of_zone(self):
        if (self.y > 1100 or -200 > self.y) and fish_hor_list.count(self) >= 1:
            fish_hor_list.remove(self)



player_1 = Player(control_1)
player_2 = Player(control_2)
player_3 = Player(control_3)

fish_list = []
fish_hor_list = []
fish_timer = 200
fish_hor_timer = 2000
Fish()
FishHorizontal()
map = pygame.transform.scale(pygame.image.load("../images/map/deep.jpg"), (1600, 900))
clock = pygame.time.Clock()
running = True
while running:
    screen.fill((50, 50, 200))
    screen.blit(map, (0, 0))
    player_1.draw()
    player_2.draw()
    player_3.draw()

    score_1 = myfont.render(str(player_1.size * 10), True, player_1.color)
    score_rect_1 = score_1.get_rect(topleft=(10, 0))
    screen.blit(score_1, score_rect_1)
    score_2 = myfont.render(str(player_2.size * 10), True, player_2.color)
    score_rect_2 = score_2.get_rect(topright=(1590, 0))
    screen.blit(score_2, score_rect_2)
    score_3 = myfont.render(str(player_3.size * 10), True, player_3.color)
    score_rect_3 = score_3.get_rect(bottomleft=(10, 900))
    screen.blit(score_3, score_rect_3)

    for fish in fish_list:
        fish.draw()
    for fish in fish_hor_list:
        fish.draw()

    if fish_timer <= 0:
        fish_timer = random.randint(150,250)
        Fish()
    else:
        fish_timer -= 1
    if fish_hor_timer <= 0:
        fish_hor_timer = random.randint(1500,2000)
        FishHorizontal()
    else:
        fish_hor_timer -= 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()

    clock.tick(120)
    pygame.display.flip()

import random

import pygame as pg

pg.init()
pg.display.set_caption("")
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
zombie = pg.image.load('../images/zombie.png')
plant = pg.image.load("../images/plant.png")
sunflower = pg.image.load("../images/sunflower.png")
nut = pg.image.load("../images/walnut.png")
cherry = pg.image.load("../images/cherries.png")
zombies = []
plants = []
sunflowers = []
nuts = []
cherries = []
bullets = []
areas = dict()
for row in range(9):
    for col in range(5):
        areas[f'{row+1} {col+1}'] = False


def bg():
    x, y = 40, 40
    even = True
    for col in range(5):
        for row in range(9):
            if even:
                pg.draw.rect(screen, (100, 200, 100), (x, y, 200, 200))
                even = False
            else:
                pg.draw.rect(screen, (50, 100, 50), (x, y, 200, 200))
                even = True
            x += 200
        x = 40
        y += 200


def main():
    global zombies
    global plants
    global bullets
    global suns
    global player
    global sunflowers
    global nuts
    global cherries
    player = Player()
    clock = pg.time.Clock()
    done = False
    #zombies = [Zombie(), Zombie(), Zombie()]
    #plants = [Plant(1, 1), Plant(1, 2), Plant(1, 3)]
    #areas['1 1'], areas['1 2'], areas['1 3'], areas['1 4'] = True, True, True, True
    #sunflowers = [Sunflower(1,4)]
    #suns = [Sun(300, 300)]
    zombies = []
    plants = []
    sunflowers = []
    nuts = []
    cherries = []
    suns = []
    bullets = []

    FONT = pg.font.Font(None, 32)

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                done = True
        screen.fill((255, 255, 255))
        bg()
        pg.draw.rect(screen, (150, 50, 20), (0, 0, 70, 40), 0)
        pg.draw.rect(screen, (200, 100, 70), (0, 0, 70, 40), 3)
        txt_surface = FONT.render(str(player.sun), True, (0, 0, 0))
        screen.blit(txt_surface, (10, 10))
        for zombie in zombies:
            zombie.draw()
            zombie.moving()
            zombie.die()
            zombie.eat()
        for plant in plants:
            plant.draw()
            plant.shoot()
            plant.die()
        for bullet in bullets:
            bullet.draw()
            bullet.moving()
        for sun in suns:
            sun.draw()
            sun.pick_up(event)
            sun.disapear()
        for sunflower in sunflowers:
            sunflower.draw()
            sunflower.sun()
            sunflower.die()
        for nut in nuts:
            nut.draw()
            nut.die()
        for cherry in cherries:
            cherry.draw()
            cherry.blow()
        player.planting(event)
        pg.draw.rect(screen, (50, 50, 50), (0, 100, 40, 40), 0)
        pg.draw.rect(screen, (80, 50, 20), (0, 150, 40, 40), 0)
        pg.draw.rect(screen, (180, 100, 90), (0, 200, 40, 40), 0)
        pg.draw.rect(screen, (220, 50, 50), (0, 250, 40, 40), 0)
        player.plant_choose(event)
        player.new_zombies()
        pg.display.flip()
        clock.tick(30)


class Player:
    def __init__(self):
        self.zombie_counter_max = 500
        self.zombie_counter = self.zombie_counter_max
        self.sun = 50
        self.planting_point = [0, 0]
        self.choosen_plant = "sunflower"
        self.choosen_plant_object = Plant(self.planting_point[0], self.planting_point[1])
        self.choosen_plant_list = plants
        self.mouse = (0, 0)

    def planting(self, event):
        self.plant_choosing()
        if event.type == pg.MOUSEBUTTONUP:
            self.mouse = pg.mouse.get_pos()
            if 40 < self.mouse[0] < 200 * 9 and 40 < self.mouse[1] < 200 * 5:
                self.planting_point = [(self.mouse[0] - 40) // 200 + 1, (self.mouse[1] - 40) // 200 + 1]
                self.plant_choosing()
                if self.sun >= self.choosen_plant_object.cost and not areas[f'{self.planting_point[0]} {self.planting_point[1]}']:
                    self.choosen_plant_list.append(self.choosen_plant_object)
                    self.sun -= self.choosen_plant_object.cost
                    areas[f'{self.planting_point[0]} {self.planting_point[1]}'] = True

    def plant_choose(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            self.mouse = pg.mouse.get_pos()
            if 0 < self.mouse[0] < 40 and 100 < self.mouse[1] < 140:
                self.choosen_plant = "plant"
            elif 0 < self.mouse[0] < 40 and 150 < self.mouse[1] < 190:
                self.choosen_plant = "sunflower"
            elif 0 < self.mouse[0] < 40 and 200 < self.mouse[1] < 240:
                self.choosen_plant = "nut"
            elif 0 < self.mouse[0] < 40 and 250 < self.mouse[1] < 290:
                self.choosen_plant = "cherry"

    def plant_choosing(self):
        if self.choosen_plant == "plant":
            self.choosen_plant_object = Plant(self.planting_point[0], self.planting_point[1])
            self.choosen_plant_list = plants
        elif self.choosen_plant == "sunflower":
            self.choosen_plant_object = Sunflower(self.planting_point[0], self.planting_point[1])
            self.choosen_plant_list = sunflowers
        elif self.choosen_plant == "nut":
            self.choosen_plant_object = Nut(self.planting_point[0], self.planting_point[1])
            self.choosen_plant_list = nuts
        elif self.choosen_plant == "cherry":
            self.choosen_plant_object = Cherry(self.planting_point[0], self.planting_point[1])
            self.choosen_plant_list = cherries

    def list_return(self):
        global plants
        global sunflowers
        global nuts
        global cherries
        if self.choosen_plant == "plant":
            plants = self.choosen_plant_list
        elif self.choosen_plant == "sunflower":
            sunflowers = self.choosen_plant_list
        elif self.choosen_plant == "nut":
            nuts = self.choosen_plant_list
        elif self.choosen_plant == "cherries":
            cherries = self.choosen_plant_list

    def new_zombies(self):
        if self.zombie_counter <= 0:
            zombies.append(Zombie())
            self.zombie_counter = self.zombie_counter_max
            self.zombie_counter_max -= 10
        self.zombie_counter -= 1


class Sun:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x-30, self.y-30, 60, 60)
        self.lifetime = 500

    def draw(self):
        pg.draw.circle(screen, (250, 250, 0), (self.x, self.y), 30)

    def pick_up(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                suns.remove(self)
                player.sun += 50

    def disapear(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            suns.remove(self)


class Zombie:
    def __init__(self):
        self.img = zombie
        self.x = 1800
        self.y = random.randint(1, 5)
        self.hp = 10

    def moving(self):
        self.x -= 1

    def draw(self):
        screen.blit(self.img, (self.x, self.y * 200 - 100))

    def die(self):
        for bullet in bullets:
            if bullet.y // 200 + 1 == self.y and abs(bullet.x - self.x) < 5:
                self.hp -= 1
                bullets.remove(bullet)
        if self.hp <= 0:
            zombies.remove(self)

    def eat(self):
        for plant in plants:
            if self.y == plant.y and -100 < self.x - plant.x*200 + 50 < 5:
                self.x += 1
        for sunflower in sunflowers:
            if self.y == sunflower.y and -100 < self.x - sunflower.x*200 + 50 < 5:
                self.x += 1
        for nut in nuts:
            if self.y == nut.y and -100 < self.x - nut.x*200 + 50 < 5:
                self.x += 1


class Plant:
    def __init__(self, x, y):
        self.img = plant
        self.x = x
        self.y = y
        self.reload_time = 90
        self.reloading = 30
        self.cost = 100
        self.hp = 100

    def draw(self):
        screen.blit(self.img, (self.x * 200 - 100, self.y * 200 - 100))

    def shoot(self):
        for zombie in zombies:
            if zombie.y == self.y and self.reloading < 0 and zombie.x > self.x * 200:
                bullets.append(Bullet(self.x * 200 + 32 - 100, self.y * 200 + 32 - 100))
                self.reloading = self.reload_time
        self.reload()

    def reload(self):
        self.reloading -= 1

    def die(self):
        for zombie in zombies:
            if zombie.y == self.y and -100 < zombie.x - self.x*200 + 50 < 6:
                self.hp -= 1
        if self.hp <= 0:
            plants.remove(self)
            areas[f'{self.x} {self.y}'] = False


class Sunflower:
    def __init__(self, x, y):
        self.img = sunflower
        self.x = x
        self.y = y
        self.reload_time = 300
        self.reloading = self.reload_time
        self.cost = 50
        self.hp = 50

    def draw(self):
        screen.blit(self.img, (self.x * 200 - 100, self.y * 200 - 100))

    def sun(self):
        if self.reloading < 0:
            suns.append(Sun(self.x * 200 - 100, self.y * 200 - 100))
            self.reloading = self.reload_time
        self.reload()

    def reload(self):
        self.reloading -= 1

    def die(self):
        for zombie in zombies:
            if zombie.y == self.y and -100 < zombie.x - self.x*200 + 50 < 6:
                self.hp -= 1
        if self.hp <= 0:
            sunflowers.remove(self)
            areas[f'{self.x} {self.y}'] = False


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.damage = 1

    def draw(self):
        pg.draw.circle(screen, (0, 200, 0), (self.x, self.y), 10, 0)

    def moving(self):
        self.x += 10


class Nut:
    def __init__(self, x, y):
        self.img = nut
        self.x = x
        self.y = y
        self.cost = 50
        self.hp = 1000

    def draw(self):
        screen.blit(self.img, (self.x * 200 - 100, self.y * 200 - 100))

    def die(self):
        for zombie in zombies:
            if zombie.y == self.y and -100 < zombie.x - self.x*200 + 50 < 6:
                self.hp -= 1
        if self.hp <= 0:
            nuts.remove(self)
            areas[f'{self.x} {self.y}'] = False


class Cherry:
    def __init__(self, x, y):
        self.img = cherry
        self.x = x
        self.y = y
        self.cost = 150
        self.clock = 100

    def draw(self):
        screen.blit(self.img, (self.x * 200 - 100, self.y * 200 - 100))

    def blow(self):
        if self.clock <= 0:
            for zombie in zombies:
                if abs(self.y - zombie.y) <= 1 and abs(self.x*200-zombie.x) <= 200:
                    zombie.hp = 0
            cherries.remove(self)
            areas[f'{self.x} {self.y}'] = False
        else:
            self.clock -= 1


if __name__ == '__main__':
    main()
    pg.quit()

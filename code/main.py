import random
from math import *
import pygame as pg
import pygame.image

pg.init()
pg.display.set_caption("")
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
infoObject = pygame.display.Info()


class Player:
    def __init__(self):
        self.mode = "idle"
        self.x = 50
        self.y = infoObject.current_h - 500
        self.max_hp = 100
        self.hp = self.max_hp
        self.real_hp = self.hp
        self.max_mana = 100
        self.mana = self.max_mana
        self.real_mana = self.mana
        self.base_dam = 10
        self.real_dam = self.base_dam
        self.dam_buff = []
        self.dam_buff_time = []
        self.img = []
        self.attack_img = []
        self.run_img = []
        self.run_back_img = []
        self.poison_dam = []
        self.poison_time = []
        for num in range(9):
            self.img.append(pygame.transform.scale(pygame.image.load(f"../images/png/Idle ({num+1}).png"),(300,350)))
        for num in range(9):
            self.attack_img.append(pygame.transform.scale(pygame.image.load(f"../images/png/Attack ({num+1}).png"),(300,350)))
        for num in range(9):
            self.run_img.append(pygame.transform.scale(pygame.image.load(f"../images/png/Run ({num+1}).png"),(300,350)))
        for num in range(9):
            self.run_back_img.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"../images/png/Run ({num+1}).png"),(300,350)),True, False))
        self.current_img = 0
        self.current_attack_img = 0
        self.current_run_img = 0
        self.current_run_back_img = 0

    def draw(self):
        if self.mode == "idle":
            screen.blit(self.img[int(self.current_img)], (self.x, self.y))
            self.current_img += 0.3
            if self.current_img >= 9:
                self.current_img = 0
        elif self.mode == "run":
            if self.x + 320 < enemy.x:
                self.x += 25
            else:
                self.mode = "attack"
            screen.blit(self.run_img[int(self.current_run_img)], (self.x, self.y))
            self.current_run_img += 0.3
            if self.current_run_img >= 9:
                self.current_run_img = 0
        elif self.mode == "attack":
            screen.blit(self.attack_img[int(self.current_attack_img)], (self.x, self.y))
            self.current_attack_img += 0.3
            if self.current_attack_img >= 8:
                self.current_attack_img = 0
                self.mode = "run_back"
        elif self.mode == "run_back":
            if self.x >= 50:
                self.x -= 25
            else:
                self.mode = "idle"
            screen.blit(self.run_back_img[int(self.current_run_back_img)], (self.x, self.y))
            self.current_run_back_img += 0.3
            if self.current_run_back_img >= 9:
                self.current_run_back_img = 0

    def bar_draw(self):
        pygame.draw.rect(screen, (139,69,19), (0, infoObject.current_h-150, infoObject.current_w, 150))

        pygame.draw.rect(screen, (170, 0, 0), (10, infoObject.current_h-60, 300, 50), 0)
        pygame.draw.rect(screen, (0, 170, 0), (10, infoObject.current_h-130, 300, 50), 0)

        pygame.draw.rect(screen, (230, 23, 23), (10, infoObject.current_h - 60, self.hp/self.max_hp*300, 50), 0)
        pygame.draw.rect(screen, (230,230,230), (10, infoObject.current_h-60, 300, 50), 5)

        pygame.draw.rect(screen, (23, 230, 23), (10, infoObject.current_h - 130, self.mana/self.max_mana*300, 50), 0)
        pygame.draw.rect(screen, (230,230,230), (10, infoObject.current_h-130, 300, 50), 5)



        if self.real_hp < self.hp:
            self.hp -= self.max_hp / 100
        elif self.real_hp != self.hp:
            self.hp = self.real_hp

        if self.real_mana < self.mana:
            self.mana -= self.max_mana / 100
        elif self.real_mana != self.mana:
            self.mana = self.real_mana

        if self.hp <= 0:
            exit()

    def too_much(self):
        if self.mana > self.max_mana:
            self.mana = self.max_mana
        if self.hp > self.max_hp:
            self.hp = self.max_hp


    def buff_and_debuff(self):
        if len(self.poison_time) > 0:
            for index in range(len(self.poison_time)):
                if self.poison_time[index] > 0:
                    self.hp -= self.poison_dam[index]
                    self.poison_time[index] -= 1
        if len(self.dam_buff_time) > 0:
            for index in range(len(self.dam_buff_time)):
                if self.dam_buff_time[index] > 0:
                    self.hp -= self.poison_dam[index]
                    self.poison_time[index] -= 1


class Skill:
    def __init__(self, img, place, dam, mana_cost, regen, poison_dam, poison_time, remove_effect, dam_buff, dam_buff_time):
        self.used = False
        self.img = pygame.transform.scale(pygame.image.load(f"../images/skills/{img}.png"), (100, 100))
        self.place = place
        self.dam = dam
        self.mana_cost = mana_cost
        self.regen = regen
        self.poison_dam = poison_dam
        self.poison_time = poison_time
        self.remove_effect = remove_effect
        self.dam_buff = dam_buff
        self.dam_buff_time = dam_buff_time
        self.mouse = pygame.mouse.get_pos()
        self.in_use = False

    def draw(self):
        screen.blit(self.img, (self.place*120 + 220, infoObject.current_h-120))

    def action(self):
        if player.mode == "idle" and not self.in_use:
            self.mouse = pygame.mouse.get_pos()
            if self.place * 120 + 220 < self.mouse[0] < self.place * 120 + 320 and infoObject.current_h-120 < self.mouse[1] < infoObject.current_h-20:
                self.in_use = True
                player.mode = "run"

    def use(self):
        if player.mode == "attack" and self.in_use and player.current_attack_img > 5:
            if player.mana >= self.mana_cost:
                if player.base_dam * self.dam > 0:
                    enemy.real_hp -= player.base_dam * self.dam
                player.real_mana -= self.mana_cost
                player.real_hp += self.regen
                if self.regen > 0:
                    fonts.append(DamageNum(self.regen, player.x+250, player.y-50, "regen"))
                if self.poison_time != 0:
                    enemy.poison_time.append(self.poison_time)
                    enemy.poison_dam.append(self.poison_dam)
                if self.remove_effect:
                    player.poison_dam.clear()
                    player.poison_time.clear()
                self.in_use = False
                self.used = True
                fonts.append(DamageNum(player.base_dam * self.dam, player.x+250, player.y))


class EnemySkill:
    def __init__(self, img, place, dam, mana_cost, regen, poison_dam, poison_time, remove_effect, dam_buff, dam_buff_time):
        self.used = False
        self.img = pygame.transform.scale(pygame.image.load(f"../images/skills/{img}.png"), (100, 100))
        self.place = place
        self.dam = dam
        self.mana_cost = mana_cost
        self.regen = regen
        self.poison_dam = poison_dam
        self.poison_time = poison_time
        self.remove_effect = remove_effect
        self.dam_buff = dam_buff
        self.dam_buff_time = dam_buff_time
        self.mouse = pygame.mouse.get_pos()
        self.in_use = False

    def use(self):
        if enemy.mode == "attack" and self.in_use and enemy.current_attack_img > 5:
            if enemy.mana >= self.mana_cost:
                if enemy.base_dam * self.dam > 0:
                    player.real_hp -= player.base_dam * self.dam
                enemy.real_mana -= self.mana_cost
                enemy.real_hp += self.regen
                if self.regen > 0:
                    fonts.append(DamageNum(self.regen, enemy.x, enemy.y-50, "regen"))
                if self.poison_time != 0:
                    player.poison_time.append(self.poison_time)
                    player.poison_dam.append(self.poison_dam)
                if self.remove_effect:
                    enemy.poison_dam.clear()
                    enemy.poison_time.clear()
                self.in_use = False
                self.used = True
                fonts.append(DamageNum(enemy.base_dam * self.dam, enemy.x, enemy.y))


class Enemy:
    def __init__(self):
        self.x = infoObject.current_w - 350
        self.y = infoObject.current_h - 500
        self.mode = "idle"
        self.max_hp = 50
        self.hp = self.max_hp
        self.real_hp = self.hp
        self.max_mana = 50
        self.mana = self.max_mana
        self.real_mana = self.mana
        self.base_dam = 7
        self.poison_dam = []
        self.poison_time = []
        self.img = []
        self.attack_img = []
        self.run_img = []
        self.run_back_img = []
        for num in range(9):
            self.run_img.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"../images/png/Run ({num+1}).png"),(300,350)),True, False))
        for num in range(9):
            self.attack_img.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"../images/png/Attack ({num+1}).png"),(300,350)),True, False))
        for num in range(9):
            self.run_back_img.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"../images/png/Run ({num+1}).png"),(300,350)),False, False))
        for num in range(9):
            self.img.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"../images/png/Idle ({num+1}).png"),(300,350)),True, False))
        self.current_img = 0
        self.current_attack_img = 0
        self.current_run_img = 0
        self.current_run_back_img = 0

    def draw(self):
        if self.mode == "idle":
            screen.blit(self.img[int(self.current_img)], (self.x, self.y))
            self.current_img += 0.3
            if self.current_img >= 9:
                self.current_img = 0
        elif self.mode == "run":
            if self.x > player.x + 320:
                self.x -= 25
            else:
                self.mode = "attack"
            screen.blit(self.run_img[int(self.current_run_img)], (self.x, self.y))
            self.current_run_img += 0.3
            if self.current_run_img >= 9:
                self.current_run_img = 0
        elif self.mode == "attack":
            screen.blit(self.attack_img[int(self.current_attack_img)], (self.x, self.y))
            self.current_attack_img += 0.3
            if self.current_attack_img >= 8:
                self.current_attack_img = 0
                self.mode = "run_back"
        elif self.mode == "run_back":
            if self.x <= infoObject.current_w - 350:
                self.x += 25
            else:
                self.mode = "idle"
            screen.blit(self.run_back_img[int(self.current_run_back_img)], (self.x, self.y))
            self.current_run_back_img += 0.3
            if self.current_run_back_img >= 9:
                self.current_run_back_img = 0

    def bar_draw(self):
        pygame.draw.rect(screen, (170, 0, 0), (infoObject.current_w-310, infoObject.current_h - 60, 300, 50), 0)
        pygame.draw.rect(screen, (0, 170, 0), (infoObject.current_w-310, infoObject.current_h - 130, 300, 50), 0)

        pygame.draw.rect(screen, (230, 23, 23), (infoObject.current_w-310, infoObject.current_h - 60, self.hp/self.max_hp*300, 50), 0)
        pygame.draw.rect(screen, (230,230,230), (infoObject.current_w-310, infoObject.current_h-60, 300, 50), 5)

        pygame.draw.rect(screen, (23, 230, 23), (infoObject.current_w-310, infoObject.current_h - 130, self.mana/self.max_mana*300, 50), 0)
        pygame.draw.rect(screen, (230,230,230), (infoObject.current_w-310, infoObject.current_h-130, 300, 50), 5)

        if self.real_hp < self.hp:
            self.hp -= self.max_hp / 100
        elif self.real_hp != self.hp:
            self.hp = self.real_hp

        if self.real_mana < self.mana:
            self.mana -= self.max_mana / 100
        elif self.real_mana != self.mana:
            self.mana = self.real_mana

        if self.hp <= 0:
            exit()

    def too_much(self):
        if self.mana > self.max_mana:
            self.mana = self.max_mana
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def poison(self):
        if len(self.poison_time) > 0:
            for index in range(len(self.poison_time)):
                if self.poison_time[index] > 0:
                    self.hp -= self.poison_dam[index]
                    self.poison_time[index] -= 1


class DamageNum:
    def __init__(self, damage, x, y, type="damage"):
        self.damage = damage
        self.type = type
        self.size = 50
        self.color = (150,20,20)
        if type == "regen":
            self.color = (150, 255, 150)
        self.font = pg.font.Font(None, self.size)
        self.text = self.font.render(str(self.damage), True, self.color)
        self.life = 45
        self.pos = [x, y]

    def draw(self):
        if self.life > 0:
            screen.blit(self.text, (int(self.pos[0]), int(self.pos[1])))
            self.life -= 1
            self.pos[1] -= 1
            self.pos[0] += 0.25
            self.size -= 0.7
            self.font = pg.font.Font(None, int(self.size))
            self.text = self.font.render(str(self.damage), True, self.color)
        else:
            fonts.remove(self)


fonts=[]

player = Player()
enemy = Enemy()


# img, place, dam, mana_cost, regen, poison_dam, poison_time
all_skills = []


def all_skill():
    all_skills.append(Skill(img=1,place=1,dam=1,mana_cost=0,regen=0,poison_dam=10,poison_time=2, remove_effect=False, dam_buff=1, dam_buff_time=1)) # basic hit
    all_skills.append(Skill(img=2,place=1,dam=2,mana_cost=20,regen=0,poison_dam=0,poison_time=0, remove_effect=True, dam_buff=1, dam_buff_time=2)) # rage
    all_skills.append(Skill(img=3,place=1,dam=3,mana_cost=50,regen=10,poison_dam=0,poison_time=0, remove_effect=False, dam_buff=1, dam_buff_time=1)) # strike
    all_skills.append(Skill(img=4,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=5,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=6,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=7,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=8,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=9,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=10,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=11,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=12,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=13,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=14,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=15,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=16,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=17,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=18,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=19,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=20,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=21,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=22,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=23,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=24,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=25,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=26,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=27,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=28,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=29,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=30,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=31,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=32,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=33,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=34,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=35,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=36,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=37,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=38,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=39,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=40,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=41,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=42,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=43,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=44,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=45,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=46,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=47,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))
    all_skills.append(Skill(img=48,place=1,dam=1,mana_cost=10,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1))


all_skill()

skills = [all_skills[0], all_skills[1], all_skills[2]]
skills[0].place = 1
skills[1].place = 2
skills[2].place = 3

enemy_skills = [EnemySkill(img=1,place=1,dam=2,mana_cost=20,regen=0,poison_dam=10,poison_time=3, remove_effect=False, dam_buff=1, dam_buff_time=1), EnemySkill(img=10,place=2,dam=1,mana_cost=0,regen=0,poison_dam=0,poison_time=0, remove_effect=False, dam_buff=1, dam_buff_time=1), EnemySkill(img=16,place=3,dam=3,mana_cost=30,regen=0,poison_dam=0,poison_time=0, remove_effect=False, dam_buff=1, dam_buff_time=1)]


def main():
    turn = random.choice(["player", "enemy"])
    turn_once = True
    clock = pg.time.Clock()
    done = False
    FONT = pg.font.Font(None, 32)
    bg = pygame.transform.scale(pygame.image.load("../images/bg.jpg"), (infoObject.current_w * 2, infoObject.current_h))

    while not done:
        screen.fill((35, 35, 35))
        screen.blit(bg, (-1000,-130))
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN and turn == "player":
                for skill in skills:
                    skill.action()

        player.draw()
        player.bar_draw()
        player.too_much()

        enemy.draw()
        enemy.bar_draw()
        enemy.too_much()

        for skill in skills:
            skill.draw()
            skill.use()
            if skill.used and player.mode == "idle":
                turn = "enemy"
                skill.used = False


        if turn == "enemy":
            for skill in enemy_skills:
                skill.use()
                if skill.used and enemy.mode == "idle":
                    skill.used = False
                    turn = "player"
                    turn_once = True


        if turn == "enemy" and turn_once:
            random_skill = random.choice(enemy_skills)
            while not (random_skill.mana_cost <= enemy.mana):
                random_skill = random.choice(enemy_skills)
            random_skill.in_use = True
            enemy.mode = "run"
            turn_once = False

        for font in fonts:
            font.draw()

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()

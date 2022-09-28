import random
from pygame import mixer
import pygame
pygame.init()
pygame.display.set_caption('A játék elkezdődött')
screen = pygame.display.set_mode((1000, 1000))
snake_body = pygame.image.load("../images/body.png")
snake_body_x = pygame.image.load("../images/body_x.png")
snake_body_ne = pygame.image.load("../images/body_leftup.png")
snake_body_nw = pygame.image.load("../images/body_rightup.png")
snake_body_se = pygame.image.load("../images/body_leftdown.png")
snake_body_sw = pygame.image.load("../images/body_rightdown.png")
sneak_head_e = pygame.image.load("../images/head_right.png")
sneak_head_n = pygame.image.load("../images/head_up.png")
sneak_head_w = pygame.image.load("../images/head_left.png")
sneak_head_s = pygame.image.load("../images/head_down.png")
apple = pygame.image.load("../images/apple.png")
pineapple = pygame.image.load("../images/pineapple.png")
pear = pygame.image.load("../images/pear.png")
fruits = [apple, pineapple, pear]

click = mixer.Sound('../audio/click.wav')
pick_up = mixer.Sound('../audio/pick up.wav')
victory = mixer.Sound('../audio/win.wav')
sound_list = (click, pick_up, victory)


class Food:
    def __init__(self):
        self.x = random.randint(1, 19)
        self.y = random.randint(1, 19)
        self.img = random.choice(fruits)

    def draw(self):
        for num in range(snake.length):
            if snake.prew_pos_x[-(num+1)] == self.x and snake.prew_pos_y[-(num+1)] == self.y:
                self.x = random.randint(1, 19)
                self.y = random.randint(1, 19)
        screen.blit(self.img, (self.x*50, self.y*50))


class SnakeBody:
    def __init__(self, x, y, num, facing):
        self.x = x
        self.y = y
        self.num = num
        self.facing = facing

    def draw(self):
        if self.facing == "up" or self.facing == "down":
            screen.blit(snake_body, (round(self.x)*50, round(self.y)*50))
        elif self.facing == "left" or self.facing == "right":
            screen.blit(snake_body_x, (round(self.x)*50, round(self.y)*50))
        elif self.facing == "ne":
            screen.blit(snake_body_ne, (round(self.x) * 50, round(self.y) * 50))
        elif self.facing == "se":
            screen.blit(snake_body_se, (round(self.x) * 50, round(self.y) * 50))
        elif self.facing == "nw":
            screen.blit(snake_body_nw, (round(self.x) * 50, round(self.y) * 50))
        elif self.facing == "sw":
            screen.blit(snake_body_sw, (round(self.x) * 50, round(self.y) * 50))


class Snake:
    def __init__(self):
        self.prew_pos_x = []
        self.prew_pos_y = []
        self.prew_facing = []
        self.x = 10
        self.y = 10
        self.x_pos = round(self.x) * 50
        self.y_pos = round(self.y) * 50
        self.keys = {
            "up": pygame.K_w,
            "down": pygame.K_s,
            "left": pygame.K_a,
            "right": pygame.K_d,
        }
        self.pressed = pygame.key.get_pressed()
        self.facing = "left"
        self.speed = 5
        self.length = 0
        self.food = False

    def draw(self):
        self.death()
        self.control()
        self.move()
        self.eat()
        self.out()
        self.prew_pos_x.append(round(self.x))
        self.prew_pos_y.append(round(self.y))
        self.prew_facing.append(self.facing)
        if self.length == 0:
            if self.prew_facing[-1] == "left":
                screen.blit(sneak_head_w, (self.x_pos + 3, self.y_pos + 2))
            elif self.prew_facing[-1] == "up":
                screen.blit(sneak_head_n, (self.x_pos - 1, self.y_pos + 3))
            elif self.prew_facing[-1] == "right":
                screen.blit(sneak_head_e, (self.x_pos - 3, self.y_pos + 2))
            elif self.prew_facing[-1] == "down":
                screen.blit(sneak_head_s, (self.x_pos - 1, self.y_pos - 3))
        else:
            if self.prew_pos_x[-2] == self.prew_pos_x[-1] and self.prew_pos_y[-2] == self.prew_pos_y[-1]:
                self.prew_pos_x.pop()
                self.prew_pos_y.pop()
                self.prew_facing.pop()
            if self.prew_facing[-2] == "down" and self.prew_facing[-1] == "left" or self.prew_facing[-2] == "right" and self.prew_facing[-1] == "up":
                self.prew_facing[-2] = "ne"
            elif self.prew_facing[-2] == "down" and self.prew_facing[-1] == "right" or self.prew_facing[-2] == "left" and self.prew_facing[-1] == "up":
                self.prew_facing[-2] = "nw"
            elif self.prew_facing[-2] == "up" and self.prew_facing[-1] == "left" or self.prew_facing[-2] == "right" and self.prew_facing[-1] == "down":
                self.prew_facing[-2] = "se"
            elif self.prew_facing[-2] == "up" and self.prew_facing[-1] == "right" or self.prew_facing[-2] == "left" and self.prew_facing[-1] == "down":
                self.prew_facing[-2] = "sw"

            if self.prew_facing[-2] == "left":
                screen.blit(sneak_head_w, (self.x_pos + 3, self.y_pos + 2))
            elif self.prew_facing[-2] == "up":
                screen.blit(sneak_head_n, (self.x_pos - 1, self.y_pos + 3))
            elif self.prew_facing[-2] == "right":
                screen.blit(sneak_head_e, (self.x_pos - 3, self.y_pos + 2))
            elif self.prew_facing[-2] == "down":
                screen.blit(sneak_head_s, (self.x_pos - 1, self.y_pos - 3))
            else:
                if self.prew_facing[-1] == "left":
                    screen.blit(sneak_head_w, (self.x_pos + 3, self.y_pos + 2))
                elif self.prew_facing[-1] == "up":
                    screen.blit(sneak_head_n, (self.x_pos - 1, self.y_pos + 3))
                elif self.prew_facing[-1] == "right":
                    screen.blit(sneak_head_e, (self.x_pos - 3, self.y_pos + 2))
                elif self.prew_facing[-1] == "down":
                    screen.blit(sneak_head_s, (self.x_pos - 1, self.y_pos - 3))

            for num in range(self.length+1):
                SnakeBody(self.prew_pos_x[-(num+2)], self.prew_pos_y[-(num+2)], num+1, self.prew_facing[-(num+2)]).draw()

        if not self.food:
            self.food = Food()
        self.food.draw()

    def control(self):
        self.pressed = pygame.key.get_pressed()
        if self.pressed[self.keys["left"]] and self.facing != "right":
            self.facing = "left"
        if self.pressed[self.keys["right"]] and self.facing != "left":
            self.facing = "right"
        if self.pressed[self.keys["up"]] and self.facing != "down":
            self.facing = "up"
        if self.pressed[self.keys["down"]] and self.facing != "up":
            self.facing = "down"

    def move(self):
        if self.facing == "up":
            self.y -= self.speed / 100
        if self.facing == "down":
            self.y += self.speed / 100
        if self.facing == "left":
            self.x -= self.speed / 100
        if self.facing == "right":
            self.x += self.speed / 100
        self.x_pos = round(self.x) * 50
        self.y_pos = round(self.y) * 50

    def out(self):
        if round(self.x) > 19:
            self.x = 0
        elif round(self.x) < 0:
            self.x = 19
        elif round(self.y) > 19:
            self.y = 0
        elif round(self.y) < 0:
            self.y = 19

    def eat(self):
        if self.food:
            if round(self.x) == self.food.x and round(self.y) == self.food.y:
                self.food = False
                self.length += 1
                self.speed += 0.1
                pick_up.play()

    def death(self):
        for num in range(self.length):
            if round(self.x) == self.prew_pos_x[-(num+2)] and round(self.y) == self.prew_pos_y[-(num+2)]:
                exit()


def bg():
    rect_x = 0
    rect_y = 0
    even = False
    even_start = True
    for row in range(50):
        for col in range(50):
            if even:
                pygame.draw.rect(screen, (0, 245, 0), (rect_x, rect_y, 50, 50), 0)
                even = False
            else:
                pygame.draw.rect(screen, (0, 225, 0), (rect_x, rect_y, 50, 50), 0)
                even = True
            rect_y += 50
        rect_x += 50
        rect_y = 0
        if even_start:
            even = True
            even_start = False
        else:
            even = False
            even_start = True


snake = Snake()
running = True
while running:
    bg()
    snake.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()


    pygame.display.update()

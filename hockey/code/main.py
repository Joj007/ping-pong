import random
from math import *
import pygame as pg
import time
from settings import *

pg.init()
pg.display.set_caption("")
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

# group setup
all_sprites = pg.sprite.Group()
ball_sprites = pg.sprite.Group()
player_sprites = pg.sprite.Group()
effect_sprites = pg.sprite.Group()


class Player(pg.sprite.Sprite):
    def __init__(self, groups, pos, size, control):
        super().__init__(groups)

        self.color = BASE_COLOR
        self.shooting_power = BASE_SHOOTING_POWER

        # image
        self.size = BASE_SIZE
        self.image = pg.Surface((BASE_THICKNESS, self.size))
        self.image.fill(self.color)

        # position
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()

        # movement
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.direction = pg.math.Vector2()
        self.speed = BASE_SPEED
        self.control = control

        self.points = 0
        self.score_limit = SCORE_LIMIT

        # fonts
        self.font = pg.font.Font(None, SCORE_FONT_SIZE)
        self.font_bonus = pg.font.Font(None, BONUS_FONT_SIZE)
        self.font_limit = pg.font.Font(None, SCORE_LIMIT_FONT_SIZE)
        self.text = self.font.render(str(self.points), True, SCORE_FONT_COLOR)
        self.text_limit = self.font_limit.render(str(self.score_limit) + "/", True, SCORE_FONT_COLOR)
        if self.pos[0] < 1000:
            self.text_rect = self.text.get_rect(center=(SCREEN_W_HALF - SCORE_FONT_MARGIN, SCORE_FONT_HEIGHT))
        else:
            self.text_rect = self.text.get_rect(center=(SCREEN_W_HALF + SCORE_FONT_MARGIN, SCORE_FONT_HEIGHT))
        self.text_limit_rect = self.text.get_rect(bottomright=(self.text_rect.left, self.text_rect.bottom + SCORE_LIMIT_FONT_SIZE))



        self.ball_color = random.choice(BALL_COLORS)

        self.good_luck = random.randint(0, 4)
        self.bad_luck = random.randint(0, 4)
        self.bonuses = ["", ""]
        self.luck()

    def luck(self):
        if self.good_luck == 0:
            self.size *= PLUS_SIZE
            self.bonuses[0] = "Méret"
        elif self.good_luck == 1:
            self.speed *= PLUS_SPEED
            self.bonuses[0] = "Sebesség"
        elif self.good_luck == 2:
            self.color[0] += PLUS_COLOR
            self.color[1] += PLUS_COLOR
            self.color[2] += PLUS_COLOR
            self.bonuses[0] = "Szín"
        elif self.good_luck == 3:
            self.shooting_power += PLUS_SHOOTING_POWER
            self.bonuses[0] = "Lövőerő"
        elif self.good_luck == 4:
            self.score_limit -= SCORE_LIMIT//5
            self.bonuses[0] = "Cél pontszám"

        if self.bad_luck == 0:
            self.size /= MINUS_SIZE
            self.bonuses[1] = "Méret"
        elif self.bad_luck == 1:
            self.speed /= MINUS_SPEED
            self.bonuses[1] = "Sebesség"
        elif self.bad_luck == 2:
            self.color[0] -= MINUS_COLOR
            self.color[1] -= MINUS_COLOR
            self.color[2] -= MINUS_COLOR
            self.bonuses[1] = "Szín"
        elif self.bad_luck == 3:
            self.shooting_power -= MINUS_SHOOTING_POWER
            self.bonuses[1] = "Lövőerő"
        elif self.bad_luck == 4:
            self.score_limit += SCORE_LIMIT//5
            self.bonuses[1] = "Cél pontszám"


        self.text_good = self.font_bonus.render(self.bonuses[0], True, BONUS_FONT_COLOR_PLUS)
        if self.pos[0] < 1000:
            self.text_good_rect = self.text.get_rect(center=(SCREEN_W_HALF - BONUS_FONT_MARGIN_OUTER, SCREEN_H))
        else:
            self.text_good_rect = self.text.get_rect(center=(SCREEN_W_HALF + BONUS_FONT_MARGIN_INNER, SCREEN_H))

        self.text_bad = self.font_bonus.render(self.bonuses[1], True, BONUS_FONT_COLOR_MINUS)
        if self.pos[0] < 1000:
            self.text_bad_rect = self.text.get_rect(center=(SCREEN_W_HALF - BONUS_FONT_MARGIN_INNER, SCREEN_H))
        else:
            self.text_bad_rect = self.text.get_rect(center=(SCREEN_W_HALF + BONUS_FONT_MARGIN_OUTER, SCREEN_H))

    def input(self):
        keys = pg.key.get_pressed()

        # movement input
        if keys[self.control[0]]:
            self.direction.y = -1
        elif keys[self.control[1]]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pg.K_d]:
            self.direction.x = 0
        elif keys[pg.K_a]:
            self.direction.x = 0
        else:
            self.direction.x = 0

    def border(self):
        if self.rect.bottom > SCREEN_H:
            self.pos.y = SCREEN_H - self.size
        elif self.rect.top < 0:
            self.pos.y = 0

    def show_points(self):
        screen.blit(self.text, self.text_rect)
        screen.blit(self.text_good, self.text_good_rect)
        screen.blit(self.text_bad, self.text_bad_rect)
        screen.blit(self.text_limit, self.text_limit_rect)

    def game_over(self):

        if self.points >= SCORE_LIMIT and SCORE_LIMIT_BOOL:
            pg.quit()
            exit()

    def update(self, dt):
        self.game_over()
        self.input()
        self.show_points()
        self.border()

        self.text_limit = self.font_limit.render(str(self.score_limit) + "/", True, SCORE_FONT_COLOR)

        self.image = pg.Surface((BASE_THICKNESS, self.size))
        self.image.fill(self.color)

        self.rect = self.image.get_rect(topleft=self.pos)
        self.old_rect = self.rect.copy()


        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)

        self.text = self.font.render(str(self.points), True, SCORE_FONT_COLOR)


class Ball(pg.sprite.Sprite):
    def __init__(self, groups, obstacles, player1, player2):
        super().__init__(groups)
        self.color = BALL_COLOR
        self.image = pg.Surface(BALL_SIZE)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(SCREEN_W_HALF, random.randint(100,SCREEN_H-100)))

        self.wait = BALL_WAIT

        self.pos = pg.math.Vector2(self.rect.topleft)

        self.direction = pg.math.Vector2(random.choice([(1,1),(-1,1),(1,-1),(-1,-1)]))
        self.speed = BASE_SPEED
        self.old_rect = self.rect.copy()

        self.obstacles = obstacles

        self.players = [player1, player2]

        self.effect_num = 0

    def collision(self, direction):
        collision_sprites = pg.sprite.spritecollide(self, self.obstacles, False)

        if collision_sprites:
            if direction == 'horizontal':
                for sprite in collision_sprites:
                    # collision on the right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.x
                        self.direction.x *= -1
                        self.speed = sprite.shooting_power
                        self.color = sprite.ball_color

                    # collision on the left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.x
                        self.direction.x *= -1
                        self.speed = sprite.shooting_power
                        self.color = sprite.ball_color

            if direction == 'vertical':
                for sprite in collision_sprites:
                    # collision on the bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.y
                        self.direction.y *= -1
                        self.speed = sprite.shooting_power
                        self.color = sprite.ball_color

                    # collision on the top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.y
                        self.direction.y *= -1
                        self.speed = sprite.shooting_power
                        self.color = sprite.ball_color

    def window_collision(self, direction):
        if direction == 'horizontal':
            if self.rect.left < 0:
                self.rect.centerx = SCREEN_W_HALF
                self.pos.x = SCREEN_W_HALF - BALL_SIZE[0] / 2
                self.pos.y = random.randint(0+BALL_SIZE[1], SCREEN_H-BALL_SIZE[1])
                self.direction.x *= -1
                self.players[1].points += 1
                self.speed = BALL_SPEED
                self.wait = BALL_WAIT

            if self.rect.right > SCREEN_W:
                self.rect.right = SCREEN_W_HALF
                self.pos.x = SCREEN_W_HALF - BALL_SIZE[0] / 2
                self.pos.y = random.randint(0+BALL_SIZE[1], SCREEN_H-BALL_SIZE[1])
                self.direction.x *= -1
                self.players[0].points += 1
                self.speed = BALL_SPEED
                self.wait = BALL_WAIT

        if direction == 'vertical':
            if self.rect.top < 0:
                self.rect.top = 0
                self.pos.y = self.rect.y
                self.direction.y *= -1
            if self.rect.bottom > SCREEN_H:
                self.rect.bottom = SCREEN_H
                self.pos.y = self.rect.y
                self.direction.y *= -1

    def waiting(self):
        if self.wait < 0:
            self.wait = 0
        elif self.wait > 0:
            self.wait -= 1

    def ball_effect(self):
        if self.effect_num == 50:
            BallEffect([effect_sprites], [self.pos[0]+BALL_SIZE[0]/2, self.pos[1]+BALL_SIZE[1]/2], self.color)
            self.effect_num = 0
        self.effect_num += 1

    def update(self, dt):
        self.waiting()
        self.ball_effect()

        self.image.fill(self.color)

        self.old_rect = self.rect.copy()

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        if self.wait == 0:
            self.pos.x += self.direction.x * self.speed * dt
            self.pos.y += self.direction.y * self.speed * dt

        self.rect.x = round(self.pos.x)
        self.collision('horizontal')
        self.window_collision('horizontal')
        self.rect.y = round(self.pos.y)
        self.collision('vertical')
        self.window_collision('vertical')


class BallEffect(pg.sprite.Sprite):
    def __init__(self, groups, pos, color):
        super().__init__(groups)
        self.random_color = BALL_EFFECT_RANDOM
        if not self.random_color:
            self.color = color
        else:
            self.color = random.choice(BALL_COLORS)
        self.pos = pos
        self.image = pg.Surface((BALL_EFFECT_SIZE, BALL_EFFECT_SIZE))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=pos)
        self.life = BALL_EFFECT_LIFE

    def die(self):
        if self.life <= 0:
            self.kill()

    def update(self, dt):
        self.die()
        self.life -= 1


class Clock:
    def __init__(self):
        self.time_limit_bool = TIME_LIMIT_BOOL
        self.time_limit = TIME_LIMIT * 60
        self.start_time = time.time()
        self.font = pg.font.Font(None, TIME_FONT_SIZE)
        self.text = self.font.render(str(int(self.time_limit - (time.time() - self.start_time))), True, SCORE_FONT_COLOR)
        self.text_rect = self.text.get_rect(center=(TIME_X, TIME_Y))

    def test_game_over(self):
        self.text = self.font.render(str(int(self.time_limit - (time.time() - self.start_time))), True, SCORE_FONT_COLOR)

        if self.time_limit_bool:
            screen.blit(self.text, self.text_rect)
        if self.time_limit_bool and time.time()-self.start_time > self.time_limit:
            pg.quit()
            exit()




def main():


    # loop
    last_time = time.time()


    done = False

    player1 = Player([all_sprites, player_sprites], [100, 100], 150, [pg.K_w, pg.K_s])
    player2 = Player([all_sprites, player_sprites], [pg.display.get_window_size()[0]-100, 100], 150, [pg.K_UP, pg.K_DOWN])
    Ball([all_sprites, ball_sprites], player_sprites, player1, player2)
    Ball([all_sprites, ball_sprites], player_sprites, player1, player2)
    clock = Clock()


    # self, groups, obstacles, player
    while not done:
        # delta time
        dt = time.time() - last_time
        last_time = time.time()

        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                done = True


        screen.fill((35, 35, 35))
        effect_sprites.update(dt)
        all_sprites.update(dt)
        all_sprites.draw(screen)
        clock.test_game_over()

        pg.display.update()


if __name__ == '__main__':
    main()
    pg.quit()

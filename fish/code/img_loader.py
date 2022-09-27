import pygame
screen = pygame.display.set_mode((1600, 900))
player_1 = pygame.image.load("../images/fish/player1.png")
player_2 = pygame.image.load("../images/fish/player2.png")
player_3 = pygame.image.load("../images/fish/player3.png")


fish_img = []
for num in range(12):
    fish_img.append(pygame.image.load(f"../images/fish/hal{num+1}.png").convert_alpha())

meduza_img = pygame.image.load(f"../images/fish/meduza.png").convert_alpha()
octopus_img = pygame.image.load(f"../images/fish/polip.png").convert_alpha()



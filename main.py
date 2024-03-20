import pygame
import sys

from obj_game.Til import Til
from obj_game.tank import Tank
from obj_game.level import Level
from obj_game.enemy_tank import EnemyTank

sys.path.insert(0, 'C:/Battle_City')


pygame.init()

WIDTH, HEIGHT = 435, 435
FPS = 60


window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

bullets = []
objects = []
available_coordinates = []

# Путь к изображению танка
tank_image_path = 'C:/Battle_City/images/tank_1.png'

level = Level(objects, available_coordinates)
tank = Tank('blue', 0, 380, 0,
            (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE),
            tank_image_path, objects)
objects.append(tank)

time = 100
count = 0

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    keys = pygame.key.get_pressed()

    for bullet in bullets:
        bullet.update(objects, bullets, WIDTH, HEIGHT)
    for obj in objects:
        if isinstance(obj, Tank):
            obj.update(keys, bullets, objects, WIDTH, HEIGHT)
        elif isinstance(obj, EnemyTank):
            obj.update(bullets, objects, WIDTH, HEIGHT)

    if time == 0 and sum(1 for obj in objects if isinstance(obj, EnemyTank)) <= 4 and count <= 5:
        objects.append(EnemyTank(available_coordinates, objects, bullets, WIDTH, HEIGHT, '1'))
        time = 200
        count += 1

    window.fill('black')
    for tile in objects:
        if isinstance(tile, Til):
            tile.draw(window)

    for bullet in bullets:
        bullet.draw(window)
    for obj in objects:
        obj.draw(window)

    pygame.display.update()
    clock.tick(FPS)
    time -= 1

pygame.quit()

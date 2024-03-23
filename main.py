import pygame
import sys

from obj_game.Til import Til
from obj_game.tank import Tank
from obj_game.level import Level
from obj_game.enemy_tank import EnemyTank
from obj_game.Eagle import Eagle

sys.path.insert(0, 'C:/Battle_City')


pygame.init()

WIDTH, HEIGHT = 520, 435
FPS = 60
# 1, 5 - обычного танка 5 раз
LEVEL = {
    0: {
        '1': 0,
        '2': 0,
        '3': 1,
        '4': 0,
        '5': 0
    },
    1: {
        '1': 0,
        '2': 0,
        '3': 1,
        '4': 0,
        '5': 0
    },
    2: {
        '1': 0,
        '2': 0,
        '3': 1,
        '4': 0,
        '5': 0
    },
    3: {
        '1': 0,
        '2': 0,
        '3': 1,
        '4': 0,
        '5': 0
    }
}
number_level = 3


window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

bullets = []
objects = []
objects_durable_tiles = []
available_coordinates = []


# Путь к изображению танка игрока
tank_image_path = 'C:/Battle_City/images/tank_player.png'

level = Level(objects, available_coordinates, objects_durable_tiles, number_level)
tank = Tank('blue', 0, 380, 0,
            (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE),
            tank_image_path, objects)
objects.append(tank)

time = 200
count = 0
general_time = 0
current_tank_type = '1'

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    keys = pygame.key.get_pressed()

    general_time += 1

    for bullet in bullets:
        bullet.update(objects, bullets, WIDTH, HEIGHT)
    for obj in objects:
        if isinstance(obj, Tank):
            obj.update(keys, bullets, objects, WIDTH, HEIGHT)
        elif isinstance(obj, EnemyTank):
            obj.update(bullets, objects, general_time)

    while count < LEVEL[number_level][current_tank_type] and count != -1:
        if time == 0:
            objects.append(EnemyTank(available_coordinates, objects, bullets, WIDTH, HEIGHT, current_tank_type))
            count += 1
            time = 600  # устанавливаем интервал времени для следующего создания объекта
        break

    if count >= LEVEL[number_level][current_tank_type]:
        count = 0
        if int(current_tank_type) + 1 < 6:
            current_tank_type = str(int(current_tank_type) + 1)
        else:
            count = -1

    if (sum(1 for obj in objects if isinstance(obj, Tank)) == 0
            or sum(1 for obj in objects if isinstance(obj, Eagle)) <= 3
            or (sum(1 for obj in objects if isinstance(obj, EnemyTank)) == 0 and count == -1)):
        print('GAME OVER')
        break

    window.fill('black')
    for tile in objects:
        if isinstance(tile, Til):
            tile.draw(window)

    for bullet in bullets:
        bullet.draw(window)
    for obj in objects:
        obj.draw(window)
    for obj in objects_durable_tiles:
        obj.draw(window)

    pygame.display.update()
    clock.tick(FPS)
    time -= 1

pygame.quit()

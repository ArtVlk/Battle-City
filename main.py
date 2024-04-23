import random

import pygame
import sys

from random import randint

from obj_game.til import Til
from obj_game.tank import Tank
from obj_game.level import Level
from obj_game.enemy_tank import EnemyTank
from obj_game.eagle import Eagle
from obj_game.bonus import Bonus
from obj_game.menu import Menu

sys.path.insert(0, 'C:/Battle-City_git')

pygame.init()


WIDTH, HEIGHT = 520, 435
FPS = 60
# '1': 5 - обычного танка 5 раз
LEVEL = {
    0: {
        '1': 1,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0
    },
    1: {
        '1': 4,
        '2': 2,
        '3': 1,
        '4': 0,
        '5': 0
    },
    2: {
        '1': 5,
        '2': 0,
        '3': 2,
        '4': 1,
        '5': 1
    },
    3: {
        '1': 0,
        '2': 2,
        '3': 3,
        '4': 2,
        '5': 3
    }
}
number_level = 0

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

bullets = []
objects = []
bonuses = []
objects_durable_tiles = []
available_coordinates = []

# Путь к изображению танка игрока
tank_image_path = 'images\\tank_player.png'

tank = Tank(0, 380, 0,
            (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE),
            tank_image_path, objects)
objects.append(tank)

time = 200
bonusTimer = 600
count = 0
general_time = 0
current_tank_type = '1'

# выбирать стрелочками вверх и вниз
menu = Menu()
menu.append_option('Начать играть', flag=0)
menu.append_option('Выбор уровня',
                   lambda: menu.switch_option(1))
menu.append_option('Выход')
run_level_select = False
run_play = False

play = True
while play:
    window.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                menu.switch_option(-1)
            elif event.key == pygame.K_DOWN:
                menu.switch_option(1)
            elif event.key == pygame.K_RETURN:

                if menu.current_option_index == 1:
                    number_level, play = menu.level_select_window(window)
                    if number_level != -1:
                        run_level_select = True
                        level = Level(objects, available_coordinates,
                                      objects_durable_tiles, number_level)
                        run_play = True
                    else:
                        menu = Menu()
                        menu.append_option('Начать играть', flag=0)
                        menu.append_option('Выбор уровня',
                                           lambda: menu.switch_option(1))
                        menu.append_option('Выход')
                        run_level_select = False
                        run_play = False
                        number_level = 0

                elif menu.current_option_index == 2:
                    play = False

                elif menu.current_option_index == 0:
                    level = Level(objects, available_coordinates,
                                  objects_durable_tiles, number_level)
                    run_play = True
    if not run_play:
        menu.draw(window, 100, 100, 75)

    if run_play:
        keys = pygame.key.get_pressed()

        general_time += 1

        if bonusTimer > 0:
            bonusTimer -= 1
        else:
            tank.moveSpeed = 1
            tank.bulletDamage = 1
            bonus_number = [1, 2, 3, 4, 1, 2, 4, 1, 2, 4]
            bonus_random = random.choice(bonus_number)
            Bonus(randint(50, WIDTH - 50), randint(50, HEIGHT - 50),
                  bonuses, bonus_random)
            bonusTimer = randint(600, 1000)

        for bullet in bullets:
            bullet.update(objects, bonuses, bullets, WIDTH, HEIGHT)
        for bonus in bonuses:
            bonus.update(objects, bonuses)
        for obj in objects:
            if isinstance(obj, Tank):
                obj.update(keys, bullets, objects,
                           bonuses, WIDTH, HEIGHT)
                if not obj and obj.tank_player_live > 0:
                    tank = Tank(0, 380, 0,
                                (pygame.K_a, pygame.K_d,
                                 pygame.K_w, pygame.K_s, pygame.K_SPACE),
                                tank_image_path, objects)
                    objects.append(tank)
            elif isinstance(obj, EnemyTank):
                obj.update(bullets, objects, bonuses, general_time)

        while (count < LEVEL[number_level][current_tank_type]
               and count != -1):
            if time == 0:
                objects.append(EnemyTank(available_coordinates,
                                         objects, bullets,
                                         WIDTH, HEIGHT, current_tank_type))
                count += 1
                # устанавливаем интервал времени для следующего создания
                time = 600

            break

        if count >= LEVEL[number_level][current_tank_type]:
            count = 0
            if int(current_tank_type) + 1 < 6:
                current_tank_type = str(int(current_tank_type) + 1)
            else:
                count = -1

        alive_tanks = sum(1 for obj in objects if isinstance(obj, Tank)
                          and obj.tank_player_live != 0)
        eagle_count = sum(1 for obj in objects if isinstance(obj, Eagle))
        enemy_tank_count = sum(1 for obj in objects
                               if isinstance(obj, EnemyTank))
        if (alive_tanks == 0 or eagle_count <= 3
                or (enemy_tank_count == 0 and count == -1)):

            if alive_tanks != 0 and not run_level_select and eagle_count == 4:
                number_level += 1
                if number_level == 4:
                    window.fill('black')
                    font = pygame.font.SysFont('arial', 50)
                    text_surface = font.render('Winner', True, (255, 255, 255))
                    window.blit(text_surface, (200, 200))
                    pygame.display.flip()
                    pygame.time.delay(3000)
                    menu = Menu()
                    menu.append_option('Начать играть', flag=0)
                    menu.append_option('Выбор уровня',
                                       lambda: menu.switch_option(1))
                    menu.append_option('Выход')
                    run_level_select = False
                    run_play = False
                    number_level = 0
                else:
                    bullets = []
                    objects = []
                    bonuses = []
                    objects_durable_tiles = []
                    available_coordinates = []

                    time = 200
                    bonusTimer = 600
                    count = 0
                    general_time = 0
                    current_tank_type = '1'
                    window = pygame.display.set_mode((WIDTH, HEIGHT))
                    window.fill('black')
                    font = pygame.font.SysFont('arial', 50)

                    text_surface = font.render('Уровень ' + str(number_level), True, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    window.blit(text_surface, text_rect)
                    pygame.display.flip()
                    pygame.time.delay(3000)

                    tank = Tank(0, 380, 0,
                                (pygame.K_a, pygame.K_d, pygame.K_w,
                                 pygame.K_s, pygame.K_SPACE),
                                tank_image_path, objects)
                    objects.append(tank)

                    level = Level(objects, available_coordinates,
                                  objects_durable_tiles, number_level)
            else:
                print("GAME OVER")
                menu = Menu()
                menu.append_option('Начать играть', flag=0)
                menu.append_option('Выбор уровня',
                                   lambda: menu.switch_option(1))
                menu.append_option('Выход')
                run_level_select = False
                run_play = False
                number_level = 0

        for tile in objects:
            if isinstance(tile, Til):
                tile.draw(window)

        for bullet in bullets:
            bullet.draw(window)
        for obj in objects:
            obj.draw(window)
        for obj in objects_durable_tiles:
            obj.draw(window)
        for bonus in bonuses:
            bonus.draw(window)

        clock.tick(FPS)
        time -= 1
    pygame.display.update()

pygame.quit()

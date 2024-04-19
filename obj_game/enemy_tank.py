import pygame
import random

from obj_game.bullet import Bullet
from obj_game.tank import Tank

coordinates_base = [240, 416]
DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]
TILE = 25
DECODING_TANK = {
    '1': 'ordinary_tank',
    '2': 'speed_tank',
    '3': 'armor_tank',
    '4': 'stalker_player_tank',
    '5': 'attacking_base_tank'
}
# Изображение, скорость, что делает, хп, мощь атаки
ENEMY_TANK = {
    "ordinary_tank": ('images\\tank_1.png', 10, 0, 2, 1),
    "speed_tank": ('images\\tank_speed.png', 20, 0, 1, 1),
    "armor_tank": ('images\\tank_armor.png', 10, 0, 5, 3),
    "stalker_player_tank": ('images\\tank_stalker.png', 10, 2, 2, 1),
    "attacking_base_tank": ('images\\tank_base.png', 10, 3, 2, 1)
}


class EnemyTank:
    def __init__(self, level, objects, bullets, width, height, number):
        self.width_window = width
        self.height_window = height

        self.type = 'enemy_tank'
        self.tank = DECODING_TANK[number]
        self.tank_info = ENEMY_TANK[self.tank]

        # Что делает танк:
        # 0 - рандомно ходит
        # 2 - охотиться за игроком, 3 - атакует базу
        self.number_action = self.tank_info[2]
        # обход препятствия нужен
        self.turn_flag = 0
        self.direct = 0
        self.direct_flag = -1
        # позиция танка
        self.rect = self.generate_random_position(level, objects,
                                                  bullets, width, height)
        self.current_coordinates_x = 0
        self.current_coordinates_y = 0
        objects.append(self)

        self.moveSpeed = self.tank_info[1]
        self.current_moveSpeed = self.moveSpeed
        self.health = self.tank_info[3]

        self.shotTimer = 0
        self.shotDelay = 150
        self.bulletSpeed = 5
        self.bulletDamage = self.tank_info[4]

        self.movement_status = 'STOP'
        self.timer_move = 0

        self.tank_image = pygame.image.load(self.tank_info[0])
        self.tank_rotated = self.tank_image

    # рандомный спавн танка противника
    @staticmethod
    def generate_random_position(level, objects, bullets, width, height):
        random.shuffle(level)  # Перемешиваем список координат
        for i in range(len(level)):
            random_x, random_y = level[i]
            if random_x < width//2 and random_y < height//2:

                # Проверяем три точки с координатами отличающимися на 16
                neighbor_x1, neighbor_y1 = random_x + 16, random_y + 16
                neighbor_x2, neighbor_y2 = random_x - 16, random_y - 16
                count = 0
                coordinates_suitable_points = []
                for x, y in [(random_x, random_y),
                             (random_x, neighbor_y1),
                             (random_x, neighbor_y2),
                             (neighbor_x1, neighbor_y1),
                             (neighbor_x1, neighbor_y2),
                             (neighbor_x2, neighbor_y2),
                             (neighbor_x1, random_y),
                             (neighbor_x2, random_y),
                             (neighbor_x2, neighbor_y1)]:
                    if (x, y) in level:
                        coordinates_suitable_points.append((x, y))
                        count += 1
                    if count == 4:
                        x = (coordinates_suitable_points[0][0]
                             + coordinates_suitable_points[1][0]
                             + coordinates_suitable_points[2][0]
                             + coordinates_suitable_points[3][0])//4
                        y = (coordinates_suitable_points[0][1]
                             + coordinates_suitable_points[1][1]
                             + coordinates_suitable_points[2][1]
                             + coordinates_suitable_points[3][1])//4

                    valid_position = ((not any(obj.rect.colliderect(pygame.
                                                                    Rect(x, y, TILE, TILE))
                                               for obj in objects))
                                      and (not any(bullet.rect.colliderect(pygame.
                                                                           Rect(x, y, TILE, TILE))
                                                   for bullet in bullets)))

                    if valid_position:
                        tank_rect = pygame.Rect(x, y, TILE, TILE)
                        return tank_rect

        # Если не найдено подходящей позиции в списке координат
        return pygame.Rect(0, 0, TILE, TILE)

    # Движение танка
    def move(self):

        # Движение влево
        if (self.direct == 3
                and self.rect.left > self.moveSpeed):
            self.rect.centerx -= self.moveSpeed
            self.direct_flag = 0
            self.tank_rotated = pygame.transform.rotate(self.tank_image, 90)

        # Движение вправо
        elif (self.direct == 1
              and self.rect.right < self.width_window - self.moveSpeed // 2):
            self.rect.centerx += self.moveSpeed
            self.tank_rotated = pygame.transform.rotate(self.tank_image, 270)
            self.direct_flag = 0

        # Движение вверх
        elif (self.direct == 0
              and self.rect.top > self.moveSpeed):
            self.rect.centery -= self.moveSpeed
            self.tank_rotated = pygame.transform.rotate(self.tank_image, 0)
            self.direct_flag = 0

        # Движение назад
        elif (self.direct == 2
              and self.rect.bottom < self.height_window - self.moveSpeed // 2):
            self.rect.centery += self.moveSpeed
            self.tank_rotated = pygame.transform.rotate(self.tank_image, 180)
            self.direct_flag = 0

    # Проверка на корректность выполнения команды из move
    def tank_movement(self, objects, bonuses, time=0):
        old_x, old_y = self.rect.topleft

        self.move()

        # обход объекта (тайла) танком
        for obj in objects:
            if obj != self and self.rect.colliderect(obj.rect):
                # Возвращаем танк на предыдущие координаты
                self.rect.topleft = old_x, old_y
                if time >= 2000:
                    # Препятствие справа
                    if obj.rect.centerx > self.rect.centerx:
                        # Устанавливаем флаг на поворот влево
                        self.turn_flag = 1

                    # Препятствие слева
                    else:
                        # Устанавливаем флаг на поворот вправо
                        self.turn_flag = -1

                    break
            else:  # Если препятствия больше нет
                self.turn_flag = 0  # Сбрасываем флаг в 0

        if self.turn_flag == 1:
            # Проверяем упирание в правую границу окна
            if self.rect.right >= self.width_window - self.current_moveSpeed:
                self.turn_flag = -1
            elif self.direct == 1:
                self.turn_flag = 0
            else:
                # Обходим препятствие слева
                self.rect.centerx -= self.current_moveSpeed
                self.tank_rotated = pygame.transform.rotate(self.tank_image, 90)
                self.direct_flag = 0
                self.direct = 3

        elif self.turn_flag == -1:
            # Проверяем упирание в левую границу окна
            if self.rect.left - self.current_moveSpeed <= 0:
                self.turn_flag = 1
            elif self.direct == 3:
                self.turn_flag = 0
            else:
                # Обходим препятствие справа
                self.rect.centerx += self.current_moveSpeed
                self.tank_rotated = pygame.transform.rotate(self.tank_image, 270)
                self.direct_flag = 0
                self.direct = 1

        # Проверка на выход за границы экрана
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(self.width_window, self.rect.right)

        for obj in objects:
            if obj != self and self.rect.colliderect(obj.rect):
                # Возвращаем танк на предыдущие координаты
                self.rect.topleft = old_x, old_y
                break

        for bonus in bonuses:
            if self.rect.colliderect(bonus.rect):
                self.rect.topleft = old_x, old_y

        # Если стоим на месте, значит нужно обходить препятствие
        if (self.current_coordinates_x == self.rect.centerx
                and self.current_coordinates_y == self.rect.centery and time >= 2000):
            self.current_moveSpeed -= 1

            if self.current_moveSpeed <= 0:
                self.current_moveSpeed = self.moveSpeed
                if self.turn_flag == 0:
                    self.turn_flag = 1
                else:
                    self.turn_flag *= (-1)

        elif time >= 2000:
            self.current_moveSpeed = self.moveSpeed
        return

    # Что делать танкам с флагами 2 и 3
    def harassment_purpose(self, time, objects, bonuses):
        self.timer_move += 1

        if self.timer_move >= 100:
            self.timer_move = 0

            # танк атакующий базу
            if self.number_action == 3:

                # Двигаемся вниз
                if coordinates_base[1] > self.rect.centerx:
                    self.direct = 2

                # Двигаемся вверх
                elif coordinates_base[1] < self.rect.centerx:
                    self.direct = 0

                if self.rect.centery >= 400:
                    if coordinates_base[0] < self.rect.centery:
                        self.direct = 1
                    elif coordinates_base[0] > self.rect.centery:
                        self.direct = 3

                self.tank_movement(objects, bonuses, time)

            # танк, который охотиться за игроком
            elif self.number_action == 2:
                nearest_tank = None
                min_distance = float('inf')

                # вычисляем расстояние до танка
                for obj in objects:
                    if isinstance(obj, Tank):
                        distance = (abs(self.rect.centerx - obj.rect.centerx)
                                    + abs(self.rect.centery - obj.rect.centery))
                        if distance < min_distance:
                            min_distance = distance
                            nearest_tank = obj

                if nearest_tank:
                    target_x = nearest_tank.rect.centerx
                    target_y = nearest_tank.rect.centery

                    if (target_y >= self.rect.centery
                            and (target_y < self.rect.centery - 16
                                 or target_y > self.rect.centery + 16)):
                        # Движение вниз
                        self.direct = 2
                        self.tank_movement(objects, bonuses, time)
                    elif (target_y < self.rect.centery
                          and (target_y < self.rect.centery - 16
                               or target_y > self.rect.centery + 16)):
                        # Движение вверх
                        self.direct = 0
                        self.tank_movement(objects, bonuses, time)
                    elif target_x > self.rect.centerx:
                        # Движение вправо
                        self.direct = 1
                        self.tank_movement(objects, bonuses, time)
                    elif target_x < self.rect.centerx:
                        # Движение влево
                        self.direct = 3
                        self.tank_movement(objects, bonuses, time)

        return

    # рандомное движение до определенного времени, дальше уход в флаг 3 и 2
    def random_direction(self, time, objects, bonuses):
        if self.movement_status == 'STOP':
            direct_flag = self.direct
            self.timer_move += 1

            if time >= 2000:
                self.moveSpeed = self.tank_info[1] // 2
                if self.number_action != 3 or self.number_action != 2:
                    number_tank_task = [3, 2]
                    self.number_action = random.choice(number_tank_task)
                self.harassment_purpose(time, objects, bonuses)

            elif self.timer_move >= 60:
                self.timer_move = 0
                directions = [1, 2, 3, 0]
                self.direct = random.choice(directions)
                self.tank_movement(objects, bonuses)

            if self.direct_flag == -1:
                self.direct = direct_flag
            self.direct_flag = -1

            return

    def update(self, bullets, objects, bonuses, time):

        if (self.tank == 'ordinary_tank'
                or self.tank == 'speed_tank' or self.tank == 'armor_tank'):
            self.random_direction(time, objects, bonuses)
        elif (self.tank == 'stalker_player_tank'
              or self.tank == 'attacking_base_tank'):
            self.harassment_purpose(time, objects, bonuses)

        self.current_coordinates_x = self.rect.centerx
        self.current_coordinates_y = self.rect.centery

        # стрельба
        if self.shotTimer == 0:
            direction = self.direct
            direction_x, direction_y = DIRECTS[direction]
            Bullet(self, self.rect.centerx, self.rect.centery,
                   direction_x * self.bulletSpeed,
                   direction_y * self.bulletSpeed, self.bulletDamage, bullets)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0:
            self.shotTimer -= 1

    def damage(self, value, objects):
        self.health -= value
        if self.health <= 0:
            objects.remove(self)

    def draw(self, window):
        window.blit(self.tank_rotated, self.rect.topleft)

import pygame
import random

from obj_game.Bullet import Bullet

DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]
TILE = 25
DECODING_TANK = {
    '1': 'ordinary_tank',
    '2': 'speed_tank',
    '3': 'patrol_tank',
    '4': 'stalker_player_tank',
    '5': 'attacking_base_tank'
}
ENEMY_TANK = {
    "ordinary_tank": ('images\\tank_2.png', 2),
    "speed_tank": ('', 5),
    "patrol_tank": ('', 2, 100, 100, 300, 300),
    "stalker_player_tank": ('', 2),
    "attacking_base_tank": ('', 2, 100, 200)
}


class EnemyTank:
    def __init__(self, level, objects, bullets, width, height, number):
        self.type = 'enemy_tank'
        self.tank = DECODING_TANK[number]
        self.tank_info = ENEMY_TANK[self.tank]

        self.rect = self.generate_random_position(level, objects, bullets, width, height)
        self.count_up = 0
        objects.append(self)

        self.moveSpeed = self.tank_info[1]
        self.health = 1

        self.shotTimer = 0
        self.shotDelay = 200
        self.bulletSpeed = 5
        self.bulletDamage = 1

        self.movement_status = 'STOP'
        self.timer_move = 0
        self.direct = 0

        self.tank_image = pygame.image.load(self.tank_info[0])
        self.tank_rotated = self.tank_image

    def generate_random_position(self, level, objects, bullets, width, height):
        random.shuffle(level)  # Перемешиваем список координат
        for i in range(len(level)):
            random_x, random_y = level[i]
            if random_x < width//2 and random_y < height//2:

                # Проверяем три точки с координатами отличающимися на 16
                neighbor_x1, neighbor_y1 = random_x + 16, random_y + 16
                neighbor_x2, neighbor_y2 = random_x - 16, random_y - 16
                count = 0
                coor = []
                for x, y in [(random_x, random_y), (random_x, neighbor_y1),
                             (random_x, neighbor_y2), (neighbor_x1, neighbor_y1),
                             (neighbor_x1, neighbor_y2), (neighbor_x2, neighbor_y2),
                             (neighbor_x1, random_y), (neighbor_x2, random_y), (neighbor_x2, neighbor_y1)]:
                    if (x, y) in level:
                        coor.append((x, y))
                        count += 1
                    if count == 4:
                        x = (coor[0][0] + coor[1][0] + coor[2][0] + coor[3][0])//4
                        y = (coor[0][1] + coor[1][1] + coor[2][1] + coor[3][1])//4
                        break

                    valid_position = ((not any(obj.rect.colliderect(pygame.Rect(x, y, TILE, TILE)) for obj in objects))
                                      and (not any(bullet.rect.colliderect(pygame.Rect(x, y, TILE, TILE))
                                                   for bullet in bullets)))

                    if valid_position:
                        tank_rect = pygame.Rect(x, y, TILE, TILE)
                        return tank_rect

        # Если не найдено подходящей позиции в списке координат
        return pygame.Rect(0, 0, TILE, TILE)

    def harassment_purpose(self, purpose_position):
        """
        Вычисляет расстояние (dx и dy) между позицией игрока и центром танка.
        Определяет основное направление (self.direct) для перемещения
        на основе компонента большего абсолютного расстояния.
        Перемещает танк в расчетном направлении, используя метод move_ip,
        с соответствующей скоростью и направлением из DIRECTS.

        Вычисляет расстояния (dx и dy) между резервуаром и местоположением базы.
        Определяет основное направление (self.direct) для перемещения
        на основе компонента большего абсолютного расстояния.
        Перемещает резервуар к базе, регулируя его положение в расчетном направлении с заданной скоростью перемещения.
        Эти функции в совокупности позволяют вражескому танку вести себя динамично, например,
        появляться случайным образом, преследовать танк игрока,
        патрулировать определенную область и продвигаться к базе игрока в вашей игровой среде.
        """
        dx = purpose_position[0] - self.rect.centerx
        dy = purpose_position[1] - self.rect.centery

        if abs(dx) > abs(dy):
            self.direct = 1 if dx > 0 else 3
        else:
            self.direct = 2 if dy > 0 else 0

        self.rect.move_ip(DIRECTS[self.direct][0] * self.moveSpeed, DIRECTS[self.direct][1] * self.moveSpeed)

    def patrol_area(self, area):
        """
        Определяет точки патрулирования, образующие квадрат вокруг заданной области.
        Отслеживает текущую_пункту и устанавливает координаты target_x и target_y для следующей точки патрулирования.
        Вычисляет расстояния dx и dy до целевой точки и проверяет, достиг ли танк текущей точки патрулирования.
        Если танк находится достаточно близко к цели,
        он перемещается к следующей точке траектории патрулирования и обновляет координаты цели.
        Корректирует положение танка по отношению к целевой точке путем
        постепенного перемещения в зависимости от оставшегося расстояния в обоих направлениях x и y.
        """
        patrol_points = [(area[0], area[1]), (area[2], area[1]), (area[2], area[3]), (area[0], area[3])]
        current_point = 0

        target_x, target_y = patrol_points[current_point]

        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery

        # Check if the tank reached the current patrol point
        if abs(dx) < self.moveSpeed and abs(dy) < self.moveSpeed:
            current_point = (current_point + 1) % len(patrol_points)  # Move to the next point in the patrol path
            target_x, target_y = patrol_points[current_point]

        if target_x != self.rect.centerx:
            self.rect.move_ip((target_x - self.rect.centerx) / abs(target_x - self.rect.centerx) * self.moveSpeed, 0)

        if target_y != self.rect.centery:
            self.rect.move_ip(0, (target_y - self.rect.centery) / abs(target_y - self.rect.centery) * self.moveSpeed)

    def random_direction(self, width, height):
        if self.movement_status == 'STOP':
            self.timer_move += 1
            if self.timer_move >= 60:  # Число кадров для каждого действия
                self.timer_move = 0
                self.count_up += 1
                if self.count_up <= 5 and self.rect.top > 0:  # Движение прямо
                    self.rect.y -= self.moveSpeed  # Двигаем танк вверх
                    self.tank_rotated = pygame.transform.rotate(self.tank_image, 0)  # Поворачиваем танк вперед
                    self.direct = 0
                elif self.count_up == 6:  # Поворот налево или направо
                    directions = [3, 1]  # Углы для поворотов налево и направо
                    random_direction = random.choice(directions)
                    if random_direction == 3 and self.rect.right < width:  # Поворот влево
                        self.rect.x += self.moveSpeed
                        self.tank_rotated = pygame.transform.rotate(self.tank_image, 90)  # Поворот танка влево
                        self.direct = 3
                    elif random_direction == 1 and self.rect.left > 0:  # Поворот вправо
                        self.rect.x -= self.moveSpeed
                        self.tank_rotated = pygame.transform.rotate(self.tank_image, 270)  # Поворот танка вправо
                        self.direct = 1
                elif self.count_up == 7:  # Рандомное выбор направления
                    directions = [0, 3, 1]  # Направления: прямо, налево, направо
                    random_direction = random.choice(directions)
                    if random_direction == 0 and self.rect.bottom < height:  # Движение прямо
                        self.rect.y += self.moveSpeed
                        self.tank_rotated = pygame.transform.rotate(self.tank_image, 180)  # Поворот танка назад
                        self.direct = 0
                    elif random_direction == 3 and self.rect.right < width:  # Поворот налево
                        self.rect.x += self.moveSpeed
                        self.tank_rotated = pygame.transform.rotate(self.tank_image, 90)  # Поворот танка влево
                        self.direct = 3
                    elif random_direction == 1 and self.rect.left > 0:  # Поворот направо
                        self.rect.x -= self.moveSpeed
                        self.tank_rotated = pygame.transform.rotate(self.tank_image, 270)  # Поворот танка вправо
                        self.direct = 1
                elif self.count_up == 8:  # Сброс счетчика для новой серии движений
                    self.count_up = 0

    def update(self, bullets, objects, width, height):
        old_x, old_y = self.rect.topleft

        if self.tank == 'ordinary_tank' or self.tank == 'speed_tank':
            self.random_direction(width, height)

        for obj in objects:
            if obj != self and self.rect.colliderect(obj.rect):
                self.rect.topleft = old_x, old_y

        if self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery,
                   dx, dy, self.bulletDamage, bullets)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0:
            self.shotTimer -= 1

    def damage(self, value, objects):
        self.health -= value
        if self.health <= 0:
            objects.remove(self)
            print('bot dead')

    def draw(self, window):
        window.blit(self.tank_rotated, self.rect.topleft)

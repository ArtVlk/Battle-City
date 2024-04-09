import pygame

from queue import Queue

from obj_game.bullet import Bullet
from obj_game.bonus import Bonus


DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]
TILE = 25


class Tank:
    def __init__(self, px, py, direct, key_list, tank_image, objects):
        objects.append(self)
        self.type = 'tank'

        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.moveSpeed = 1
        self.health = 10
        self.tank_player_live = 3

        self.shotTimer = 0
        self.shotDelay = 60
        self.bulletSpeed = 5
        self.bulletDamage = 1

        self.numberBonus = Queue()

        self.keyLEFT = key_list[0]
        self.keyRIGHT = key_list[1]
        self.keyUP = key_list[2]
        self.keyDOWN = key_list[3]
        self.keySHOT = key_list[4]

        self.tank_image = pygame.image.load(tank_image)
        self.tank_rotated = self.tank_image

    def update(self, keys, bullets, objects, bonuses, width, height):
        old_x, old_y = self.rect.topleft

        if keys[self.keyLEFT] and self.rect.left > 0:
            self.rect.x -= self.moveSpeed
            self.tank_rotated = pygame.transform.rotate(self.tank_image, 90)
            self.direct = 3
        elif keys[self.keyRIGHT] and self.rect.right < width:
            self.rect.x += self.moveSpeed
            self.tank_rotated = pygame.transform.rotate(self.tank_image, 270)
            self.direct = 1
        elif keys[self.keyUP] and self.rect.top > 0:
            self.rect.y -= self.moveSpeed
            self.tank_rotated = pygame.transform.rotate(self.tank_image, 0)
            self.direct = 0
        elif keys[self.keyDOWN] and self.rect.bottom < height:
            self.rect.y += self.moveSpeed
            self.tank_rotated = pygame.transform.rotate(self.tank_image, 180)
            self.direct = 2

        for obj in objects:
            if obj != self and self.rect.colliderect(obj.rect):
                self.rect.topleft = old_x, old_y
                break

        for bonus in bonuses:
            if isinstance(bonus, Bonus) and self.rect.colliderect(bonus.rect):
                bonus.update(objects, bonuses)
                self.numberBonus.put([bonus.bonus_number, 600])

        if keys[self.keySHOT] and self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery,
                   dx, dy, self.bulletDamage, bullets)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0:
            self.shotTimer -= 1

        new_number_bonus = Queue()
        while not self.numberBonus.empty():
            bonus_info = self.numberBonus.get()
            time = bonus_info[1] - 1
            if time > 0:
                new_number_bonus.put([bonus_info[0], time])
            else:
                if bonus_info[0] == 1:
                    self.moveSpeed -= 0.3
                elif bonus_info[0] == 4:
                    self.bulletDamage -= 1

        self.numberBonus = new_number_bonus

    def damage(self, value, objects):
        self.health -= value
        if self.health <= 0:
            objects.remove(self)
            self.tank_player_live -= 1
            print('dead player')

    def draw(self, window):
        window.blit(self.tank_rotated, self.rect.topleft)

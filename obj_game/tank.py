import pygame

from obj_game.Bullet import Bullet


DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]
TILE = 25


class Tank:
    def __init__(self, color, px, py, direct, key_list, tank_image, objects):
        objects.append(self)
        self.type = 'tank'

        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.moveSpeed = 1
        self.health = 10

        self.shotTimer = 0
        self.shotDelay = 60
        self.bulletSpeed = 5
        self.bulletDamage = 1

        self.keyLEFT = key_list[0]
        self.keyRIGHT = key_list[1]
        self.keyUP = key_list[2]
        self.keyDOWN = key_list[3]
        self.keySHOT = key_list[4]

        self.tank_image = pygame.image.load(tank_image)
        self.tank_rotated = self.tank_image

    def update(self, keys, bullets, objects, width, height):
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

        if keys[self.keySHOT] and self.shotTimer == 0:
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
            print(self.color, 'dead')

    def draw(self, window):
        window.blit(self.tank_rotated, self.rect.topleft)

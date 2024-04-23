import pygame


IMAGES_BONUS = {
    '1': ('SPEED', 'images\\bonus\\BONUS_SPEED.png'),
    '2': ('LIVE', 'images\\bonus\\BONUS_LIVE.png'),
    '3': ('EXPLOSION', 'images\\bonus\\BONUS_TANK_EXPLOSION.png'),
    '4': ('ARMOR', 'images\\bonus\\BONUS_ARMOR.png')
}
TILE = 30


class Bonus:
    def __init__(self, px, py, bonuses, bonus_number):
        bonuses.append(self)
        self.type = 'bonus'
        self.bonus_number = bonus_number

        self.image = pygame.image.load(IMAGES_BONUS[str(bonus_number)][1])
        self.rect = pygame.Rect(px, py, TILE, TILE)

        self.timer = 600
        self.bonus_rotated = self.image

    def update(self, objects, bonuses):
        if self.timer > 0:
            self.timer -= 1
        else:
            bonuses.remove(self)

        tank_hit = None
        for obj in objects:
            if obj.type == 'tank' and self.rect.colliderect(obj.rect):
                tank_hit = obj
                break

        if tank_hit:
            if self.bonus_number == 1:
                tank_hit.moveSpeed += 0.3
            elif self.bonus_number == 2:
                tank_hit.tank_player_live += 1
            elif self.bonus_number == 3:
                enemy_tanks = [obj for obj in objects
                               if obj.type == 'enemy_tank']
                for enemy_tank in enemy_tanks:
                    objects.remove(enemy_tank)
            elif self.bonus_number == 4:
                tank_hit.bulletDamage += 1
            bonuses.remove(self)

    def draw(self, window):
        if self.timer % 30 < 15:
            window.blit(self.image, self.rect)

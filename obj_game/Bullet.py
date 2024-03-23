import pygame

path = "images\\bullet.png"
TILE = 10


class Bullet:
    def __init__(self, parent, parent_x, parent_y,
                 direction_x, direction_y, damage, bullets):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = parent_x, parent_y
        self.rect = pygame.Rect(self.px, self.py, TILE, TILE)
        self.dx, self.dy = direction_x, direction_y
        self.damage = damage
        self.bullet_image = pygame.image.load(path)

    def update(self, objects, bullets, width, height):
        self.px += self.dx
        self.py += self.dy
        self.rect.topleft = (self.px, self.py)

        if self.px < 0 or self.px > width or self.py < 0 or self.py > height:
            bullets.remove(self)
        else:
            for obj in objects:
                if (obj != self.parent
                        and obj.rect.colliderect(self.rect)):
                    if self.parent.__class__.__name__ != obj.__class__.__name__:
                        obj.damage(self.damage, objects)
                    bullets.remove(self)
                    break

    def draw(self, window):
        window.blit(self.bullet_image, (self.px, self.py))

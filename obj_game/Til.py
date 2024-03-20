import pygame


class Til:
    def __init__(self, px, py, size, tils, path):
        self.health = 1
        self.tils = tils
        self.type = 'block'
        self.image = pygame.image.load(path)
        self.rect = pygame.Rect(px, py, size, size)

    def update(self):
        pass

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def damage(self, value, objects):
        if self.tils[1] != 1:
            self.health -= value
            if self.health <= 0:
                objects.remove(self)

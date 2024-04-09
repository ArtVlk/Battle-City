import pygame

TILE = 16
EAGLE_IMAGES = {
    '1': 'images\\Eagle\\Eagle_upper_left_corner.png',
    '2': 'images\\Eagle\\Eagle_upper_right_corner.png',
    '3': 'images\\Eagle\\Eagle_lower_left_corner.png',
    '4': 'images\\Eagle\\Eagle_lower_right_corner.png'
}


class Eagle:
    def __init__(self, char, px, py):
        self.health = 1
        self.type = 'eagle'
        self.image = pygame.image.load(EAGLE_IMAGES[char[1]])
        self.rect = pygame.Rect(px, py, TILE, TILE)

    def update(self):
        pass

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def damage(self, value, objects):
        self.health -= value
        if self.health <= 0:
            objects.remove(self)

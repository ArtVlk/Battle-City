from obj_game.Til import Til

BLOCK_SIZE = 16
TILES = ['B', 'S', 'L']
TILE_TO_TYPE = {
    'B': ('BRICK', 0),
    'S': ('STEEL', 1),
    'L': ('LEAVES', 2)
}
TILE_TO_PATH = {
    'BRICK': 'images\\BRICK.png',
    'STEEL': 'images\\STEEL.png',
    'LEAVES': 'images\\LEAVES.png'
}


class Level:
    def __init__(self, object, available_coordinates):
        self.initialize_level(object, available_coordinates)

    def initialize_level(self, object, available_coordinates):
        level = 0
        path = 'images/levels/level_' + str(level) + '.txt'
        with open(path, 'r') as file:
            data = file.read().split('\n')

        y = 0
        for string in data:
            x = 0
            for char in string:
                if char == '.':
                    available_coordinates.append((x, y))
                elif char in TILES:
                    tils = TILE_TO_TYPE[char]
                    image_path = TILE_TO_PATH[tils[0]]
                    obj = Til(x, y, BLOCK_SIZE, tils, image_path)
                    object.append(obj)
                x += BLOCK_SIZE
            y += BLOCK_SIZE

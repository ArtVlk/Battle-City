from obj_game.til import Til
from obj_game.eagle import Eagle

BLOCK_SIZE = 16
TILES = ['B', 'S', 'L', 'K', 'W']
TILE_TO_TYPE = {
    'B': ('BRICK', 0),
    'S': ('STEEL', 1),
    'L': ('LEAVES', 2),
    'K': ('BUSH', 2),
    'W': ('WATER', 1)
}
TILE_TO_PATH = {
    'BRICK': 'images\\BRICK.png',
    'STEEL': 'images\\STEEL.png',
    'LEAVES': 'images\\LEAVES.png',
    'BUSH': 'images\\BUSH.png',
    'WATER': 'images\\WATER.png'
}


class Level:
    def __init__(self, object, available_coordinates,
                 objects_durable_tiles, number):
        self.initialize_level(object, available_coordinates,
                              objects_durable_tiles, number)

    def initialize_level(self, object, available_coordinates,
                         objects_durable_tiles, number):
        path = 'images/levels/level_' + str(number) + '.txt'
        with open(path, 'r') as file:
            data = file.read().split('\n')

        char_eagle = ''
        flag_char_eagle = 0
        y = 0
        for string in data:
            x = 0
            for char in string:
                if char == '.':
                    available_coordinates.append((x, y))
                elif char == 'E' or flag_char_eagle == 1:
                    char_eagle += char
                    flag_char_eagle = 1
                    if len(char_eagle) == 2:
                        x -= BLOCK_SIZE
                        obj = Eagle(char_eagle, x, y)
                        object.append(obj)
                        char_eagle = ''
                        flag_char_eagle = 0

                elif char in TILES:
                    tils = TILE_TO_TYPE[char]
                    image_path = TILE_TO_PATH[tils[0]]
                    obj = Til(x, y, BLOCK_SIZE, tils, image_path)
                    if tils[0] != 'LEAVES' and tils[0] != 'BUSH':
                        object.append(obj)
                    else:
                        objects_durable_tiles.append(obj)
                x += BLOCK_SIZE
            y += BLOCK_SIZE

import pygame

pygame.font.init()


FONT_ARIAL_50 = pygame.font.SysFont('arial', 50)


class Menu:
    def __init__(self):
        self.option_surfaces = []
        self.called_functions = []
        self.current_option_index = 0

    def append_option(self, option, called_function=None, flag=None):
        self.option_surfaces.append(FONT_ARIAL_50.render
                                    (option, True, (255, 255, 255)))
        if flag is None:
            self.called_functions.append(called_function)

    def switch_option(self, direction):
        self.current_option_index = (
            max(0, min(self.current_option_index + direction,
                       len(self.option_surfaces) - 1)))

    def choosing_option(self):
        self.called_functions[self.current_option_index]()

    def draw(self, surface, x, y, button_margins):
        for i, option in enumerate(self.option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * button_margins - 50)

            if i == self.current_option_index:
                pygame.draw.rect(surface, (0, 100, 0), option_rect)

            surface.blit(option, option_rect)

    def quit_game(self):
        pygame.quit()

    def level_select_window(self, window):
        run_level_select = True
        number_level = 1

        while run_level_select:
            window.fill('black')
            self.option_surfaces = []

            self.append_option('Уровень 1', flag=0)
            self.append_option('Уровень 2', flag=0)
            self.append_option('Уровень 3', flag=0)
            self.append_option('Уровень 4', flag=0)
            self.append_option('Меню', flag=0)

            self.draw(window, 100, 100, 75)

            pygame.display.update()
            play = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                    return number_level, play
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.switch_option(-1)
                        number_level = max(0, number_level - 1)
                    elif event.key == pygame.K_DOWN:
                        self.switch_option(1)
                        number_level = min(len(self.option_surfaces), number_level + 1)
                    elif event.key == pygame.K_RETURN:
                        if number_level == 4:
                            number_level = -1
                        return number_level, play

import pygame


class TicTacToeScene:
    def __init__(self, extension):
        self._extension = extension
        self._background_color = (200, 200, 200)

    def render(self, screen):
        background = pygame.Surface(screen.get_size())
        background.fill(self._background_color)
        screen.blit(background, (0, 0))

        # for button in self._extension.buttons:
        #     xd = button.get_figure()
        #     color = button.get_color(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0] == 1)
        #     pygame.draw.rect(screen, color, xd)

        pygame.display.flip()

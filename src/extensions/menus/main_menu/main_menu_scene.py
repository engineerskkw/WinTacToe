import pygame


class MainMenuScene:
    def __init__(self, extension):
        self._extension = extension
        self._background_color = (55, 55, 55)

    def render(self, screen):
        background = pygame.Surface(screen.get_size())
        background.fill(self._background_color)
        screen.blit(background, (0, 0))

        for button in self._extension.get_buttons():
            figure = button.get_figure()
            figures_color = button.get_color(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0] == 1)
            pygame.draw.rect(screen, figures_color, figure)
            screen.blit(button.text, button.get_text_position())

        pygame.display.flip()

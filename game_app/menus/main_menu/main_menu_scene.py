#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import pygame


class MainMenuScene:
    def __init__(self, component, screen):
        self._component = component
        self._screen = screen
        self._background_color = (55, 55, 55)
        self._background_displayed = False

    def render(self):
        self._display_background()
        for button in self._component.get_buttons():
            self._display_button(button)
        pygame.display.flip()

    def _display_background(self):
        if not self._background_displayed:
            background_surface = pygame.Surface(self._screen.get_size())
            background_surface.fill(self._background_color)
            self._screen.blit(background_surface, (0, 0))
            self._background_displayed = True

    def _display_button(self, button):
        figure = button.get_figure()
        figures_color = button.get_color(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0] == 1)
        pygame.draw.rect(self._screen, figures_color, figure)
        self._screen.blit(button.text, button.get_text_position())

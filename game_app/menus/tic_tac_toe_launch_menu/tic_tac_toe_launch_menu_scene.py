#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import pygame


class TicTacToeLaunchMenuScene:
    def __init__(self, component, screen):
        self._component = component
        self._screen = screen
        self._background_color = (100, 100, 100)
        self._background_displayed = False

    def render(self):
        self._display_background()
        for button in self._component.get_buttons():
            button.render(self._screen, pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0] == 1)
        pygame.display.flip()

    def _display_background(self):
        if not self._background_displayed:
            background_surface = pygame.Surface(self._screen.get_size())
            background_surface.fill(self._background_color)
            self._screen.blit(background_surface, (0, 0))
            self._background_displayed = True

            pygame.font.init()
            font = pygame.font.Font(None, 50)
            text1 = font.render("Board Size", True, (255, 255, 255))
            text2 = font.render("Goal", True, (255, 255, 255))
            text3 = font.render("Your Mark", True, (255, 255, 255))
            self._screen.blit(text1, (0, 0))
            self._screen.blit(text2, (0, 300))
            self._screen.blit(text3, (0, 500))

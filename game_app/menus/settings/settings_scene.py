#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import pygame


class SettingsScene:
    def __init__(self, component, screen):
        self._component = component
        self._screen = screen
        self._text_color = (255, 255, 255)
        self._background_color = (55, 0, 55)
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
            font = pygame.font.Font(None, 30)
            text1 = font.render("Select size of the board:", True, self._text_color)
            text2 = font.render("Select number of marks to connect required to win:", True, self._text_color)
            text3 = font.render("Select your mark:", True, self._text_color)
            self._screen.blit(text1, (640 - text1.get_width() / 2, 60))
            self._screen.blit(text2, (640 - text2.get_width() / 2, 260))
            self._screen.blit(text3, (640 - text3.get_width() / 2, 460))

# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import pygame
from game_app.common.common_helper import Settings, ColorMode


class CreditsScene:
    def __init__(self, component, screen, settings):
        self._component = component
        self._screen = screen
        self._text_color = (230, 230, 230) if settings[Settings.COLOR] == ColorMode.DARK else (25, 25, 25)
        self._background_color = (45, 45, 45) if settings[Settings.COLOR] == ColorMode.DARK else (230, 230, 230)
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
            font = pygame.font.Font(None, 27)
            icons_text_1 = font.render("All icons used in the project were based on icons downloaded from www.flaticon.com" , True, self._text_color)
            icons_text_2 = font.render("Some of them were modified and all of them were scaled and colored", True, self._text_color)
            icons_text_3 = font.render("Click the icon button to visit its core creator's flaticon page", True, self._text_color)
            self._screen.blit(icons_text_1, (640 - icons_text_1.get_width() / 2, 460))
            self._screen.blit(icons_text_2, (640 - icons_text_2.get_width() / 2, 485))
            self._screen.blit(icons_text_3, (640 - icons_text_3.get_width() / 2, 510))

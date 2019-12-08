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
            text_1 = pygame.font.Font(None, 75).render("WinTacToe", True, self._text_color)
            text_2 = pygame.font.Font(None, 25).render("by", True, self._text_color)
            text_3 = pygame.font.Font(None, 55).render("Jan Kapała,  Jakub Konieczny,  Patryk Wójtowicz", True, self._text_color)
            text_4 = pygame.font.Font(None, 30).render("advised by Prof. Witold Dzwinel", True, self._text_color)
            self._screen.blit(text_1, (640 - text_1.get_width() / 2, 45))
            self._screen.blit(text_2, (640 - text_2.get_width() / 2, 125))
            self._screen.blit(text_3, (640 - text_3.get_width() / 2, 155))
            self._screen.blit(text_4, (640 - text_4.get_width() / 2, 215))

            font = pygame.font.Font(None, 25)
            music_text_1 = font.render("Songs used as background music are \"Sneaky Snitch\" (in menu)         and \"Sneaky Adventure\" (in game)         by Kevin MacLeod", True, self._text_color)
            music_text_2 = font.render("both licensed under Creative Commons: By Attribution 3.0 License", True, self._text_color)
            self._screen.blit(music_text_1, (640 - music_text_1.get_width() / 2, 290))
            self._screen.blit(music_text_2, (640 - music_text_2.get_width() / 2, 310))

            sounds_text_1 = font.render("Sound effects used are downloaded from soundbible.com and freesoud.org", True, self._text_color)
            sounds_text_2 = font.render("ones that have copyrights are licensed under Creative Commons: By Attribution 3.0 License", True, self._text_color)
            self._screen.blit(sounds_text_1, (640 - sounds_text_1.get_width() / 2, 370))
            self._screen.blit(sounds_text_2, (640 - sounds_text_2.get_width() / 2, 390))

            icons_text_1 = font.render("Icons used are based on icons downloaded from www.flaticon.com, some of them were slightly modified,", True, self._text_color)
            icons_text_2 = font.render("all of them were colored and scaled, original icon creator's flaticon page can be found by clicking buttons below", True, self._text_color)
            self._screen.blit(icons_text_1, (640 - icons_text_1.get_width() / 2, 560))
            self._screen.blit(icons_text_2, (640 - icons_text_2.get_width() / 2, 580))

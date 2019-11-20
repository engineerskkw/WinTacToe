# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from pygame.locals import *
from pygame.mixer import Sound

from game_app.common_helper import Components
from game_app.menus.menus_scene_commons.buttons import RectangularTextButton, RectangularChoiceButton, \
    DisableableRectangularTextButton, RoundIconButton


class SettingsLogic:
    def __init__(self, app):
        self._app = app
        self._board_size = 3
        self._marks_required = 3
        self._mark = 0

        self._settings_buttons = [
            RectangularTextButton("Music On/Off",
                                  lambda: print("TODO"),
                                  (450, 100),
                                  (380, 100)),
            RectangularTextButton("Sound On/Off",
                                  lambda: print("TODO"),
                                  (450, 300),
                                  (380, 100)),
            RectangularTextButton("Dark mode",
                                  lambda: print("TODO"),
                                  (450, 500),
                                  (380, 100)),
            RectangularTextButton("Reset to defaults",
                                  lambda: print("TODO"),
                                  (450, 620),
                                  (380, 100)),
        ]

        self._back_to_menu_button = RoundIconButton(
            'game_app/resources/images/tic_tac_toe_launch_menu/left_arrow_white.png',
            lambda: self.switch_back_to_main_menu(),
            (40, 40),
            30)

        self.all_buttons = [self._back_to_menu_button] + self._settings_buttons

    def handle_event(self, event):
        if event.type == MOUSEBUTTONUP:
            for pressed_button in filter(lambda button: button.contains_point(event.pos), self.all_buttons):
                pressed_button.on_pressed()

    def switch_back_to_main_menu(self):
        self._app.switch_component(Components.MAIN_MENU, switch_music=False)

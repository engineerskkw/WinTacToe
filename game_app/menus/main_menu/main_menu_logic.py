# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from pygame.locals import *

from game_app.common_helper import Components
from game_app.menus.menus_scene_commons.buttons import RectangularTextButton


class MainMenuLogic:
    def __init__(self, app):
        self._app = app
        self.buttons = [
            RectangularTextButton("TicTacToe",
                                  lambda: self.switch_to_tic_tac_toe(),
                                  (450, 100),
                                  (380, 100)),
            RectangularTextButton("TODO",
                                  lambda: self.switch_to_tic_tac_toe_launcher_menu(),
                                  (450, 300),
                                  (380, 100)),
            RectangularTextButton("TODO",
                                  lambda: print("TODO"),
                                  (450, 500),
                                  (380, 100)),
        ]

    def handle_event(self, event):
        if event.type == MOUSEBUTTONUP:
            for pressed_button in filter(lambda button: button.contains_point(event.pos), self.buttons):
                pressed_button.on_pressed()

    def switch_to_tic_tac_toe(self):
        self._app.switch_component(Components.TIC_TAC_TOE)

    def switch_to_tic_tac_toe_launcher_menu(self):
        self._app.switch_component(Components.TIC_TAC_TOE_LAUNCH_MENU)

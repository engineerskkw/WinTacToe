#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
PROJECT_ROOT_PATH = "./../../../"
sys.path.append(os.path.join(os.path.dirname(__file__), PROJECT_ROOT_PATH))
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from game_app.common_helper import Components
from game_app.menus.menus_scene_commons.buttons import RectangularTextButton
from pygame.locals import *


class MainMenuLogic:
    def __init__(self, app):
        self._app = app
        self.buttons = [
            RectangularTextButton("TicTacToe",
                                  lambda: self.switch_to_tic_tac_toe(),
                                  (450, 100),
                                  (380, 100)),
            RectangularTextButton("TODO",
                                  lambda: print("TODO"),
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

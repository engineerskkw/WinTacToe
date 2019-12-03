# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from pygame.locals import *

from game_app.common_helper import Components
from game_app.common.buttons import RectangularTextButton


class MainMenuLogic:
    def __init__(self, app):
        self._app = app
        self.buttons = [
            RectangularTextButton("Start game",
                                  self.switch_to_tic_tac_toe_launcher_menu,
                                  app,
                                  (410, 75),
                                  (460, 100)),
            RectangularTextButton("Credits",
                                  lambda: print("TODO"),
                                  app,
                                  (410, 235),
                                  (460, 100)),
            RectangularTextButton("Settings",
                                  self.switch_to_settings,
                                  app,
                                  (410, 395),
                                  (460, 100)),
            RectangularTextButton("Exit",
                                  self._app.exit_application,
                                  app,
                                  (410, 555),
                                  (460, 100)),
        ]

    def handle_event(self, event):
        if event.type == MOUSEBUTTONUP:
            for pressed_button in filter(lambda button: button.contains_point(event.pos), self.buttons):
                pressed_button.on_pressed()

    def switch_to_tic_tac_toe_launcher_menu(self):
        self._app.switch_component(Components.TIC_TAC_TOE_LAUNCH_MENU)

    def switch_to_settings(self):
        self._app.switch_component(Components.SETTINGS)

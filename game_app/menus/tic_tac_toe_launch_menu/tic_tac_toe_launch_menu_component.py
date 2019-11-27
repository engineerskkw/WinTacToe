#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from game_app.menus.abstract_menu_component import AbstractMenuComponent
from game_app.menus.tic_tac_toe_launch_menu.tic_tac_toe_launch_menu_logic import TicTacToeLaunchMenuLogic
from game_app.menus.tic_tac_toe_launch_menu.tic_tac_toe_launch_menu_scene import TicTacToeLaunchMenuScene


class TicTacToeLaunchMenuComponent(AbstractMenuComponent):
    def __init__(self, app):
        self._app = app
        self._logic = TicTacToeLaunchMenuLogic(app)
        self._scene = TicTacToeLaunchMenuScene(self, app.screen, app.settings)

    def get_buttons(self):
        return self._logic.all_buttons

# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from game_app.menus.abstract_menu_component import AbstractMenuComponent
from game_app.menus.main_menu.main_menu_logic import MainMenuLogic
from game_app.menus.main_menu.main_menu_scene import MainMenuScene


class MainMenuComponent(AbstractMenuComponent):
    def __init__(self, app, switch_music=True):
        self._app = app
        self._logic = MainMenuLogic(app)
        self._scene = MainMenuScene(self, app.screen, app.settings)
        if switch_music:
            self._app.switch_music(
                os.path.join(ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/common/SneakySnitch.mp3"))

    def get_buttons(self):
        return self._logic.buttons

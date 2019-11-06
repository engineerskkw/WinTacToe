#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from game_app.common_helper import MusicSwitcher
from game_app.menus.abstract_menu_component import AbstractMenuComponent
from game_app.menus.main_menu.main_menu_logic import MainMenuLogic
from game_app.menus.main_menu.main_menu_scene import MainMenuScene


class MainMenuComponent(AbstractMenuComponent):
    def __init__(self, app):
        self._app = app
        self._logic = MainMenuLogic(app)
        self._scene = MainMenuScene(self, app.screen)
        MusicSwitcher("resources/sounds/common/SneakySnitch.mp3").start()

    def get_buttons(self):
        return self._logic.buttons

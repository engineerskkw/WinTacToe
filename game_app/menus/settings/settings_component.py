#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from game_app.menus.abstract_menu_component import AbstractMenuComponent
from game_app.menus.settings.settings_logic import SettingsLogic
from game_app.menus.settings.settings_scene import SettingsScene


class SettingsComponent(AbstractMenuComponent):
    def __init__(self, app):
        self._app = app
        self._logic = SettingsLogic(self, app)
        self._scene = SettingsScene(self, app.screen, app.settings)

    def get_buttons(self):
        return self._logic.all_buttons

    def rerender(self):
        self._scene.rerender_background(self._app.settings)

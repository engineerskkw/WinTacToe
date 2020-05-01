import os
from global_constants import ABS_PROJECT_ROOT_PATH

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
                os.path.join(ABS_PROJECT_ROOT_PATH, "test_game_app/resources/sounds/common/SneakySnitch.mp3"))

    def get_buttons(self):
        return self._logic.buttons

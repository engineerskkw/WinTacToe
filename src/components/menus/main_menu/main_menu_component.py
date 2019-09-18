from ....common_helper import MusicSwitcher
from ..abstract_menu_component import AbstractMenuComponent
from .main_menu_logic import MainMenuLogic
from .main_menu_scene import MainMenuScene


class MainMenuComponent(AbstractMenuComponent):
    def __init__(self, app):
        self._app = app
        self._logic = MainMenuLogic(app)
        self._scene = MainMenuScene(self, app.screen)
        MusicSwitcher("resources/sounds/common/SneakySnitch.mp3").start()

    def get_buttons(self):
        return self._logic.buttons

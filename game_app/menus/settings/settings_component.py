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

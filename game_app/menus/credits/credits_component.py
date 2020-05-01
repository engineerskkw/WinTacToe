from game_app.menus.abstract_menu_component import AbstractMenuComponent
from game_app.menus.credits.credits_logic import CreditsLogic
from game_app.menus.credits.credits_scene import CreditsScene


class CreditsComponent(AbstractMenuComponent):
    def __init__(self, app):
        self._app = app
        self._logic = CreditsLogic(app)
        self._scene = CreditsScene(self, app.screen, app.settings)

    def get_buttons(self):
        return self._logic.all_buttons

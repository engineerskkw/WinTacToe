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

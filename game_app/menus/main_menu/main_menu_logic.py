from pygame.locals import *

from game_app.common.common_helper import Components
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
                                  self.switch_to_credits,
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

    def switch_to_credits(self):
        self._app.switch_component(Components.CREDITS)

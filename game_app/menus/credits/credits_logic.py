# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from pygame.locals import *

from game_app.common.common_helper import Components
from game_app.common.buttons import RoundIconButton
from game_app.common.common_helper import Settings, ColorMode


class CreditsLogic:
    def __init__(self, app):
        self._app = app

        self._back_to_menu_button = RoundIconButton(resolve_back_arrow_image_path(app.settings[Settings.COLOR]),
                                                    self.switch_back_to_main_menu, app, (40, 40), 30)

        self.all_buttons = [self._back_to_menu_button]

    def handle_event(self, event):
        if event.type == MOUSEBUTTONUP:
            for pressed_button in filter(lambda button: button.contains_point(event.pos), self.all_buttons):
                pressed_button.on_pressed()

    def switch_back_to_main_menu(self):
        self._app.switch_component(Components.MAIN_MENU, switch_music=False)


def resolve_back_arrow_image_path(color_mode):
    resource_dir = os.path.join(ABS_PROJECT_ROOT_PATH, 'game_app/resources/images/common')
    return os.path.join(resource_dir,
                        'left_arrow_white.png' if color_mode == ColorMode.DARK else 'left_arrow_black.png')

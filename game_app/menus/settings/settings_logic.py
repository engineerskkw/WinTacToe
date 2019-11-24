# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from pygame.locals import *
from game_app.common_helper import Components, ColorMode, Settings, MusicSwitcher
from game_app.common.buttons import RectangularTextButton, RoundIconButton
import pickle


class SettingsLogic:
    def __init__(self, component, app):
        self._component = component
        self._app = app
        self._board_size = 3
        self._marks_required = 3
        self._mark = 0
        self._initialize_buttons(app.settings)

    def _initialize_buttons(self, settings):
        self._settings_buttons = [
            RectangularTextButton("Toggle color mode",
                                  self.toggle_color_mode,
                                  settings,
                                  (450, 100),
                                  (380, 100)),
            RectangularTextButton("Toggle music",
                                  self.toggle_music,
                                  settings,
                                  (450, 300),
                                  (380, 100)),
            RectangularTextButton("Toggle sounds",
                                  self.toggle_sounds,
                                  settings,
                                  (450, 500),
                                  (380, 100)),
            RectangularTextButton("Reset to defaults",
                                  self.reset_to_defaults,
                                  settings,
                                  (900, 620),
                                  (380, 100)),
        ]

        self._save_settings_button = RoundIconButton(
            self._resolve_save_icon_path(settings[Settings.COLOR]),
            self.save_selected_settings,
            settings,
            (1240, 40),
            30)

        self._back_to_menu_button = RoundIconButton(
            self._resolve_back_arrow_icon_path(settings[Settings.COLOR]),
            self.switch_back_to_main_menu,
            settings,
            (40, 40),
            30)

        self.all_buttons = [self._save_settings_button, self._back_to_menu_button] + self._settings_buttons

    def _resolve_back_arrow_icon_path(self, color_mode):
        if color_mode == ColorMode.DARK:
            return 'game_app/resources/images/common/left_arrow_white.png'
        else:
            return 'game_app/resources/images/common/left_arrow_black.png'

    def _resolve_save_icon_path(self, color_mode):
        if color_mode == ColorMode.DARK:
            return 'game_app/resources/images/settings/save_icon_white.png'
        else:
            return 'game_app/resources/images/settings/save_icon_black.png'

    def _reinitialize_buttons(self, settings):
        self._initialize_buttons(settings)

    def _switch_music(self, music_on):
        MusicSwitcher(
            os.path.join(ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/common/SneakySnitch.mp3"),
            music_on,
        ).start()

    def handle_event(self, event):
        if event.type == MOUSEBUTTONUP:
            for pressed_button in filter(lambda button: button.contains_point(event.pos), self.all_buttons):
                pressed_button.on_pressed()

    def toggle_color_mode(self):
        if self._app.settings[Settings.COLOR] == ColorMode.LIGHT:
            self._app.settings[Settings.COLOR] = ColorMode.DARK
        else:
            self._app.settings[Settings.COLOR] = ColorMode.LIGHT
        self._component.rerender()
        self._reinitialize_buttons(self._app.settings)

    def toggle_music(self):
        self._app.settings[Settings.MUSIC] = not self._app.settings[Settings.MUSIC]
        self._switch_music(self._app.settings[Settings.MUSIC])

    def toggle_sounds(self):
        self._app.settings[Settings.SOUNDS] = not self._app.settings[Settings.SOUNDS]
        self._reinitialize_buttons(self._app.settings)

    def reset_to_defaults(self):
        self._app.settings[Settings.COLOR] = ColorMode.LIGHT
        if not self._app.settings[Settings.MUSIC]:
            self._switch_music(True)
        self._app.settings[Settings.MUSIC] = True
        self._app.settings[Settings.SOUNDS] = True
        self._component.rerender()
        self._reinitialize_buttons(self._app.settings)

    def save_selected_settings(self):
        with open(os.path.join(ABS_PROJECT_ROOT_PATH, "game_app/settings.cfg"), 'wb') as settings_file:
            pickle.dump(self._app.settings, settings_file, protocol=pickle.HIGHEST_PROTOCOL)

    def switch_back_to_main_menu(self):
        self._app.switch_component(Components.MAIN_MENU, switch_music=False)

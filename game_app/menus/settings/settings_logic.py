# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from pygame.locals import *
from game_app.common_helper import Components, ColorMode, Settings
from game_app.common.buttons import RoundIconButton, RectangularTextButtonWithIcon
import pickle


class SettingsLogic:
    def __init__(self, component, app):
        self._component = component
        self._app = app
        self._board_size = 3
        self._marks_required = 3
        self._mark = 0
        self._initialize_buttons(app.settings)
        self._music_file_path = os.path.join(ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/common/SneakySnitch.mp3")

    def _initialize_buttons(self, settings):
        self._settings_buttons = [
            RectangularTextButtonWithIcon(
                *resolve_color_mode_button_text_and_icon_path(settings[Settings.COLOR]),
                self.toggle_color_mode,
                settings,
                (410, 75),
                (460, 100)),
            RectangularTextButtonWithIcon(
                *resolve_music_button_text_and_icon_path(settings[Settings.COLOR], settings[Settings.MUSIC]),
                self.toggle_music,
                settings,
                (410, 235),
                (460, 100)),
            RectangularTextButtonWithIcon(
                *resolve_sounds_button_text_and_icon_path(settings[Settings.COLOR], settings[Settings.SOUNDS]),
                self.toggle_sounds,
                settings,
                (410, 395),
                (460, 100)),
            RectangularTextButtonWithIcon("Reset to defaults",
                                          resolve_reset_icon_path(settings[Settings.COLOR]),
                                          self.reset_to_defaults,
                                          settings,
                                          (410, 555),
                                          (460, 100)),
        ]

        self._back_to_menu_button = RoundIconButton(
            resolve_back_arrow_icon_path(settings[Settings.COLOR]),
            self.switch_back_to_main_menu,
            settings,
            (40, 40),
            30)

        self.all_buttons = [self._back_to_menu_button] + self._settings_buttons

    def _reinitialize_buttons(self, settings):
        self._initialize_buttons(settings)

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
        save_selected_settings(self._app.settings)

    def toggle_music(self):
        self._app.settings[Settings.MUSIC] = not self._app.settings[Settings.MUSIC]
        self._app.switch_music(self._music_file_path)
        self._reinitialize_buttons(self._app.settings)
        save_selected_settings(self._app.settings)

    def toggle_sounds(self):
        self._app.settings[Settings.SOUNDS] = not self._app.settings[Settings.SOUNDS]
        self._reinitialize_buttons(self._app.settings)
        save_selected_settings(self._app.settings)

    def reset_to_defaults(self):
        self._app.settings[Settings.COLOR] = ColorMode.LIGHT
        if not self._app.settings[Settings.MUSIC]:
            self._app.settings[Settings.MUSIC] = True
            self._app.switch_music(self._music_file_path)
        self._app.settings[Settings.SOUNDS] = True
        self._component.rerender()
        self._reinitialize_buttons(self._app.settings)
        save_selected_settings(self._app.settings)

    def switch_back_to_main_menu(self):
        self._app.switch_component(Components.MAIN_MENU, switch_music=False)


def save_selected_settings(settings):
    with open(os.path.join(ABS_PROJECT_ROOT_PATH, "game_app/settings.cfg"), 'wb') as settings_file:
        pickle.dump(settings, settings_file, protocol=pickle.HIGHEST_PROTOCOL)


def resolve_back_arrow_icon_path(color_mode):
    resource_dir = os.path.join(ABS_PROJECT_ROOT_PATH, 'game_app/resources/images/common')
    return os.path.join(resource_dir,
                        'left_arrow_white.png' if color_mode == ColorMode.DARK else 'left_arrow_black.png')


def resolve_color_mode_button_text_and_icon_path(color_mode):
    resource_dir = os.path.join(ABS_PROJECT_ROOT_PATH, 'game_app/resources/images/settings')
    if color_mode == ColorMode.DARK:
        return "Switch to light mode", os.path.join(resource_dir, 'moon.png')
    else:
        return "Switch to dark mode", os.path.join(resource_dir, 'sun.png')


def resolve_music_button_text_and_icon_path(color_mode, music_on):
    resource_dir = os.path.join(ABS_PROJECT_ROOT_PATH, 'game_app/resources/images/common')
    if music_on:
        return "Switch music off", os.path.join(resource_dir,
                                                'music_on_white.png' if color_mode == ColorMode.DARK
                                                else 'music_on_black.png')
    else:
        return "Switch music on", os.path.join(resource_dir,
                                               'music_off_white.png' if color_mode == ColorMode.DARK
                                               else 'music_off_black.png')


def resolve_sounds_button_text_and_icon_path(color_mode, sounds_on):
    resource_dir = os.path.join(ABS_PROJECT_ROOT_PATH, 'game_app/resources/images/common')
    if sounds_on:
        return "Switch sounds off", os.path.join(resource_dir,
                                                 'sounds_on_white.png' if color_mode == ColorMode.DARK
                                                 else 'sounds_on_black.png')
    else:
        return "Switch sounds on", os.path.join(resource_dir,
                                                'sounds_off_white.png' if color_mode == ColorMode.DARK
                                                else 'sounds_off_black.png')


def resolve_reset_icon_path(color_mode):
    resource_dir = os.path.join(ABS_PROJECT_ROOT_PATH, 'game_app/resources/images/settings')
    return os.path.join(resource_dir,
                        'reset_icon_white.png' if color_mode == ColorMode.DARK else 'reset_icon_black.png')

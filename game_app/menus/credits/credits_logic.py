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
import webbrowser

common_image_resource_dir = os.path.join(ABS_PROJECT_ROOT_PATH, 'game_app/resources/images/common')
settings_image_resource_dir = os.path.join(ABS_PROJECT_ROOT_PATH, 'game_app/resources/images/settings')
tic_tac_toe_image_resource_dir = os.path.join(ABS_PROJECT_ROOT_PATH, 'game_app/resources/images/tic_tac_toe')


class CreditsLogic:
    def __init__(self, app):
        self._app = app

        self._link_buttons = [
            # back_arrow
            RoundIconButton(resolve_back_arrow_image_path(app.settings[Settings.COLOR]),
                            lambda: webbrowser.open('https://www.flaticon.com/authors/roundicons'),
                            app, (100, 600), 30),
            # music on
            RoundIconButton(resolve_music_on_image_path(app.settings[Settings.COLOR]),
                            lambda: webbrowser.open('https://www.flaticon.com/authors/smashicons'),
                            app, (200, 600), 30),
            # music off
            RoundIconButton(resolve_music_off_image_path(app.settings[Settings.COLOR]),
                            lambda: webbrowser.open('https://www.flaticon.com/authors/smashicons'),
                            app, (300, 600), 30),
            # sounds on
            RoundIconButton(resolve_sounds_on_image_path(app.settings[Settings.COLOR]),
                            lambda: webbrowser.open('https://www.flaticon.com/authors/smashicons'),
                            app, (400, 600), 30),
            # sounds off
            RoundIconButton(resolve_sounds_off_image_path(app.settings[Settings.COLOR]),
                            lambda: webbrowser.open('https://www.flaticon.com/authors/smashicons'),
                            app, (500, 600), 30),
            # moon
            RoundIconButton(resolve_moon_image_path(app.settings[Settings.COLOR]),
                            lambda: webbrowser.open('https://www.flaticon.com/authors/freepik'),
                            app, (600, 600), 30),
            # sun
            RoundIconButton(resolve_sun_image_path(app.settings[Settings.COLOR]),
                            lambda: webbrowser.open('https://www.flaticon.com/authors/good-ware'),
                            app, (700, 600), 30),
            # reset
            RoundIconButton(resolve_reset_image_path(app.settings[Settings.COLOR]),
                            lambda: webbrowser.open('https://www.flaticon.com/authors/freepik'),
                            app, (800, 600), 30),
            # play
            RoundIconButton(resolve_play_image_path(app.settings[Settings.COLOR]),
                            lambda: webbrowser.open('https://www.flaticon.com/authors/those-icons'),
                            app, (900, 600), 30),
            # pause
            RoundIconButton(resolve_pause_image_path(app.settings[Settings.COLOR]),
                            lambda: webbrowser.open('https://www.flaticon.com/authors/freepik'),
                            app, (1000, 600), 30),
            # next
            RoundIconButton(resolve_next_image_path(app.settings[Settings.COLOR]),
                            lambda: webbrowser.open('https://www.flaticon.com/authors/those-icons'),
                            app, (1100, 600), 30),
        ]

        self._back_to_menu_button = RoundIconButton(resolve_back_arrow_image_path(app.settings[Settings.COLOR]),
                                                    self.switch_back_to_main_menu, app, (40, 40), 30)

        self.all_buttons = [self._back_to_menu_button] + self._link_buttons

    def handle_event(self, event):
        if event.type == MOUSEBUTTONUP:
            for pressed_button in filter(lambda button: button.contains_point(event.pos), self.all_buttons):
                pressed_button.on_pressed()

    def switch_back_to_main_menu(self):
        self._app.switch_component(Components.MAIN_MENU, switch_music=False)


def resolve_back_arrow_image_path(color_mode):
    return os.path.join(common_image_resource_dir,
                        'back_arrow_white.png' if color_mode == ColorMode.DARK else 'back_arrow_black.png')


def resolve_music_on_image_path(color_mode):
    return os.path.join(common_image_resource_dir,
                        'music_on_white.png' if color_mode == ColorMode.DARK else 'music_on_black.png')


def resolve_music_off_image_path(color_mode):
    return os.path.join(common_image_resource_dir,
                        'music_off_white.png' if color_mode == ColorMode.DARK else 'music_off_black.png')


def resolve_sounds_on_image_path(color_mode):
    return os.path.join(common_image_resource_dir,
                        'sounds_on_white.png' if color_mode == ColorMode.DARK else 'sounds_on_black.png')


def resolve_sounds_off_image_path(color_mode):
    return os.path.join(common_image_resource_dir,
                        'sounds_off_white.png' if color_mode == ColorMode.DARK else 'sounds_off_black.png')


def resolve_moon_image_path(color_mode):
    return os.path.join(settings_image_resource_dir,
                        'moon_white.png' if color_mode == ColorMode.DARK else 'moon_black.png')


def resolve_sun_image_path(color_mode):
    return os.path.join(settings_image_resource_dir,
                        'sun_white.png' if color_mode == ColorMode.DARK else 'sun_black.png')


def resolve_reset_image_path(color_mode):
    return os.path.join(settings_image_resource_dir,
                        'reset_icon_white.png' if color_mode == ColorMode.DARK else 'reset_icon_black.png')


def resolve_play_image_path(color_mode):
    return os.path.join(tic_tac_toe_image_resource_dir,
                        'play_white.png' if color_mode == ColorMode.DARK else 'play_black.png')


def resolve_pause_image_path(color_mode):
    return os.path.join(tic_tac_toe_image_resource_dir,
                        'pause_white.png' if color_mode == ColorMode.DARK else 'pause_black.png')


def resolve_next_image_path(color_mode):
    return os.path.join(tic_tac_toe_image_resource_dir,
                        'next_white.png' if color_mode == ColorMode.DARK else 'next_black.png')

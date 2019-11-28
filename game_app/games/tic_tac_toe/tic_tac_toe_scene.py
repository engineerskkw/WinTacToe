# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#


import pygame
from itertools import product
from pygame.rect import Rect
from pygame.mixer import Sound
from game_app.common_helper import TurnState, Settings, ColorMode
from game_app.common.buttons import RectangularTextButton, RoundIconButton

symbols = {
    0: 'X',
    1: 'O',
    2: 'A',
}


class TicTacToeScene:
    def __init__(self, component, screen, board_size, settings, player_mark, opponent_mark):
        self._component = component
        self._screen = screen
        self._board_size = board_size
        self._player_mark = player_mark
        self._opponent_mark = opponent_mark

        self._background_color = (45, 45, 45) if settings[Settings.COLOR] == ColorMode.DARK else (230, 230, 230)
        self._message_color = (230, 230, 230) if settings[Settings.COLOR] == ColorMode.DARK else (25, 25, 25)
        self._game_over_displayed = False

        self._background_displayed = False

        self._square_size = 720 // self._board_size
        self._tic_tac_toe_buttons = []
        for row in range(self._board_size):
            self._tic_tac_toe_buttons.append([])
            for column in range(self._board_size):
                position = (280 + column * self._square_size, row * self._square_size)
                self._tic_tac_toe_buttons[row].append(TicTacToeButton(settings,
                                                                      position,
                                                                      self._square_size,
                                                                      self._component,
                                                                      (row, column),
                                                                      self._player_mark,
                                                                      self._opponent_mark))

        self._restart_button = RectangularTextFramedButton("Restart",
                                                           lambda: self._component.restart(),
                                                           settings, (1040, 20), (200, 50), 3)

        self._main_menu_button = RectangularTextFramedButton("MainMenu",
                                                             lambda: self._component.back_to_menu(),
                                                             settings, (1040, 90), (200, 50), 3)

        # icon_path, action, settings, position, center_position, radius
        self._toggle_sounds_button = RoundFramedIconButton(
            resolve_sounds_button_icon_path(settings[Settings.COLOR], settings[Settings.SOUNDS]),
            lambda: print("TODODOODODOSOUNDS"),
            settings,
            (1100, 665), #(1090, 665),
            35,
            3)

        self._toggle_music_button = RoundFramedIconButton(
            resolve_music_button_icon_path(settings[Settings.COLOR], settings[Settings.SOUNDS]),
            lambda: print("TODODOODODOMUSIC"),
            settings,
            (1200, 665), #(1190, 665),
            35,
            3)

        # RectangularTextButtonWithIcon(
        #     *resolve_sounds_button_text_and_icon_path(settings[Settings.COLOR], settings[Settings.SOUNDS]),
        #     self.toggle_sounds,
        #     settings,
        #     (410, 395),
        #     (460, 100)),
        # RectangularTextButtonWithIcon("Reset to defaults",
        #                               resolve_reset_icon_path(settings[Settings.COLOR]),
        #                               self.reset_to_defaults,
        #                               settings,
        #                               (410, 555),
        #                               (460, 100)),
        #
        # def resolve_music_button_text_and_icon_path(color_mode, music_on):
        #     resource_dir = os.path.join(ABS_PROJECT_ROOT_PATH, 'game_app/resources/images/common')
        #     if music_on:
        #         return "Switch music off", os.path.join(resource_dir,
        #                                                 'music_on_white.png' if color_mode == ColorMode.DARK
        #                                                 else 'music_on_black.png')
        #     else:
        #         return "Switch music on", os.path.join(resource_dir,
        #                                                'music_off_white.png' if color_mode == ColorMode.DARK
        #                                                else 'music_off_black.png')
        #
        # def resolve_sounds_button_text_and_icon_path(color_mode, sounds_on):
        #     resource_dir = os.path.join(ABS_PROJECT_ROOT_PATH, 'game_app/resources/images/common')
        #     if sounds_on:
        #         return "Switch sounds off", os.path.join(resource_dir,
        #                                                  'sounds_on_white.png' if color_mode == ColorMode.DARK
        #                                                  else 'sounds_on_black.png')
        #     else:
        #         return "Switch sounds on", os.path.join(resource_dir,
        #                                                 'sounds_off_white.png' if color_mode == ColorMode.DARK
        #                                                 else 'sounds_off_black.png')

        self.all_buttons = [self._restart_button, self._main_menu_button, self._toggle_sounds_button,
                            self._toggle_music_button] + sum(self._tic_tac_toe_buttons, [])

    def render(self):
        self._display_background(self._screen)
        self._display_game_over_situation()
        self._render_buttons()
        pygame.display.flip()

    def _display_background(self, screen):
        if not self._background_displayed:
            background = pygame.Surface(screen.get_size())
            background.fill(self._background_color)
            screen.blit(background, (0, 0))
            self._background_displayed = True

    def _display_game_over_situation(self):
        if not self._game_over_displayed and self._component.winnings:
            [button.set_disabled() for button in sum(self._tic_tac_toe_buttons, [])]
            for winning in self._component.winnings:
                [self._tic_tac_toe_buttons[x][y].set_winning() for (x, y) in winning.points_included]
            self._display_game_over_message(self._component.winnings[0].mark)
            self._play_game_over_sound(self._component.winnings[0].mark == self._player_mark)
            self._game_over_displayed = True

    def _play_game_over_sound(self, victory):
        directory = os.path.join(ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/tic_tac_toe")
        self._component.play_sound_stopping_music(os.path.join(directory, "victory.wav" if victory else "failure.wav"))

    def _render_buttons(self):
        for button in self.all_buttons:
            button.render(self._screen, pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0] == 1)

    def _display_mesasge(self, text):
        font = pygame.font.Font(None, 50)
        self._screen.blit(font.render(text, True, self._message_color), (5, 5))

    def _display_game_over_message(self, winners_mark):
        if winners_mark == self._player_mark:
            self._display_mesasge("You win!  :D")
        else:
            self._display_mesasge("You lose  :(")

    def handle_state_changed(self, new_game_state):
        new_game_board = new_game_state.board
        for row, col in product(list(range(self._board_size)), repeat=2):
            if not new_game_board[row, col] == self._tic_tac_toe_buttons[row][col].mark:
                if new_game_board[row, col] == -1:
                    self._tic_tac_toe_buttons[row][col].set_unmarked()
                else:
                    self._tic_tac_toe_buttons[row][col].set_marked_by_opponent()


class RectangularTextFramedButton(RectangularTextButton):
    def __init__(self, text, action, settings, position, size, frame_size):
        super().__init__(text, action, settings, position, size)
        self._base_color = (45, 45, 45) if settings[Settings.COLOR] == ColorMode.DARK else (230, 230, 230)
        self._hovered_color = (70, 70, 70) if settings[Settings.COLOR] == ColorMode.DARK else (200, 200, 200)
        self._pressed_color = (32, 32, 32) if settings[Settings.COLOR] == ColorMode.DARK else (150, 150, 150)
        self._frame_color = (230, 230, 230) if settings[Settings.COLOR] == ColorMode.DARK else (25, 25, 25)
        self._text_color = (230, 230, 230) if settings[Settings.COLOR] == ColorMode.DARK else (25, 25, 25)
        self._frame_size = frame_size

    def render(self, screen, mouse_position, is_mouse_pressed):
        super().render(screen, mouse_position, is_mouse_pressed)
        figure = Rect(self._position, self._size)
        pygame.draw.rect(screen, self._frame_color, figure, self._frame_size)


class RoundFramedIconButton(RoundIconButton):
    def __init__(self, icon_path, action, settings, center_position, radius, frame_size):
        super().__init__(icon_path, action, settings, center_position, radius)

        # self._base_color = (70, 70, 70) if settings[Settings.COLOR] == ColorMode.DARK else (190, 190, 190)
        # self._hovered_color = (60, 60, 60) if settings[Settings.COLOR] == ColorMode.DARK else (170, 170, 170)
        # self._pressed_color = (50, 50, 50) if settings[Settings.COLOR] == ColorMode.DARK else (155, 155, 155)

        self._base_color = (45, 45, 45) if settings[Settings.COLOR] == ColorMode.DARK else (230, 230, 230)
        self._hovered_color = (70, 70, 70) if settings[Settings.COLOR] == ColorMode.DARK else (200, 200, 200)
        self._pressed_color = (32, 32, 32) if settings[Settings.COLOR] == ColorMode.DARK else (150, 150, 150)

        self._frame_color = (230, 230, 230) if settings[Settings.COLOR] == ColorMode.DARK else (25, 25, 25)

        self._frame_size = frame_size

    def render(self, screen, mouse_position, is_mouse_pressed):
        super().render(screen, mouse_position, is_mouse_pressed)
        pygame.draw.circle(screen, self._frame_color, self._center_position, self._radius, self._frame_size)


class TicTacToeButton(RectangularTextFramedButton):
    def __init__(self, settings, position, size, component, game_position, player_mark, opponent_mark):
        super().__init__("", self.action, settings, position, (size, size), max(min(size // 30, 5), 1))
        self._component = component
        self._game_position = game_position
        self._player_mark = player_mark
        self._opponent_mark = opponent_mark

        self.mark = -1
        self._font = pygame.font.Font(None, size)
        self._is_disabled = False
        self._is_winning = False
        self._disabled_color = (32, 32, 32) if settings[Settings.COLOR] == ColorMode.DARK else (150, 150, 150)
        self._winning_color = (100, 100, 100) if settings[Settings.COLOR] == ColorMode.DARK else (230, 230, 230)
        self._mark_color = (230, 230, 230) if settings[Settings.COLOR] == ColorMode.DARK else (25, 25, 25)
        self._click_sound = Sound(
            os.path.join(ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/tic_tac_toe/move_sound_1.wav"))
        self._disabled_click_sound = Sound(os.path.join(
            ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/common/disabled_button_sound.wav"))

    def on_pressed(self):
        if self._is_disabled or self._component.turn == TurnState.NOT_YOUR_TURN:
            if self._sounds_on:
                self._disabled_click_sound.play()
        else:
            super().on_pressed()

    def action(self):
        self.set_disabled()
        self.mark = self._player_mark
        self.set_text(symbols[self._player_mark])
        self._component.step(self._game_position)

    def set_marked_by_opponent(self):
        if self._is_disabled:
            return
        self.set_text(symbols[self._opponent_mark])
        self.mark = self._opponent_mark
        self.set_disabled()

    def set_unmarked(self):
        self._is_disabled = False
        self.set_text("")
        self.mark = -1
        return

    def set_text(self, text):
        self._text = self._font.render(text, True, self._mark_color)

    def _get_color(self, mouse_position, is_mouse_pressed):
        if self._is_winning:
            return self._winning_color
        if self._is_disabled:
            return self._disabled_color
        return super()._get_color(mouse_position, is_mouse_pressed)

    def set_disabled(self):
        self._is_disabled = True

    def set_winning(self):
        self._is_winning = True


def resolve_music_button_icon_path(color_mode, music_on):
    resource_dir = os.path.join(ABS_PROJECT_ROOT_PATH, 'game_app/resources/images/common')
    if music_on:
        return os.path.join(resource_dir,
                            'music_on_white.png' if color_mode == ColorMode.DARK else 'music_on_black.png')
    else:
        return os.path.join(resource_dir,
                            'music_off_white.png' if color_mode == ColorMode.DARK else 'music_off_black.png')


def resolve_sounds_button_icon_path(color_mode, sounds_on):
    resource_dir = os.path.join(ABS_PROJECT_ROOT_PATH, 'game_app/resources/images/common')
    if sounds_on:
        return os.path.join(resource_dir,
                            'sounds_on_white.png' if color_mode == ColorMode.DARK else 'sounds_on_black.png')
    else:
        return os.path.join(resource_dir,
                            'sounds_off_white.png' if color_mode == ColorMode.DARK else 'sounds_off_black.png')

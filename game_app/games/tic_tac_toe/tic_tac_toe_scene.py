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
from game_app.common.common_helper import TurnState, Settings, ColorMode, GameMode
from game_app.common.buttons import RectangularTextButton, RoundIconButton
from pygame import gfxdraw


symbols = {
    0: 'X',
    1: 'O',
    2: 'A',
}


class TicTacToeScene:
    def __init__(self, component, app, screen, board_size, player_mark, opponent_mark):
        self._component = component
        self._app = app
        self._screen = screen
        self._board_size = board_size
        self._player_mark = player_mark
        self._opponent_mark = opponent_mark

        self._background_color = (45, 45, 45) if app.settings[Settings.COLOR] == ColorMode.DARK else (230, 230, 230)
        self._message_color = (230, 230, 230) if app.settings[Settings.COLOR] == ColorMode.DARK else (25, 25, 25)
        self._message_font = pygame.font.Font(None, 50)
        self._sub_message_font = pygame.font.Font(None, 25)
        self._game_over_situation_displayed = False
        self._background_and_messages_displayed = False

        self._opponent_sound_on = self._component.game_mode == GameMode.AgentVsAgent
        self._square_size = 720 // self._board_size
        self._tic_tac_toe_buttons = []
        for row in range(self._board_size):
            self._tic_tac_toe_buttons.append([])
            for column in range(self._board_size):
                position = (280 + column * self._square_size, row * self._square_size)
                self._tic_tac_toe_buttons[row].append(TicTacToeButton(app,
                                                                      position,
                                                                      self._square_size,
                                                                      self._component,
                                                                      (row, column),
                                                                      self._player_mark,
                                                                      self._opponent_mark))

        self._restart_button = RectangularTextFramedButton("Restart", lambda: self._component.restart(),
                                                           app, (1040, 20), (200, 50), 3)

        self._main_menu_button = RectangularTextFramedButton("MainMenu", lambda: self._component.back_to_menu(),
                                                             app, (1040, 90), (200, 50), 3)

        self._toggle_sounds_button = RoundFramedIconButton(
            resolve_sounds_button_icon_path(app.settings[Settings.COLOR], app.settings[Settings.SOUNDS]),
            self._component.toggle_sounds, app, (1085, 665), 32, 2)

        self._toggle_music_button = RoundFramedIconButton(
            resolve_music_button_icon_path(app.settings[Settings.COLOR], app.settings[Settings.MUSIC]),
            self._component.toggle_music, app, (1195, 665), 32, 2)

        self.all_buttons = [self._restart_button, self._main_menu_button, self._toggle_sounds_button,
                            self._toggle_music_button] + sum(self._tic_tac_toe_buttons, [])

    def render(self):
        self._display_game_over_situation()
        self._display_background_and_messages(self._screen)
        self._render_buttons()
        pygame.display.flip()

    def _display_game_over_situation(self):
        if not self._game_over_situation_displayed and self._component.winnings:
            if self._component.winnings == -1:
                self._play_game_over_sound(0)
            else:
                [button.set_disabled() for button in sum(self._tic_tac_toe_buttons, [])]
                for winning in self._component.winnings:
                    [self._tic_tac_toe_buttons[x][y].set_winning() for (x, y) in winning.points_included]
                self._play_game_over_sound(1 if self._component.winnings[0].mark == self._player_mark else 2)
            self._background_and_messages_displayed = False
            self._game_over_situation_displayed = True

    def _play_game_over_sound(self, game_over_state):
        directory = os.path.join(ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/tic_tac_toe")
        if game_over_state == 0:
            self._component.play_sound_stopping_music(os.path.join(directory, "moderate_applause.wav"))
        elif game_over_state == 1:
            self._component.play_sound_stopping_music(os.path.join(directory, "victory.wav"))
        else:
            self._component.play_sound_stopping_music(os.path.join(directory, "failure.wav"))

    def _display_background_and_messages(self, screen):
        if not self._background_and_messages_displayed:
            background = pygame.Surface(screen.get_size())
            background.fill(self._background_color)
            screen.blit(background, (0, 0))
            if self._game_over_situation_displayed:
                self._display_game_over_message(self._component.winnings)
            else:
                self._display_helper_message()
                if self._component.game_mode == GameMode.PlayerVsAgent:
                    if self._component.turn == TurnState.NOT_YOUR_TURN:
                        self._display_game_state_message("Agent's move", "Please, wait for your turn...")
                    else:
                        self._display_game_state_message("Your move", "Select a field on the board",
                                                         "to place your mark there")
            self._background_and_messages_displayed = True

    def _display_helper_message(self):
        #TODO think about how the helper texts should look like in AvA
        if self._component.game_mode == GameMode.PlayerVsAgent:
            self._screen.blit(self._sub_message_font.render("You're playing as:", True, self._message_color), (20, 655))
            self._screen.blit(self._message_font.render(symbols[self._player_mark], True, self._message_color), (173, 646))
        else:
            self._screen.blit(self._sub_message_font.render("Your agent's playing as:", True, self._message_color), (20, 655))
            self._screen.blit(self._message_font.render(symbols[self._player_mark], True, self._message_color),
                              (220, 646))
        self._screen.blit(self._sub_message_font.render("Connect %d marks to win" % self._component.marks_required,
                                                        True, self._message_color), (20, 683))

    def _display_game_state_message(self, text1, text2='', text3=''):
        self._screen.blit(self._message_font.render(text1, True, self._message_color), (20, 20))
        self._screen.blit(self._sub_message_font.render(text2, True, self._message_color), (20, 67))
        self._screen.blit(self._sub_message_font.render(text3, True, self._message_color), (20, 95))

    def _display_game_over_message(self, winnings):
        if winnings == -1:
            self._display_game_state_message("It's a tie!", "Nice try")
        elif winnings[0].mark == self._player_mark:
            self._display_game_state_message("You win!", "Congratulations")
        else:
            self._display_game_state_message("You lose!", "Better luck next time")

    def _render_buttons(self):
        for button in self.all_buttons:
            button.render(self._screen, pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0] == 1)

    def handle_state_changed(self, new_game_state):
        new_game_board = new_game_state.board
        for row, col in product(list(range(self._board_size)), repeat=2):
            if not new_game_board[row, col] == self._tic_tac_toe_buttons[row][col].mark:
                if new_game_board[row, col] == -1:
                    self._tic_tac_toe_buttons[row][col].set_unmarked()
                else:
                    self._tic_tac_toe_buttons[row][col].set_marked_by_opponent(self._opponent_sound_on)

    def handle_turn_changed(self):
        self._background_and_messages_displayed = False

    def update_music_button(self):
        self._toggle_music_button.set_icon(resolve_music_button_icon_path(
            self._app.settings[Settings.COLOR], self._app.settings[Settings.MUSIC]))

    def update_sounds_button(self):
        self._toggle_sounds_button.set_icon(resolve_sounds_button_icon_path(
            self._app.settings[Settings.COLOR], self._app.settings[Settings.SOUNDS]))


class RectangularTextFramedButton(RectangularTextButton):
    def __init__(self, text, action, app, position, size, frame_size):
        super().__init__(text, action, app, position, size)
        self._base_color = (45, 45, 45) if self._dark_mode_on else (230, 230, 230)
        self._hovered_color = (70, 70, 70) if self._dark_mode_on else (200, 200, 200)
        self._pressed_color = (32, 32, 32) if self._dark_mode_on else (150, 150, 150)
        self._frame_color = (230, 230, 230) if self._dark_mode_on else (25, 25, 25)
        self._text_color = (230, 230, 230) if self._dark_mode_on else (25, 25, 25)
        self._frame_size = frame_size

    def render(self, screen, mouse_position, is_mouse_pressed):
        super().render(screen, mouse_position, is_mouse_pressed)
        figure = Rect(self._position, self._size)
        pygame.draw.rect(screen, self._frame_color, figure, self._frame_size)


class RoundFramedIconButton(RoundIconButton):
    def __init__(self, icon_path, action, app, center_position, radius, frame_size):
        super().__init__(icon_path, action, app, center_position, radius)
        self._frame_size = frame_size
        self._base_color = (45, 45, 45) if self._dark_mode_on else (230, 230, 230)
        self._hovered_color = (70, 70, 70) if self._dark_mode_on else (200, 200, 200)
        self._pressed_color = (32, 32, 32) if self._dark_mode_on else (150, 150, 150)
        self._frame_color = (230, 230, 230) if self._dark_mode_on else (25, 25, 25)

    def render(self, screen, mouse_position, is_mouse_pressed):
        gfxdraw.filled_circle(screen, self._center_position[0], self._center_position[1],
                              self._radius + self._frame_size, self._frame_color)
        super().render(screen, mouse_position, is_mouse_pressed)


class TicTacToeButton(RectangularTextFramedButton):
    def __init__(self, app, position, size, component, game_position, player_mark, opponent_mark):
        super().__init__("", self.action, app, position, (size, size), max(min(size // 30, 5), 1))
        self._component = component
        self._game_position = game_position
        self._player_mark = player_mark
        self._opponent_mark = opponent_mark

        self.mark = -1
        self._font = pygame.font.Font(None, size)
        self._is_disabled = False
        self._is_winning = False
        self._disabled_color = (32, 32, 32) if self._dark_mode_on else (150, 150, 150)
        self._winning_color = (100, 100, 100) if self._dark_mode_on else (230, 230, 230)
        self._mark_color = (230, 230, 230) if self._dark_mode_on else (25, 25, 25)
        self._click_sound = Sound(
            os.path.join(ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/tic_tac_toe/move_sound.wav"))
        self._disabled_click_sound = Sound(os.path.join(
            ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/common/disabled_button_sound.wav"))

    def on_pressed(self):
        if self._is_disabled or self._component.turn == TurnState.NOT_YOUR_TURN:
            if self._app.settings[Settings.SOUNDS]:
                self._disabled_click_sound.play()
        else:
            super().on_pressed()

    def action(self):
        self.set_disabled()
        self.mark = self._player_mark
        self.set_text(symbols[self._player_mark])
        self._component.step(self._game_position)

    def set_marked_by_opponent(self, play_sound=False):
        if self._is_disabled:
            return
        if play_sound:
            self._click_sound.play()
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

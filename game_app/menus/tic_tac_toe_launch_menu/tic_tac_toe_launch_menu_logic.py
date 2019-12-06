# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from pygame.locals import *
from game_app.common.common_helper import Components, ColorMode, Settings, Difficulty, GameMode
from game_app.common.buttons import RectangularTextButton, RoundIconButton, RectangularChoiceButtonWithSubtext, \
    RectangularDisableableChoiceButton


class TicTacToeLaunchMenuLogic:
    def __init__(self, app):
        self._app = app
        self._board_size = 3
        self._marks_required = 3
        self._mark = 0
        self._difficulty = Difficulty.MEDIUM
        self._game_mode = GameMode.PlayerVsAgent

        self._size_buttons = [RectangularChoiceButtonWithSubtext("3x3", "Playing to 3",
                                                                 lambda: self.change_board_size(3, 3),
                                                                 app, (250, 90), (180, 100), True),
                              RectangularChoiceButtonWithSubtext("5x5", "Playing to 3",
                                                                 lambda: self.change_board_size(5, 3),
                                                                 app, (450, 90), (180, 100), False),
                              RectangularChoiceButtonWithSubtext("5x5", "Playing to 4",
                                                                 lambda: self.change_board_size(5, 4),
                                                                 app, (650, 90), (180, 100), False),
                              RectangularChoiceButtonWithSubtext("10x10", "Playing to 4",
                                                                 lambda: self.change_board_size(10, 4),
                                                                 app, (850, 90), (180, 100), False),
                              RectangularChoiceButtonWithSubtext("10x10", "Playing to 5",
                                                                 lambda: self.change_board_size(10, 5),
                                                                 app, (250, 210), (180, 100), False),
                              RectangularChoiceButtonWithSubtext("20x20", "Playing to 5",
                                                                 lambda: self.change_board_size(20, 5),
                                                                 app, (450, 210), (180, 100), False),
                              RectangularChoiceButtonWithSubtext("30x30", "Playing to 5",
                                                                 lambda: self.change_board_size(30, 5),
                                                                 app, (650, 210), (180, 100), False),
                              RectangularChoiceButtonWithSubtext("40x40", "Playing to 5",
                                                                 lambda: self.change_board_size(40, 5),
                                                                 app, (850, 210), (180, 100), False),
                              ]

        self._game_mode_buttons = [RectangularChoiceButtonWithSubtext("Medium", "PlayerVsAgent",
                                                                      lambda: self.change_game_mode(
                                                                          GameMode.PlayerVsAgent, Difficulty.MEDIUM),
                                                                      app, (350, 380), (180, 100), True),
                                   RectangularChoiceButtonWithSubtext("Hard", "PlayerVsAgent",
                                                                      lambda: self.change_game_mode(
                                                                          GameMode.PlayerVsAgent, Difficulty.HARD),
                                                                      app, (550, 380), (180, 100), False),
                                   RectangularChoiceButtonWithSubtext("Spectator", "AgentVsAgent",
                                                                      lambda: self.change_game_mode(
                                                                          GameMode.AgentVsAgent, Difficulty.HARD),
                                                                      app, (750, 380), (180, 100), False),
                                   ]

        self._mark_buttons = [RectangularDisableableChoiceButton("X", lambda: self.change_mark(0),
                                                                 app, (450, 550), (180, 100), True, True),
                              RectangularDisableableChoiceButton("O", lambda: self.change_mark(1),
                                                                 app, (650, 550), (180, 100), False, True),
                              ]

        self._start_button = RectangularTextButton("Let's go!",
                                                   self.switch_to_tic_tac_toe,
                                                   app, (1080, 600), (180, 100))

        self._back_to_menu_button = RoundIconButton(resolve_back_arrow_image_path(app.settings[Settings.COLOR]),
                                                    self.switch_back_to_main_menu, app, (40, 40), 30)

        self.all_buttons = [self._start_button, self._back_to_menu_button] + self._size_buttons + self._mark_buttons \
                           + self._game_mode_buttons

    def handle_event(self, event):
        if event.type == MOUSEBUTTONUP:
            for pressed_button in filter(lambda button: button.contains_point(event.pos), self.all_buttons):
                pressed_button.on_pressed()

    def change_board_size(self, new_size, new_marks_required):
        if new_size != self._board_size or new_marks_required != self._marks_required:
            for size_button in self._size_buttons:
                size_button.set_chosen(False)
            self._board_size = new_size
            self._marks_required = new_marks_required

    def change_mark(self, new_mark):
        if new_mark != self._mark:
            for button in self._mark_buttons:
                button.set_chosen(False)
            self._mark = new_mark

    def change_game_mode(self, new_game_mode, new_difficulty):
        if new_game_mode != self._game_mode or new_difficulty != self._difficulty:
            for button in self._game_mode_buttons:
                button.set_chosen(False)
            self._game_mode = new_game_mode
            self._difficulty = new_difficulty
            self.mark_buttons_set_enabled(new_game_mode == GameMode.PlayerVsAgent)

    def mark_buttons_set_enabled(self, enabled):
        for mark_button in self._mark_buttons:
            mark_button.set_enabled(enabled)

    def switch_back_to_main_menu(self):
        self._app.switch_component(Components.MAIN_MENU, switch_music=False)

    def switch_to_tic_tac_toe(self):
        player_mark = self._mark if self._game_mode == GameMode.PlayerVsAgent else 0
        opponent_mark = abs(self._mark - 1) if self._game_mode == GameMode.PlayerVsAgent else 1
        self._app.switch_component(Components.TIC_TAC_TOE,
                                   board_size=self._board_size,
                                   marks_required=self._marks_required,
                                   player_mark=player_mark,
                                   opponent_mark=opponent_mark,
                                   difficulty=self._difficulty,
                                   game_mode=self._game_mode)


def resolve_back_arrow_image_path(color_mode):
    resource_dir = os.path.join(ABS_PROJECT_ROOT_PATH, 'game_app/resources/images/common')
    return os.path.join(resource_dir,
                        'left_arrow_white.png' if color_mode == ColorMode.DARK else 'left_arrow_black.png')

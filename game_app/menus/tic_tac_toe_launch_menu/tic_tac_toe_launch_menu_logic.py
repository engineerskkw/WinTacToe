# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from pygame.locals import *

from game_app.common_helper import Components, ColorMode, Settings
from game_app.common.buttons import RectangularChoiceButton, \
    DisableableRectangularTextButton, RoundIconButton


class TicTacToeLaunchMenuLogic:
    def __init__(self, app):
        self._app = app
        self._board_size = 3
        self._marks_required = 3
        self._mark = 0

        self._size_buttons = [RectangularChoiceButton("3x3",
                                                      lambda: self.change_board_size(3),
                                                      app,
                                                      (150, 100),
                                                      (130, 100),
                                                      True),
                              RectangularChoiceButton("5x5",
                                                      lambda: self.change_board_size(5),
                                                      app,
                                                      (320, 100),
                                                      (130, 100),
                                                      False),
                              RectangularChoiceButton("10x10",
                                                      lambda: self.change_board_size(10),
                                                      app,
                                                      (490, 100),
                                                      (130, 100),
                                                      False),
                              RectangularChoiceButton("20x20",
                                                      lambda: self.change_board_size(20),
                                                      app,
                                                      (660, 100),
                                                      (130, 100),
                                                      False),
                              RectangularChoiceButton("30x30",
                                                      lambda: self.change_board_size(30),
                                                      app,
                                                      (830, 100),
                                                      (130, 100),
                                                      False),
                              RectangularChoiceButton("40x40",
                                                      lambda: self.change_board_size(40),
                                                      app,
                                                      (1000, 100),
                                                      (130, 100),
                                                      False),
                              ]

        self._marks_required_buttons = [RectangularChoiceButton("3",
                                                                lambda: self.change_marks_required(3),
                                                                app,
                                                                (400, 300),
                                                                (130, 100),
                                                                True),
                                        RectangularChoiceButton("4",
                                                                lambda: self.change_marks_required(4),
                                                                app,
                                                                (575, 300),
                                                                (130, 100),
                                                                False),
                                        RectangularChoiceButton("5",
                                                                lambda: self.change_marks_required(5),
                                                                app,
                                                                (750, 300),
                                                                (130, 100),
                                                                False),
                                        ]

        self._mark_buttons = [RectangularChoiceButton("X",
                                                      lambda: self.change_mark(0),
                                                      app,
                                                      (490, 500),
                                                      (130, 100),
                                                      True),
                              RectangularChoiceButton("O",
                                                      lambda: self.change_mark(1),
                                                      app,
                                                      (660, 500),
                                                      (130, 100),
                                                      False),
                              ]

        self._start_button = DisableableRectangularTextButton("Let's go!",
                                                              "Bad params",
                                                              self.switch_to_tic_tac_toe,
                                                              app,
                                                              (1030, 590),
                                                              (230, 110),
                                                              False)

        self._back_to_menu_button = RoundIconButton(
            resolve_back_arrow_image_path(app.settings[Settings.COLOR]),
            self.switch_back_to_main_menu,
            app,
            (40, 40),
            30)

        self.all_buttons = [self._start_button, self._back_to_menu_button] + \
                           self._size_buttons + self._marks_required_buttons + self._mark_buttons

    def handle_event(self, event):
        if event.type == MOUSEBUTTONUP:
            for pressed_button in filter(lambda button: button.contains_point(event.pos), self.all_buttons):
                pressed_button.on_pressed()

    def change_board_size(self, new_size):
        if new_size != self._board_size:
            for size_button in self._size_buttons:
                size_button.set_chosen(False)
            self._board_size = new_size
            self._start_button.set_disabled(new_size < self._marks_required)

    def change_marks_required(self, new_marks_required):
        if new_marks_required != self._marks_required:
            for button in self._marks_required_buttons:
                button.set_chosen(False)
            self._marks_required = new_marks_required
            self._start_button.set_disabled(new_marks_required > self._board_size)

    def change_mark(self, new_mark):
        if new_mark != self._mark:
            for button in self._mark_buttons:
                button.set_chosen(False)
            self._mark = new_mark

    def switch_back_to_main_menu(self):
        self._app.switch_component(Components.MAIN_MENU, switch_music=False)

    def switch_to_tic_tac_toe(self):
        self._app.switch_component(Components.TIC_TAC_TOE,
                                   board_size=self._board_size,
                                   marks_required=self._marks_required,
                                   player_mark=self._mark,
                                   opponent_mark=abs(self._mark - 1))


def resolve_back_arrow_image_path(color_mode):
    resource_dir = os.path.join(ABS_PROJECT_ROOT_PATH, 'game_app/resources/images/common')
    return os.path.join(resource_dir,
                        'left_arrow_white.png' if color_mode == ColorMode.DARK else 'left_arrow_black.png')

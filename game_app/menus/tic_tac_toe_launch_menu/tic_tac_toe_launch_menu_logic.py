# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from pygame.locals import *
from game_app.common_helper import Components, ColorMode, Settings, Difficulty
from game_app.common.buttons import RectangularChoiceButton, RectangularTextButton, RoundIconButton, \
    RectangularChoiceButtonWithSubtext


class TicTacToeLaunchMenuLogic:
    def __init__(self, app):
        self._app = app
        self._board_size = 3
        self._marks_required = 3
        self._mark = 0
        self._difficulty = Difficulty.MEDIUM

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

        self._mark_buttons = [RectangularChoiceButton("X",
                                                      lambda: self.change_mark(0),
                                                      app, (450, 380), (180, 100), True),
                              RectangularChoiceButton("O",
                                                      lambda: self.change_mark(1),
                                                      app, (650, 380), (180, 100), False),
                              ]

        self._difficulty_buttons = [RectangularChoiceButton("Medium",
                                                            lambda: self.change_difficulty(Difficulty.MEDIUM),
                                                            app, (450, 550), (180, 100), True),
                                    RectangularChoiceButton("Hard",
                                                            lambda: self.change_difficulty(Difficulty.HARD),
                                                            app, (650, 550), (180, 100), False),
                                    ]

        self._start_button = RectangularTextButton("Let's go!",
                                                   self.switch_to_tic_tac_toe,
                                                   app, (1080, 600), (180, 100))

        self._back_to_menu_button = RoundIconButton(resolve_back_arrow_image_path(app.settings[Settings.COLOR]),
                                                    self.switch_back_to_main_menu, app, (40, 40), 30)

        self.all_buttons = [self._start_button, self._back_to_menu_button] + self._size_buttons + self._mark_buttons \
                           + self._difficulty_buttons

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

    def change_difficulty(self, new_difficulty):
        if new_difficulty != self._difficulty:
            for button in self._difficulty_buttons:
                button.set_chosen(False)
            self._difficulty = new_difficulty

    def switch_back_to_main_menu(self):
        self._app.switch_component(Components.MAIN_MENU, switch_music=False)

    def switch_to_tic_tac_toe(self):
        self._app.switch_component(Components.TIC_TAC_TOE,
                                   board_size=self._board_size,
                                   marks_required=self._marks_required,
                                   player_mark=self._mark,
                                   opponent_mark=abs(self._mark - 1),
                                   difficulty=self._difficulty)


def resolve_back_arrow_image_path(color_mode):
    resource_dir = os.path.join(ABS_PROJECT_ROOT_PATH, 'game_app/resources/images/common')
    return os.path.join(resource_dir,
                        'left_arrow_white.png' if color_mode == ColorMode.DARK else 'left_arrow_black.png')

# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from pygame.locals import *
from pygame.mixer import Sound

from game_app.common_helper import Components
from game_app.menus.menus_scene_commons.buttons import RectangularTextButton, RectangularChoiceButton, \
    DisableableRectangularTextButton, RoundIconButton


class TicTacToeLaunchMenuLogic:
    def __init__(self, app):
        self._app = app
        self._board_size = 3
        self._marks_required = 3
        self._mark = 0

        self._size_buttons = [RectangularChoiceButton("3x3",
                                                      lambda: self.change_board_size(3),
                                                      (150, 100),
                                                      (130, 100),
                                                      True),
                              RectangularChoiceButton("5x5",
                                                      lambda: self.change_board_size(5),
                                                      (320, 100),
                                                      (130, 100),
                                                      False),
                              RectangularChoiceButton("10x10",
                                                      lambda: self.change_board_size(10),
                                                      (490, 100),
                                                      (130, 100),
                                                      False),
                              RectangularChoiceButton("20x20",
                                                      lambda: self.change_board_size(20),
                                                      (660, 100),
                                                      (130, 100),
                                                      False),
                              RectangularChoiceButton("30x30",
                                                      lambda: self.change_board_size(30),
                                                      (830, 100),
                                                      (130, 100),
                                                      False),
                              RectangularChoiceButton("50x50",
                                                      lambda: self.change_board_size(50),
                                                      (1000, 100),
                                                      (130, 100),
                                                      False),
                              ]

        self._marks_required_buttons = [RectangularChoiceButton("3",
                                                                lambda: self.change_marks_required(3),
                                                                (400, 300),
                                                                (130, 100),
                                                                True),
                                        RectangularChoiceButton("4",
                                                                lambda: self.change_marks_required(4),
                                                                (575, 300),
                                                                (130, 100),
                                                                False),
                                        RectangularChoiceButton("5",
                                                                lambda: self.change_marks_required(5),
                                                                (750, 300),
                                                                (130, 100),
                                                                False),
                                        ]

        self._mark_buttons = [RectangularChoiceButton("X",
                                                      lambda: self.change_mark(0),
                                                      (500, 500),
                                                      (130, 100),
                                                      True),
                              RectangularChoiceButton("O",
                                                      lambda: self.change_mark(1),
                                                      (700, 500),
                                                      (130, 100),
                                                      False),
                              ]

        self._start_button = DisableableRectangularTextButton("Start",
                                                              lambda: self.switch_to_tic_tac_toe(),
                                                              (450, 550),
                                                              (380, 100),
                                                              False)

        self._back_to_menu_button = RoundIconButton(
            'game_app/resources/images/menus/tic_tac_toe_launch_menu/left-arrow.png',
            lambda: self.switch_back_to_main_menu(),
            (50, 50),
            35)

        self.all_buttons = [self._start_button, self._back_to_menu_button] \
                           + self._size_buttons + self._marks_required_buttons + self._mark_buttons

        self._button_click_sound = Sound(
            os.path.join(ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/tic_tac_toe/move_sound_1.wav"))

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
        self._button_click_sound.play()

    def change_marks_required(self, new_marks_required):
        if new_marks_required != self._marks_required:
            for button in self._marks_required_buttons:
                button.set_chosen(False)
            self._marks_required = new_marks_required
            self._start_button.set_disabled(new_marks_required > self._board_size)
        self._button_click_sound.play()

    def change_mark(self, new_mark):
        if new_mark != self._mark:
            for button in self._mark_buttons:
                button.set_chosen(False)
            self._mark = new_mark
        self._button_click_sound.play()

    def switch_back_to_main_menu(self):
        self._app.switch_component(Components.MAIN_MENU, switch_music=False)

    def switch_to_tic_tac_toe(self):
        self._app.switch_component(Components.TIC_TAC_TOE, board_size=self._board_size,
                                   marks_required=self._marks_required, mark=self._mark)

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
from game_app.menus.menus_scene_commons.buttons import RectangularTextButton, RectangularChoiceButton


class TicTacToeLaunchMenuLogic:
    def __init__(self, app):
        self._app = app
        self._board_size = 3
        self._marks_required = 3

        self.size_buttons = [RectangularChoiceButton("3x3",
                                                     lambda: self.change_board_size(3),
                                                     (150, 150),
                                                     (130, 100),
                                                     True),
                             RectangularChoiceButton("5x5",
                                                     lambda: self.change_board_size(5),
                                                     (320, 150),
                                                     (130, 100),
                                                     False),
                             RectangularChoiceButton("10x10",
                                                     lambda: self.change_board_size(10),
                                                     (490, 150),
                                                     (130, 100),
                                                     False),
                             RectangularChoiceButton("20x20",
                                                     lambda: self.change_board_size(20),
                                                     (660, 150),
                                                     (130, 100),
                                                     False),
                             RectangularChoiceButton("30x30",
                                                     lambda: self.change_board_size(30),
                                                     (830, 150),
                                                     (130, 100),
                                                     False),
                             RectangularChoiceButton("50x50",
                                                     lambda: self.change_board_size(50),
                                                     (1000, 150),
                                                     (130, 100),
                                                     False),
                             ]

        self.marks_required_buttons = [RectangularChoiceButton("3",
                                                               lambda: self.change_marks_required(3),
                                                               (150, 400),
                                                               (130, 100),
                                                               True),
                                       RectangularChoiceButton("4",
                                                               lambda: self.change_marks_required(5),
                                                               (320, 400),
                                                               (130, 100),
                                                               False),
                                       RectangularChoiceButton("5",
                                                               lambda: self.change_marks_required(10),
                                                               (490, 400),
                                                               (130, 100),
                                                               False),
                                       ]

        self.buttons = [
            RectangularTextButton("Start",
                                  lambda: print("TODO"),
                                  (450, 550),
                                  (380, 100)),
        ]

        self._button_click_sound = Sound(
            os.path.join(ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/tic_tac_toe/move_sound_1.wav"))

    def handle_event(self, event):
        if event.type == MOUSEBUTTONUP:
            for pressed_button in filter(lambda button: button.contains_point(event.pos),
                                         self.buttons + self.size_buttons + self.marks_required_buttons):
                pressed_button.on_pressed()

    def change_board_size(self, new_size):
        if new_size != self._board_size:
            for size_button in self.size_buttons:
                size_button.set_chosen(False)
            self._board_size = new_size
        self._button_click_sound.play()

    def change_marks_required(self, new_marks_required):
        if new_marks_required != self._marks_required:
            for button in self.marks_required_buttons:
                button.set_chosen(False)
            self._marks_required = new_marks_required
        self._button_click_sound.play()

    def switch_to_tic_tac_toe(self):
        self._app.switch_component(Components.TIC_TAC_TOE)

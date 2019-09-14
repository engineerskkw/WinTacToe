from ....common_helper import Extensions
from ....ui_commons import RectangularTextButton
from pygame.locals import *
import pygame


class MainMenuLogic:
    def __init__(self, extension):
        self._extension = extension
        self.buttons = [
            RectangularTextButton("TicTacToe",
                                  lambda: self.switch_to_tic_tac_toe(),
                                  (450, 100),
                                  (380, 100)),
            RectangularTextButton("TODO",
                                  lambda: switch_music(),
                                  (450, 300),
                                  (380, 100)),
            RectangularTextButton("TODO",
                                  lambda: refr(),
                                  (450, 500),
                                  (380, 100)),
        ]

    def handle_event(self, event):
        if event.type == MOUSEBUTTONUP:
            for button in filter(lambda butt: butt.contains_point(event.pos), self.buttons):
                button.on_pressed()

    def switch_to_tic_tac_toe(self):
        self._extension.app.switch_extension(Extensions.TIC_TAC_TOE)

def switch_music():
    pygame.mixer.music.load("resources/sounds/common/SneakyAdventure.mp3")
    pygame.mixer.music.play(loops=-1)

def refr():
    pygame.mixer.music.play()



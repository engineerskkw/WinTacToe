from ....extensions_enum import Extensions
from ....ui_commons import RectangularTextButton
from pygame.locals import *


class MainMenuLogic:
    def __init__(self, extension):
        self._extension = extension
        self.buttons = [
            RectangularTextButton("TicTacToe",
                                  lambda: extension.app.switch_extension(Extensions.TIC_TAC_TOE),
                                  (450, 100),
                                  (380, 100)),
            RectangularTextButton("TODO",
                                  lambda: print("not implemented"),
                                  (450, 300),
                                  (380, 100)),
            RectangularTextButton("TODO",
                                  lambda: print("not implemented"),
                                  (450, 500),
                                  (380, 100)),
        ]

    def handle_event(self, event):
        if event.type == MOUSEBUTTONUP:
            for button in filter(lambda butt: butt.contains_point(event.pos), self.buttons):
                button.on_pressed()

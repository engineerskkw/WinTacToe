from ...abstract_extension import AbstractExtension
from .tic_tac_toe_scene import TicTacToeScene
from .tic_tac_toe_logic import TicTacToeLogic
from pygame.locals import *


class TicTacToeExtension(AbstractExtension):
    def __init__(self, app):
        self._app = app
        self._scene = TicTacToeScene(self)
        # self._logic = TicTacToeLogic()

    def render(self, screen):
        self._scene.render(screen)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONUP:
            print("uuup")

    def loop(self):
        pass

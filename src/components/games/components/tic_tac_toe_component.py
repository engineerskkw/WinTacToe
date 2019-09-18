from src.common_helper import MusicSwitcher
from src.components.abstract_component import AbstractComponent
from tic_tac_toe.logics.tic_tac_toe_logic import *
import gym


class TicTacToeComponent(AbstractComponent):
    def __init__(self, app):
        self._app = app
        self._env = gym.make('tic_tac_toe:tictactoe-v0')
        players = [Player('A', 0), Player('B', 1)]
        marks_required = 3
        size = 5
        self._env.initialize(players, size, marks_required, app)
        MusicSwitcher("resources/sounds/common/SneakyAdventure.mp3").start()

    def render(self):
        self._env.render(mode='app', screen=self._app.screen)

    def handle_event(self, event):
        self._env.handle_event(event)

    def loop(self):
        pass

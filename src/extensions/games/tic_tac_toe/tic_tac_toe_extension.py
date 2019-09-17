from ....common_helper import MusicSwitcher
from ...abstract_extension import AbstractExtension
from .tic_tac_toe_logic import *
from pygame.locals import *
import pygame
import gym


class TicTacToeExtension(AbstractExtension):
    def __init__(self, app):
        self._app = app
        self._env = gym.make('tic_tac_toe:tictactoe-v0')
        players = [Player('A', 0), Player('B', 1)]
        marks_required = 3
        size = 5
        self._env.initialize(players, size, marks_required, app)
        MusicSwitcher("resources/sounds/common/SneakyAdventure.mp3").start()

    def render(self, screen):
        self._env.render(mode='app', screen=screen)

    def handle_event(self, event):
        self._env.handle_event(event)

    def loop(self):
        pass

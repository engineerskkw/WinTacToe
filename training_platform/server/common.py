#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from thespian.actors import *
import datetime

from game_app.games.tic_tac_toe.engine.tic_tac_toe_engine import TicTacToeEngine
from game_app.games.tic_tac_toe.engine.tic_tac_toe_engine_utils import *



# start_server script <-> GameManager Actor comumnication

class InitGameManagerMsg:
    def __init__(self, environment):
        self.environment = environment


# GameManager Actor <-> MatchMaker Actor communication

class InitMatchMakerMsg:
    def __init__(self, players):
        self.players = players


class LaunchGameMsg:
    def __init__(self, players_clients, relaunch=False):
        self.players_clients = players_clients
        self.relaunch = relaunch


# player_client script <-> MatchMaker comumnication

class JoinMsg:
    def __init__(self, player):
        self.player = player

class InvalidPlayerMsg:
    def __init__(self, available_or_replaceable_players):
        self.available_or_replaceable_players = available_or_replaceable_players

class JoinAcknowledgementsMsg:
    pass

class ServiceNotLaunchedMsg:
    pass


class DetachMsg:
    pass



# player_client script <-> GameManager communication

class YourTurnMsg:
    def __init__(self, state, allowed_actions):
        self.state = state
        self.allowed_actions = allowed_actions


class MakeMoveMsg:
    def __init__(self, move):
        self.move = move


class RewardMsg:
    def __init__(self, reward):
        self.reward = reward


class GameOverMsg:
    def __init__(self, state):
        self.state = state

# GUI <-> GameManager communication

class RestartEnvMsg:
    pass

class ShutdownMsg:
    pass


# Logger & Monitor
class InitLoggerMsg:
    pass


class JoinMonitorMsg:
    pass

class DetachMonitorMsg:
    pass


class LogMsg:
    def __init__(self, text, author=None):
        self.text = text
        self.author = author
        self.time = datetime.datetime.now()

    def __str__(self):
        return f"{self.time.__str__()} [{self.author}]: {self.text}"
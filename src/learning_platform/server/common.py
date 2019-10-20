from thespian.actors import *
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../components/games/tic_tac_toe"))
from engine.tic_tac_toe_engine_utils import *
from engine.tic_tac_toe_engine import TicTacToeEngine

# start_server script <-> GameManager Actor comumnication

class InitGameManagerMsg:
    def __init__(self, environment):
        self.environment = environment


# GameManager Actor <-> MatchMaker Actor communication

class InitMatchMakerMsg:
    def __init__(self, players):
        self.players = players


class LaunchGameMsg:
    def __init__(self, players_clients):
        self.players_clients = players_clients


# player_client script <-> MatchMaker comumnication

class JoinMsg:
    def __init__(self, player):
        self.player = player


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
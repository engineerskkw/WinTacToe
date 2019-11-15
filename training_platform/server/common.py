#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import datetime


# start_server script <-> GameManager Actor communication
class InitGameManagerMsg:
    def __init__(self, environment):
        self.environment = environment


# GameManager Actor <-> MatchMaker Actor communication
class InitMatchMakerMsg:
    def __init__(self, players):
        self.players = players


class PlayerClientsMsg:
    def __init__(self, players_clients):
        self.players_clients = players_clients


# player_client script <-> MatchMaker communication
class JoinMsg:
    def __init__(self, player):
        self.player = player


class InvalidPlayerMsg:
    def __init__(self, available_or_replaceable_players):
        self.available_or_replaceable_players = available_or_replaceable_players


class JoinAcknowledgementsMsg:
    pass


class ServiceUninitializedMsg:
    pass


class DetachMsg:
    pass


# PlayerClient <-> GameManager communication
class StartEnvMsg:
    pass


class YourTurnMsg:
    def __init__(self, state, action_space):
        self.state = state
        self.action_space = action_space


class TakeActionMsg:
    def __init__(self, action):
        self.action = action


class RewardMsg:
    def __init__(self, reward):
        self.reward = reward


class GameOverMsg:
    def __init__(self, state=None, winnings=None):
        self.state = state
        self.winnings = winnings


class GameRestartedMsg:
    pass


class ShutdownAcknowledgement:
    pass


# GUI <-> GameManager communication
class StateUpdateMsg:
    def __init__(self, state):
        self.state = state


class RestartEnvMsg:
    pass


class NotReadyToStartMsg:
    pass

class StartedMsg:
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

# Messages for initialization checking
class AreYouInitializedMsg:
    def __init__(self):
        pass

class IAmInitializedMsg:
    def __init__(self):
        pass

class IAmUninitializedMsg:
    def __init__(self):
        pass

class GetEngineMsg:
    def __init__(self):
        pass

class EngineMsg:
    def __init__(self, engine):
        self.engine = engine
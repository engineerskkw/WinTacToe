# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import datetime
import configparser
config = configparser.ConfigParser()
config.read(os.path.join(ABS_PROJECT_ROOT_PATH, "training_platform", "config.ini"))
ACTOR_SYSTEM_BASE = config["TRAINING PLATFORM PARAMETERS"]["actorsystembase"]

# MESSAGES

# GameManager <-> MatchMaker communication
class InitMatchMakerMsg:
    def __init__(self, players):
        self.players = players


class PlayerClientsMsg:
    def __init__(self, players_clients):
        self.players_clients = players_clients


# AgentClient <-> AgentClientActor <-> MatchMaker communication
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


# AgentClient <-> AgentClientActor <-> GameManager communication
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


class StateUpdateMsg:
    def __init__(self, state):
        self.state = state


# EnvironmentServer <-> GameManager communication
class InitGameManagerMsg:
    def __init__(self, environment):
        self.environment = environment


class StartEnvMsg:
    pass


class EnvStartedMsg:
    pass


class EnvNotReadyToStartMsg:
    pass


class RestartEnvMsg:
    pass


class EnvRestartedMsg:
    pass


# Logger & Monitor
class InitLoggerMsg:
    pass


class JoinMonitorMsg:
    pass


class MonitorJoinAcknowledgement:
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
    pass


class GameManagerInitializedMsg:
    def __init__(self, environment=None):
        self.environment = environment


class GameManagerUninitializedMsg:
    pass


class MatchMakerInitializedMsg:
    pass


class MatchMakerUninitializedMsg:
    pass


# Common errors
class UnexpectedMessageError(Exception):
    def __init(self, message):
        self.message = message

    def __str__(self):
        return f"Received unexpected message: {str(self.message)}"

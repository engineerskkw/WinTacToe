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

    def __str__(self):
        return f"{self.__class__.__name__}: players: {self.players}"


class PlayerClientsMsg:
    def __init__(self, players_clients, gui_clients):
        self.players_clients = players_clients
        self.gui_clients = gui_clients

    def __str__(self):
        return f"{self.__class__.__name__}: players_clients: {self.players_clients}, gui_clients: {self.gui_clients}"


# AgentClient <-> AgentClientActor <-> MatchMaker communication
class JoinMsg:
    def __init__(self, player, gui_client=False):
        self.player = player
        self.gui_client = gui_client

    def __str__(self):
        return f"{self.__class__.__name__}: player: {self.player}, gui_client: {self.gui_client}"


class InvalidPlayerMsg:
    def __init__(self, available_or_replaceable_players):
        self.available_or_replaceable_players = available_or_replaceable_players

    def __str__(self):
        return f"{self.__class__.__name__}: available_or_replaceable_players: {self.available_or_replaceable_players}"


class JoinAcknowledgementsMsg:
    def __str__(self):
        return f"{self.__class__.__name__}"


class ServiceUninitializedMsg:
    def __str__(self):
        return f"{self.__class__.__name__}"


class DetachMsg:
    def __str__(self):
        return f"{self.__class__.__name__}"


# AgentClient <-> AgentClientActor <-> GameManager communication
class YourTurnMsg:
    def __init__(self, state, action_space):
        self.state = state
        self.action_space = action_space

    def __str__(self):
        return f"{self.__class__.__name__}: state: {self.state}, action_space: {self.action_space}"


class TakeActionMsg:
    def __init__(self, action):
        self.action = action

    def __str__(self):
        return f"{self.__class__.__name__}: action: {self.action}"

class RewardMsg:
    def __init__(self, reward):
        self.reward = reward

    def __str__(self):
        return f"{self.__class__.__name__}: reward: {self.reward}"


class GameOverMsg:
    def __init__(self, state=None, winnings=None):
        self.state = state
        self.winnings = winnings

    def __str__(self):
        return f"{self.__class__.__name__}: state: {self.state}, winnings: {self.winnings}"


class StateUpdateMsg:
    def __init__(self, state):
        self.state = state

    def __str__(self):
        return f"{self.__class__.__name__}: state: {self.state}"


# EnvironmentServer <-> GameManager communication
class InitGameManagerMsg:
    def __init__(self, environment):
        self.environment = environment

    def __str__(self):
        return f"{self.__class__.__name__}: environment: {self.environment}"


class StartEnvMsg:
    def __init__(self, notify_on_end):
        # Used by blocking start method in environment server to inform game manager if
        # it should or not send GameOverMsg or EnvRestartedMsg to who started (or restarted a game) on
        # game ending (both game over and restart cases)
        self.notify_on_end = notify_on_end

    def __str__(self):
        return f"{self.__class__.__name__}: notify_on_end: {self.notify_on_end}"


class EnvStartedMsg:
    def __str__(self):
        return f"{self.__class__.__name__}"


class RestartEnvMsg:
    def __init__(self, notify_on_end):
        # Used by blocking restart method in environment server to inform game manager if
        # it should or not send GameOverMsg or EnvRestartedMsg to who started (or restarted a game) on
        # game ending (both game over and restart cases)
        self.notify_on_end = notify_on_end

    def __str__(self):
        return f"{self.__class__.__name__}: notify_on_end: {self.notify_on_end}"


class EnvRestartedMsg:
    def __str__(self):
        return f"{self.__class__.__name__}"


class EnvNotReadyToStartMsg:
    def __str__(self):
        return f"{self.__class__.__name__}"


# Logger & Monitor
class InitLoggerMsg:
    def __str__(self):
        return f"{self.__class__.__name__}"


class JoinMonitorMsg:
    def __str__(self):
        return f"{self.__class__.__name__}"


class MonitorJoinAcknowledgement:
    def __str__(self):
        return f"{self.__class__.__name__}"


class LogMsg:
    def __init__(self, text, author=None):
        self.text = text
        self.author = author
        self.time = datetime.datetime.now()

    def __str__(self):
        return f"{self.time.__str__()} [{self.author}]: {self.text}"


# Messages for initialization checking
class AreYouInitializedMsg:
    def __str__(self):
        return f"{self.__class__.__name__}"


class GameManagerInitializedMsg:
    def __init__(self, environment=None):
        self.environment = environment

    def __str__(self):
        return f"{self.__class__.__name__}: environment: {self.environment}"


class GameManagerUninitializedMsg:
    def __str__(self):
        return f"{self.__class__.__name__}"


class MatchMakerInitializedMsg:
    def __str__(self):
        return f"{self.__class__.__name__}"


class MatchMakerUninitializedMsg:
    def __str__(self):
        return f"{self.__class__.__name__}"


# COMMON ERRORS
class UnexpectedMessageError(Exception):
    def __init(self, message):
        self.message = message

    def __str__(self):
        return f"Received unexpected message: {str(self.message)}"

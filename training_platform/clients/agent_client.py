# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from thespian.actors import *
from training_platform.server.common import *
from training_platform.server.service import GameManager, MatchMaker
from training_platform.server.logger import Logger


class InitClientActorMsg:
    def __init__(self, agent, match_maker_addr, game_manager_addr, logger_addr):
        self.agent = agent
        self.match_maker_addr = match_maker_addr
        self.game_manager_addr = game_manager_addr
        self.logger_addr = logger_addr


class AgentClientActor(Actor):
    def __init__(self):
        super().__init__()
        self.agent = None
        self.match_maker_addr = None
        self.game_manager_addr = None
        self.logger_addr = None
        self.client_endpoint = None
        self.player = None

    def receiveMessage(self, msg, sender):
        if isinstance(msg, InitClientActorMsg):
            self.agent = msg.agent
            self.match_maker_addr = msg.match_maker_addr
            self.game_manager_addr = msg.game_manager_addr
            self.logger_addr = msg.logger_addr
            self.client_endpoint = sender
            self.send(self.client_endpoint, GameManagerInitializedMsg())

        elif isinstance(msg, JoinMsg):
            self.player = msg.player
            self.send(self.match_maker_addr, msg)
            self.log("CCC")

        elif isinstance(msg, MatchMakerUninitializedMsg):
            self.log("Can't join server because MatchMaker hasn't ben initialized")
            self.send(self.client_endpoint, msg)

        elif isinstance(msg, InvalidPlayerMsg):
            self.log("Invalid player sent during joining server")
            self.send(self.client_endpoint, msg)

        elif isinstance(msg, JoinAcknowledgementsMsg):
            self.send(self.client_endpoint, msg)
            self.log("Successfully joined server!")

        elif isinstance(msg, YourTurnMsg):
            state = msg.state
            action = self.agent.take_action(msg.state, msg.action_space)
            self.log(f"Received state \n{state}\n and take action {action}")
            self.send(self.game_manager_addr, TakeActionMsg(action))

        elif isinstance(msg, RewardMsg):
            self.log(f"Reward: {msg.reward}")
            self.agent.receive_reward(msg.reward)

        elif isinstance(msg, GameOverMsg):
            self.agent.exit(msg.state)

        elif isinstance(msg, StateUpdateMsg):
            pass

        elif isinstance(msg, ActorExitRequest):
            self.log("Exiting")

        else:
            raise UnexpectedMessageError(msg)

    def log(self, text):
        self.send(self.logger_addr, LogMsg(text, f"client:{self.player}"))


class AgentClient:
    def __init__(self, agent):
        self.joined = False
        self.agent = agent
        self.asys = ActorSystem('multiprocTCPBase')
        self.client_actor_address = self.asys.createActor(AgentClientActor)
        self.game_manager_addr = self.asys.createActor(GameManager, globalName="GameManager")
        self.match_maker_addr = self.asys.createActor(MatchMaker, globalName="MatchMaker")
        self.logger_addr = self.asys.createActor(Logger, globalName="Logger")
        msg = InitClientActorMsg(self.agent, self.match_maker_addr, self.game_manager_addr, self.logger_addr)
        response = self.asys.ask(self.client_actor_address, msg)
        if not isinstance(response, GameManagerInitializedMsg):
            raise UnexpectedMessageError(response)

    def join(self, player):
        if self.joined:
            raise RejoiningError
        print("bb")
        response = self.asys.ask(self.client_actor_address, JoinMsg(player))
        print("after response")
        if isinstance(response, MatchMakerUninitializedMsg):
            raise MatchMakerUninitializedError
        elif isinstance(response, InvalidPlayerMsg):
            raise InvalidPlayer
        elif isinstance(response, JoinAcknowledgementsMsg):
            self.joined = True
            return True
        raise UnexpectedMessageError


class RejoiningError(Exception):
    def __str__(self):
        return "Attempt of rejoining while already joined"


class InvalidPlayer(Exception):
    def __str__(self):
        return "Invalid player sent during joining server"


class MatchMakerUninitializedError(Exception):
    def __str__(self):
        return "Can't join server because MatchMaker hasn't ben initialized"

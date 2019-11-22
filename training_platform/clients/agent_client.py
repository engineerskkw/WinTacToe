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


class GetAgentMsg:
    pass


class AgentMsg:
    def __init__(self, agent, Gs):
        self.agent = agent
        self.Gs = Gs


class AgentClientActor(Actor):
    def __init__(self):
        super().__init__()
        self.agent = None
        self.match_maker_addr = None
        self.game_manager_addr = None
        self.logger_addr = None
        self.client_endpoint = None
        self.player = "Unjoined"

    def receiveMessage(self, msg, sender):
        self.log(f"Received {msg} from {sender}")
        # Initialization
        if isinstance(msg, InitClientActorMsg):
            self.agent = msg.agent
            self.match_maker_addr = msg.match_maker_addr
            self.game_manager_addr = msg.game_manager_addr
            self.logger_addr = msg.logger_addr
            self.client_endpoint = sender
            self.send(self.client_endpoint, AgentClientActorInitializedMsg())

        # Joining server
        elif isinstance(msg, JoinMsg):
            self.player = msg.player
            self.send(self.match_maker_addr, msg)

        elif isinstance(msg, MatchMakerUninitializedMsg):
            self.log("Can't join server because MatchMaker hasn't ben initialized")
            self.send(self.client_endpoint, msg)

        elif isinstance(msg, InvalidPlayerMsg):
            self.log("Invalid player sent during joining server")
            self.send(self.client_endpoint, msg)

        elif isinstance(msg, JoinAcknowledgementsMsg):
            self.send(self.client_endpoint, msg)
            self.log("Successfully joined server!")

        elif isinstance(msg, GetAgentMsg):
            self.send(self.client_endpoint, AgentMsg(self.agent, self.agent.Gs))

        # Main Game loop
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

        # Exiting
        elif isinstance(msg, ActorExitRequest):
            self.log("Exiting")

        else:
            raise UnexpectedMessageError(msg)

    def log(self, text):
        if self.logger_addr is not None:
            super().send(self.logger_addr, LogMsg(text, f"client:{self.player}"))

    def send(self, target_address, message):
        super().send(target_address, message)
        self.log(f"Sent {message} to {target_address}")


class AgentClient:
    def __init__(self, agent):
        self.joined = False
        self.asys = ActorSystem(ACTOR_SYSTEM_BASE)
        self.client_actor_address = self.asys.createActor(AgentClientActor)
        self.game_manager_addr = self.asys.createActor(GameManager, globalName="GameManager")
        self.match_maker_addr = self.asys.createActor(MatchMaker, globalName="MatchMaker")
        self.logger_addr = self.asys.createActor(Logger, globalName="Logger")
        msg = InitClientActorMsg(agent, self.match_maker_addr, self.game_manager_addr, self.logger_addr)
        response = self.ask(self.client_actor_address, msg)
        if not isinstance(response, AgentClientActorInitializedMsg):
            raise UnexpectedMessageError(response)

    @property
    def agent(self):
        response = self.ask(self.client_actor_address, GetAgentMsg())
        if isinstance(response, AgentMsg):
            return response.agent
        raise UnexpectedMessageError(response)

    def join(self, player):
        if self.joined:
            raise RejoiningError
        response = self.ask(self.client_actor_address, JoinMsg(player))
        if isinstance(response, MatchMakerUninitializedMsg):
            raise MatchMakerUninitializedError
        elif isinstance(response, InvalidPlayerMsg):
            raise InvalidPlayer
        elif isinstance(response, JoinAcknowledgementsMsg):
            self.joined = True
            return True
        raise UnexpectedMessageError(response)

    def log(self, text):
        if self.logger_addr is not None:
            self.asys.tell(self.logger_addr, LogMsg(text, f"AgentClientEndpoint of {self.client_actor_address} client"))

    def tell(self, target_address, message):
        self.asys.tell(target_address, message)
        self.log(f"Sent {message} to {target_address}")

    def listen(self):
        response = self.asys.listen()
        self.log(f"Received {response}")
        return response

    def ask(self, target_address, message):
        self.tell(target_address, message)
        return self.listen()


class RejoiningError(Exception):
    def __str__(self):
        return "Attempt of rejoining while already joined"


class InvalidPlayer(Exception):
    def __str__(self):
        return "Invalid player sent during joining server"


class MatchMakerUninitializedError(Exception):
    def __str__(self):
        return "Can't join server because MatchMaker hasn't ben initialized"

# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from thespian.actors import *
import pygame
from pygame.locals import MOUSEBUTTONUP
from enum import Enum

from game_app.abstract_component import AbstractComponent
from game_app.common_helper import MusicSwitcher, Components
from game_app.games.tic_tac_toe.tic_tac_toe_scene import TicTacToeScene
from environments.tic_tac_toe.tic_tac_toe_engine_utils import TicTacToeAction
from training_platform.server.common import *
from training_platform.server.service import MatchMaker, GameManager
from training_platform.server.logger import Logger
from environments.tic_tac_toe.tic_tac_toe_engine import TicTacToeEngine
from training_platform import EnvironmentServer, AgentClient
from reinforcement_learning.agents.basic_mc_agent.basic_mc_agent import BasicAgent
from training_platform.clients.agent_client import MatchMakerUninitializedError, InvalidPlayer


class TurnState(Enum):
    NOT_YOUR_TURN = 0
    YOUR_TURN = 1
    NEW_YOUR_TURN = 2


class UserEventTypes(Enum):
    STATE_CHANGED = pygame.USEREVENT + 1
    TURN_CHANGED = pygame.USEREVENT + 2
    GAME_OVER = pygame.USEREVENT + 3


class MoveMsg:
    def __init__(self, action):
        self.action = action


class InitTTTClientActorMsg:
    def __init__(self, match_maker_addr,
                 game_manager_addr,
                 logger_addr):
        self.match_maker_addr = match_maker_addr
        self.game_manager_addr = game_manager_addr
        self.logger_addr = logger_addr


class JoinServerMsg:
    def __init__(self, player):
        self.player = player


class GetEventsToPostMsg:
    pass

class EventsToPostMsg:
    def __init__(self, events_to_post):
        self.events_to_post = events_to_post

class TicTacToeClientActor(Actor):
    def __init__(self):
        super().__init__()
        self.turn = TurnState.NOT_YOUR_TURN
        self._events_to_post = []
        self.match_maker_addr = None
        self.game_manager_addr = None
        self.logger_addr = None
        self.player = None

    def receiveMessage(self, msg, sender):
        # Message exchanged between GUI and client at every tic of application
        if isinstance(msg, GetEventsToPostMsg):
            self.send(sender, EventsToPostMsg(self._events_to_post.copy()))
            self._events_to_post = []

        # Initialization
        elif isinstance(msg, InitTTTClientActorMsg):
            self.match_maker_addr = msg.match_maker_addr
            self.game_manager_addr = msg.game_manager_addr
            self.logger_addr = msg.logger_addr
            self.log("Initialized")

        # Joining server
        elif isinstance(msg, JoinServerMsg):
            self.log(f"Received JoinServerMsg message from {sender}")
            self.player = msg.player
            self.send(self.match_maker_addr, JoinMsg(self.player))

        elif isinstance(msg, MatchMakerUninitializedMsg):
            self.log(f"Received MatchMakerUninitializedMsg message from {sender}")
            self.log("Can't join server because MatchMaker hasn't ben initialized")
            raise MatchMakerUninitializedError

        elif isinstance(msg, InvalidPlayerMsg):
            self.log(f"Received InvalidPlayerMsg message from {sender}")
            self.log("Invalid player sent during joining server")
            raise InvalidPlayer

        elif isinstance(msg, JoinAcknowledgementsMsg):
            self.log(f"Received JoinAcknowledgementsMsg message from {sender}")
            self.log("Successfully joined server!")

        # Main Game loop
        elif isinstance(msg, YourTurnMsg):
            self.log(f"Received YourTurnMsg message from {sender}")
            state_changed_event = {"type": UserEventTypes.STATE_CHANGED.value, "new_game_state": msg.state}
            turn_changed_event = {"type": UserEventTypes.TURN_CHANGED.value, "new_turn": TurnState.NEW_YOUR_TURN}
            self._events_to_post += [state_changed_event, turn_changed_event]

        elif isinstance(msg, MoveMsg):
            self.log(f"Received MoveMsg message from {sender}")
            self.send(self.game_manager_addr, TakeActionMsg(msg.action))
            self.log(f"Sent TakeActionMsg message to GameManager {self.game_manager_addr}")

        elif isinstance(msg, RewardMsg):
            pass

        elif isinstance(msg, GameOverMsg):
            self.log(f"Received GameOverMsg message from {sender}")
            game_over_event = {"type": UserEventTypes.GAME_OVER.value, "new_winnings": msg.winnings}
            self._events_to_post.append(game_over_event)

        elif isinstance(msg, StateUpdateMsg):
            self.log(f"Received StateUpdateMsg message from {sender}")
            state_changed_event = {"type": UserEventTypes.STATE_CHANGED.value, "new_game_state": msg.state}
            self._events_to_post += [state_changed_event]

        # Exiting
        elif isinstance(msg, ActorExitRequest):
            self.log(f"Received ActorExitRequest message from {sender}")

        else:
            self.log(f"Received unexpected message {msg} of type {msg} from {sender}")
            raise UnexpectedMessageError(msg)

    def log(self, text):
        if self.logger_addr is not None:
            self.send(self.logger_addr, LogMsg(text, f"GUI client:{self.player}"))


class TicTacToeComponent(AbstractComponent):
    def __init__(self, app, number_of_players=2, board_size=3, marks_required=3, mark=1):
        self._app = app

        # TODO stworzyc menu ktore pozwala wpisac te parametry (albo wybrac z proponowanych)
        self._number_of_players = number_of_players
        self._board_size = board_size
        self._marks_required = marks_required
        self._mark = mark

        # TicTacToeClientActor initialization
        self.asys = ActorSystem(ACTOR_SYSTEM_BASE)
        self.client_actor_address = self.asys.createActor(TicTacToeClientActor)
        self.game_manager_addr = self.asys.createActor(GameManager, globalName="GameManager")
        self.match_maker_addr = self.asys.createActor(MatchMaker, globalName="MatchMaker")
        self.logger_addr = self.asys.createActor(Logger, globalName="Logger")
        msg = InitTTTClientActorMsg(self.match_maker_addr, self.game_manager_addr, self.logger_addr)
        self.asys.tell(self.client_actor_address, msg)
        self.log(f"Sent InitTTTClientActorMsg to TicTacToeClientActor: {self.client_actor_address}")

        # Training Platform initialization
        engine = TicTacToeEngine(self._number_of_players, self._board_size, self._marks_required)
        self.server = EnvironmentServer(engine)
        self.log(f"Spawned server")
        players = self.server.players

        # TicTacToeClientActor server joining
        p0 = players[0]
        self.asys.tell(self.client_actor_address, JoinServerMsg(p0))
        self.log(f"Sent JoinServerMsg to TicTacToeClientActor: {self.client_actor_address}")

        # Opponent joining
        p1 = players[1]
        c1 = AgentClient(BasicAgent())
        self.server.join(c1, p1)
        self.log(f"Joined opponent")

        # Environment starting
        self.server.start(blocking=False)
        self.log("launched server.start(blocking=False)")

        self._scene = TicTacToeScene(self, app.screen, self._board_size)
        self.turn = TurnState.YOUR_TURN
        self.winnings = None

        resource_path = os.path.join(ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/common/SneakyAdventure.mp3")
        MusicSwitcher(resource_path).start()

    def render(self):
        self._scene.render()

    def handle_event(self, event):
        if event.type == UserEventTypes.STATE_CHANGED.value:
            self._scene.handle_state_changed(event.new_game_state)
        elif event.type == UserEventTypes.TURN_CHANGED.value:
            self.turn = event.new_turn
        elif event.type == UserEventTypes.GAME_OVER.value:
            self.winnings = event.new_winnings
        elif event.type == MOUSEBUTTONUP:
            buttons = [self._scene.restart_button, self._scene.main_menu_button]
            if self.turn != TurnState.NOT_YOUR_TURN:
                buttons += sum(self._scene.buttons, [])
            for button in filter(lambda b: b.contains_point(event.pos), buttons):
                button.on_pressed()

    def loop(self):
        msg = self.asys.ask(self.client_actor_address, GetEventsToPostMsg())
        for event in msg.events_to_post:
            event_type = event['type']
            del event['type']
            pygame.event.post(pygame.event.Event(event_type, event))

    def step(self, position):
        self.turn = TurnState.NOT_YOUR_TURN
        row, col = position
        action = TicTacToeAction(row, col)
        self.asys.tell(self.client_actor_address, MoveMsg(action))

    def restart(self):
        self.server.restart(blocking=False)
        self.log("called: self.server.restart(blocking=False)")

    def back_to_menu(self):
        self.server.shutdown()
        self._app.switch_component(Components.MAIN_MENU)

    def log(self, text):
        if self.logger_addr is not None:
            self.asys.tell(self.logger_addr, LogMsg(text, "TicTacToeComponent"))

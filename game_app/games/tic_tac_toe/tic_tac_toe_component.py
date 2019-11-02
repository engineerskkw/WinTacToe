#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from thespian.actors import *
from enum import Enum
from pygame.locals import MOUSEBUTTONUP
import subprocess

from game_app.abstract_component import AbstractComponent
from game_app.common_helper import MusicSwitcher, Components
from game_app.games.tic_tac_toe.tic_tac_toe_scene import TicTacToeScene
from game_app.application import pygame
from training_platform.server.common import *

class TurnState(Enum):
    NOT_YOUR_TURN = 0
    YOUR_TURN = 1
    NEW_YOUR_TURN = 2


class UserEventTypes(Enum):
    STATE_CHANGED = pygame.USEREVENT + 1
    TURN_CHANGED = pygame.USEREVENT + 2
    GAME_OVER = pygame.USEREVENT + 3


class MoveMsg:
    def __init__(self, position):
        self.position = position


class InitTTTClientActorMsg:
    def __init__(self, match_maker_addr,
                       game_manager_addr,
                       logger_addr):
    self.match_maker_addr = match_maker_addr
    self.game_manager_addr = game_manager_addr
    self.logger_addr = logger_addr

# TODO: move player making to the server or remove it completely
class JoinServerMsg:
    def __init__(self, player):
    self.player = player


class GetEventsToPostMsg:
    pass


class EndMsg:
    pass


class TicTacToeClientActor(Actor):
    def __init__(self):
        super().__init__()
        self.turn = TurnState.NOT_YOUR_TURN
        self._events_to_post = []
        self.match_maker_addr = None
        self.game_manager_addr = None
        self.logger_addr = None

    def receiveMessage(self, msg, sender):
        # Message exchanged between GUI and client at every tic of application
        if isinstance(msg, GetEventsToPostMsg):
            self.send(sender, self._events_to_post.copy())
            self._events_to_post = []
        # Message exchanged between GUI and client at TicTacToeClientActor creation
        elif isinstance(msg, InitTTTClientActorMsg):
            self.match_maker_addr = msg.match_maker_addr
            self.game_manager_addr = msg.game_manager_addr
            self.logger_addr = msg.logger_addr

        # Messages exchanged between GUI and client at special events
        elif isinstance(msg, JoinServerMsg):
            self.send(self.match_maker_addr, JoinMsg(msg.player))

        elif isinstance(msg, MoveMsg):
            print("wanna make a step", msg.position)
            self.send(self.game_manager_addr, MakeMoveMsg(msg.position))

        elif isinstance(msg, RestartEnvMsg):
            self.send(self.game_manager_addr, msg)
            
        elif isinstance(msg, EndMsg):
            print("back to menu button pressed")
            # TODO wyslij msg ze chcesz pozamykac wszystko

        # Messages exchanged between server and client
        elif isinstance(msg, YourTurnMsg):
            state_changed_event = {"type": UserEventTypes.STATE_CHANGED.value, "new_game_state": msg.state}
            turn_changed_event = {"type": UserEventTypes.TURN_CHANGED.value, "new_turn": TurnState.NEW_YOUR_TURN}
            self._events_to_post += [state_changed_event, turn_changed_event]
        elif isinstance(msg, GameOverMsg):
            game_over_event = {"type": UserEventTypes.GAME_OVER.value, "new_winnings": msg.state}
            self._events_to_post.append(game_over_event)

        # TODO nie mialo byc przypadkiem kurde state changed message dziejacego sie czesciej niz co ture?

        # TODO: implement errors handling in GUI-friendly way
        elif isinstance(msg, ServiceNotLaunchedMsg):
            # log("Attempt of using not launched service")
            # _ = input("Service hasn't been launched yet. Launch service and then press Enter...")
            # asys.tell(match_maker_addr, JoinMsg(player))

        elif isinstance(msg, InvalidPlayerMsg):
            # log("Invalid player received during joining client handling")
            # print("Invalid player received during joining client handling, try one of below:")

            # for i in range(len(msg.available_or_replaceable_players)):
                # print(f"{i}: {msg.available_or_replaceable_players[i]}")

            # input_string = input("\nType number of the chosen player: ")
            # result = parse("{}", input_string)
            # n = int(result[0])
            # player = msg.available_or_replaceable_players[n]

            # # Server rejoining
            # asys.tell(match_maker_addr, JoinMsg(player))

        elif isinstance(msg, JoinAcknowledgementsMsg):
            # log("Succesfully joined server!")
            # print("Succesfully joined server!")
            # print("Waiting for your turn...")

class TicTacToeComponent(AbstractComponent):
    def __init__(self, app):
        self._app = app

        # TODO stworzyc menu ktore pozwala wpisac te parametry (albo wybrac z proponowanych)
        self._number_of_players = 2
        self._board_size = 3
        self._marks_required = 3
        self._mark = 1

        call_string = f"python start_server.py {self._number_of_players} {self._board_size} {self._marks_required}"
        cwd = os.path.join("..", "training_platform", "server")
        subprocess.call(call_string, shell=True, cwd=cwd)

        self.asys = ActorSystem('multiprocTCPBase')
        # TicTacToeClientActor initialization
        self._client_actor_address = self.asys.createActor(TicTacToeClientActor)
        match_maker_addr = asys.createActor(MatchMaker, globalName="MatchMaker")
        game_manager_addr = asys.createActor(GameManager, globalName="GameManager")
        logger_addr = asys.createActor(Logger, globalName="Logger")
        msg = InitTTTClientActorMsg(match_maker_addr, game_manager_addr, logger_addr)
        self.asys.tell(self._client_actor_address, msg)
        # TODO: move player making to the server or remove it completely
        player_name = "Player 0"
        player_mark = 0
        player = Player(player_name, player_mark)
        self.asys.tell(self._client_actor_address, JoinServerMsg(player))

        self._scene = TicTacToeScene(self, app.screen, self._board_size)
        self.turn = TurnState.YOUR_TURN
        self.winnings = None

        MusicSwitcher("resources/sounds/common/SneakyAdventure.mp3").start()

    def render(self):
        self._scene.render()

    def handle_event(self, event):
        if event.type == UserEventTypes.STATE_CHANGED.value:
            print("STATE CHANGED - gui to wie")
            self._scene.handle_state_changed(event.new_game_state)
        elif event.type == UserEventTypes.TURN_CHANGED.value:
            print("TURN CHANGED - gui to wie")
            self.turn = event.new_turn
        elif event.type == UserEventTypes.GAME_OVER.value:
            print("GAME OVER - gui to wie")
            print(event.new_winnings) #TODO czemu game over msg posiada state a nie winnings?
            # self.winnings = event.new_winnings
        elif event.type == MOUSEBUTTONUP:
            buttons = [self._scene.restart_button, self._scene.main_menu_button]
            if self.turn != TurnState.NOT_YOUR_TURN:
                buttons += sum(self._scene.buttons, [])
            for button in filter(lambda b: b.contains_point(event.pos), buttons):
                button.on_pressed()

    def loop(self):
        events_to_post = self.asys.ask(self._client_actor_address, GetEventsToPostMsg(), 1)
        for event in events_to_post:
            event_type = event['type']
            del event['type']
            pygame.event.post(pygame.event.Event(event_type, event))

    def step(self, position):
        self.asys.tell(self._client_actor_address, MoveMsg(position))

    def restart(self):
        self.asys.tell(self._client_actor_address, RestartMsg())

    def back_to_menu(self):
        self.asys.tell(self._client_actor_address, EndMsg())
        self._app.switch_component(Components.MAIN_MENU)

from thespian.actors import *

from src.components.abstract_component import AbstractComponent
from src.common_helper import MusicSwitcher, Components
from src.learning_platform.server.common import *

from .tic_tac_toe_scene import TicTacToeScene

from enum import Enum

from pygame.locals import MOUSEBUTTONUP
from src.application import pygame


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


class JoinServerMsg:
    pass


class GetEventsToPostMsg:
    pass


class RestartMsg:
    pass


class EndMsg:
    pass


class TicTacToeClientActor(Actor):
    def __init__(self):
        super().__init__()
        self.turn = TurnState.NOT_YOUR_TURN
        self._events_to_post = []

    def receiveMessage(self, msg, sender):
        # Message exchanged between GUI and client at every tic of application
        if isinstance(msg, GetEventsToPostMsg):
            self.send(sender, self._events_to_post.copy())
            self._events_to_post = []

        # Messages exchanged between GUI and client at special events
        elif isinstance(msg, JoinServerMsg):
            print("time to join")
            # TODO wyslij msg ze chcesz dolaczyc
        elif isinstance(msg, MoveMsg):
            print("wanna make a step", msg.position)
            # TODO wyslij msg z ruchem
        elif isinstance(msg, RestartMsg):
            print("restart button pressed")
            # TODO wyslij msg ze chcesz restart
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


class TicTacToeComponent(AbstractComponent):
    def __init__(self, app):
        self._app = app

        # TODO stworzyc menu ktore pozwala wpisac te parametry (albo wybrac z proponowanych)
        self._number_of_players = 2
        self._board_size = 3
        self._marks_required = 3

        # TODO zespawnuj tutaj serwer WAZNE musisz zapamietac jego adres
        # TODO tell do aktora jaki jest adres na ktory ma wysylac wiadomosci

        self._client_actor_address = ActorSystem('multiprocTCPBase').createActor(TicTacToeClientActor)
        ActorSystem('multiprocTCPBase').tell(self._client_actor_address, JoinServerMsg())

        self._scene = TicTacToeScene(self, app.screen, self._board_size)
        self.turn = TurnState.YOUR_TURN
        self.winnings = None

        # TODO usunac ponizej, to tylko symulacja otrzymania wiadomosci od serwera
        ActorSystem('multiprocTCPBase').tell(self._client_actor_address, YourTurnMsg("new_state_for_real", []))
        ActorSystem('multiprocTCPBase').tell(self._client_actor_address, GameOverMsg("game over state is sad"))

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
        events_to_post = ActorSystem('multiprocTCPBase').ask(self._client_actor_address, GetEventsToPostMsg(), 1)
        for event in events_to_post:
            event_type = event['type']
            del event['type']
            pygame.event.post(pygame.event.Event(event_type, event))

    def step(self, position):
        ActorSystem('multiprocTCPBase').tell(self._client_actor_address, MoveMsg(position))

    def restart(self):
        ActorSystem('multiprocTCPBase').tell(self._client_actor_address, RestartMsg())

    def back_to_menu(self):
        ActorSystem('multiprocTCPBase').tell(self._client_actor_address, EndMsg())
        self._app.switch_component(Components.MAIN_MENU)

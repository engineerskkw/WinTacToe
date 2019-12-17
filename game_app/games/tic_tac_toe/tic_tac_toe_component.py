# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import pygame
from pygame.locals import MOUSEBUTTONUP
from thespian.actors import *
from game_app.common.abstract_component import AbstractComponent
from game_app.common.common_helper import TurnState, Components, Settings, Difficulty, GameMode
from game_app.games.tic_tac_toe.tic_tac_toe_scene import TicTacToeScene
from game_app.games.tic_tac_toe.agent_file_path_resolver import resolve_agent_file_path
from game_app.games.tic_tac_toe.agent_fake_player import init_agent_fake_player, ActionFakePlayerCommand, \
    KillFakePlayerCommand, RestartFakePlayerCommand
from game_app.menus.settings.settings_logic import save_selected_settings
from environments.tic_tac_toe.tic_tac_toe_engine_utils import TicTacToeAction
from training_platform.common import *
from training_platform.server.service import MatchMaker, GameManager
from training_platform.server.logger import Logger
from training_platform.common import LOGGING
from environments.tic_tac_toe.tic_tac_toe_engine import TicTacToeEngine
from training_platform import EnvironmentServer, AgentClient
from training_platform.clients.agent_client import MatchMakerUninitializedError, InvalidPlayer
from reinforcement_learning.base.base_agent import BaseAgent
from reinforcement_learning.agents.basic_mc_agent.basic_mc_agent import BasicAgent
from reinforcement_learning.new_agents.dqn_agent.dqn_agent import DQNAgent
from reinforcement_learning.agents_database.agents_db import AgentsDB


class UserEventTypes(Enum):
    STATE_CHANGED = pygame.USEREVENT + 1
    TURN_CHANGED = pygame.USEREVENT + 2
    GAME_OVER = pygame.USEREVENT + 3


class MoveMsg:
    def __init__(self, action):
        self.action = action


class InitTTTClientActorMsg:
    def __init__(self, match_maker_addr, game_manager_addr, logger_addr, spectator_mode):
        self.match_maker_addr = match_maker_addr
        self.game_manager_addr = game_manager_addr
        self.logger_addr = logger_addr
        self.spectator_mode = spectator_mode


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
        self.spectator_mode = None
        self.player = None

    def log(self, text, logging_level=LoggingLevel.GAME_EVENTS):
        if not LOGGING:
            return
        if self.logger_addr is not None:
            super().send(self.logger_addr, LogMsg(text, f"GUI client:{self.player}", logging_level))

    def send(self, target_address, message):
        super().send(target_address, message)
        if not isinstance(message, EventsToPostMsg):
            self.log(f"Sent {message} to {target_address}", LoggingLevel.PLATFORM_COMMUNICATION_MESSAGES)

    def receiveMessage(self, msg, sender):
        if not isinstance(msg, GetEventsToPostMsg):
            self.log(f"Received {msg} from {sender}", LoggingLevel.PLATFORM_COMMUNICATION_MESSAGES)
        # Message exchanged between GUI and client at every tic of application
        if isinstance(msg, GetEventsToPostMsg):
            self.send(sender, EventsToPostMsg(self._events_to_post.copy()))
            self._events_to_post = []

        # Initialization
        elif isinstance(msg, InitTTTClientActorMsg):
            self.match_maker_addr = msg.match_maker_addr
            self.game_manager_addr = msg.game_manager_addr
            self.logger_addr = msg.logger_addr
            self.spectator_mode = msg.spectator_mode
            self.log("Initialized")

        # Joining server
        elif isinstance(msg, JoinServerMsg):
            self.player = msg.player
            self.send(self.match_maker_addr, JoinMsg(self.player, True))

        elif isinstance(msg, MatchMakerUninitializedMsg):
            self.log("Can't join server because MatchMaker hasn't ben initialized")
            raise MatchMakerUninitializedError

        elif isinstance(msg, InvalidPlayerMsg):
            self.log("Invalid player sent during joining server")
            raise InvalidPlayer

        elif isinstance(msg, JoinAcknowledgementsMsg):
            self.log("Successfully joined server!")

        # Main Game loop
        elif isinstance(msg, YourTurnMsg):
            state_changed_event = {"type": UserEventTypes.STATE_CHANGED.value, "new_game_state": msg.state}
            turn_changed_event = {"type": UserEventTypes.TURN_CHANGED.value, "new_turn": TurnState.YOUR_TURN}
            if self.spectator_mode:
                turn_changed_event["action_space"] = msg.action_space
                turn_changed_event["new_game_state"] = msg.state
            self._events_to_post += [state_changed_event, turn_changed_event]

        elif isinstance(msg, MoveMsg):
            self.send(self.game_manager_addr, TakeActionMsg(msg.action))

        elif isinstance(msg, GameOverMsg):
            game_over_event = {"type": UserEventTypes.GAME_OVER.value, "new_winnings": msg.winnings}
            self._events_to_post.append(game_over_event)

        elif isinstance(msg, StateUpdateMsg):
            state_changed_event = {"type": UserEventTypes.STATE_CHANGED.value, "new_game_state": msg.state}
            self._events_to_post += [state_changed_event]

        elif isinstance(msg, EnvRestartedMsg):
            pass

        # Exiting
        elif isinstance(msg, ActorExitRequest):
            self.log(f"Exiting")
        else:
            raise UnexpectedMessageError(msg)


class TicTacToeComponent(AbstractComponent):
    def __init__(self, app, board_size, marks_required, player_mark, opponent_mark, difficulty, game_mode):
        self._app = app
        self._board_size = board_size
        self.marks_required = marks_required
        self._player_mark = player_mark
        self._opponent_mark = opponent_mark
        self._difficulty = difficulty
        self.spectator_mode = game_mode == GameMode.AgentVsAgent

        # Fake player initialisation in spectator mode
        if self.spectator_mode:
            self.show_match_ended = False
            self.show_match_paused = False
            self.next_moves_to_show = 0
            self._fake_player_commands_queue = init_agent_fake_player()
            self._fake_player_agent = BaseAgent.load(
                resolve_agent_file_path(self._player_mark, self._board_size, self.marks_required))

        self.asys = ActorSystem(ACTOR_SYSTEM_BASE)

        # TicTacToeClientActor initialization
        self.client_actor_address = self.asys.createActor(TicTacToeClientActor)
        self.game_manager_addr = self.asys.createActor(GameManager, globalName="GameManager")
        self.match_maker_addr = self.asys.createActor(MatchMaker, globalName="MatchMaker")
        self.logger_addr = self.asys.createActor(Logger, globalName="Logger")
        msg = InitTTTClientActorMsg(self.match_maker_addr, self.game_manager_addr, self.logger_addr,
                                    self.spectator_mode)
        self.tell(self.client_actor_address, msg)

        # Training Platform initialization
        engine = TicTacToeEngine(2, self._board_size, self.marks_required)
        self.server = EnvironmentServer(engine)
        self.log(f"Spawned server")
        players = self.server.players

        # TicTacToeClientActor server joining
        human_player = players[self._player_mark]
        self.tell(self.client_actor_address, JoinServerMsg(human_player))

        # Opponent joining
        agent_player = players[self._opponent_mark]
        matching_agents = AgentsDB.load(player=self._opponent_mark,
                                        board_size=self._board_size,
                                        marks_required=self.marks_required)  # List of all agents that satisfy criteria

        # TODO: Make convenient select agent function (maybe in GUI)
        # For now it's just last agent
        def agent_select(agents):
            if not agents:
                raise ValueError("There are now agents satisfying given criteria in the Agents Database")
            return agents[-1]
        agent = agent_select(matching_agents)

        # TODO: implement proper difficulty level handling
        # agent.epsilon = 0.0 if self._difficulty == Difficulty.HARD else 0.2
        agent_client = AgentClient(agent)
        self.server.join(agent_client, agent_player)
        self.log(f"Joined opponent")

        # Environment starting
        self.server.start(blocking=False)
        self.log("Started server")

        self._scene = TicTacToeScene(self, app, app.screen, self._board_size, self._player_mark, self._opponent_mark)
        self.turn = TurnState.YOUR_TURN
        self.winnings = None

        self._app.switch_music(
            os.path.join(ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/common/SneakyAdventure.mp3"))

    def log(self, text, logging_level=LoggingLevel.GAME_EVENTS):
        if not LOGGING:
            return
        if self.logger_addr is not None:
            self.asys.tell(self.logger_addr, LogMsg(text, "TicTacToeComponent", logging_level))

    def tell(self, target_address, message):
        self.asys.tell(target_address, message)
        if not isinstance(message, GetEventsToPostMsg):
            self.log(f"Sent {message} to {target_address}", LoggingLevel.PLATFORM_COMMUNICATION_MESSAGES)

    def listen(self):
        response = self.asys.listen()
        if not isinstance(response, EventsToPostMsg):
            self.log(f"Received {response}", LoggingLevel.PLATFORM_COMMUNICATION_MESSAGES)
        return response

    def ask(self, target_address, message):
        self.tell(target_address, message)
        return self.listen()

    def render(self):
        self._scene.render()

    def handle_event(self, event):
        if event.type == UserEventTypes.STATE_CHANGED.value:
            self._scene.handle_state_changed(event.new_game_state)

        elif event.type == UserEventTypes.TURN_CHANGED.value:
            self.turn = event.new_turn
            self._scene.handle_turn_changed()

            if self.spectator_mode:
                # Take a delayed action if in spectator mode
                self._fake_player_agent.receive_reward(0)
                action = self._fake_player_agent.take_action(event.new_game_state, event.action_space)
                self._fake_player_commands_queue.put(ActionFakePlayerCommand(
                    lambda: self._scene.tic_tac_toe_buttons[action.row][action.col].on_pressed(), self))

        elif event.type == UserEventTypes.GAME_OVER.value:
            tie_on_even_sized_board = not event.new_winnings and self._board_size % 2 == 0
            defeat = event.new_winnings and event.new_winnings[0].mark == self._opponent_mark
            if self.spectator_mode and (tie_on_even_sized_board or defeat):
                # Delay game over situation if in spectator mode and there would by no delay
                self._fake_player_commands_queue.put(
                    ActionFakePlayerCommand(lambda: self.set_winnings(event.new_winnings), self))
            else:
                self.set_winnings(event.new_winnings)

        elif event.type == MOUSEBUTTONUP:
            buttons = self._scene.navigation_buttons if self.spectator_mode else self._scene.all_buttons
            for button in filter(lambda b: b.contains_point(event.pos), buttons):
                button.on_pressed()

    def set_winnings(self, new_winnings):
        self.winnings = new_winnings if new_winnings else -1

    def loop(self):
        msg = self.ask(self.client_actor_address, GetEventsToPostMsg())
        for event in msg.events_to_post:
            event_type = event['type']
            del event['type']
            pygame.event.post(pygame.event.Event(event_type, event))

    def step(self, position):
        self.turn = TurnState.NOT_YOUR_TURN
        row, col = position
        action = TicTacToeAction(row, col)
        if self.spectator_mode:
            # Delay sending move message to the server in spectator mode to delay opponent's move
            self._fake_player_commands_queue.put(
                ActionFakePlayerCommand(lambda: self.tell(self.client_actor_address, MoveMsg(action)), self))
        else:
            self.tell(self.client_actor_address, MoveMsg(action))

    def restart(self):
        if self.spectator_mode:
            if self.show_match_ended:
                return
            self.next_moves_to_show = 0
            self.show_match_ended = True
            self._fake_player_agent.restart()
            self._fake_player_commands_queue.put(RestartFakePlayerCommand(self))
        self.turn = TurnState.NOT_YOUR_TURN
        self.winnings = []
        self._scene = TicTacToeScene(self, self._app, self._app.screen, self._board_size, self._player_mark,
                                     self._opponent_mark)
        self.server.restart(blocking=False)
        self.log("Restarted server")

    def back_to_menu(self):
        if self.spectator_mode:
            self.kill_fake_player()
        self.server.shutdown()
        self._app.switch_component(Components.MAIN_MENU)

    def kill_fake_player(self):
        self.next_moves_to_show = 0
        self.show_match_ended = True
        self._fake_player_commands_queue.put(KillFakePlayerCommand())

    def play_sound_stopping_music(self, sound_file_path):
        self._app.play_sound_stopping_music(sound_file_path)

    def toggle_music(self):
        self._app.settings[Settings.MUSIC] = not self._app.settings[Settings.MUSIC]
        self._app.switch_music(
            os.path.join(ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/common/SneakyAdventure.mp3"))
        self._scene.update_music_button()
        save_selected_settings(self._app.settings)

    def toggle_sounds(self):
        self._app.settings[Settings.SOUNDS] = not self._app.settings[Settings.SOUNDS]
        self._scene.update_sounds_button()
        save_selected_settings(self._app.settings)

    def toggle_show_match_pause(self):
        self.show_match_paused = not self.show_match_paused
        self._scene.update_pause_button()

    def show_next_move(self):
        self.next_moves_to_show += 1

#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#


from thespian.actors import *
from training_platform.server.common import *
from training_platform.server.logger import Logger


class GameManager(Actor):
    def __init__(self):
        super().__init__()
        self.environment = None
        self.players_clients = None
        self.match_maker_addr = None
        self.logger_addr = None
        self.before_first_move = {}
        self.initialized = False
        self.creator = None
        self.ready_to_start = False
        self.who_started_game = None

    def receiveMessage(self, msg, sender):
        if isinstance(msg, InitGameManagerMsg):
            # TODO: maybe check if initialized already
            self.environment = msg.environment
            self.match_maker_addr = self.createActor(MatchMaker, globalName="MatchMaker")
            self.logger_addr = self.createActor(Logger, globalName="Logger")
            self.creator = sender
            self.send(self.match_maker_addr, InitMatchMakerMsg(self.environment.players))

        elif isinstance(msg, MatchMakerInitializedMsg):
            self.initialized = True
            self.log("Initialization done")
            self.send(self.creator, GameManagerInitializedMsg())

        elif isinstance(msg, AreYouInitializedMsg):
            if self.initialized:
                response = GameManagerInitializedMsg(self.environment)
            else:
                response = GameManagerUninitializedMsg()
            self.send(sender, response)

        elif isinstance(msg, PlayerClientsMsg):
            self.players_clients = msg.players_clients
            self.ready_to_start = True

        elif isinstance(msg, StartEnvMsg):
            if not self.ready_to_start:
                self.send(sender, NotReadyToStartMsg())
                return
            self.ready_to_start = False
            self.who_started_game = sender
            for player in self.players_clients.keys():
                self.before_first_move[player] = True
            self.environment.reset()
            self.log(f"Launched game with following players and clients: {self.players_clients}")
            current_client = self.players_clients[self.environment.current_player]
            self.send(current_client, YourTurnMsg(self.environment.current_board, self.environment.allowed_actions))
            self.send(self.who_started_game, StartedMsg())


        elif isinstance(msg, TakeActionMsg):
            self.before_first_move[self.environment.current_player] = False
            self.environment.make_move(msg.action)  # It implicitly makes next player current player
            # State update for GUI clients TODO: send StateUpdateMsg only to GUI clients
            for client in self.players_clients.values():
                self.send(client, StateUpdateMsg(self.environment.current_board))

            if self.environment.ended:
                for player, client in self.players_clients.items():
                    if not self.before_first_move[player]:
                        self.send(client, RewardMsg(self.environment.rewards[player]))
                    self.send(client, GameOverMsg(self.environment.current_board, self.environment.winnings))
                self.ready_to_start = True
                self.send(self.who_started_game, GameOverMsg())
                self.log(f"Game over!\n{self.environment.current_board}")
            else:
                current_player = self.environment.current_player
                current_client = self.players_clients[current_player]
                if not self.before_first_move[current_player]:
                    self.send(current_client, RewardMsg(self.environment.rewards[current_player]))
                self.send(current_client, YourTurnMsg(self.environment.current_board, self.environment.allowed_actions))

        elif isinstance(msg, RestartEnvMsg):
            self.send(self.who_started_game, GameRestartedMsg())
            self.who_started_game = sender
            self.environment.reset()
            for player in self.players_clients.keys():
                self.before_first_move[player] = True
            for client in self.players_clients.values():
                self.send(client, StateUpdateMsg(self.environment.current_board))
            self.send(self.who_started_game, GameRestartedMsg())
            current_client = self.players_clients[self.environment.current_player]
            self.send(current_client, YourTurnMsg(self.environment.current_board, self.environment.allowed_actions))

        elif isinstance(msg, ActorExitRequest):
            for client in self.players_clients.values():
                self.send(client, ActorExitRequest())
            self.send(self.match_maker_addr, ActorExitRequest())
            self.send(self.logger_addr, ActorExitRequest())
            self.send(sender, ShutdownAcknowledgement())

        else:
            raise UnexpectedMessageError(msg)

    def log(self, text):
        self.send(self.logger_addr, LogMsg(text, "GameManager"))


class MatchMaker(Actor):
    def __init__(self):
        super().__init__()
        self.players_clients = {}
        self.game_manager_addr = None
        self.logger_addr = None
        self.initialized = False

    def receiveMessage(self, msg, sender):
        self.log("cos odebralem")
        if isinstance(msg, InitMatchMakerMsg):
            self.game_manager_addr = self.createActor(GameManager, globalName="GameManager")
            self.logger_addr = self.createActor(Logger, globalName="Logger")
            for player in msg.players:
                self.players_clients[player] = "available"
            self.log(f"Initial players <-> clients mapping: {self.players_clients}")
            self.initialized = True
            self.log("Initialization done")
            self.send(self.game_manager_addr, MatchMakerInitializedMsg())

        elif isinstance(msg, JoinMsg):
            self.log("DDD")
            if not self.initialized:
                self.log("Can't' join client, because MatchMaker hasn't been initialized")
                self.send(sender, MatchMakerUninitializedMsg())
                return

            if self.players_clients.get(msg.player) == "available":
                self.players_clients[msg.player] = sender
                self.send(sender, JoinAcknowledgementsMsg())
                self.log(f"Current players <-> clients mapping: {self.players_clients}")

                # Check if all players have been allocated for clients
                for value in self.players_clients.values():
                    if value == "available" or value == "replaceable":
                        return

                # Send player_clients mapping to the GameManager
                self.log("Clients for all players have joined!")
                self.send(self.game_manager_addr, PlayerClientsMsg(self.players_clients))

            elif self.players_clients.get(msg.player) == "replaceable":
                self.players_clients[msg.player] = sender
                self.send(sender, JoinAcknowledgementsMsg())
                self.log(f"Current players <-> clients mapping: {self.players_clients}")

                # Check if all players have been allocated for clients
                for value in self.players_clients.values():
                    if value == "available" or value == "replaceable":
                        return

                # Relaunch a game
                self.log("Relaunching the game!")
                self.send(self.game_manager_addr, PlayerClientsMsg(self.players_clients))

            else:
                self.log("Invalid player received during joining client handling")
                available_or_replaceable_players = []
                for player, client in self.players_clients.items():
                    if client == "available" or client == "replaceable":
                        available_or_replaceable_players.append(player)
                self.send(sender, InvalidPlayerMsg(available_or_replaceable_players))

        elif isinstance(msg, DetachMsg):
            # TODO: finish implementation of detaching in all places
            self.log(f"Detaching client: {sender}")

            for player, client in self.players_clients.items():
                if client == sender:
                    self.players_clients[player] = "replaceable"
                    self.log(f"Current players <-> clients mapping: {self.players_clients}")
        elif isinstance(msg, ActorExitRequest):
            self.log("Exiting")
        else:
            raise UnexpectedMessageError(msg)

    def log(self, text):
        self.send(self.logger_addr, LogMsg(text, "MatchMaker"))
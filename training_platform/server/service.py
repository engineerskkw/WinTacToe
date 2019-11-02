#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

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

    def receiveMessage(self, msg, sender):
        if isinstance(msg, InitGameManagerMsg):
            self.environment = msg.environment
            self.match_maker_addr = self.createActor(MatchMaker, globalName="MatchMaker")
            self.logger_addr = self.createActor(Logger, globalName="Logger")
            self.send(self.match_maker_addr, InitMatchMakerMsg(self.environment.players))
            self.log("Initialization done")

        elif isinstance(msg, LaunchGameMsg):
            self.players_clients = msg.players_clients
            if not msg.relaunch:
                for player in self.players_clients.keys():
                    self.before_first_move[player] = True
                self.log(f"Launched game with following players and clients: {self.players_clients}")
            else:
                self.log(f"Relaunched game with following players and clients: {self.players_clients}")

            current_client = self.players_clients[self.environment.current_player]
            self.send(current_client, YourTurnMsg(self.environment.current_board, self.environment.allowed_actions))

        elif isinstance(msg, MakeMoveMsg):
            x, y = msg.move
            self.environment.make_move(x, y)  # It implicitly makes next player current player

            if self.environment.ended:
                for player, client in self.players_clients.items():
                    if not self.before_first_move[player]:
                        self.send(client, RewardMsg(self.environment.rewards[player]))
                    self.send(client, GameOverMsg(self.environment.current_board))
                
            else:
                current_player = self.environment.current_player
                current_client = self.players_clients[current_player]
                if not self.before_first_move[current_player]:
                    self.send(current_client, RewardMsg(self.environment.rewards[current_player]))
                else:
                    self.before_first_move[current_player] = False

                self.send(current_client, YourTurnMsg(self.environment.current_board, self.environment.allowed_actions))

    def log(self, text):
        self.send(self.logger_addr, LogMsg(text, "GameManager"))


class MatchMaker(Actor):
    def __init__(self):
        super().__init__()
        self.players_clients = {}
        self.game_manager_addr = None
        self.logger_addr = None

    def receiveMessage(self, msg, sender):
        if isinstance(msg, InitMatchMakerMsg):
            self.game_manager_addr = self.createActor(GameManager, globalName="GameManager")
            self.logger_addr = self.createActor(Logger, globalName="Logger")
            for player in msg.players:
                self.players_clients[player] = "available"

            self.log(f"Initial players <-> clients mapping: {self.players_clients}")

        elif isinstance(msg, JoinMsg):
            if self.game_manager_addr == None:
                self.log("Can not join client, because service hasn't been launched")
                self.send(sender, ServiceNotLaunchedMsg())
                return

            if self.players_clients.get(msg.player) == "available":
                self.players_clients[msg.player] = sender
                self.send(sender, JoinAcknowledgementsMsg())
                self.log(f"Current players <-> clients mapping: {self.players_clients}")

                # Check if all players have been allocated for clients
                for value in self.players_clients.values():
                    if value == "available" or value == "replaceable":
                        return

                # Launch a game
                self.log("Launching the game!")
                self.send(self.game_manager_addr, LaunchGameMsg(self.players_clients))

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
                self.send(self.game_manager_addr, LaunchGameMsg(self.players_clients, True))

            else:
                self.log("Invalid player received during joining client handling")
                available_or_replaceable_players = []
                for player, client in self.players_clients.items():
                    if client == "available" or client == "replaceable":
                        available_or_replaceable_players.append(player)
                self.send(sender, InvalidPlayerMsg(available_or_replaceable_players))



        elif isinstance(msg, DetachMsg):
            self.log(f"Detaching client: {sender}")

            for player, client in self.players_clients.items():
                if client == sender:
                    self.players_clients[player] = "replaceable"
                    self.log(f"Current players <-> clients mapping: {self.players_clients}")

    def log(self, text):
        self.send(self.logger_addr, LogMsg(text, "MatchMaker"))
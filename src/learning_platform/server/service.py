from common import *
from logger import Logger

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
            self.log("cos sie stalo")

        elif isinstance(msg, LaunchGameMsg):
            self.players_clients = msg.players_clients
            if not msg.relaunch:
                for player in self.players_clients.keys():
                    self.before_first_move[player] = True
                print(f"[GameManager]: Launched game with following players and clients: {self.players_clients}")
            else:
                print(f"[GameManager]: Relaunched game with following players and clients: {self.players_clients}")

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

            print("[MatchMaker]: initial self.player_clients")
            print(self.players_clients)
            self.log("cos sie stalo")

        elif isinstance(msg, JoinMsg):
            if self.game_manager_addr == None:
                print("[MatchMaker]: cannot join client, because service hasn't been launched")
                self.send(sender, ServiceNotLaunchedMsg())
                return

            if self.players_clients.get(msg.player) == "available":
                self.players_clients[msg.player] = sender
                self.send(sender, JoinAcknowledgementsMsg())
                print("[MatchMaker]: initial self.player_clients")
                print(self.players_clients)

                # Check if all players have been allocated for clients
                for value in self.players_clients.values():
                    if value == "available" or value == "replaceable":
                        return

                # Launch a game
                print("[MatchMaker]: Launching game!")
                self.send(self.game_manager_addr, LaunchGameMsg(self.players_clients))

            elif self.players_clients.get(msg.player) == "replaceable":
                self.players_clients[msg.player] = sender
                self.send(sender, JoinAcknowledgementsMsg())
                print("[MatchMaker]: updated self.player_clients")
                print(self.players_clients)

                # Check if all players have been allocated for clients
                for value in self.players_clients.values():
                    if value == "available" or value == "replaceable":
                        return

                # Relaunch a game
                print("[MatchMaker]: Relaunching game!")
                self.send(self.game_manager_addr, LaunchGameMsg(self.players_clients, True))

            else:
                print("Invalid player received during joining client handling")
                available_or_replaceable_players = []
                for player, client in self.players_clients.items():
                    if client == "available" or client == "replaceable":
                        available_or_replaceable_players.append(player)
                self.send(sender, InvalidPlayerMsg(available_or_replaceable_players))



        elif isinstance(msg, DetachMsg):
            print(f"Detaching client: {sender}")

            for player, client in self.players_clients.items():
                if client == sender:
                    self.players_clients[player] = "replaceable"
                    print("[MatchMaker]: current self.player_clients")
                    print(self.players_clients)

    def log(self, text):
        self.send(self.logger_addr, LogMsg(text, "MatchMaker"))
from tic_tac_toe_engine_components import *
from src.components.games.tic_tac_toe.engine.tic_tac_toe_engine import TicTacToeEngine
from thespian.actors import *
from bidict import bidict
import time
import logging
from parse import parse

# logger = logging.getLogger()
# handler = logging.StreamHandler()
# formatter = logging.Formatter(
#         '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.DEBUG)
#
# logger.info("test")


class InitGameManagerMsg:
    def __init__(self, environment):
        self.environment = environment


class LaunchGameMsg:
    def __init__(self, players_clients):
        self.players_clients = players_clients


class YourTurnMsg:
    def __init__(self, state, allowed_actions):
        self.state = state
        self.allowed_actions = allowed_actions


class RewardMsg:
    def __init__(self, reward):
        self.reward = reward


class GameOverMsg:
    def __init__(self, state):
        self.state = state


class GameManager(Actor):
    def __init__(self):
        super().__init__()
        self.environment = None
        self.players_clients = None
        self.match_maker_addr = None
        self.before_first_move = {}

    def receiveMessage(self, msg, sender):
        if isinstance(msg, InitGameManagerMsg):
            self.environment = msg.environment
            self.match_maker_addr = self.createActor(MatchMaker, globalName="MatchMaker")
            self.send(self.match_maker_addr, InitMatchMakerMsg(self.environment.players))
        elif isinstance(msg, LaunchGameMsg):
            self.players_clients = msg.players_clients
            for player in self.players_clients.keys():
                self.before_first_move[player] = True
            print(f"[GameManager]: Launched game with following players and clients: {self.players_clients}")

            current_client = self.players_clients[self.environment.current_player]
            self.send(current_client, YourTurnMsg(self.environment.current_board, self.environment.allowed_actions))

        elif isinstance(msg, MakeMoveMsg):
            x, y = msg.move
            self.environment.make_move(x, y)  # It implicitly makes next player current player

            if self.environment.check_for_gameover():
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


class InitMatchMakerMsg:
    def __init__(self, players):
        self.players = players


class JoinMsg:
    def __init__(self, player):
        self.player = player


class DetachMsg:
    def __init__(self):
        pass


class EndGameMsg:
    def __init__(self):
        pass


class MatchMaker(Actor):
    def __init__(self):
        super().__init__()
        self.players_clients = {}
        self.game_manager_addr = None

    def receiveMessage(self, msg, sender):
        if isinstance(msg, InitMatchMakerMsg):
            self.game_manager_addr = self.createActor(GameManager, globalName="GameManager")
            for player in msg.players:
                self.players_clients[player] = "available"

            print("[MatchMaker]: initial self.player_clients")
            print(self.players_clients)

        elif isinstance(msg, JoinMsg):
            # Join client
            if self.players_clients.get(msg.player) == "available":
                self.players_clients[msg.player] = sender
                print("[MatchMaker]: initial self.player_clients")
                print(self.players_clients)
            else:
                # TODO: implement better error handling with feedback message
                print("Invalid player received during joining client handling "
                      "(or this player has been already allocated)")

            # Check if all players have been allocated for clients
            for value in self.players_clients.values():
                if value == "available":
                    return

            # Launch a game
            print("[MatchMaker]: Launching game!")
            self.send(self.game_manager_addr, LaunchGameMsg(self.players_clients))
        elif isinstance(msg, DetachMsg):
            pass
        elif isinstance(msg, EndGameMsg):
            pass


class InitClientMsg:
    def __init__(self, player, agent):
        self.player = player
        self.agent = agent


class MakeMoveMsg:
    def __init__(self, move):
        self.move = move


class Client(Actor):
    def __init__(self):
        super().__init__()
        self.player = None
        self.agent = None
        self.match_maker_addr = None
        self.game_manager_addr = None

    def receiveMessage(self, msg, sender):
        if isinstance(msg, InitClientMsg):
            self.player = msg.player
            self.agent = msg.agent
            self.match_maker_addr = self.createActor(MatchMaker, globalName="MatchMaker")
            self.game_manager_addr = self.createActor(GameManager, globalName="GameManager")

            self.send(self.match_maker_addr, JoinMsg(self.player))

        elif isinstance(msg, YourTurnMsg):
            print(f"[Client]: {self.player}")
            self.send(self.game_manager_addr, MakeMoveMsg(self.agent.step(msg.state, msg.allowed_actions)))
        elif isinstance(msg, RewardMsg):
            self.agent.reward(msg.reward)
        elif isinstance(msg, GameOverMsg):
            self.agent.exit(msg.state)


class Agent:
    def __init__(self):
        pass

    def step(self, state, allowed_actions):
        print("[Agent]: State:")
        print(state)
        input_string = input("\nType move's coordinates in order y, x (i.e 1,2): ")
        print("\n")
        result = parse("{},{}", input_string)
        y = int(result[0])
        x = int(result[1])
        return y, x

    def reward(self, reward):
        print(f"[Agent]: Received reward: {reward}")

    def exit(self, final_state):
        print(f"[Agent]: Game Over:")
        print(final_state)


if __name__ == '__main__':
    asys = ActorSystem()
    game_manager = asys.createActor(GameManager, globalName="GameManager")
    asys.tell(game_manager, InitGameManagerMsg(TicTacToeEngine(2, 3, 3)))

    client0 = asys.createActor(Client)
    asys.tell(client0, InitClientMsg(Player("Player 0", 0), Agent()))

    client1 = asys.createActor(Client)
    asys.tell(client1, InitClientMsg(Player("Player 1", 1), Agent()))
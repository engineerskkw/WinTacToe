#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from parse import parse

from reinforcement_learning.base.base_agent import BaseAgent
from environments.tic_tac_toe.tic_tac_toe_engine_utils import TicTacToeAction


def pretty_print(board):
    representation = ''
    height, width = board.shape
    
    for h in range(height):
        for w in range(width):
            if board[h, w] == -1:
                representation += '#'
            elif board[h, w] == 0:
                representation += 'O'
            elif board[h, w] == 1:
                representation += 'X'
            else:
                print("Invalid mark code")
                raise
        if h < height-1:
            representation += '\n'
    print(representation)


class HumanPlayerAgent(BaseAgent):
    def __init__(self):
        pass

    def take_action(self, state, action_space):
        print("State:")
        pretty_print(state.board)
        while True:
            input_string = input("\nType move's coordinates in order y, x (i.e 1,2): ")
            print("\n")
            result = parse("{},{}", input_string)
            y = int(result[0])
            x = int(result[1])
            action = TicTacToeAction(x, y)
            if action in action_space:
                return action
            else:
                print("Invalid action, try again")

    def update(self, state):
        print("State:")
        pretty_print(state.board)

    def receive_reward(self, reward):
        pass

    def exit(self, final_state):
        print(f"Game Over:")
        pretty_print(final_state.board)
#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from random import choice, sample, randrange

from reinforcement_learning.base.base_state import BaseState
from reinforcement_learning.base.base_action import BaseAction
from reinforcement_learning.base.base_action_space import BaseActionSpace
from environments.base.base_engine_utils import BasePlayer, BaseWinning

from random import choice, sample, randrange
import numpy as np

from dataclasses import dataclass


class Player(BasePlayer):
    """Class representing a Tic Tac Toe player.

    Parameters
    ----------
    name : str
        A player's name.
    mark: int
        A number corresponding to a player's mark.

    Attributes
    ----------
    name : str
        A player's name.
    mark: int
        A number corresponding to a player's mark.

    """

    def __init__(self, name, mark):
        assert name, "A player's name cannot be blank"
        self.name = name

        assert mark >= 0, "A player's mark has to be non-negative"
        self.mark = mark

    def __str__(self):
        return f"{self.name}({self.mark})"

    def __hash__(self):
        return hash((self.name, self.mark))

    def __eq__(self, other):
        return hash(self) == hash(other)


class Winning(BaseWinning):
    """Class representing a Tic Tac Toe winning line.

    Parameters
    ----------
    mark : int
        A number corresponding to a player's mark.
    points_included: list[(int, int)]
        List of tuples with coordinates of the winning line.

    Attributes
    ----------
    mark : int
        A number corresponding to a player's mark.
    points_included: list[(int, int)]
        List of tuples with coordinates of the winning line.
    """

    def __init__(self, mark, points_included):
        self.mark = mark
        self.points_included = points_included

    def __str__(self):
        return f"mark:{self.mark} points_included:{self.points_included}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, Winning) and \
               self.mark == other.mark and \
               self.points_included == other.points_included

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.mark, *self.points_included))


@dataclass(frozen=True)
class TicTacToeState:
    board: np.ndarray

    def __post_init__(self):
        self.board.flags.writeable = False
        assert len(self.board.shape) == 2, "Invalid dimensions of the board"
        assert self.board.shape[0] == self.board.shape[1], "The board is not square"

    def __str__(self):
        representation = ''
        height, width = self.board.shape
        for h in range(height):
            for w in range(width):
                if self.board[h, w] == -1:
                    representation += '#'
                elif self.board[h, w] == 0:
                    representation += 'O'
                elif self.board[h, w] == 1:
                    representation += 'X'
                else:
                    print("Invalid mark code")
                    raise
            if h < height - 1:
                representation += '\n'
        return representation

    def __hash__(self):
        return hash(self.board.data.tobytes())

    def __eq__(self, other):
        if not isinstance(other, TicTacToeState):
            return False
        return hash(self) == hash(other)


@dataclass(frozen=True)
class TicTacToeAction:
    row: int
    col: int


class TicTacToeActionSpace(BaseActionSpace):
    """
    actions: Set
    """
    def __init__(self, actions: set):
        self.actions = actions

    def __contains__(self, action):
        return action in self.actions

    def __len__(self):
        return len(self.actions)

    @property
    def random_action(self):
        return choice(list(self.actions))

    @property
    def random_actions(self, no_of_actions=None):
        no_of_actions = randrange(1, len(self.actions)) if not no_of_actions else no_of_actions
        return sample(list(self.actions), no_of_actions)

    def __eq__(self, other):
        return self.actions == other.actions

    def __str__(self):
        return str(self.actions)


class IllegalMoveError(Exception):
    """Raised when there is an illegal move made"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


a = np.array([[0, 0, 1], [1, 1, 0], [0, 0, 1]])
state = TicTacToeState(a)
state2 = TicTacToeState(a)
# a[0][0] = 1
# print(len(a.shape))
# print(hash(state))

# print(state == state2)

x = {state: 2}

print(x[state])
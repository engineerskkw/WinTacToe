#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from random import choice, sample, randrange
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Set

from reinforcement_learning.base.base_state import BaseState
from reinforcement_learning.base.base_action import BaseAction
from reinforcement_learning.base.base_action_space import BaseActionSpace
from environments.base.base_engine_utils import BasePlayer, BaseWinning


@dataclass(frozen=True)
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
    name: str
    mark: int

    def __post_init__(self):
        assert self.name, "A player's name cannot be blank"
        assert self.mark >= 0, "A player's mark has to be non-negative"


@dataclass(frozen=True)
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
    mark: int
    points_included: List[Tuple[int, int]]

    def __hash__(self):
        return hash((self.mark, *self.points_included))

    def __eq__(self, other):
        if not isinstance(other, Winning):
            return False
        return hash(self) == hash(other)


@dataclass(frozen=True)
class TicTacToeState(BaseState):
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

    def flatten(self):
        return np.array(self.board.flatten(), dtype=np.float)

    def __hash__(self):
        return hash(self.board.data.tobytes())

    def __eq__(self, other):
        if isinstance(other, TicTacToeState):
            return hash(self) == hash(other)
        return False


@dataclass(frozen=True)
class TicTacToeAction(BaseAction):
    row: int
    col: int

    def flatten(self):
        return np.array([self.row, self.col], dtype=np.float)


@dataclass(frozen=True)
class TicTacToeActionSpace(BaseActionSpace):
    actions: Set[TicTacToeAction]

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


class IllegalMoveError(Exception):
    """Raised when there is an illegal move made"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)
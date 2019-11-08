#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from reinforcement_learning.abstract.abstract_state import AbstractState
from reinforcement_learning.abstract.abstract_action import AbstractAction
from reinforcement_learning.abstract.abstract_action_space import AbstractActionSpace



class Player:
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

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.name, self.mark))

    def __eq__(self, other):
        return hash(self) == hash(other)


class Winning:
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


class TicTacToeState(AbstractState):
    def __init__(self, board):
        self.board = board

    def __str__(self):
        return str(self.board)

    def __hash__(self):
        return hash(str(self.board))


class TicTacToeAction(AbstractAction):
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))


class TicTacToeActionSpace(AbstractActionSpace):
    pass


class IllegalMoveError(Exception):
    """Raised when there is an illegal move made"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)

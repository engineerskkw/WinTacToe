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
        if isinstance(other, Player):
            return hash(self) == hash(other)
        return NotImplemented


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


class IllegalMoveError(Exception):
    """Raised when there is an illegal move made"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)

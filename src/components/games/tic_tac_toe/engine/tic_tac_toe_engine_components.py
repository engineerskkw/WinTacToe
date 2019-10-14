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


class Winning:
    """Class representing a Tic Tac Toe winning line.

    Parameters
    ----------
    mark : int
        A number corresponding to a player's mark.
    starting_point: (int, int)
        A tuple with coordinates of the starting point of the winning line.
    ending_point: (int, int)
        A tuple with coordinates of the ending point of the winning line.

    Attributes
    ----------
    mark : int
        A number corresponding to a player's mark.
    starting_point: (int, int)
        A tuple with coordinates of the starting point of the winning line.
    ending_point: (int, int)
        A tuple with coordinates of the ending point of the winning line.

    """

    def __init__(self, mark, starting_point, ending_point):
        self.mark = mark
        self.starting_point = starting_point
        self.ending_point = ending_point

    def __str__(self):
        return f"mark:{self.mark} start:{self.starting_point} end:{self.ending_point}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, Winning) and \
               self.mark == other.mark and \
               self.starting_point == other.starting_point and \
               self.ending_point == other.ending_point

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.mark, self.starting_point, self.ending_point))

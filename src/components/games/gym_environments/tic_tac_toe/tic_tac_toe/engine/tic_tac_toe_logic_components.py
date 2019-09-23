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
        self.name = name
        self.mark = mark


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
        return str(self.mark) + ", start: " + str(self.starting_point) + ", end: " + str(self.ending_point)

    def __repr__(self):
        return self.__str__()

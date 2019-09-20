import numpy as np
import random


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


class Board:
    """Class representing a Tic Tac Toe board.

    Parameters
    ----------
    size : int
        Dimension of the square board.
    marks_required: int
        Number of marks required to form a winning line.

    Attributes
    ----------
    size : int
        Dimension of the square board.
    marks_required: int
        Number of marks required to form a winning line.
    board: np.array(dtype=int)
        A numpy array representing the board. At the begining the board is filled with
        value -1 to represent a non-occupied place.

    Methods
    -------
    place_mark(x, y, mark)
        Places a mark at the (x, y) coordinates.
    gather_winnings()
        Gathers all the winning lines and marks along with their coordinates.

    """

    def __init__(self, height, width, marks, marks_required, end_game_strategy):
        self.height = height
        self.width = width
        self.marks = marks
        self.marks_required = marks_required
        self.end_game_strategy = end_game_strategy

        self.board = np.full((height, width), -1)

    def place_mark(self, x, y, mark):
        """Places a mark at the (x,y) coordinates.

        Parameters
        ----------
        x : int
            The x coordinate.
        y : int
            The y coordinate.
        mark: int
                A number corresponding to a player's mark.

        Returns
        -------
        bool
            True if successful, False if the place is already taken.
        """
        if self.board[x][y] == -1:
            self.board[x][y] = mark
            return True

        return False

    def get_unoccupied_fields(self):
        unoccupied_fields = []

        for i in range(self.height):
            for j in range(self.width):
                if self.board[i, j] == -1:
                    unoccupied_fields.append([i, j])

        return unoccupied_fields

    def gather_winnings(self):
        return self.end_game_strategy.gather_winnings(self)

    def randomize(self):
        # Uniform random initialization, but without
        # Game-endind or illegal(win of both players) states

        # All possible players' marks and empty mark
        all_marks = self.marks + [-1]

        # Random fields filling order
        coords = []
        size = self.board.size
        for v in range(size):
            for h in range(size):
                coords.append((v, h))

        random.shuffle(coords)
        n = random.randint(0, len(coords))  # Number of fields to fill

        # Random fields value
        for i in range(n):
            v, h = coords[i]
            random_mark = random.choice(all_marks)
            self.place_mark(v, h, random_mark)
            if self.gather_winnings():
                self.board[v, h] = -1

        # Check all fields filled
        # if so, then randomly unmark one of them
        all_filled = True
        for v in range(size):
            for h in range(size):
                if self.board[v, h] == -1:
                    all_filled = False
                    break

        if all_filled:
            v = random.randint(0, size - 1)
            h = random.randint(0, size - 1)
            self.board[v, h] = -1

# import abstract_logic
import numpy as np
from itertools import chain, cycle
from ..abstract_logic import AbstractLogic


class Player:
    """Class representing a Tic Tac Toe player.

    Parameters
    ----------
    name : str
        A player's name.
    mark: int
        A number coresponding to a player's mark.

    Attributes
    ----------
    name : str
        A player's name.
    mark: int
        A number coresponding to a player's mark.
        
    """

    def __init__(self, name, mark):
        self.name = name
        self.mark = mark


class Winning:
    """Class representing a Tic Tac Toe winning line.

    Parameters
    ----------
    mark : int
        A number coresponding to a player's mark.
    starting_point: (int, int)
        A tuple with coordinates of the starting point of the winning line.
    ending_point: (int, int)
        A tuple with coordinates of the ending point of the winning line.

    Attributes
    ----------
    mark : int
        A number coresponding to a player's mark.
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

    def __init__(self, size, marks_required):
        self.size = size
        self.marks_required = marks_required
        self.board = np.full((size, size), -1)

    def place_mark(self, x, y, mark):
        """Places a mark at the (x,y) coordinates.

        Parameters
        ----------
        x : int
            The x coordinate.
        y : int
            The y coordinate.

        Returns
        -------
        bool
            True if successful, False if the place is already taken.
        """
        if self.board[x][y] == -1:
            self.board[x][y] = mark
            return True

        return False

    def gather_winnings(self):
        """Gathers winnings from the current state of the board.

        In some versions of the game there can be multiple winners or there can be a tie.

        Returns
        -------
        list[Winning]
            A list of the current winnings on the board.
        """
        winnings = []

        for i in range(size - marks_required + 1):
            for j in range(size - marks_required + 1):
                subboard = self.board[i:i + marks_required, j:j + marks_required]
                winnings += self._check_subboard(subboard, (i, j))

        return winnings

    def _check_subboard(self, subboard, top_left):
        winnings = []
        subboard_size = subboard.shape[0]

        # Check for the winning line in rows
        for i in range(subboard_size):
            if self._check_line(subboard[i]):
                mark = subboard[i][0]
                starting_point = (top_left[0] + i, top_left[1])
                ending_point = (top_left[0] + i, top_left[1] + subboard_size - 1)

                winnings.append(Winning(mark, starting_point, ending_point))

        # Check for the winning line in columns
        for j in range(subboard_size):
            if self._check_line(subboard[:, j]):
                mark = subboard[:, j][0]
                starting_point = (top_left[0], top_left[1] + j)
                ending_point = (top_left[0] + subboard_size - 1, top_left[1] + j)

                winnings.append(Winning(mark, starting_point, ending_point))

        # Check for the winning line on the main diagonal
        main_diag = np.diag(subboard)
        if self._check_line(main_diag):
            mark = main_diag[0]
            starting_point = (top_left[0], top_left[1])
            ending_point = (top_left[0] + subboard_size - 1, top_left[1] + subboard_size - 1)

            winnings.append(Winning(mark, starting_point, ending_point))

        # Check for the winning line on the second diagonal
        second_diag = np.diag(np.flip(subboard, 1))
        if self._check_line(second_diag):
            mark = second_diag[0]
            starting_point = (top_left[0], top_left[1] + subboard_size - 1)
            ending_point = (top_left[0] + subboard_size - 1, top_left[1])

            winnings.append(Winning(mark, starting_point, ending_point))

        return winnings

    def _check_line(self, line):
        if not np.any(line == -1) and np.all(line == line[0]):
            return True


class TicTacToeLogic(AbstractLogic):
    """Class containing a Tic Tac Toe logic.

    It contains all the necessary methods to run a single instance of the game
    between arbitrary number of players and an arbitrary size of the board 
    (though not inifite). 


    Parameters
    ----------
    players : list[Player]
        A list of participating players.
    size: int
        Dimension of the square tic tac toe board.
    marks_required: int
        Number of marks required to form a winning line.

    Attributes
    ----------
    players : list[Player]
        A list of participating players.
    current_player: Player
        A player that is supposed to take the next turn.
    board: Board
        A board object representing a playing board.

    Methods
    -------
    place_mark(x, y, mark)
        Places a mark at the (x, y) coordinates and change the current player to the next one.
    gather_winnings()
        Gathers all the winning lines and marks along with their coordinates.
    get_current_state()
        Shares a numpy board represnting a current state of the board. 
        Used only by the AI playing the game.
    main_loop()
        Runs a single instance of the game ending with a single player winning.
    """

    def __init__(self, players, size, marks_required):
        self.players = players
        self._player_generator = cycle(players)
        self.current_player = next(self._player_generator)
        self.board = Board(size, marks_required)

    def place_mark(self, x, y):
        """Places a mark at the (x, y) coordinates and change the current player to the next one.

        Parameters
        ----------
        x : int
            The x coordinate.
        y : int
            The y coordinate.

        Returns
        -------
        bool
            True if successful, False if the place is already taken.
        """
        if self.board.place_mark(x, y, self.current_player.mark):
            self.current_player = next(self._player_generator)
            return True

        return False

    def gather_winnings(self):
        """Gathers winnings from the current state of the board.

        In some versions of the game there can be multiple winners or there can be a tie.

        Returns
        -------
        list[Winning]
            A list of the current winnings on the board.
        """
        return self.board.gather_winnings()

    def get_current_state(self):
        """Shares a numpy board represnting a current state of the board. 
        Used only by the AI playing the game.

        Returns
        -------
        np.array(dtype=int)
            A numpy array represnting the current board.
        """
        return self.board.board

    # TODO: Improve or move or replace.
    def main_loop(self):
        """Runs a single instance of the game ending with a single player winning."""
        current_winnings = []

        # Early version, needs polishing, maybe it should be implemented in one of the GUI classes
        while not current_winnings:
            print(self.board.board)
            x, y = input(str(self.current_player.name) + "'s turn... enter coordinates (e.g 1, 2):")
            self.place_mark(int(x), int(y))
            current_winnings = self.gather_winnings()

        winning_mark = current_winnings[0].mark
        winning_player = list(filter(lambda player: player.mark == winning_mark, self.players))[0]

        print(str(winning_player.name) + " won!")


# Exmaple initialization of the game
players = [Player('Wuju', 0), Player('Kapala', 1)]
size = 3
marks_required = 3

tic_tac_toe = TicTacToeLogic(players, size, marks_required)

tic_tac_toe.main_loop()

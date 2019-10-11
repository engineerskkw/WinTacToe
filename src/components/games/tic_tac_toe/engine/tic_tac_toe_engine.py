from gather_winnings_strategies import *
from itertools import cycle
import random
import numpy as np


class _Board:
    def __init__(self, size, marks, marks_required, gather_winnings_strategy):
        self.size = size
        self.marks = marks
        self.marks_required = marks_required
        self.gather_winnings_strategy = gather_winnings_strategy
        self.last_move = None

        self.board = np.full((size, size), -1)

    def place_mark(self, x, y, mark):
        if self.board[x][y] == -1 and mark in self.marks:
            self.board[x][y] = mark
            self.last_move = (x, y)
            return True

        return False

    def get_unoccupied_fields(self):
        unoccupied_fields = []

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i, j] == -1:
                    unoccupied_fields.append((i, j))

        return unoccupied_fields

    def gather_winnings(self):
        return self.gather_winnings_strategy.gather_winnings(self)

    def randomize(self):
        possible_marks = self.marks + [-1]

        # Random filling order
        coords = self.get_unoccupied_fields()
        random.shuffle(coords)

        # Random number of fields to fill
        n = random.randint(0, len(coords))

        # Random field values
        for k in range(n):
            i, j = coords[k]
            random_mark = random.choice(possible_marks)
            self.place_mark(i, j, random_mark)
            if self.gather_winnings():
                self.board[i, j] = -1

        # Check all fields filled
        # if so, then randomly unmark one of them
        all_filled = True
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i, j] == -1:
                    all_filled = False
                    break

        if all_filled:
            i = random.randint(0, self.size - 1)
            j = random.randint(0, self.size - 1)
            self.board[i, j] = -1


class TicTacToeEngine:
    """Class containing a Tic Tac Toe logic.

    It contains all the necessary methods to run an instance of the game
    between arbitrary number of players and an arbitrary size of the board 
    (though not infinite).


    Parameters
    ----------
    players : list[Player]
        A list of participating players.
    board_size: int
        Size of the square tic tac toe board.
    marks_required: int
        Number of marks required to form a winning line.
    gather_winnings_strategy: GatherWinningsStrategy
        An algorithm to check for the winner. Default is a StandardGatherWinningsStrategy

    Attributes
    ----------
    players : list[Player]
        A list of participating players.
    current_player: Player
        A player that is supposed to take the next turn.
    board_size: int
        Size of the square tic tac toe board.
    marks_required: int
        Number of marks required to form a winning line.
    gather_winnings_strategy: GatherWinningsStrategy
        An algorithm to check for the winner.

    Methods
    -------
    place_mark(x, y, mark)
        Places a mark at the (x, y) coordinates and change the current player to the next one.
    gather_winnings()
        Gathers all the winning lines and marks along with their coordinates.
    get_unoccupied_fields()
        Get a list of tuples of the coordinates of the unoccupied fields on the board.
    get_current_state()
        Shares a numpy board representing a current state of the board.
        Used only by the AI playing the game.
    main_loop()
        Runs a single instance of the game ending with a single player winning.
    """

    def __init__(self, players, board_size, marks_required,
                 gather_winnings_strategy=StandardGatherWinningsStrategy()):
        assert (len(players) >= 2), "There should be more than 2 players in the game..."
        self.players = players
        self._player_generator = cycle(players)
        self.current_player = next(self._player_generator)

        assert (board_size > 0), "Board size should be positive..."
        self.board_size = board_size

        assert (marks_required <= board_size), "Marks required should be less or equal to the board_size"
        self.marks_required = marks_required

        marks = list(map(lambda player: player.mark, players))
        assert (len(set(marks)) == len(marks)), "Marks of all players should be unique.."
        self.marks = marks

        self.gather_winnings_strategy = gather_winnings_strategy
        
        self._board = _Board(
            size=board_size,
            marks=marks,
            marks_required=marks_required,
            gather_winnings_strategy=gather_winnings_strategy
        )

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
        if self._board.place_mark(x, y, self.current_player.mark):
            self.current_player = next(self._player_generator)
            return True

        return False

    def gather_winnings(self):
        """Gathers winnings from the current state of the board according to gather winnings strategy.

        In some versions of the game there can be multiple winners or there can be a tie.

        Returns
        -------
        list[Winning]
            A list of the current winnings on the board.
        """
        return self._board.gather_winnings()

    def get_unoccupied_fields(self):
        """Get a list of tuples of the coordinates of the unoccupied fields on the board.

        Returns
        ------
        list[(x, y)]
            A list of coordinates.
        """
        return self._board.get_unoccupied_fields()

    def randomize_board(self):
        """Randomly and uniformly initialize board, without a game-ending scenario or illegal states."""
        self._board.randomize()

    def get_current_state(self):
        """Shares a numpy board representing a current state of the board and a current player object.

        Returns
        -------
        (np.array(dtype=int), Player)
            A numpy array representing the current board and a current player object.
        """
        return self._board.board, self.current_player

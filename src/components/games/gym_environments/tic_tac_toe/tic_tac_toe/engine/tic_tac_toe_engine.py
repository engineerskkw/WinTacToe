from .gather_winnings_strategies import *
from itertools import cycle
import random


class _Board:
    def __init__(self, height, width, marks, marks_required, gather_winnings_strategy):
        self.height = height
        self.width = width
        self.marks = marks
        self.marks_required = marks_required
        self.gather_winnings_strategy = gather_winnings_strategy
        self.last_move = None

        self.board = np.full((height, width), -1)

    def place_mark(self, x, y, mark):
        if self.board[x][y] == -1 and mark in self.marks:
            self.board[x][y] = mark
            self.last_move = (x, y)
            return True

        return False

    def get_unoccupied_fields(self):
        unoccupied_fields = []

        for i in range(self.height):
            for j in range(self.width):
                if self.board[i, j] == -1:
                    unoccupied_fields.append((i, j))

        return unoccupied_fields

    def gather_winnings(self, alternate_gather_winnings_strategy=None):
        if alternate_gather_winnings_strategy is not None:
            return alternate_gather_winnings_strategy.gather_winnings(self)

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
            if self.gather_winnings(AlternateGatherWinningsStrategy()):
                self.board[i, j] = -1

        # Check all fields filled
        # if so, then randomly unmark one of them
        all_filled = True
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i, j] == -1:
                    all_filled = False
                    break

        if all_filled:
            i = random.randint(0, self.height - 1)
            j = random.randint(0, self.width - 1)
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
    height: int
        Height of the tic tac toe board.
    width: int
        Height of the tic tac toe board.
    marks_required: int
        Number of marks required to form a winning line.
    gather_winnings_strategy: EndGameStrategy
        An algorithm to check for the winner. Default is a BasicEndGameStrategy

    Attributes
    ----------
    players : list[Player]
        A list of participating players.
    current_player: Player
        A player that is supposed to take the next turn.

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

    def __init__(self, players, height, width, marks_required,
                 gather_winnings_strategy=StandardGatherWinningsStrategy()):
        self.players = players
        self._player_generator = cycle(players)
        self.current_player = next(self._player_generator)

        self._board = _Board(
            height=height,
            width=width,
            marks=map(lambda player: player.mark, players),
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
        """Gathers winnings from the current state of the board.

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
        """Shares a numpy board representing a current state of the board.

        Returns
        -------
        np.array(dtype=int)
            A numpy array representing the current board.
        """
        return self._board.board, self.current_player

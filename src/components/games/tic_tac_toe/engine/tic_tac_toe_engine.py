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
        self.last_mark = None

        self.board = np.full((size, size), -1)

    def place_mark(self, x, y, mark):
        if self.board[x][y] == -1 and mark in self.marks:
            self.board[x][y] = mark
            self.last_move = (x, y)
            self.last_mark = mark
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
    (though not infinite). It also contains some helper methods for the RL agent to use.


    Parameters
    ----------
    no_of_players : int
        Number of participating players.
    board_size: int
        Size of the square tic tac toe board.
    marks_required: int
        Number of marks required to form a winning line.
    gather_winnings_strategy: GatherWinningsStrategy
        An algorithm to check for the winner. Default is a StandardGatherWinningsStrategy


    Methods
    -------
    current_player(): player
        A player currently supposed to make a move.
    players(): list[Player]
        A list of player objects representing real players.
    current_board(): np.array(dtype=int)
        An numpy array representing current state of the board.
    winnings(): list[Winnings]
        A list of current winnings.
    allowed_actions(): list[(int, int)]
        Get a list of tuples of the coordinates of the unoccupied fields on the board.
    rewards(): {player: int}
        A hash containing a reward for each player. Used by RL agent when learning.
    check_for_gameover(): bool
        Return true if the game is over, false otherwise.
    make_move(x, y)
        Places a mark at the (x, y) coordinates, changes the current player to the next one and gathers winnings.
    randomize_board()
        Randomly and uniformly initialize board, without a game-ending scenario or illegal states.
    reset()
        Resets the board to the starting arrangement and resets current player.
    """

    def __init__(self, no_of_players, board_size, marks_required,
                 gather_winnings_strategy=StandardGatherWinningsStrategy()):
        assert (no_of_players >= 2), "There should be more than 2 players in the game..."
        self._players = []
        self._init_players(no_of_players)
        self._player_generator = cycle(self.players)
        self._current_player = next(self._player_generator)

        assert (board_size > 0), "Board size should be positive..."
        self._board_size = board_size

        assert (marks_required <= board_size), "Marks required should be less or equal to the board_size"
        self._marks_required = marks_required

        marks = list(map(lambda player: player.mark, self.players))
        assert (len(set(marks)) == len(marks)), "Marks of all players should be unique.."
        self._marks = marks

        self._gather_winnings_strategy = gather_winnings_strategy
        self._winnings = set()
        
        self._board = _Board(
            size=board_size,
            marks=marks,
            marks_required=marks_required,
            gather_winnings_strategy=gather_winnings_strategy
        )

    @property
    def current_player(self):
        return self._current_player

    @property
    def players(self):
        return self._players

    @property
    def current_board(self):
        return self._board.board

    @property
    def winnings(self):
        return self._winnings

    @property
    def allowed_actions(self):
        """Get a list of tuples of the coordinates of the unoccupied fields on the board.

        Returns
        ------
        list[(x, y)]
            A list of coordinates.
        """
        return self._board.get_unoccupied_fields()

    @property
    def rewards(self):
        if self.check_for_gameover():
            winning_marks = map(lambda winning: winning.mark, self.winnings)
            rewards = map(lambda player: 1 if player.mark in winning_marks else -1, self.players)
            return {player: reward for player, reward in zip(self.players, rewards)}
        else:
            return {player: 0 for player in self.players}

    def check_for_gameover(self):
        return bool(self.winnings)

    def make_move(self, x, y):
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
            self._current_player = next(self._player_generator)
            self._gather_winnings()
            return True

        return False

    def randomize_board(self):
        """Randomly and uniformly initialize board, without a game-ending scenario or illegal states."""
        self.reset()
        self._board.randomize()
        last_player = list(filter(lambda player: player.mark == self._board.last_mark, self.players))[0]

        while last_player != self.current_player:
            self._current_player = next(self._player_generator)

        self._current_player = next(self._player_generator)

    def reset(self):
        self._player_generator = cycle(self.players)
        self._current_player = next(self._player_generator)

        self._board = _Board(
            size=self._board_size,
            marks=self._marks,
            marks_required=self._marks_required,
            gather_winnings_strategy=self._gather_winnings_strategy
        )

    def _gather_winnings(self):
        self._winnings |= set(self._board.gather_winnings())

    def _init_players(self, no_of_players):
        names = [f"Player {i}" for i in range(no_of_players)]
        marks = range(no_of_players)
        self._players = [Player(name, mark) for name, mark in zip(names, marks)]

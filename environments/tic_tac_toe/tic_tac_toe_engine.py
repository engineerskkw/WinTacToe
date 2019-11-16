import sys, os
import random
from itertools import cycle

from environments.tic_tac_toe.gather_winnings_strategies import *
from environments.tic_tac_toe.tic_tac_toe_engine_utils import *

# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
REL_PROJECT_ROOT_PATH = "./../../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#


class _Board:
    def __init__(self, size, marks, marks_required):
        self._size = size
        self._marks = marks
        self._marks_required = marks_required

        self._points_placed = []
        self._marks_placed = []

        self._board = np.full((size, size), -1)

    @property
    def size(self):
        return self._size

    @property
    def marks_required(self):
        return self._marks_required

    @property
    def last_point(self):
        return self._points_placed[-1] if self._points_placed else None

    @property
    def last_mark(self):
        return self._marks_placed[-1] if self._marks_placed else None

    @property
    def raw_board(self):
        return self._board

    @property
    def unoccupied_fields(self):
        unoccupied_fields = []

        for row in range(self.size):
            for col in range(self.size):
                if self._board[row, col] == -1:
                    unoccupied_fields.append((row, col))

        return unoccupied_fields

    def place_mark(self, row, col, mark):
        if self._board[row][col] == -1 and mark in self._marks:
            self._board[row][col] = mark
            self._points_placed.append((row, col))
            self._marks_placed.append(mark)

        elif self._board[row][col] != -1:
            raise IllegalMoveError(f"These coordinates (row={row}, col={col}) are already taken...")

        elif mark not in self._marks:
            raise IllegalMoveError("This is an illegal mark...")

    def remove_last_mark(self):
        if self._points_placed:
            last_row, last_col = self._points_placed.pop()
            self._board[last_row][last_col] = -1
            self._marks_placed.pop()


class TicTacToeEngine:
    """Class containing a Tic Tac Toe logic.

    It contains all the necessary methods to run an instance of the game
    between arbitrary number of players and an arbitrary size of the board (though not infinite).
    It also contains some helper methods for the RL agent to use.

    In this version of the game there can only be one winner. The first one to score a winning line wins.

    Parameters
    ----------
    no_of_players : int
        Number of participating players.
    board_size: int
        Size of the square tic tac toe board.
    marks_required: int
        Number of marks required to form a winning line.


    Methods
    -------
    current_player()
        Get a player that is currently supposed to make a move.
    players()
        Get a list of player objects representing players.
    current_board()
        Get an state representing current state of the board.
    winnings()
        Get a list of current winnings.
    allowed_actions()
        Get a action space containing actions that indicate coordinates of unoccupied fields on the board.
    rewards(): {player: int}
        Get a hash containing a reward for each player. Used by RL agent when learning.
    ended()
        Check if the game has ended.
    make_move(action)
        Places a mark at the coordinates indicated by action, changes the current player
        to the next one and gathers winnings.
    randomize_board(seed)
        Randomly and uniformly initialize board, without a game-ending scenario or illegal states.
    reset()
        Reset the board to the starting arrangement and resets current player.
    run()
        Run the main loop of the game using the user keyboard input.
    """

    def __init__(self, no_of_players, board_size, marks_required):
        assert (no_of_players >= 2), "There should be more than 2 players in the game..."
        self._players = []
        self._init_players(no_of_players)
        self._player_generator = cycle(self._players)
        self._current_player = next(self._player_generator)

        assert (board_size > 0), "Board size should be positive..."
        self._board_size = board_size

        assert (marks_required <= board_size), "Marks required should be less or equal to the board_size"
        self._marks_required = marks_required

        marks = list(map(lambda player: player.mark, self._players))
        assert (len(set(marks)) == len(marks)), "Marks of all players should be unique.."
        self._marks = marks

        self._gather_winnings_strategy = StandardGatherWinningsStrategy()
        self._winnings = set()

        self._board = _Board(
            size=board_size,
            marks=marks,
            marks_required=marks_required
        )

    @property
    def current_player(self):
        """Get a player that is currently supposed to make a move.

        Returns
        -------
        Player
            A player that is currently supposed to make a move.
        """
        return self._current_player

    @property
    def players(self):
        """Get a list of player objects representing players.

        Returns
        -------
        list[Player]
            A list of player objects representing players.
        """
        return self._players

    @property
    def current_board(self):
        """Get an state representing current state of the board.

        Returns
        -------
        TicTacToeState
            A state representing current state of the board.
        """
        return TicTacToeState(self._board.raw_board)

    @property
    def winnings(self):
        """Get a list of current winning objects. It contains all the necessary information about the winners and
        positions of their winning marks.

        Returns
        -------
        list[Winnings]
            A list of current winnings.
        """
        return list(self._winnings)

    @property
    def allowed_actions(self):
        """Get a action space containing actions that indicate coordinates of unoccupied fields on the board.

        Returns
        -------
        TicTacToeActionSpace()
            Action space - list of actions containing tuples of the coordinates of the unoccupied fields on the board.
        """
        return TicTacToeActionSpace([TicTacToeAction(row, col) for row, col in self._board.unoccupied_fields])

    @property
    def rewards(self):
        """Get a hash containing a reward for each player. Used by RL agent when learning. When nobody has won yet,
        everybody get a reward of 0, if there is a winner he gets a reward of 1 and other players get -1.

        Returns
        -------
        hash{player: float}
                A hash containing a reward for each player.
        """
        if self.ended:
            winning_marks = map(lambda winning: winning.mark, self._winnings)
            rewards = map(lambda player: 1.0 if player.mark in winning_marks else -1.0, self._players)
            return {player: reward for player, reward in zip(self._players, rewards)}
        else:
            return {player: 0.0 for player in self._players}

    @property
    def ended(self):
        """Check if the game has ended. In this version of the game, the game ends when there is at most 1 winning
        or there are no other allowed moves.

        Returns
        -------
        bool
            True is the game has ended, False otherwise.
        """
        return bool(self._winnings) or not bool(self.allowed_actions.actions)

    def make_move(self, action):
        """Places a mark at the (row, col) coordinates indicated by the action
        and change the current player to the next one.

        Parameters
        ----------
        action: TicTacToeAction

        Raises
        ------
        IllegalMoveError
            If there is an illegal move made, that is coordinates row, col are already taken or there is an illegal mark.
        IndexError
            If there are invalid coordinates.

        """
        self._board.place_mark(action.row, action.col, self._current_player.mark)
        self._current_player = next(self._player_generator)
        self._gather_winnings()

    def randomize_board(self, seed=None):
        """Randomly and uniformly initialize board, without a game-ending scenario or illegal states.

        Parameters
        ----------
        seed : int
            Seed for the randomization algorithm.
        """
        self.reset()
        random.seed(seed)

        chosen_moves = self.allowed_actions.random_actions

        for move in chosen_moves:
            try:
                self.make_move(move)
                if self.ended:
                    self._undo_last_move()
            except (IndexError, IllegalMoveError):
                continue

    def reset(self):
        """Resets the board to the starting arrangement, resets current player and winnings."""
        self._player_generator = cycle(self._players)
        self._current_player = next(self._player_generator)
        self._winnings = set()

        self._board = _Board(
            size=self._board_size,
            marks=self._marks,
            marks_required=self._marks_required
        )

    def run(self):
        """Runs the main loop of the game using the user keyboard input."""
        while not self.ended:
            print(self._board.raw_board)
            print(f"{self._current_player}")

            while True:
                try:
                    row, col = input("Input coordinates: ")
                    self.make_move(TicTacToeAction(int(row), int(col)))
                    break
                except IndexError:
                    print("These are not valid coordinates, try again...")
                    continue
                except IllegalMoveError as error:
                    print(error)
                    continue

        print(self._board.raw_board)

        try:
            winning_mark = list(self._winnings)[0].mark
            winner = next(filter(lambda player: player.mark == winning_mark, self._players))
            print(f"{winner} won!")
            print(f"Winings: {self.winnings}")
        except (IndexError, StopIteration):
            print("There is a draw!")

    def _gather_winnings(self):
        self._winnings |= set(self._gather_winnings_strategy.run(self._board))

    def _init_players(self, no_of_players):
        names = [f"Player {i}" for i in range(no_of_players)]
        marks = range(no_of_players)
        self._players = [Player(name, mark) for name, mark in zip(names, marks)]

    def _undo_last_move(self):
        last_mark = self._board.last_mark
        last_point = self._board.last_point

        self._board.remove_last_mark()
        self._remove_last_winning(last_mark, last_point)
        self._rewind_last_player(last_mark)

    def _remove_last_winning(self, last_mark, last_point):
        try:
            last_winning = next(filter(lambda winning: winning.mark == last_mark and
                                                       last_point in winning.points_included, self._winnings))
            self._winnings.remove(last_winning)
        except StopIteration:
            pass

    def _rewind_last_player(self, last_mark):
        while self.current_player.mark != self._board.last_mark:
            self._current_player = next(self._player_generator)

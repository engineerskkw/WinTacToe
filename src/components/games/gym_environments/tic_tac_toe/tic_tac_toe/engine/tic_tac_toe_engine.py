from .tic_tac_toe_logic_components import *
from .end_game_strategies import *
from itertools import cycle


class TicTacToeEngine:
    """Class containing a Tic Tac Toe logic.

    It contains all the necessary methods to run a single instance of the game
    between arbitrary number of players and an arbitrary size of the board 
    (though not infinite).


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
        Shares a numpy board representing a current state of the board.
        Used only by the AI playing the game.
    main_loop()
        Runs a single instance of the game ending with a single player winning.
    """

    def __init__(self, players, height, width, marks_required, end_game_strategy=BasicEndGameStrategy()):
        self.players = players
        self._player_generator = cycle(players)
        self.current_player = next(self._player_generator)

        self.board = Board(height, width, map(lambda player: player.mark, players), marks_required, end_game_strategy)

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

    def get_unoccupied_fields(self):
        return self.board.get_unoccupied_fields()

    def randomize_board(self):
        self.board.randomize()

    def get_current_state(self):
        """Shares a numpy board representing a current state of the board.
        Used only by the AI playing the game.

        Returns
        -------
        np.array(dtype=int)
            A numpy array representing the current board.
        """
        return self.board.board, self.current_player



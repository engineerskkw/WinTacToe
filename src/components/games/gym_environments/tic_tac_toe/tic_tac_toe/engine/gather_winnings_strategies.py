from tic_tac_toe_logic_components import *
from abc import ABC, abstractmethod
import numpy as np


class GatherWinningsStrategy(ABC):
    @abstractmethod
    def gather_winnings(self, board):
        pass

    @staticmethod
    def _check_subboard(subboard, top_left):
        winnings = []
        size = subboard.shape[0]

        def check_line(line):
            return not np.any(line == -1) and np.all(line == line[0])

        # Check for the winning line in rows
        for i in range(size):
            if check_line(subboard[i]):
                mark = subboard[i][0]
                starting_point = (top_left[0] + i, top_left[1])
                ending_point = (top_left[0] + i, top_left[1] + size - 1)

                winnings.append(Winning(mark, starting_point, ending_point))

        # Check for the winning line in columns
        for j in range(size):
            if check_line(subboard[:, j]):
                mark = subboard[:, j][0]
                starting_point = (top_left[0], top_left[1] + j)
                ending_point = (top_left[0] + size - 1, top_left[1] + j)

                winnings.append(Winning(mark, starting_point, ending_point))

        # Check for the winning line on the main diagonal
        main_diag = np.diag(subboard)
        if check_line(main_diag):
            mark = main_diag[0]
            starting_point = (top_left[0], top_left[1])
            ending_point = (top_left[0] + size - 1, top_left[1] + size - 1)

            winnings.append(Winning(mark, starting_point, ending_point))

        # Check for the winning line on the second diagonal
        second_diag = np.diag(np.flip(subboard, 1))
        if check_line(second_diag):
            mark = second_diag[0]
            starting_point = (top_left[0], top_left[1] + size - 1)
            ending_point = (top_left[0] + size - 1, top_left[1])

            winnings.append(Winning(mark, starting_point, ending_point))

        return winnings


class AlternateGatherWinningsStrategy(GatherWinningsStrategy):
    def gather_winnings(self, board):
        """Gathers winnings from the current state of the board, by checking the whole board for the winner.

        There can be multiple winners in this scenario. It is useful when game doesn't end when a single player
        forms a first winning line.

        Returns
        -------
        list[Winning]
            A list of the current winnings on the board.
        """
        winnings = []

        for i in range(board.size - board.marks_required + 1):
            for j in range(board.size - board.marks_required + 1):
                subboard = board.board[i:i + board.marks_required, j:j + board.marks_required]
                winnings += self._check_subboard(subboard, (i, j))

        return winnings


class StandardGatherWinningsStrategy(GatherWinningsStrategy):
    """Gathers winnings from the current state of the board, by checking the surrounding of the last move made.

    There should be only one winner in this scenario.

    Returns
    -------
    list[Winning]
        A list of the current winnings on the board. There should be only one winning.
    """
    def gather_winnings(self, board):
        if board.last_move is None:
            return []

        if board.size // 2 < board.marks_required:
            return AlternateGatherWinningsStrategy().gather_winnings(board)

        winnings = []
        x, y = board.last_move

        # Change the coordinates of the last move if it is in one of the corners
        if x - board.marks_required < 0:
            x = board.marks_required - 1
        elif x + board.marks_required >= board.size:
            x = board.size - board.marks_required

        if y - board.marks_required < 0:
            y = board.marks_required - 1
        elif y + board.marks_required >= board.size:
            y = board.size - board.marks_required

        # Check 4 subboards surrounding last move made
        subboard = board.board[x:x + board.marks_required, y:y + board.marks_required]
        top_left = (x, y)
        winnings += self._check_subboard(subboard, top_left)

        subboard = board.board[x - board.marks_required + 1: x + 1, y:y + board.marks_required]
        top_left = (x - board.marks_required, y)
        winnings += self._check_subboard(subboard, top_left)

        subboard = board.board[x: x + board.marks_required, y - board.marks_required + 1:y + 1]
        top_left = (x, y - board.marks_required)
        winnings += self._check_subboard(subboard, top_left)

        subboard = board.board[x - board.marks_required + 1: x + 1, y - board.marks_required + 1:y + 1]
        top_left = (x - board.marks_required, y - board.marks_required)
        winnings += self._check_subboard(subboard, top_left)

        return winnings

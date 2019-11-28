#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from abc import ABC, abstractmethod
import numpy as np
import math

from environments.tic_tac_toe.tic_tac_toe_engine_utils import *



class GatherWinningsStrategy(ABC):
    @abstractmethod
    def run(self, board):
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

                points_included = []
                for k in range(size):
                    points_included.append((top_left[0] + i, top_left[1] + k))

                winnings.append(Winning(mark, points_included))

        # Check for the winning line in columns
        for j in range(size):
            if check_line(subboard[:, j]):
                mark = subboard[:, j][0]

                points_included = []
                for k in range(size):
                    points_included.append((top_left[0] + k, top_left[1] + j))

                winnings.append(Winning(mark, points_included))

        # Check for the winning line on the main diagonal
        main_diag = np.diag(subboard)
        if check_line(main_diag):
            mark = main_diag[0]

            points_included = []
            for k in range(size):
                points_included.append((top_left[0] + k, top_left[1] + k))

            winnings.append(Winning(mark, points_included))

        # Check for the winning line on the second diagonal
        second_diag = np.diag(np.flip(subboard, 1))
        if check_line(second_diag):
            mark = second_diag[0]

            points_included = []
            for k in range(size):
                points_included.append((top_left[0] + k, top_left[1] + size - 1 - k))

            winnings.append(Winning(mark, points_included))

        return winnings


class AlternateGatherWinningsStrategy(GatherWinningsStrategy):
    def run(self, board):
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
                subboard = board.raw_board[i:i + board.marks_required, j:j + board.marks_required]
                winnings += self._check_subboard(subboard, (i, j))

        return winnings


class StandardGatherWinningsStrategy(GatherWinningsStrategy):
    """Gathers winnings from the current state of the board, by checking the surrounding of the last move made.

    There should be only one winner in this scenario.

    Returns
    -------
    list[Winning]
        A list of the current winnings on the board in the neighbourhood of the last move made.
    """
    def run(self, board):
        if not board.last_point:
            return []

        if math.ceil(board.size/2) < board.marks_required:
            return AlternateGatherWinningsStrategy().run(board)

        winnings = []
        row, col = board.last_point

        # Change the coordinates of the last move if it is in one of the corners
        if row - board.marks_required < 0:
            row = board.marks_required - 1
        elif row + board.marks_required > board.size:
            row = board.size - board.marks_required

        if col - board.marks_required < 0:
            col = board.marks_required - 1
        elif col + board.marks_required > board.size:
            col = board.size - board.marks_required

        for i in range(row-board.marks_required+1, row+1):
            for j in range(col-board.marks_required+1, col+1):
                subboard = board.raw_board[i:i + board.marks_required, j:j + board.marks_required]
                winnings += self._check_subboard(subboard, (i, j))

        return winnings

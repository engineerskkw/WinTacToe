from .tic_tac_toe_logic_components import *
from abc import ABC, abstractmethod
from threading import Thread


class EndGameStrategy(ABC):
    @abstractmethod
    def gather_winnings(self, board):
        pass

    @staticmethod
    def _check_subboard(subboard, top_left):
        winnings = []
        subboard_size = subboard.shape[0]

        def check_line(line):
            not np.any(line == -1) and np.all(line == line[0])

        # Check for the winning line in rows
        for i in range(subboard_size):
            if check_line(subboard[i]):
                mark = subboard[i][0]
                starting_point = (top_left[0] + i, top_left[1])
                ending_point = (top_left[0] + i, top_left[1] + subboard_size - 1)

                winnings.append(Winning(mark, starting_point, ending_point))

        # Check for the winning line in columns
        for j in range(subboard_size):
            if check_line(subboard[:, j]):
                mark = subboard[:, j][0]
                starting_point = (top_left[0], top_left[1] + j)
                ending_point = (top_left[0] + subboard_size - 1, top_left[1] + j)

                winnings.append(Winning(mark, starting_point, ending_point))

        # Check for the winning line on the main diagonal
        main_diag = np.diag(subboard)
        if check_line(main_diag):
            mark = main_diag[0]
            starting_point = (top_left[0], top_left[1])
            ending_point = (top_left[0] + subboard_size - 1, top_left[1] + subboard_size - 1)

            winnings.append(Winning(mark, starting_point, ending_point))

        # Check for the winning line on the second diagonal
        second_diag = np.diag(np.flip(subboard, 1))
        if check_line(second_diag):
            mark = second_diag[0]
            starting_point = (top_left[0], top_left[1] + subboard_size - 1)
            ending_point = (top_left[0] + subboard_size - 1, top_left[1])

            winnings.append(Winning(mark, starting_point, ending_point))

        return winnings


class BasicEndGameStrategy(EndGameStrategy):
    def gather_winnings(self, board):
        """Gathers winnings from the current state of the board, by checking the whole board for the winner.

        Returns
        -------
        list[Winning]
            A list of the current winnings on the board.
        """
        winnings = []

        for i in range(board.height - board.marks_required + 1):
            for j in range(board.width - board.marks_required + 1):
                subboard = board.board[i:i + board.marks_required, j:j + board.marks_required]
                winnings += self._check_subboard(subboard, (i, j))

        return winnings


class AdvancedEndGameStrategy(EndGameStrategy):
    def gather_winnings(self, board):
        winnings = []

        x, y = board.last_move

        first_subboard = board.board[x:x + board.marks_required, y:y + board.marks_required]

        winnings.append(self._check_subboard(first_subboard, (last_move_x, last_move_y))

        second_subboard = numpy_board[
            last_move_x - marks_required: last_move_x,
            last_move_y: last_move_y + marks_required
        ]

        winnings.append(self._check_subboard(second_subboard, last_move_x - marks_required, last_move_y))

        third_subboard = numpy_board[
                          last_move_x - marks_required: last_move_x,
                          last_move_y: last_move_y + marks_required
                          ]






class ParallelEndGameStrategy(EndGameStrategy):

    def gather_winnings(self, board):
        height, width = board.height, board.width
        marks_required = board.marks_required
        numpy_board = board.board
        winnings = []

        threads = []

        for i in range(height - marks_required + 1):
            for j in range(width - marks_required + 1):
                subboard = numpy_board[i:i + marks_required, j:j + marks_required]
                threads.append(
                    Thread(
                        target=self._check_subboard,
                        args=(subboard, (i, j))
                    )
                )
        for thread in threads:
            thread.start()

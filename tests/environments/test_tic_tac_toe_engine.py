import numpy as np
from unittest import TestCase
from itertools import product

from environments.tic_tac_toe.tic_tac_toe_engine import TicTacToeEngine
from environments.tic_tac_toe.tic_tac_toe_engine_utils import Player, Winning, IllegalMoveError, TicTacToeAction, TicTacToeActionSpace


class TestTicTacToeEngine(TestCase):
    def setUp(self):
        self.no_of_players = 3
        self.board_size = 5
        self.marks_required = 3
        self.engine = TicTacToeEngine(self.no_of_players, self.board_size, self.marks_required)

        self.partial_move_sequence = \
            [TicTacToeAction(row, col) for row, col in [(0, 0), (1, 0), (2, 0), (0, 1), (1, 4), (2, 3)]]
        self.full_move_sequence = \
            [TicTacToeAction(row, col) for row, col in list(product(range(self.board_size), range(self.board_size)))]
        self.winning_move_sequence = \
            [TicTacToeAction(row, col) for row, col in  [(0, 0), (1, 0), (2, 0), (0, 1), (1, 4), (2, 3), (0, 2)]]

    def init_board(self, actions):
        for action in actions:
            self.engine.make_move(action)

    def test_proper_initialization(self):
        self.assertFalse(self.engine.winnings)
        self.assertTrue(self.engine.players == [Player("Player 0", 0), Player("Player 1", 1), Player("Player 2", 2)])
        self.assertTrue(self.engine.current_player == Player("Player 0", 0))
        self.assertTrue(np.array_equal(self.engine.current_board.board, np.full((5, 5), -1)))
        # self.assertTrue(self.engine.allowed_actions == TicTacToeActionSpace(list(product(range(self.board_size), range(self.board_size)))))
        self.assertTrue(self.engine.rewards ==
                        {Player("Player 0", 0): 0, Player("Player 1", 1): 0, Player("Player 2", 2): 0})
        self.assertFalse(self.engine.ended)

    def test_improper_initialization(self):
        self.assertRaises(AssertionError, TicTacToeEngine, 1, 5, 5)  # wrong no of players
        self.assertRaises(AssertionError, TicTacToeEngine, 2, 1, 5)  # wrong board_size
        self.assertRaises(AssertionError, TicTacToeEngine, 2, 5, 6)  # wrong marks_required

    def test_make_move(self):
        self.engine.make_move(TicTacToeAction(0, 0))  # Player 0
        self.assertTrue(self.engine.current_board.board[0][0] == 0)
        self.assertTrue(self.engine.current_player == Player("Player 1", 1))
        self.assertFalse(self.engine.winnings)

        self.engine.make_move(TicTacToeAction(0, 1))  # Player 1
        self.assertTrue(self.engine.current_board.board[0][1] == 1)
        self.assertTrue(self.engine.current_player == Player("Player 2", 2))
        self.assertFalse(self.engine.winnings)

        self.engine.make_move(TicTacToeAction(3, 3))  # Player 2
        self.assertTrue(self.engine.current_board.board[3][3] == 2)
        self.assertTrue(self.engine.current_player == Player("Player 0", 0))
        self.assertFalse(self.engine.winnings)

        self.assertTrue(self.engine.rewards ==
                        {Player("Player 0", 0): 0, Player("Player 1", 1): 0, Player("Player 2", 2): 0})

    def test_make_move_fail(self):
        self.init_board(self.partial_move_sequence)
        self.assertRaises(IllegalMoveError, self.engine.make_move, TicTacToeAction(2, 3))
        self.assertRaises(IndexError, self.engine.make_move, TicTacToeAction(5, 5))

    def test_winnings_and_ended(self):
        self.init_board(self.winning_move_sequence)  # Player 0 should win
        self.assertTrue(self.engine.winnings == [Winning(0, [(0, 0), (0, 1), (0, 2)])])
        self.assertTrue(self.engine.ended)

        self.assertTrue(self.engine.rewards ==
                        {Player("Player 0", 0): 1, Player("Player 1", 1): -1, Player("Player 2", 2): -1})

    def test_allowed_actions_normally(self):
        pass
        # self.init_board(self.partial_move_sequence)
        # expected_allowed_actions = set(self.full_move_sequence).difference(set(self.partial_move_sequence))
        # self.assertTrue(set(self.engine.allowed_actions) == expected_allowed_actions)

    def test_allowed_actions_with_no_actions(self):
        self.init_board(self.full_move_sequence)
        self.assertFalse(set(self.engine.allowed_actions.actions))

    def test_reset(self):
        self.init_board(self.full_move_sequence)
        self.engine.reset()
        self.test_proper_initialization()

    def test_randomize_board(self):
        self.engine.randomize_board()

        self.assertFalse(self.engine.winnings)
        self.assertFalse(self.engine.ended)

    def test_set_proper_player(self):
        pass
        # # self.engine._rewind_last_player(None)
        # # self.assertEqual(self.engine.current_player, Player("Player 0", 0))
        #
        # self.engine._rewind_last_player(0)
        # self.assertEqual(self.engine.current_player, Player("Player 0", 0))
        #
        # self.engine._rewind_last_player(1)
        # self.assertEqual(self.engine.current_player, Player("Player 1", 1))
        #
        # self.engine._rewind_last_player(2)
        # self.assertEqual(self.engine.current_player, Player("Player 2", 2))

    def test_undo_last_move(self):
        pass
        # self.engine.make_move(TicTacToeAction(0, 0))
        # self.assertTrue(self.engine.current_player == Player("Player 1", 1))
        # self.assertFalse(self.engine.winnings)
        # self.assertFalse(self.engine.ended)
        #
        # self.engine._undo_last_move()
        #
        # self.assertTrue(self.engine.current_player == Player("Player 0", 0))
        # self.assertFalse(self.engine.winnings)
        # self.assertFalse(self.engine.ended)
        #
        # self.init_board(self.winning_move_sequence)
        # self.assertTrue(self.engine.current_player == Player("Player 1", 1))
        # self.assertTrue(self.engine.winnings == {Winning(0, [(0, 0), (0, 1), (0, 2)])})
        # self.assertTrue(self.engine.ended)
        #
        # self.engine._undo_last_move()
        #
        # self.assertTrue(self.engine.current_player == Player("Player 2", 2))
        # self.assertFalse(self.engine.winnings)
        # self.assertFalse(self.engine.ended)

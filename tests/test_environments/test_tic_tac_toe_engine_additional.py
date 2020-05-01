import numpy as np
from unittest import TestCase
from itertools import product

from environments.tic_tac_toe.tic_tac_toe_engine import TicTacToeEngine
from environments.tic_tac_toe.tic_tac_toe_engine_utils import Player, Winning, IllegalMoveError, TicTacToeAction, \
    TicTacToeActionSpace
from tests.test_environments.test_tic_tac_toe_engine import TestTicTacToeEngine


class TestTicTacToeEngineAdditional(TestTicTacToeEngine):
    def setUp(self):
        self.no_of_players = 2
        self.board_size = 3
        self.marks_required = 3
        self.engine = TicTacToeEngine(self.no_of_players, self.board_size, self.marks_required)

        self.partial_move_sequence = \
            [TicTacToeAction(row, col) for row, col in [(0, 0), (1, 1), (2, 1)]]
        self.full_move_sequence = \
            [TicTacToeAction(row, col) for row, col in list(product(range(self.board_size), range(self.board_size)))]
        self.player_0_winning_move_sequence = \
            [TicTacToeAction(row, col) for row, col in [(2, 0), (0, 1), (1, 1), (0, 0), (0, 2)]]
        self.player_1_winning_move_sequence = \
            [TicTacToeAction(row, col) for row, col in [(2, 2), (0, 1), (2, 0), (0, 0), (1, 1), (0, 2)]]

    def test_proper_initialization(self):
        self.assertFalse(self.engine.winnings)
        self.assertTrue(self.engine.players == (Player("Player 0", 0), Player("Player 1", 1)))
        self.assertTrue(self.engine.current_player == Player("Player 0", 0))
        self.assertTrue(np.array_equal(self.engine.current_state.board, np.full((3, 3), -1)))
        self.assertTrue(self.engine.allowed_actions == TicTacToeActionSpace(set(self.full_move_sequence)))
        self.assertTrue(self.engine.rewards == {Player("Player 0", 0): 0, Player("Player 1", 1): 0})
        self.assertFalse(self.engine.ended)

    def test_make_move(self):
        self.engine.make_move(TicTacToeAction(2, 2))  # Player 0
        self.assertTrue(self.engine.current_state.board[2][2] == 0)
        self.assertTrue(self.engine.current_player == Player("Player 1", 1))
        self.assertFalse(self.engine.winnings)

        self.engine.make_move(TicTacToeAction(1, 1))  # Player 1
        self.assertTrue(self.engine.current_state.board[1][1] == 1)
        self.assertTrue(self.engine.current_player == Player("Player 0", 0))
        self.assertFalse(self.engine.winnings)

        self.assertTrue(self.engine.rewards == {Player("Player 0", 0): 0, Player("Player 1", 1): 0})

    def test_make_move_fail(self):
        self.init_board(self.partial_move_sequence)
        self.assertRaises(IllegalMoveError, self.engine.make_move, TicTacToeAction(0, 0))
        self.assertRaises(IndexError, self.engine.make_move, TicTacToeAction(5, 5))

    def test_winnings_and_ended(self):
        self.init_board(self.player_0_winning_move_sequence)
        self.assertEqual(len(self.engine.winnings), 1)

        self.assertTrue(self.engine.winnings == (Winning(0, [(0, 2), (1, 1), (2, 0)]), ))
        self.assertTrue(self.engine.ended)
        self.assertTrue(self.engine.rewards == {Player("Player 0", 0): 1, Player("Player 1", 1): -1})

        self.engine.reset()

        self.init_board(self.player_1_winning_move_sequence)
        self.assertEqual(len(self.engine.winnings), 1)
        self.assertTrue(self.engine.winnings == (Winning(1, [(0, 0), (0, 1), (0, 2)]), ))
        self.assertTrue(self.engine.ended)
        self.assertTrue(self.engine.rewards == {Player("Player 0", 0): -1, Player("Player 1", 1): 1})

    def test_set_proper_player(self):
        self.engine._rewind_to_player(None)
        self.assertEqual(self.engine.current_player, Player("Player 0", 0))

        self.engine._rewind_to_player(0)
        self.assertEqual(self.engine.current_player, Player("Player 0", 0))

        self.engine._rewind_to_player(1)
        self.assertEqual(self.engine.current_player, Player("Player 1", 1))

    def test_remove_winning(self):
        pass

    def test_undo_last_move(self):
        pass

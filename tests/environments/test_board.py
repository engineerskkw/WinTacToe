# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os

REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from unittest import TestCase
from environments.tic_tac_toe.tic_tac_toe_engine import _Board


class TestBoard(TestCase):
    def setUp(self):
        size = 5
        marks = [0, 1, 2]
        marks_required = 3

        self.board = _Board(size, marks, marks_required)

    def test_last_point(self):
        self.assertFalse(self.board.last_point)

    def test_last_mark(self):
        self.assertFalse(self.board.last_mark)

    def test_remove_last_mark_with_no_marks(self):
        self.board.remove_last_mark()
        self.assertFalse(self.board.last_mark)
        self.assertFalse(self.board.last_point)

    def test_remove_last_mark_with_one_mark(self):
        self.board.place_mark(0, 0, 0)
        self.assertEqual(self.board.last_mark, 0)
        self.assertEqual(self.board.last_point, (0, 0))

        self.board.remove_last_mark()
        self.assertFalse(self.board.last_mark)
        self.assertFalse(self.board.last_point)

    def test_remove_last_mark_with_multiple_marks(self):
        self.board.place_mark(0, 0, 0)
        self.board.place_mark(2, 2, 1)

        self.assertEqual(self.board.last_mark, 1)
        self.assertEqual(self.board.last_point, (2, 2))

        self.board.remove_last_mark()
        self.assertEqual(self.board.last_mark, 0)
        self.assertEqual(self.board.last_point, (0, 0))

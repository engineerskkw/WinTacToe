# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from unittest import TestCase
from reinforcement_learning.agents.common.lazy_tabular_action_value import LazyTabularActionValue
from tests.mock.mock_action import MockAction
from tests.mock.mock_state import MockState


class TestLazyTabularActionValue(TestCase):
    def setUp(self):
        self.action_value = LazyTabularActionValue()
        self.mock_state1 = MockState([1, 2, 3, 4, 5])
        self.mock_state2 = MockState([6, 5, 4, 3])
        self.mock_action1 = MockAction([1, 2, 3])
        self.mock_action2 = MockAction([2, 3, 4])
        self.mock_action3 = MockAction([5, 6, 7])

        self.mock_state1_copy = MockState([1, 2, 3, 4, 5])

    def test_get_and_set_item(self):
        # Default value
        self.assertEqual(self.action_value[self.mock_state1, self.mock_action1], 0.)

        # Assigned value
        self.action_value[self.mock_state1, self.mock_action1] = 2.0
        self.assertEqual(self.action_value[self.mock_state1, self.mock_action1], 2.)

        # Assigned value to the different action
        self.action_value[self.mock_state1, self.mock_action2] = 3.0
        self.assertEqual(self.action_value[self.mock_state1, self.mock_action2], 3.)

        # Check getting with copied state
        self.assertEqual(self.action_value[self.mock_state1_copy, self.mock_action1], 2.)

        # Overwrite value
        self.action_value[self.mock_state1, self.mock_action2] = 10.0
        self.assertEqual(self.action_value[self.mock_state1_copy, self.mock_action2], 10.)

    def test_max_over_actions(self):
        self.action_value[self.mock_state1, self.mock_action1] = 2.0
        self.action_value[self.mock_state1, self.mock_action2] = 3.0

        self.assertEqual(self.action_value.max(self.mock_state1), 3.)
        self.assertEqual(self.action_value.max(self.mock_state2), 0.)

    def test_argmax_over_actions(self):
        self.action_value[self.mock_state1, self.mock_action1] = 2.0
        self.action_value[self.mock_state1, self.mock_action2] = 1.0
        self.action_value[self.mock_state1, self.mock_action3] = 2.0

        self.assertEqual(self.action_value.argmax(self.mock_state1),
                         {MockAction([1, 2, 3]), MockAction([5, 6, 7])})

        # For empty state
        self.assertFalse(self.action_value.argmax(self.mock_state2))

    def test_action_returns(self):
        self.action_value[self.mock_state1, self.mock_action1] = 2.0
        self.action_value[self.mock_state1, self.mock_action2] = 1.0
        self.action_value[self.mock_state1, self.mock_action3] = 2.0

        self.assertEqual(self.action_value.action_returns(self.mock_state1),
                         {MockAction([1, 2, 3]): 2.0, MockAction([2, 3, 4]): 1.0, MockAction([5, 6, 7]): 2.0})

        # For empty state
        self.assertFalse(self.action_value.action_returns(self.mock_state2))

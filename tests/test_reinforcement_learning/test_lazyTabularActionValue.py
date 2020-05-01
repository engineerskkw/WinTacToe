from unittest import TestCase
from reinforcement_learning.agents.common_building_blocks.lazy_tabular_action_value import LazyTabularActionValue
from tests.mock.test_mock_action import MockAction
from tests.mock.test_mock_state import MockState
import numpy as np


class TestLazyTabularActionValue(TestCase):
    def setUp(self):
        self.action_value = LazyTabularActionValue()
        self.mock_state1 = MockState(np.array([1, 2, 3, 4, 5]))
        self.mock_state2 = MockState(np.array([6, 5, 4, 3]))
        self.mock_action1 = MockAction(1, 2)
        self.mock_action2 = MockAction(5, 6)
        self.mock_action3 = MockAction(7, 8)

        self.mock_state1_copy = MockState(np.array([1, 2, 3, 4, 5]))

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
                         {self.mock_action1, self.mock_action3})

        # For empty state
        self.assertFalse(self.action_value.argmax(self.mock_state2))

    def test_action_returns(self):
        self.action_value[self.mock_state1, self.mock_action1] = 2.0
        self.action_value[self.mock_state1, self.mock_action2] = 1.0
        self.action_value[self.mock_state1, self.mock_action3] = 2.0

        self.assertEqual(self.action_value.action_returns(self.mock_state1),
                         {self.mock_action1: 2.0, self.mock_action2: 1.0, self.mock_action3: 2.0})

        # For empty state
        self.assertFalse(self.action_value.action_returns(self.mock_state2))

    def test_sample_update(self):

        self.action_value.sample_update(
            state=self.mock_state1,
            action=self.mock_action1,
            target=2,
            step_size=0.5
        )

        self.assertEqual(self.action_value[self.mock_state1, self.mock_action1], 1)

        self.action_value.sample_update(
            state=self.mock_state1,
            action=self.mock_action1,
            target=5,
            step_size=0.8
        )

        self.assertEqual(self.action_value[self.mock_state1, self.mock_action1], 4.2)


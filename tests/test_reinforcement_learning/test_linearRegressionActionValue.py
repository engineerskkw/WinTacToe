from unittest import TestCase
from reinforcement_learning.agents.common_building_blocks.linear_regression_action_value import LinearRegressionActionValue
from tests.mock.test_mock_action import MockAction
from tests.mock.test_mock_state import MockState
from tests.mock.test_mock_action_space import MockActionSpace
import numpy as np


class TestLinearRegressionActionValue(TestCase):
    def setUp(self):
        self.action_value = LinearRegressionActionValue(init_weights_zeros=True)

        self.mock_state1 = MockState(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
        self.mock_action1 = MockAction(1, 2)
        self.mock_action2 = MockAction(5, 6)

    def test_default_get_item(self):
        self.assertEqual(self.action_value[self.mock_state1, self.mock_action1], 0)

    def test_update_weights(self):
        self.action_value.sample_update(target=5, step_size=0.5, state=self.mock_state1, action=self.mock_action1)
        self.assertEqual(self.action_value[self.mock_state1, self.mock_action1], 727.5)

        self.action_value.sample_update(target=5, step_size=0.8, state=self.mock_state1, action=self.mock_action1)
        self.assertEqual(self.action_value[self.mock_state1, self.mock_action1], -167470.5)

    def test_max_over_actions(self):
        # TODO: More tests
        self.action_value.sample_update(target=5, step_size=0.5, state=self.mock_state1, action=self.mock_action1)
        max_value = self.action_value.max(self.mock_state1, MockActionSpace({self.mock_action1, self.mock_action2}))

        self.assertEqual(max_value, 757.5)

    def test_argmax_over_actions(self):
        # TODO: More tests
        self.action_value.sample_update(target=5, step_size=0.5, state=self.mock_state1, action=self.mock_action1)
        argmax_action = self.action_value.argmax(self.mock_state1, MockActionSpace({self.mock_action1, self.mock_action2}))

        self.assertEqual(argmax_action, {self.mock_action2})

    def test_action_returns(self):
        self.fail("TODO")

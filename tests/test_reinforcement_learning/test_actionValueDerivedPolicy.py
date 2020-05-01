from unittest import TestCase

from reinforcement_learning.agents.common.lazy_tabular_action_value import LazyTabularActionValue
from reinforcement_learning.agents.common.action_value_derived_policy import ActionValueDerivedPolicy

from tests.mock.test_mock_state import MockState
from tests.mock.test_mock_action import MockAction
from tests.mock.test_mock_action_space import MockActionSpace


class TestActionValueDerivedPolicy(TestCase):

    def setUp(self):
        self.action_value = LazyTabularActionValue()
        self.policy = ActionValueDerivedPolicy(self.action_value)

        self.mock_state1 = MockState([1, 2, 3, 4, 5])
        self.mock_state2 = MockState([6, 5, 4, 3])
        self.mock_action1 = MockAction([1, 2, 3])
        self.mock_action2 = MockAction([2, 3, 4])
        self.mock_action3 = MockAction([5, 6, 7])
        self.mock_action4 = MockAction([5, 6, 8])

        self.mock_state1_copy = MockState([1, 2, 3, 4, 5])

    def test_get_and_set_item(self):
        self.action_value[self.mock_state1, self.mock_action1] = 1.
        self.action_value[self.mock_state1, self.mock_action2] = 2.
        self.action_value[self.mock_state1, self.mock_action3] = 3.

        self.assertAlmostEqual(self.policy[self.mock_state1, self.mock_action1], 0.09003057)
        self.assertAlmostEqual(self.policy[self.mock_state1, self.mock_action2], 0.24472847)
        self.assertAlmostEqual(self.policy[self.mock_state1, self.mock_action3], 0.66524096)

        # Update one action value
        self.action_value[self.mock_state1, self.mock_action2] = 1.
        self.action_value[self.mock_state1, self.mock_action3] = 1.

        self.assertAlmostEqual(self.policy[self.mock_state1, self.mock_action1], 0.33333333)
        self.assertAlmostEqual(self.policy[self.mock_state1, self.mock_action2], 0.33333333)
        self.assertAlmostEqual(self.policy[self.mock_state1, self.mock_action3], 0.33333333)

        # Empty state
        self.assertAlmostEqual(self.policy[self.mock_state2, self.mock_action1], 1.)

        # State with no value for that action, should set action value to default before computing probability
        self.assertAlmostEqual(self.policy[self.mock_state1, self.mock_action4], 0.10923177)

    def test_epsilon_greedy(self):
        self.action_value[self.mock_state1, self.mock_action1] = 1.
        self.action_value[self.mock_state1, self.mock_action2] = 2.
        self.action_value[self.mock_state1, self.mock_action3] = 3.

        self.assertEqual(
            self.policy.epsilon_greedy(
                self.mock_state1,
                MockActionSpace({self.mock_action1, self.mock_action2, self.mock_action3}), epsilon=0
            ),
            MockAction([5, 6, 7])
        )

        self.action_value[MockState([1, 2, 3, 4, 5]), self.mock_action2] = 10.

        self.assertEqual(
            self.policy.epsilon_greedy(
                self.mock_state1,
                MockActionSpace({self.mock_action1, self.mock_action2, self.mock_action3}), epsilon=0
            ),
            MockAction([2, 3, 4])
        )

        self.assertEqual(
            self.policy.epsilon_greedy(
                self.mock_state1,
                MockActionSpace({self.mock_action1}), epsilon=0
            ),
            MockAction([1, 2, 3])
        )

        self.assertEqual(
            self.policy.epsilon_greedy(
                self.mock_state2,
                MockActionSpace({self.mock_action3}), epsilon=0
            ),
            MockAction([5, 6, 7])
        )


# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

from reinforcement_learning.agents.common.auxiliary_utilities import linear_map

REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import random
from graphviz import Digraph
from scipy.special import softmax
from reinforcement_learning.base.base_policy import BasePolicy
from reinforcement_learning.agents.common.lazy_tabular_action_value import LazyTabularActionValue

from all_tests.mock.test_mock_action import MockAction
from all_tests.mock.test_mock_state import MockState


class ActionValueDerivedPolicy(BasePolicy):
    MIN_PEN_WIDTH = 1
    MAX_PEN_WIDTH = 4

    def __init__(self, action_value):
        self.action_value = action_value

    def __getitem__(self, key: tuple):
        assert len(key) == 2, f"Invalid key: {key}, should be tuple(BaseState, BaseAction)..."

        state, action = key
        self.action_value[state, action]  # Initialize state action value by defaultdict
        expected_returns = self.action_value.action_returns(state)

        # Softmax on action returns gives the probability that they will be chosen
        softmax_returns = dict(zip(expected_returns.keys(), softmax(list(expected_returns.values()))))

        return softmax_returns[action]

    def epsilon_greedy(self, state, action_space, epsilon=0.1):
        if random.random() > epsilon:  # Choose action in the epsilon-greedy way
            greedy_actions = list(self.action_value.argmax(state))

            if greedy_actions:  # Check if there are any chosen possibilities
                action = random.choice(greedy_actions)  # Random drawback settlement

                if action in action_space:  # Check action validity
                    return action

        return action_space.random_action  # Otherwise (in each case) get a random action

    def __str__(self):
        acc = ""

        for state, actions in self.action_value.action_value_dict.items():
            greedy_actions = self.action_value.argmax(state)
            greedy_action_value = self.action_value.max(state)
            acc += f"State: \n"
            acc += f"{state}\n"
            acc += f"Greedy value: {greedy_action_value}\n"
            for action in greedy_actions:
                acc += f"Action: {action}\n"

        return acc

    def __repr__(self):
        return self.__str__()



    def _get_graph(self):
        graph = Digraph()
        for state in self.action_value.action_value_dict.keys():
            # Calculate sum of all actions' values from this state
            greedy_actions = self.action_value.argmax(state)
            greedy_action_value = self.action_value.max(state)

            graph.node(str(hash(state)), str(state))
            for greedy_action in greedy_actions:
                graph.node(str(hash(greedy_action)), str(greedy_action))
                # red = int(linear_map(value, 0, 255, actions.values()))
                # color = '#%02x%02x%02x' % (red, 0, 0)
                # penwidth = str(linear_map(value, self.MIN_PEN_WIDTH, self.MAX_PEN_WIDTH, actions.values()))
                graph.edge(str(hash(state)), str(hash(greedy_action)), label=str(greedy_action_value),
                           color="red", penwidth="2")
        return graph

    def _repr_svg_(self):
        return self._get_graph()._repr_svg_()

    def view(self):
        return self._get_graph().view()


if __name__ == '__main__':
    av = LazyTabularActionValue()

    s = MockState([[-1, -1], [-1, 1]])

    a1 = MockAction([0, 0])
    a2 = MockAction([0, 1])
    a3 = MockAction([1, 0])

    av[s, a1] = 6
    av[s, a2] = 2.9
    av[s, a3] = -10

    egp = ActionValueDerivedPolicy(av)

    print(egp)
    # egp.view()

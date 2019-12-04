# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from graphviz import Digraph
from collections import defaultdict

from reinforcement_learning.agents.common.auxiliary_utilities import linear_map
from reinforcement_learning.base.base_action_value import BaseActionValue
from all_tests.mock.test_mock_state import MockState
from all_tests.mock.test_mock_action import MockAction


class LazyTabularActionValue(BaseActionValue):
    MIN_PEN_WIDTH = 1
    MAX_PEN_WIDTH = 4

    def __init__(self):
        self.action_value_dict = defaultdict(self._default_state_action_dict)

    def __getitem__(self, key: tuple):
        assert len(key) == 2, f"Invalid key: {key}, should be tuple(BaseState, BaseAction)..."

        state, action = key
        return float(self.action_value_dict[state][action])

    def sample_update(self, **kwargs):
        state = kwargs['state']
        action = kwargs['state']
        step_size = kwargs['step_size']
        target = kwargs['target']

        old_estimate = self.action_value_dict[state][action]
        new_estimate = old_estimate + step_size * (target - old_estimate)
        self.action_value_dict[state][action] = new_estimate

    def max(self, state, action_space=None):
        expected_returns = self.action_value_dict[state].values()
        return max(expected_returns) if expected_returns else self._default_cell_value

    def argmax(self, state, action_space=None):
        actions = self.action_value_dict[state]
        return {key for (key, value) in actions.items() if value == max(actions.values())}

    def action_returns(self, state, action_space=None):
        return self.action_value_dict[state]

    @property
    def _default_cell_value(self):
        """
        This function is used specify the default action value

        Returns
        -------
        Float
            Default value of the action-value table cell.
        """
        return float(0)

    # Needed for pickle...
    def _default_action_value(self):
        return self._default_cell_value

    # Needed for pickle...
    def _default_state_action_dict(self):
        return defaultdict(self._default_action_value)

    def __str__(self):
        acc = ""

        for k1, v1 in self.action_value_dict.items():
            acc += f"State: \n"
            acc += f"{k1}\n"
            for k2, v2 in v1.items():
                acc += f"\tAction: {k2}, value: {v2} \n"

        return acc

    def __repr__(self):
        return self.__str__()

    def _get_graph(self):
        graph = Digraph()
        for state, actions in self.action_value_dict.items():
            # Calculate sum of all actions' values from this state

            graph.node(str(hash(state)), str(state))
            for action, value in actions.items():
                graph.node(str(hash(action)), str(action))
                red = int(linear_map(value, 0, 255, actions.values()))
                color = '#%02x%02x%02x' % (red, 0, 0)
                penwidth = str(linear_map(value, self.MIN_PEN_WIDTH, self.MAX_PEN_WIDTH, actions.values()))
                graph.edge(str(hash(state)), str(hash(action)), label=str(value),
                           color=color, penwidth=penwidth)
        return graph

    def _repr_svg_(self):
        return self._get_graph()._repr_svg_()

    def view(self):
        return self._get_graph().view()

if __name__ == '__main__':
    # # SimpleAction-value test
    av = LazyTabularActionValue()
    # print(av)
    #
    s = MockState([[-1, -1], [-1, 1]])

    a1 = MockAction([0, 0])
    a2 = MockAction([0, 1])
    a3 = MockAction([1, 0])

    av[s, a1] = 6
    av[s, a2] = 0.8
    av[s, a3] = -10

    print(av)
    # print(av.action_returns(s))
    # av.view()
    # print(s)

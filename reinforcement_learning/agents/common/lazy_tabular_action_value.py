# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from graphviz import Digraph

from reinforcement_learning.agents.basic_mc_agent.simple_state import SimpleState
from reinforcement_learning.agents.basic_mc_agent.simple_action import SimpleAction
from reinforcement_learning.agents.basic_mc_agent.auxiliary_utilities import linear_map
from reinforcement_learning.base.base_action_value import BaseActionValue


class LazyTabularActionValue(BaseActionValue):
    MIN_PEN_WIDTH = 1
    MAX_PEN_WIDTH = 4

    def __init__(self):
        self.action_value_dict = dict()

    def __getitem__(self, key: tuple):
        assert len(key) == 2, f"Invalid key: {key}, should be tuple(BaseState, BaseAction)..."

        state, action = key

        # Lazy initialization
        if not self.action_value_dict.get(state):
            self.action_value_dict[state] = {action: self._initial_cell_value}
        elif not self.action_value_dict[state].get(action):
            self.action_value_dict[state][action] = self._initial_cell_value

        return float(self.action_value_dict[state][action])

    def __setitem__(self, key, value):
        assert len(key) == 2, f"Invalid key: {key}, should be tuple(BaseState, BaseAction)..."

        state, action = key

        if not self.action_value_dict.get(state):
            self.action_value_dict[state] = dict()

        self.action_value_dict[state][action] = float(value)

    def max_over_actions(self, state):
        expected_returns = self.action_value_dict.get(state, dict()).values()
        return max(expected_returns) if expected_returns else self._initial_cell_value

    def argmax_over_actions(self, state):
        max_value = float('-inf')
        max_value_actions = set()
        for action, value in self.action_value_dict.get(state, {}).items():
            if value > max_value:
                max_value = value
                max_value_actions = {action}
            elif value == max_value:
                max_value_actions.add(action)
        return max_value_actions

    @property
    def _initial_cell_value(self):
        """
        This function is used to initialize action value table,
        despite the fact that it's lazy initialization.

        Returns
        -------
        Float
            Arbitrarily chosen, initial value of the action-value table cell.
        """
        return float(0)

    def returns_of_actions(self, state):
        return self.action_value_dict.get(state, dict())

    def __str__(self):
        return str(self.action_value_dict)

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
    # SimpleAction-value test
    av = LazyTabularActionValue()

    s = SimpleState([[-1, -1], [-1, 1]])

    a1 = SimpleAction([0, 0])
    a2 = SimpleAction([0, 1])
    a3 = SimpleAction([1, 0])

    av[s, a1] = 6
    av[s, a2] = 0.8
    av[s, a3] = -10

    print(av)
    av.view()
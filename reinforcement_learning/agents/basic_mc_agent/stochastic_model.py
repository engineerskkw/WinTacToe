#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from graphviz import Digraph
import numpy as np

from tests.mock.mock_state import SimpleState
from tests.mock.mock_action import SimpleAction
from reinforcement_learning.agents.basic_mc_agent.auxiliary_utilities import linear_map


class StochasticModel:
    MIN_PEN_WIDTH = 1
    MAX_PEN_WIDTH = 4

    def __init__(self):
        self.model_dict = {}

    # Lazy initialization
    def __getitem__(self, key):
        state, action = key
        return self.model_dict.get(state, {}).get(action, {})

    def __setitem__(self, key, next_state):
        state, action = key
        if self.model_dict.get(state) is None:
            self.model_dict[state] = {}
        if self.model_dict[state].get(action) is None:
            self.model_dict[state][action] = {}
        if self.model_dict[state][action].get(next_state) is None:
            self.model_dict[state][action][next_state] = 0
        self.model_dict[state][action][next_state] += 1

    def _get_graph(self):
        graph = Digraph()
        for state, actions in self.model_dict.items():
            # SimpleState node
            graph.attr('node', shape='doublecircle')
            graph.attr('node', style='', color='', fontcolor='black')
            state_hash = str(hash(state))
            graph.node(state_hash, str(state))
            for action, next_states in actions.items():
                # SimpleAction node
                graph.attr('node', shape='circle')
                graph.attr('node', style='filled', color='black', fontcolor='white')
                action_hash = str(hash(action)) + state_hash
                graph.node(action_hash, str(action))
                graph.edge(state_hash, action_hash)

                # Calculate sum of all visits numbers
                all_visits_no = sum(next_states.values())

                for next_state, visits_number in next_states.items():
                    # Next state node
                    graph.attr('node', shape='doublecircle')
                    graph.attr('node', style='', fontcolor='black')
                    next_state_hash = str(hash(next_state))
                    graph.node(next_state_hash, str(next_state))
                    visits_percentage = np.round(visits_number / all_visits_no * 100, 2)
                    label = f"{visits_number} ({visits_percentage}%)"
                    blue = int(linear_map(visits_number, 0, 255, next_states.values()))
                    color = '#%02x%02x%02x' % (0, 0, blue)
                    penwidth = str(linear_map(visits_number, self.MIN_PEN_WIDTH,
                                              self.MAX_PEN_WIDTH, next_states.values()))
                    graph.edge(action_hash, next_state_hash, label=label,
                               color=color, penwidth=penwidth)
        return graph

    def _repr_svg_(self):
        return self._get_graph()._repr_svg_()

    def view(self):
        return self._get_graph().view()


if __name__ == '__main__':
    # Model test

    m = StochasticModel()

    s1 = SimpleState([[-1, 0], [-1, -1]])
    a1 = SimpleAction([1, 0])
    s2 = SimpleState([[-1, 0], [0, -1]])
    s3 = SimpleState([[-1, 0], [-1, 0]])
    m[s1, a1] = s2
    m[s1, a1] = s3
    m[s1, a1] = s3
    m[s1, a1] = s3
    m[s1, a1] = s3

    a2 = SimpleAction([0, 0])
    s4 = SimpleState([[0, 0], [0, -1]])
    m[s2, a2] = s4

    a4 = SimpleAction([1, 1])
    s5 = SimpleState([[-1, 0], [0, 0]])
    s6 = SimpleState([[-1, 0], [-1, 0]])
    s7 = SimpleState([[-1, -1], [-1, -1]])
    m[s2, a4] = s5
    m[s2, a4] = s5
    m[s2, a4] = s5
    m[s2, a4] = s5
    m[s2, a4] = s5
    m[s2, a4] = s5
    m[s2, a4] = s5
    m[s2, a4] = s5
    m[s2, a4] = s6
    m[s2, a4] = s6
    m[s2, a4] = s6
    m[s2, a4] = s6
    m[s2, a4] = s6
    m[s2, a4] = s7
    m[s2, a4] = s7
    m[s2, a4] = s7

    m.view()
#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from graphviz import Digraph
import uuid

from reinforcement_learning.agents.basic_mc_agent.state import State
from reinforcement_learning.agents.basic_mc_agent.action import Action

class Returns:
    def __init__(self):
        self.returns_dict = {}

    # Lazy initialization
    def __getitem__(self, key):
        state, action = key
        if self.returns_dict.get(state) is None:
            self.returns_dict[state] = {action: []}  # Arbitrarily initialization
        elif self.returns_dict[state].get(action) is None:
            self.returns_dict[state][action] = []  # Arbitrarily initialization

        return self.returns_dict[state][action]

    def __setitem__(self, key, value):
        state, action = key
        if self.returns_dict.get(state) is None:
            self.returns_dict[state] = {}
        self.returns_dict[state][action] = value

    # Representations
    def __str__(self):
        return self.returns_dict.__str__()

    def _get_graph(self):
        graph = Digraph()
        graph.attr(rankdir="LR")
        for state, actions in self.returns_dict.items():
            for action, returns in actions.items():
                graph.attr('node', shape='doublecircle')
                state_hash = str(uuid.uuid4())
                graph.node(state_hash, str(state))
                graph.attr('node', shape='circle')
                action_hash = str(uuid.uuid4())
                graph.node(action_hash, str(action))
                graph.edge(state_hash, action_hash)

                graph.attr('node', shape='diamond')
                last_hash = action_hash
                for the_return in returns:
                    return_hash = str(uuid.uuid4())
                    graph.node(return_hash, str(the_return))
                    graph.edge(last_hash, return_hash)
                    last_hash = return_hash
        return graph

    def _repr_svg_(self):
        return self._get_graph()._repr_svg_()

    def view(self):
        return self._get_graph().view()


if __name__ == '__main__':
    # Returns test

    r = Returns()

    s1 = State([[-1, 0], [-1, -1]])
    a1 = Action([1, 0])
    G = -3
    r[s1, a1].append(G)

    s2 = State([[-1, 0], [0, -1]])
    a2 = Action([0, 0])
    G = 10.0
    r[s2, a2].append(G)
    G = 7.8
    r[s2, a2].append(G)

    s3 = State([[0, 0], [0, -1]])
    a3 = Action([1, 1])
    G = -5.1
    r[s3, a3].append(G)
    G = 3.2
    r[s3, a3].append(G)
    G = -1.9
    r[s3, a3].append(G)

    s4 = State([[-1, 0], [0, 0]])
    a4 = Action([0, 0])
    G = -5.1
    r[s4, a4].append(G)
    G = -6.5
    r[s4, a4].append(G)
    G = -9.4
    r[s4, a4].append(G)
    G = -10
    r[s4, a4].append(G)

    print(r)
    r.view()
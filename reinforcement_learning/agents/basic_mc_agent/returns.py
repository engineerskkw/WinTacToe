#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from graphviz import Digraph
import uuid
import copy


class Returns:
    def __init__(self):
        self.returns_dict = dict()

    # Lazy initialization
    def __getitem__(self, key):
        state, action = key
        state = copy.copy(state)
        if self.returns_dict.get(state) is None:
            self.returns_dict[state] = {action: []}  # Arbitrarily initialization
        elif self.returns_dict[state].get(action) is None:
            self.returns_dict[state][action] = []  # Arbitrarily initialization

        return self.returns_dict[state][action]

    def __setitem__(self, key, value):
        state, action = key
        if self.returns_dict.get(state) is None:
            self.returns_dict[state] = {action: value}
        self.returns_dict[state][action] = value

    def __str__(self):
        representation = ""
        for state, actions in self.returns_dict.items():
            for action, value in actions.items():
                representation += "State:\n"
                representation += state.__str__()
                representation += "\nAction:\n"
                representation += action.__str__()
                representation += "\nValues:\n"
                representation += value.__str__()
                representation += "\n\n"
        return representation

    def __len__(self):
        result = 0
        for state, actions in self.returns_dict.items():
            for action in actions.keys():
                result += 1
        return result

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

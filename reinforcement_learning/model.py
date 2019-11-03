from graphviz import Digraph

from state import State
from action import Action


class Model:
    def __init__(self):
        self.model_dict = {}

    # Lazy initialization
    def __getitem__(self, key):
        state, action = key
        return self.model_dict.get(state, {}).get(action)

    def __setitem__(self, key, value):
        state, action = key
        if self.model_dict.get(state) is None:
            self.model_dict[state] = {}
        self.model_dict[state][action] = value

    # Representations
    def __str__(self):
        return self.model_dict.__str__()

    def _get_graph(self):
        graph = Digraph()
        for state, actions in self.model_dict.items():
            for action, next_state in actions.items():
                # State node
                graph.attr('node', shape='doublecircle')
                graph.attr('node', style='', color='', fontcolor='black')
                state_hash = str(hash(state))
                graph.node(state_hash, str(state))

                # Action node
                graph.attr('node', shape='circle')
                graph.attr('node', style='filled', color='black', fontcolor='white')
                action_hash = str(hash(action)) + state_hash
                graph.node(action_hash, str(action))
                graph.edge(state_hash, action_hash)

                # Next state node
                graph.attr('node', shape='doublecircle')
                graph.attr('node', style='', fontcolor='black')
                next_state_hash = str(hash(next_state))
                graph.node(next_state_hash, str(next_state))
                graph.edge(action_hash, next_state_hash)
        return graph

    def _repr_svg_(self):
        return self._get_graph()._repr_svg_()

    def view(self):
        return self._get_graph().view()

if __name__ == '__main__':
    # Model test
    m = Model()

    s1 = State([[-1, 0], [-1, -1]])
    a1 = Action([1, 0])
    s2 = State([[-1, 0], [0, -1]])
    m[s1, a1] = s2

    a2 = Action([0, 0])
    s3 = State([[0, 0], [0, -1]])
    m[s2, a2] = s3

    a3 = Action([1, 1])
    s4 = State([[-1, 0], [0, 0]])
    m[s2, a3] = s4

    print(m)
    m.view()
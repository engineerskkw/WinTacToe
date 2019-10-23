import random
from graphviz import Digraph

from state import State
from action import Action
from auxiliary_utilities import linear_map


class ActionValue:
    MIN_PEN_WIDTH = 1
    MAX_PEN_WIDTH = 4

    def __init__(self):
        self.action_value_dict = {}

    # Lazy initialization
    def __getitem__(self, key):
        if type(key) == tuple and len(key) == 2:
            state, action = key
            if self.action_value_dict.get(state) is None:
                self.action_value_dict[state] = {action: 0}  # Arbitrarily initialization
            elif self.action_value_dict[state].get(action) is None:
                self.action_value_dict[state][action] = 0  # Arbitrarily initialization

            return self.action_value_dict[state][action]

        elif type(key) == State:
            return self.action_value_dict[key]

    def get_state_actions(self, state):
        return self.action_value_dict.get(state)

    def __setitem__(self, key, value):
        state, action = key
        if self.action_value_dict.get(state) is None:
            self.action_value_dict[state] = {}
        self.action_value_dict[state][action] = value

    # Argmax over action as argument, state is constant
    # Settle draw randomly with uniform distribution
    def argmax_a(self, state):
        max_value = float('-inf')
        max_value_actions = []
        for action, value in self.action_value_dict.get(state, {}).items():
            if value > max_value:
                max_value = value
                max_value_actions = [action]
            elif value == max_value:
                max_value_actions.append(action)
        if max_value_actions:
            return random.choice(max_value_actions)
        else:
            return Action([])

    # Representations
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


# Action-value test
av = ActionValue()

s = State([[-1, -1], [-1, 1]])

a1 = Action([0, 0])
a2 = Action([0, 1])
a3 = Action([1, 0])

av[s, a1] = 6
av[s, a2] = 0.8
av[s, a3] = -10

print(av)
av.view()
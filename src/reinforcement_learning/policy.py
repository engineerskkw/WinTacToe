from action import Action
from state import State
import random
from graphviz import Digraph


class Policy:
    def __init__(self, env):
        self.policy_dict = {}
        self.env = env

    # Lazy initialization
    def __getitem__(self, state):
        if self.policy_dict.get(state) is None:
            if self.env.possible_actions:
                self.policy_dict[state] = Action(random.choice(self.env.possible_actions))
            else:
                self.policy_dict[state] = Action([])
        return self.policy_dict[state]

    def __setitem__(self, state, action):
        self.policy_dict[state] = action

    # Representations
    def __str__(self):
        representation = ''
        for key, value in self.policy_dict.items():
            representation += str(key)
            representation += "\n"
            representation += str(value)
            representation += "\n\n"
        return representation

    def __repr__(self):
        return self.__str__()

    def _get_graph(self):
        graph = Digraph()
        for state, action in self.policy_dict.items():
            graph.attr('node', shape='doublecircle')
            state_hash = str(hash(state))
            graph.node(state_hash, str(state))
            graph.attr('node', shape='circle')
            action_hash = str(hash(action))
            graph.node(action_hash, str(action))
            graph.edge(state_hash, action_hash)
        return graph

    def _repr_svg_(self):
        return self._get_graph()._repr_svg_()

    def view(self):
        return self._get_graph().view()


# env = gym.make('tic_tac_toe:tictactoe-v0')
env = None

p = Policy(env)

s1 = State([[-1, 1], [-1, 0]])
a1 = Action([1, 0])
p[s1] = a1

s2 = State([[-1, 0], [1, 0]])
a2 = Action([0, 0])
p[s2] = a2

s3 = State([[0, 1], [1, -1]])
a3 = Action([1, 1])
p[s3] = a3

# print(p)
p.view()
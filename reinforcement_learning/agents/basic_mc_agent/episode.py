# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#


from reinforcement_learning.base.base_action import BaseAction
from reinforcement_learning.base.base_state import BaseState
from numbers import Number
import numpy as np
import uuid
from graphviz import Digraph

from tests.mock.mock_action import MockAction
from tests.mock.mock_state import MockState


class Episode(list):
    def __init__(self, the_list=None):
        if the_list is None:
            the_list = []
        super().__init__(the_list)

    def __str__(self):
        representation = ''
        for element in self:
            if isinstance(element, Number):
                representation += 'Reward:\n'
            elif isinstance(element, BaseState):
                representation += 'State:\n'
            elif isinstance(element, BaseAction):
                representation += 'Action:\n'
            else:
                raise Exception(f"Ivalid episode's element error: {element}")
            representation += str(element)
            representation += '\n\n'
        return representation

    def _get_graph(self):
        graph = Digraph()
        graph.attr(rankdir="LR")
        last_reward_hash = None
        for i in range(int(len(self) / 3)):
            state = self[3 * i]
            action = self[3 * i + 1]
            reward = self[3 * i + 2]

            # SimpleState node
            graph.attr('node', shape='doublecircle')
            state_hash = str(uuid.uuid4())
            graph.node(state_hash, str(state))

            if last_reward_hash:
                graph.edge(last_reward_hash, state_hash)

            # SimpleAction node
            graph.attr('node', shape='circle')
            action_hash = str(uuid.uuid4())
            graph.node(action_hash, str(action))
            graph.edge(state_hash, action_hash)

            # Next state node
            graph.attr('node', shape='diamond')
            reward_hash = str(uuid.uuid4())
            graph.node(reward_hash, str(reward))
            graph.edge(action_hash, reward_hash)
            last_reward_hash = reward_hash
        return graph

    def _repr_svg_(self):
        return self._get_graph()._repr_svg_()

    def view(self):
        return self._get_graph().view()


if __name__ == '__main__':
    # Episode test

    e = Episode()

    s1 = MockState(np.array([[-1, 0], [-1, -1]]))
    a1 = MockAction([1, 0])
    r1 = -3
    e.append(s1)
    e.append(a1)
    e.append(r1)

    s2 = MockState([[-1, 0], [0, -1]])
    a2 = MockAction([0, 0])
    r2 = 4
    e.append(2)
    e.append(a2)
    e.append(r2)

    s3 = MockState([[0, 0], [0, -1]])
    a3 = MockAction([1, 1])
    r3 = -8
    e.append(s3)
    e.append(a3)
    e.append(r2)

    s4 = MockState([[-1, 0], [0, 0]])
    a4 = MockAction([0, 0])
    r4 = 10
    e.append(s4)
    e.append(a4)
    e.append(r4)

    print(e)
    e.view()


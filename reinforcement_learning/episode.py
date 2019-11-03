from graphviz import Digraph
import uuid

from state import State
from action import Action


class Episode(list):
    def __init__(self, the_list=[]):
        super().__init__(the_list)

    # TODO better structure, getters, easy access to chosen objects (states, actions, rewards)

    def __str__(self):
        representation = ''
        for element in self:
            if type(element) == int:
                representation += 'Reward:\n'
                representation += str(element)
                representation += '\n'
            elif (type(element[0]), type(element[1])) == (State, Action):
                representation += 'State:\n'
                representation += str(element[0])
                representation += '\n\n'
                representation += 'Action:\n'
                representation += str(element[1])
                representation += '\n'
            else:
                print("Ivalid episode's element error")
                raise
            representation += '\n'
        return representation

    def _get_graph(self):
        graph = Digraph()
        graph.attr(rankdir="LR")
        last_reward_hash = None
        for i in range(int(len(self) / 2)):
            state = self[2 * i][0]
            action = self[2 * i][1]
            reward = self[2 * i + 1]

            # State node
            graph.attr('node', shape='doublecircle')
            state_hash = str(uuid.uuid4())
            graph.node(state_hash, str(state))

            if last_reward_hash:
                graph.edge(last_reward_hash, state_hash)

            # Action node
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

    s1 = State([[-1, 0], [-1, -1]])
    a1 = Action([1, 0])
    e.append((s1, a1))
    r1 = -3
    e.append(r1)

    s2 = State([[-1, 0], [0, -1]])
    a2 = Action([0, 0])
    e.append((s2, a2))
    r2 = 4
    e.append(r2)

    s3 = State([[0, 0], [0, -1]])
    a3 = Action([1, 1])
    e.append((s3, a3))
    r3 = -8
    e.append(r2)

    s4 = State([[-1, 0], [0, 0]])
    a4 = Action([0, 0])
    e.append((s4, a4))
    r4 = 10
    e.append(r4)

    print(e)
    e.view()
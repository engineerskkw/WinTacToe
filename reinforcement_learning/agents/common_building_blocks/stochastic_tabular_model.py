from graphviz import Digraph
import numpy as np
from reinforcement_learning.agents.auxiliary_utilities import linear_map

from tests.mock.test_mock_action import MockAction
from tests.mock.test_mock_state import MockState

from reinforcement_learning.agents.common_building_blocks.lazy_tabular_action_value import LazyTabularActionValue
from environments.tic_tac_toe.tic_tac_toe_engine_utils import TicTacToeActionSpace


class StochasticTabularModel:
    MIN_PEN_WIDTH = 1
    MAX_PEN_WIDTH = 4

    def __init__(self, agent_action_value):
        self.model_dict = {}
        self.action_value = agent_action_value

    # Lazy initialization
    def __getitem__(self, key):
        state, action = key
        return self.model_dict.get(state, {}).get(action, {})

    def __setitem__(self, key, value):
        # if key value pair existed before the reward is averaged
        state, action = key
        next_state, reward = value
        if self.model_dict.get(state) is None:
            self.model_dict[state] = {}
        if self.model_dict[state].get(action) is None:
            self.model_dict[state][action] = {}
        if self.model_dict[state][action].get(next_state) is None:
            self.model_dict[state][action][next_state] = [0, reward]
        old_count = self.model_dict[state][action][next_state][0]
        old_reward = self.model_dict[state][action][next_state][1]
        new_count = old_count+1
        new_reward = (old_count*old_reward+reward)/new_count
        self.model_dict[state][action][next_state][0] = new_count
        self.model_dict[state][action][next_state][1] = new_reward

    def get_distribution(self, state, action):
        # TODO: refactor, None handling
        distribution = self[state, action]
        denominator = sum(np.array(list(distribution.values()))[:, 0])
        normalized_distribution = {}
        for key in distribution.keys():
            normalized_distribution[key] = [distribution[key][0]/denominator, distribution[key][1]]
        return normalized_distribution

    def get_sample(self, state, action, size=1):
        # TODO: refactor, None handling
        distribution = self.get_distribution(state, action)
        states = list(distribution.keys())
        rewards = np.array(list(distribution.values()))[:, 1]
        probabilities = np.array(list(distribution.values()))[:, 0]
        max_size = len(states)
        indices = np.arange(max_size)
        chosen_indices = np.random.choice(indices, min(size, max_size), False, probabilities)
        return [(states[index], rewards[index]) for index in chosen_indices]

    def get_allowed_actions(self, state):
        # TODO: refactor, None handling, non-specific action space
        return TicTacToeActionSpace(set(self.model_dict.get(state, {}).keys()))

    def plan(self, n):
        step_size = 0.1
        discount = 1

        states = list(self.model_dict.keys())
        if not states:
            return

        for i in range(n):
            prev_state = np.random.choice(states)

            actions = list(self.model_dict[prev_state].keys())
            if not actions:
                return
            prev_action = np.random.choice(actions)

            new_state, reward = self.get_sample(prev_state, prev_action)[0]
            allowed_actions = self.get_allowed_actions(new_state)

            update_target = reward + discount * self.action_value.max(new_state, allowed_actions)

            self.action_value.sample_update(state=prev_state,
                                            action=prev_action,
                                            step_size=step_size,
                                            target=update_target)

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

    m = StochasticTabularModel(LazyTabularActionValue())

    s1 = MockState(np.array([[-1, 0], [-1, -1]]))
    a1 = MockAction(1, 0)
    s2 = MockState(np.array([[-1, 0], [0, -1]]))
    s3 = MockState(np.array([[-1, 0], [-1, 0]]))
    m[s1, a1] = s2, 3
    m[s1, a1] = s3, 2
    m[s1, a1] = s3, 1
    m[s1, a1] = s3, 1
    m[s1, a1] = s3, 3

    a2 = MockAction(0, 0)
    s4 = MockState(np.array([[0, 0], [0, -1]]))
    m[s2, a2] = s4, 1

    a4 = MockAction(1, 1)
    s5 = MockState(np.array([[-1, 0], [0, 0]]))
    s6 = MockState(np.array([[-1, 0], [-1, 0]]))
    s7 = MockState(np.array([[-1, -1], [-1, -1]]))
    m[s2, a4] = s5, 3
    m[s2, a4] = s5, 3
    m[s2, a4] = s5, 3
    m[s2, a4] = s5, 2
    m[s2, a4] = s5, 1
    m[s2, a4] = s5, 1
    m[s2, a4] = s5, 3
    m[s2, a4] = s5, 3
    m[s2, a4] = s6, 2
    m[s2, a4] = s6, 1
    m[s2, a4] = s6, 1
    m[s2, a4] = s6, 3
    m[s2, a4] = s6, 3
    m[s2, a4] = s7, 2
    m[s2, a4] = s7, 1
    m[s2, a4] = s7, 1

    # print(m[s2, a4])
    # print(m.get_distribution(s2, a4))
    # print(m.get_sample(s2, a4))
    print(m.get_allowed_actions(s1))

    # m.view()

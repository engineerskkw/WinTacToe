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

    def __init__(self, agent):
        self.model_dict = dict()
        self.agent = agent
        self.states_frequency = dict()

    # Lazy initialization
    def __getitem__(self, key):
        state, action = key
        return self.model_dict.get(state, dict()).get(action, dict())

    def __setitem__(self, key, value):
        # if key value pair existed before the reward is averaged
        state, action = key
        next_state, reward = value
        if self.model_dict.get(state) is None:
            self.model_dict[state] = dict()
        if self.model_dict[state].get(action) is None:
            self.model_dict[state][action] = dict()
        if self.model_dict[state][action].get(next_state) is None:
            self.model_dict[state][action][next_state] = [0, reward]
        old_count = self.model_dict[state][action][next_state][0]
        old_reward = self.model_dict[state][action][next_state][1]
        new_count = old_count+1
        new_reward = (old_count*old_reward+reward)/new_count
        self.model_dict[state][action][next_state][0] = new_count
        self.model_dict[state][action][next_state][1] = new_reward

    def distribution(self, state, action):
        normalized_dist = dict()
        dist = self[state, action]
        if not dist:
            return normalized_dist
        denominator = sum(np.array(list(dist.values()))[:, 0])
        for key in dist.keys():
            normalized_dist[key] = [dist[key][0]/denominator, dist[key][1]]
        return normalized_dist

    def sample(self, state, action, size=1):
        dist = self.distribution(state, action)
        if not dist:
            return []
        states = list(dist.keys())
        rewards = np.array(list(dist.values()))[:, 1]
        probabilities = np.array(list(dist.values()))[:, 0]
        max_size = len(states)
        indices = np.arange(max_size)
        chosen_indices = np.random.choice(indices, min(size, max_size), False, probabilities)
        return [(states[index], rewards[index]) for index in chosen_indices]

    def random_state(self, frequency=False):
        if frequency:
            states = list(self.states_frequency.keys())
            counts = np.array(list(self.states_frequency.values()))
            the_sum = np.sum(counts)
            probabilities = counts/the_sum
        else:
            states = list(self.model_dict.keys())
            probabilities = np.full(len(states), 1/len(states))

        if states:
            return np.random.choice(a=states, p=probabilities)
        return None

    def actions(self, state):
        return set(self.model_dict.get(state, dict()).keys())

    def random_action(self, state):
        actions = self.actions(state)
        if actions:
            return np.random.choice(actions)
        return None

    def random_state_action(self):
        state = self.random_state()
        action = self.random_action(state)
        return state, action

    def count_state(self, state):
        self.states_frequency[state] = self.states_frequency.get(state, 0) + 1

    def init_state(self):
        return self.random_state(frequency=True)

    def plan(self, n):
        # Preserve epsilon
        saved_epsilon = self.agent.current_epsilon

        self.agent.current_epsilon = 0.0

        # choose initial state
        state = self.init_state()

        for _ in range(n):
            possible_actions = self.actions(state)
            if not possible_actions:
                # Exit episode if there is no transition from 'state' in model
                # print(self.agent.all_episodes_returns[-4:-1])
                # TODO: reward?
                self.agent._exit(state)
                # print(self.agent.all_episodes_returns[-4:-1])
                self.agent.all_episodes_returns.pop()
                # print(self.agent.all_episodes_returns[-4:-1])
                # It's not real episode so its return should be removed
                state = self.init_state()
                continue

            # take action
            allowed_actions = TicTacToeActionSpace(possible_actions)
            action = self.agent._take_action(state, allowed_actions)

            # Simulate environment response
            state, reward = self.sample(state, action)[0]
            self.agent._receive_reward(reward)

        # Restore epsilon
        self.agent.current_epsilon = saved_epsilon

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
    # print(m.distribution(s2, a4))
    # print(m.sample(s2, a4))
    # print(m.allowed_actions(s1))

    # print(m.random_state_action())
    m.plan(3)

    # m.view()

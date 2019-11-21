import sys, os
import numpy as np
from reinforcement_learning.abstract.abstract_agent import Agent
from reinforcement_learning.agents.common.action_value_derived_policy import ActionValueDerivedPolicy
from reinforcement_learning.agents.common.lazy_tabular_action_value import LazyTabularActionValue

# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

class QLearningAgent(Agent):
    def __init__(self, step_size, epsilon, discount):
        self.action_value = LazyTabularActionValue()
        self.policy = ActionValueDerivedPolicy(self.action_value)
        self.step_size = step_size
        self.epsilon = epsilon
        self.discount = discount
        self.performance_measure = []

        self._prev_action = None
        self._prev_state = None
        self._prev_reward = None
        self._current_episode_return = 0

    def take_action(self, state, allowed_actions):
        if self._prev_state:
            self._update(state)

        action = self.policy.epsilon_greedy(state, allowed_actions, self.epsilon)
        self._prev_action = action
        self._prev_state = state

        return action

    def receive_reward(self, reward):
        self._prev_reward = reward
        self._current_episode_return += reward

    def exit(self, terminal_state):
        self._update(terminal_state)
        self.performance_measure.append(self._current_episode_return)
        self.get_performance_graph(10)
        self._reset_prev_info()

    def _update(self, new_state):
        prev_action_value = self.action_value[self._prev_state, self._prev_action]
        error = self.step_size * \
            (self._prev_reward + self.discount * self.action_value.max_over_actions(new_state) - prev_action_value)
        self.action_value[self._prev_state, self._prev_action] = prev_action_value + error

    def _reset_prev_info(self):
        # print(self._current_episode_return)
        self._prev_action = None
        self._prev_state = None
        self._prev_reward = None
        self._current_episode_return = 0

    def get_performance_graph(self, no_of_buckets):
        no_of_episodes = len(self.performance_measure)
        bucket_size = no_of_episodes // no_of_buckets
        bins = np.array(range(0, no_of_episodes, bucket_size))

        bin_numbers = np.digitize(self.performance_measure, bins)
        buckets = [[] for _ in range(no_of_buckets)]

        for bin_no, value in zip(bin_numbers, self.performance_measure):
            buckets[bin_no - 1].append(value)

        print(buckets)

        ret = []

        for bucket in buckets:
            ret.append(np.average(bucket))

        return ret







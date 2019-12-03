# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import numpy as np
import copy

from reinforcement_learning.base.base_agent import BaseAgent
from reinforcement_learning.agents.common.action_value_derived_policy import ActionValueDerivedPolicy
from reinforcement_learning.agents.common.lazy_tabular_action_value import LazyTabularActionValue
from reinforcement_learning.agents.common.agent_utils import bucketify


class QLearningAgent(BaseAgent):
    def __init__(self, step_size, epsilon, discount):
        super().__init__()
        self.step_size = step_size
        self.epsilon = epsilon
        self.discount = discount

        self.action_value = LazyTabularActionValue()
        self.policy = ActionValueDerivedPolicy(self.action_value)

        self._prev_action = None
        self._prev_state = None
        self._prev_reward = None
        self._current_episode_return = 0

    def take_action(self, state, allowed_actions):
        state = copy.deepcopy(state)
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
        self.all_episodes_returns.append(self._current_episode_return)
        self._reset_episode_info()

    def restart(self):
        self._reset_episode_info()

    def _update(self, new_state):
        new_state = copy.deepcopy(new_state)
        prev_state = copy.deepcopy(self._prev_state)
        prev_action = copy.deepcopy(self._prev_action)
        prev_reward = copy.deepcopy(self._prev_reward)
        prev_action_value = self.action_value[prev_state, prev_action]
        error = self.step_size * \
            (prev_reward + self.discount * self.action_value.max(new_state) - prev_action_value)
        self.action_value[prev_state, prev_action] = prev_action_value + error

    def _reset_episode_info(self):
        self._prev_action = None
        self._prev_state = None
        self._prev_reward = None
        self._current_episode_return = 0

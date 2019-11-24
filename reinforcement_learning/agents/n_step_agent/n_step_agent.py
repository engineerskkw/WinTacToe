# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os

REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from reinforcement_learning.base.base_agent import BaseAgent
from reinforcement_learning.agents.common.action_value_derived_policy import ActionValueDerivedPolicy
from reinforcement_learning.agents.common.lazy_tabular_action_value import LazyTabularActionValue

import numpy as np


class NStepAgent(BaseAgent):
    def __init__(self, n, step_size, epsilon, discount):
        self.n = n
        self.step_size = step_size
        self.epsilon = epsilon
        self.discount = discount

        self.action_value = LazyTabularActionValue()
        self.policy = ActionValueDerivedPolicy(self.action_value)

        self._final_time_step = np.inf
        self._current_time_step = 0
        self._state_history = []
        self._action_history = []
        self._reward_history = [None]  # There is no R0

    def take_action(self, state, allowed_actions):
        self._state_history.append(state)
        self._update()

        action = self.policy.epsilon_greedy(state, allowed_actions, self.epsilon)
        self._action_history.append(action)
        self._current_time_step += 1

        return action

    def receive_reward(self, reward):
        self._reward_history.append(reward)

    def exit(self, terminal_state):
        self._state_history.append(terminal_state)
        self._update()
        self._current_time_step += 1
        self._final_time_step = self._current_time_step

    def restart(self):
        self._final_time_step = np.inf
        self._current_time_step = 0
        self._state_history = []
        self._action_history = []
        self._reward_history = [None]  # There is no R0

    def _update(self):
        tau = self._current_time_step - self.n + 1

        if tau < 0:
            return

        updated_state = self._state_history[tau]
        updated_action = self._action_history[tau]
        prev_action_value = self.action_value[updated_action, updated_state]

        estimated_return = self._calculate_estimated_return(tau)
        error = self.step_size * (estimated_return - prev_action_value)

        self.action_value[updated_action, updated_state] = prev_action_value + error

    def _calculate_estimated_return(self, tau):
        high_bound = min(tau + self.n, self._final_time_step)
        elements = [np.power(self.discount, i-tau-1) * self._reward_history[i] for i in range(tau+1, high_bound+1)]
        estimated_return = np.sum(elements)

        if tau + self.n < self._final_time_step:
            last_state = self._state_history[tau + self.n]
            last_action = self._action_history[tau + self.n]
            estimated_return += np.power(self.discount, self.n) * self.action_value[last_state, last_action]

        return estimated_return

import numpy as np

from reinforcement_learning.agents.base_agent import BaseAgent
from reinforcement_learning.agents.common_building_blocks.action_value_derived_policy import ActionValueDerivedPolicy
from reinforcement_learning.agents.common_building_blocks.lazy_tabular_action_value import LazyTabularActionValue
from reinforcement_learning.agents.auxiliary_utilities import safe_return
from reinforcement_learning.agents.common_building_blocks.stochastic_tabular_model import StochasticTabularModel


class DynaNStepAgent(BaseAgent):
    def __init__(self, n, step_size, epsilon_strategy, discount, action_value=LazyTabularActionValue()):
        super().__init__(epsilon_strategy)
        self.n = n
        self.step_size = step_size
        self.discount = discount

        self.action_value = action_value
        self.policy = ActionValueDerivedPolicy(self.action_value)

        self._final_time_step = np.inf
        self._current_time_step = 0
        self._state_history = []
        self._action_history = []
        self._reward_history = [0]  # There is no R0 according to Sutton notation

        self.model = StochasticTabularModel(self.action_value)

    def take_action(self, state, allowed_actions):
        self.model.plan(100)
        self._state_history.append(state)
        action = self.policy.epsilon_greedy(state, allowed_actions, self.current_epsilon)
        self._action_history.append(action)

        self._update(self._current_time_step - self.n)

        return action

    def receive_reward(self, reward):
        self._current_time_step += 1
        self._reward_history.append(reward)

        # Model update
        if len(self._state_history) >= 2:
            state = self._state_history[-2]
            action = self._action_history[-1]
            next_state = self._state_history[-1]
            self.model[state, action] = next_state, reward

    def exit(self, terminal_state):
        self._state_history.append(terminal_state)
        self._final_time_step = self._current_time_step

        for tau in range(self._current_time_step - self.n, self._final_time_step):
            self._update(tau)

        self.all_episodes_returns.append(np.sum(self._reward_history))
        self._reset_episode_info()

    def restart(self):
        self._reset_episode_info()

    def _update(self, tau):
        if tau < 0:
            return

        updated_state = self._state_history[tau]
        updated_action = self._action_history[tau]
        estimated_return = self._calculate_estimated_return(tau)

        self.action_value.sample_update(state=updated_state,
                                        action=updated_action,
                                        step_size=self.step_size,
                                        target=estimated_return)

    def _calculate_estimated_return(self, tau):
        high_bound = min(tau + self.n, self._final_time_step)
        elements = [np.power(self.discount, i - tau - 1) * safe_return(self._reward_history, i)
                    for i in range(tau + 1, high_bound + 1)]
        estimated_return = np.sum(elements)

        if tau + self.n < self._final_time_step:
            last_state = self._state_history[tau + self.n]
            last_action = self._action_history[tau + self.n]
            estimated_return += np.power(self.discount, self.n - 1) * self.action_value[last_state, last_action]

        return estimated_return

    def _reset_episode_info(self):
        self._final_time_step = np.inf
        self._current_time_step = 0
        self._state_history = []
        self._action_history = []
        self._reward_history = [0]  # There is no R0 according to Sutton notation


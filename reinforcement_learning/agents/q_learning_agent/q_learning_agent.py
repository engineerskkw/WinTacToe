from reinforcement_learning.agents.base_agent import BaseAgent
from reinforcement_learning.agents.common_building_blocks.action_value_derived_policy import ActionValueDerivedPolicy
from reinforcement_learning.agents.common_building_blocks.lazy_tabular_action_value import LazyTabularActionValue


class QLearningAgent(BaseAgent):
    def __init__(self, step_size, epsilon_strategy, discount, action_value=LazyTabularActionValue()):
        super().__init__(epsilon_strategy)
        self.step_size = step_size
        self.discount = discount

        self.action_value = action_value
        self.policy = ActionValueDerivedPolicy(self.action_value)

        self._prev_action = None
        self._prev_state = None
        self._prev_reward = None
        self._current_episode_return = 0

    def take_action(self, state, allowed_actions):
        if self._prev_state:
            self._update(state, allowed_actions)

        action = self.policy.epsilon_greedy(state, allowed_actions, self.current_epsilon)
        self._prev_action = action
        self._prev_state = state

        return action

    def receive_reward(self, reward):
        # print(reward)
        self._prev_reward = reward
        self._current_episode_return += reward

    def exit(self, terminal_state):
        self._update(terminal_state, None)
        self.all_episodes_returns.append(self._current_episode_return)
        self._reset_episode_info()

    def restart(self):
        self._reset_episode_info()

    def _update(self, new_state, allowed_actions):
        update_target = self._prev_reward + self.discount * self.action_value.max(new_state, allowed_actions)

        self.action_value.sample_update(state=self._prev_state,
                                        action=self._prev_action,
                                        step_size=self.step_size,
                                        target=update_target)

    def _reset_episode_info(self):
        self._prev_action = None
        self._prev_state = None
        self._prev_reward = None
        self._current_episode_return = 0

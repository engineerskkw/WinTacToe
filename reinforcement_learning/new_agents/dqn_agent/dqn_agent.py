# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from reinforcement_learning.base.base_agent import BaseAgent
from reinforcement_learning.new_agents.common.action_value_derived_policy import ActionValueDerivedPolicy
from reinforcement_learning.new_agents.common.lazy_tabular_action_value import LazyTabularActionValue
from dataclasses import dataclass
from reinforcement_learning.base.base_state import BaseState
from reinforcement_learning.base.base_action import BaseAction
import tensorflow as tf
import numpy as np
from bidict import bidict
from environments.tic_tac_toe.tic_tac_toe_engine_utils import TicTacToeAction
from environments.tic_tac_toe.tic_tac_toe_engine_utils import TicTacToeActionSpace
import random

@dataclass
class MemoryElement:
    state: BaseState
    action: BaseAction
    update_target: float

class DQNAgent(BaseAgent):
    def __init__(self, step_size, epsilon, discount, fit_period, batch_size):
        super().__init__()
        self.step_size = step_size
        self.epsilon = epsilon
        self.discount = discount
        self._current_episode_return = 0
        self.memory = []  # Contains memory elements
        self.model = tf.keras.models.Sequential([
            tf.keras.layers.Input(9),
            tf.keras.layers.Dense(500, activation='relu'),
            tf.keras.layers.Dense(9)
        ])
        self.model.compile(optimizer=tf.keras.optimizers.RMSprop(learning_rate=step_size),
                           loss=tf.keras.losses.mean_squared_error,
                           metric=['accuracy'])

        self.n = 3
        self.action_index_dict = bidict({self.n * i + j:TicTacToeAction(i, j) for i in range(self.n) for j in range(self.n)})

        self.prev_state = None
        self.prev_action = None
        self.tmp_reward = None

        self.iter = 0
        self.fit_period = fit_period
        self.batch_size = batch_size


    def take_action(self, state, allowed_actions):
        self.iter += 1

        if self.prev_state:
            update_target = self.tmp_reward + self.discount * self.__max(state, allowed_actions)
            self.__store(self.prev_state, self.prev_action, update_target)

        action = self.__epsilon_greedy(state, allowed_actions)

        self.prev_state = state
        self.prev_action = action

        return action

    def receive_reward(self, reward):
        self.tmp_reward = reward
        self._current_episode_return += reward

    def exit(self, terminal_state):
        self.iter += 1

        update_target = self.tmp_reward
        self.__store(self.prev_state, self.prev_action, update_target)

        self.all_episodes_returns.append(self._current_episode_return)
        self._reset_episode_info()

    def restart(self):
        self._reset_episode_info()

    def __max(self, state, action_space):
        if action_space is None:
            return 0.

        features = self.__get_features(state)
        all_action_values = self.model(features)

        available_action_indices = [self.action_index_dict.inverse[action] for action in action_space.actions]
        return np.max(all_action_values[available_action_indices])

    def __argmax(self, state, action_space):
        features = self.__get_features(state)
        all_action_values = self.model(features)

        available_action_indices = [self.action_index_dict.inverse[action] for action in action_space.actions]

        max_action_value = self.__max(state, action_space)
        return {self.action_index_dict[available_index] for available_index in available_action_indices
                if np.isclose(all_action_values[available_index], max_action_value)}

    def __get_features(self, state):
        not_normalized_features = state.flatten()
        return not_normalized_features / np.linalg.norm(not_normalized_features)

    def __epsilon_greedy(self, state, action_space):
        if random.random() > self.epsilon:  # Choose action in the epsilon-greedy way
            greedy_actions = self.__argmax(state, action_space)

            if greedy_actions:  # Check if there are any chosen possibilities
                return random.choice(list(greedy_actions))

        return action_space.random_action  # Otherwise (in each case) get a random action

    def __store(self, state, action, update_target):
        self.memory.append(MemoryElement(state, action, update_target))

        if self.iter % self.fit_period == 0 and len(self.memory) >= self.batch_size:
            self.__fit_batch()

    def __fit_batch(self):
        chosen_elements = random.sample(self.memory, self.batch_size)

        batch_X = np.array([self.__get_features(element.state) for element in chosen_elements])
        predictions = self.model(batch_X)

        for i in range(len(chosen_elements)):
            action_index = self.action_index_dict.inverse(chosen_elements[i].action)
            predictions[i][action_index] = chosen_elements[i].update_target

        batch_Y = predictions

        self.model.fit(batch_X, batch_Y, verbose=0, epochs=1)

    def _reset_episode_info(self):
        self._current_episode_return = 0
        self.prev_state = None
        self.prev_action = None
        self.tmp_reward = None


if __name__ == "__main__":
    print('a')
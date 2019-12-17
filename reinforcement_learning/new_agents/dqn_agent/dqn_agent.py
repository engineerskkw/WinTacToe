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

import io
from reinforcement_learning.agents.common.agent_utils import gen_tempfile_path
import random
from collections import deque

import pickle
from copy import deepcopy


@dataclass
class MemoryElement:
    state: BaseState
    action: BaseAction
    update_target: float


class DQNAgent(BaseAgent):
    def __init__(self, step_size, epsilon_strategy, discount, fit_period, batch_size, max_memory_size):
        super().__init__(epsilon_strategy)
        self.step_size = step_size
        self.discount = discount
        self.fit_period = fit_period
        self.batch_size = batch_size
        self.memory = deque([], max_memory_size)

        # Lazy init
        self.model = None
        self.action_index_dict = None

        # Temporary prev state variables
        self.prev_state = None
        self.prev_action = None
        self.tmp_reward = None

        # Iteration state variables
        self.iter = 0
        self._current_episode_return = 0

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

    def __store(self, state, action, update_target):
        self.memory.append(MemoryElement(state, action, update_target))

        if self.iter % self.fit_period == 0 and len(self.memory) >= self.batch_size:
            self.__fit_batch()

    def __fit_batch(self):
        chosen_elements = random.sample(self.memory, self.batch_size)

        batch_X = np.array([self.__get_features(element.state) for element in chosen_elements])
        predictions = self.model(batch_X).numpy()

        for i in range(len(chosen_elements)):
            action_index = self.action_index_dict.inverse[chosen_elements[i].action]
            predictions[i][action_index] = chosen_elements[i].update_target

        batch_Y = predictions

        self.model.train_on_batch(batch_X, batch_Y)

    def __epsilon_greedy(self, state, action_space):
        if random.random() > self.current_epsilon:  # Choose action in the epsilon-greedy way
            greedy_actions = self.__argmax(state, action_space)

            if greedy_actions:  # Check if there are any chosen possibilities
                return random.choice(list(greedy_actions))

        return action_space.random_action  # Otherwise (in each case) get a random action

    def __argmax(self, state, action_space):
        features = self.__get_features(state)

        if self.model is None:
            self.__lazy_init_info(features.size)

        all_action_values = self.model(features.reshape(1, -1)).numpy()[0]
        available_action_indices = [self.action_index_dict.inverse[action] for action in action_space.actions]

        max_action_value = self.__max(state, action_space)

        return {self.action_index_dict[available_index] for available_index in available_action_indices
                if np.isclose(all_action_values[available_index], max_action_value)}

    def __max(self, state, action_space):
        features = self.__get_features(state)

        if self.model is None:
            self.__lazy_init_info(features.size)

        all_action_values = self.model(features.reshape(1, -1)).numpy()[0]
        available_action_indices = [self.action_index_dict.inverse[action] for action in action_space.actions]

        return np.max(all_action_values[available_action_indices])

    def __get_features(self, state):
        not_normalized_features = state.flatten()
        return not_normalized_features / np.linalg.norm(not_normalized_features)

    def _reset_episode_info(self):
        self._current_episode_return = 0
        self.prev_state = None
        self.prev_action = None
        self.tmp_reward = None

    def __lazy_init_info(self, features_size):
        self.model = tf.keras.models.Sequential([
                tf.keras.layers.Input(features_size),
                tf.keras.layers.Dense(50, activation='relu'),
                tf.keras.layers.Dense(50, activation='relu'),
                tf.keras.layers.Dense(50, activation='relu'),
                tf.keras.layers.Dense(features_size)
        ])

        self.model.compile(optimier='rmsprop', loss=tf.losses.mean_squared_error, metrics=['accuracy'])

        # Beta dictionary TODO: delete it or move it elsewhere
        board_size = int(np.sqrt(features_size))
        self.action_index_dict = bidict({board_size*i+j: TicTacToeAction(i, j)
                                         for i in range(board_size)
                                         for j in range(board_size)})

    def __getstate__(self):
        if self.model is not None:
            # Obtain temp file path
            agent_file_path = os.path.join(ABS_PROJECT_ROOT_PATH, "placeholder")
            temp_model_path = gen_tempfile_path(agent_file_path)

            # convert model object to bytes
            self.model.save(temp_model_path)
            with open(temp_model_path, 'rb') as file:
                self.model = file.read()

        # Dumps agent with raw bytes model
        state = self.__dict__.copy()

        # Restoring object-like model
        if self.model is not None:
            self.model = tf.keras.models.load_model(temp_model_path)

            # Removing temp file
            os.remove(temp_model_path)

        return state

    def __setstate__(self, state):
        # Restore instance attributes
        self.__dict__.update(state)

        if self.model is not None:
            # Obtain temp file path
            agent_file_path = os.path.join(ABS_PROJECT_ROOT_PATH, "placeholder")
            temp_model_path = gen_tempfile_path(agent_file_path)

            # Convert model bytes to the model object
            with open(temp_model_path, 'wb') as file:
                file.write(self.model)
            self.model = tf.keras.models.load_model(temp_model_path)

            # Remove temp file
            os.remove(temp_model_path)

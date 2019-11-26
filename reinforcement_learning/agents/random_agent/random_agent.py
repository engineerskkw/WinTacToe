# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from reinforcement_learning.base.base_agent import BaseAgent
from reinforcement_learning.agents.common.agent_utils import bucketify
import random
import numpy as np

class RandomAgent(BaseAgent):
    def __init__(self):
        self._current_episode_rewards = []
        self._all_episode_rewards = []

    def take_action(self, state, allowed_actions):
        return allowed_actions.random_action

    def receive_reward(self, reward):
        self._current_episode_rewards.append(reward)

    def restart(self):
        self._current_episode_rewards = []

    def exit(self, terminal_state):
        self._all_episode_rewards.append(np.sum(self._current_episode_rewards))
        self.restart()

    def get_performance_measure(self, no_of_buckets):
        return bucketify(self._all_episode_rewards, no_of_buckets, np.mean)

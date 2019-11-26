# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import numpy as np

from reinforcement_learning.base.base_agent import BaseAgent
from reinforcement_learning.agents.common.agent_utils import bucketify


class RandomAgent(BaseAgent):
    def __init__(self):
        self._current_episode_return = 0
        self._all_episodes_returns = []

    def take_action(self, state, allowed_actions):
        return allowed_actions.random_action

    def receive_reward(self, reward):
        self._current_episode_return += reward

    def exit(self, terminal_state):
        self._all_episodes_returns.append(self._current_episode_return)
        self._reset_episode_info()

    def restart(self):
        self._reset_episode_info()

    def _reset_episode_info(self):
        self._current_episode_return = 0

    def get_episodes_returns(self):
        return self._all_episodes_returns

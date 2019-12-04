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

# TODO
class ConstantAlfaMCAgent(BaseAgent):
    def __init__(self, step_size, epsilon, discount, action_value=ActionValueDerivedPolicy()):
        super().__init__()

    def take_action(self, state, allowed_actions):
        pass

    def receive_reward(self, reward):
        pass

    def exit(self, terminal_state):
        pass

    def restart(self):
        pass
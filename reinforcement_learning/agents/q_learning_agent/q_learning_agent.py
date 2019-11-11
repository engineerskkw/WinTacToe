import sys, os
from reinforcement_learning.abstract.abstract_agent import Agent
from reinforcement_learning.agents.basic_mc_agent.action_value_derived_policy import ActionValueDerivedPolicy
from reinforcement_learning.agents.basic_mc_agent.lazy_tabular_action_value import LazyTabularActionValue

# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from

class QLearningAgent(Agent):
    def __init__(self, step_size, epsilon):
        self.action_value = LazyTabularActionValue()
        self.policy = ActionValueDerivedPolicy(self.action_value)
        self.step_size = step_size
        self.epsilon = epsilon

    def take_action(self, state, allowed_actions):
        pass

    def receive_reward(self, reward):
        pass

    def exit(self, terminal_state):
        pass

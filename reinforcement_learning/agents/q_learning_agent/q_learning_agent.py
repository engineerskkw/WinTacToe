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

class QLearningAgent(Agent):
    def __init__(self, step_size, epsilon, delta):
        self.action_value = LazyTabularActionValue()
        self.policy = ActionValueDerivedPolicy(self.action_value)
        self.step_size = step_size
        self.epsilon = epsilon
        self.delta = delta

        self.prev_action = None
        self.prev_state = None
        self.prev_reward = None

    def take_action(self, state, allowed_actions):
        if not self.prev_state:
            self.update_rule(self.prev_state, self.prev_action, self.prev_reward, state)

        action = self.policy.epsilon_greedy(state, allowed_actions, self.epsilon)
        self.prev_action = action
        self.prev_state = state

        return action

    def receive_reward(self, reward):
        self.prev_reward = reward

    def update_rule(self, prev_state, prev_action, reward_for_prev_action, current_state):
        prev_action_value = self.action_value[prev_state, prev_action]
        error = self.step_size * \
                (reward_for_prev_action + self.delta * self.action_value.max_over_actions(current_state) - prev_action_value)
        self.action_value[prev_state, prev_action] = prev_action_value + error

    def exit(self, terminal_state):
        self.update_rule(self.prev_state, self.prev_action, self.prev_reward, terminal_state)

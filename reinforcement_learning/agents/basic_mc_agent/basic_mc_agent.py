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
from reinforcement_learning.agents.common.lazy_tabular_action_value import LazyTabularActionValue
from reinforcement_learning.agents.basic_mc_agent.episode import Episode
from reinforcement_learning.agents.common.action_value_derived_policy import ActionValueDerivedPolicy
from reinforcement_learning.agents.basic_mc_agent.mdp import MDP
from reinforcement_learning.agents.basic_mc_agent.returns import Returns
from reinforcement_learning.agents.basic_mc_agent.stochastic_model import StochasticModel


class BasicAgent(BaseAgent):
    def __init__(self):
        # BaseAgent's building blocks
        self.action_value = LazyTabularActionValue()
        self.policy = ActionValueDerivedPolicy(self.action_value)
        self.returns = Returns()
        self.last_episode = Episode()
        self.model = StochasticModel()

        # Auxiliary attributes
        self.last_state = None
        self.last_action = None
        self.last_MDP = None
        self.Gs = []

    def take_action(self, state, action_space):
        state = copy.deepcopy(state) # TODO: understand why this fix works

        # Choose action in epsilon-greedy way
        action = self.policy.epsilon_greedy(state, action_space)

        # Register model transition
        if self.last_state and self.last_action:
            self.model[self.last_state, self.last_action] = state
        self.last_state, self.last_action = state, action

        # Register state and action in the episode
        self.last_episode.append(state)
        self.last_episode.append(action)

        return action

    def receive_reward(self, reward):
        self.last_episode.append(reward)

    def restart(self):
        # Preparation for a new episode
        self.last_episode = Episode()
        self.last_state = None
        self.last_action = None


    def exit(self, terminal_state):
        # Episode ending
        self.last_episode.append(terminal_state)

        # Episode analysing
        G = self.pass_episode()
        self.Gs.append(G)

        # Preparation for a new episode
        self.last_episode = Episode()
        self.last_state = None
        self.last_action = None

    # RL Monte Carlo algorithm
    def pass_episode(self):
        episode = self.last_episode
        gamma = 0.9  # Discount factor
        G = 0.0  # Episode's accumulative discounted total reward/return
        steps_no = len(episode) // 3
        for t in reversed(range(steps_no)):
            # Step, action, reward
            S, A, R = episode[3 * t], episode[3 * t + 1], episode[3 * t + 2]

            G = gamma * G + R  # Calculate discounted return

            # Update rule according to the Monte Carlo first-visit approach
            first_visit = True
            for i in reversed(range(t)):
                temp_S = episode[i]
                temp_A = episode[i+1]
                if (S, A) == (temp_S, temp_A):
                    first_visit = False
                    break

            if first_visit:
                # Policy evaluation
                self.returns[S, A].append(G)
                self.action_value[S, A] = np.mean(self.returns[S, A])  # Improve policy of both agents
                # Greedy policy improvement in the background (as a consequence of action_value change)
        return G

    def __add__(self, other):
        if not isinstance(other, BasicAgent):
            raise Exception

        new_agent = BasicAgent()
        self._iterate_return(self, other, new_agent.returns)
        self._iterate_return(other, self, new_agent.returns)

        for state, actions in new_agent.returns.returns_dict.items():
            for action, returns in actions.items():
                self_visits_no = len(self.returns[state, action])
                other_visits_no = len(other.returns[state, action])
                self_part = self.action_value[state, action] * self_visits_no
                other_part = other.action_value[state, action] * other_visits_no
                new_value = (self_part + other_part) / (self_visits_no + other_visits_no)
                new_agent.action_value[state, action] = new_value

        new_agent.policy = ActionValueDerivedPolicy(new_agent.action_value)

        self.last_episode = Episode()
        self.model = StochasticModel()  # TODO: model merging

        # Auxiliary attributes
        self.last_state = None
        self.last_action = None
        self.last_MDP = None
        self.Gs = []
        return new_agent

    def _iterate_return(self, iteration_agent, check_agent, output_returns):
        for state, actions in iteration_agent.returns.returns_dict.items():
            for action, returns in actions.items():
                output_returns[state, action] = list(returns + check_agent.returns[state, action])

    # Auxiliary methods
    def get_mdp(self):
        self.last_MDP = MDP(self.model, self.action_value)
        return self.last_MDP

    def reset_action_value(self):
        self.action_value = LazyTabularActionValue()

    def reset_returns(self):
        self.returns = Returns()

    def reset_episode(self):
        self.last_episode = Episode()
        self.last_state = None
        self.last_action = None

    def reset_model(self):
        self.model = StochasticModel()
        self.last_state = None
        self.last_action = None

    def reset_agent(self):
        self.reset_action_value()
        self.reset_returns()
        self.reset_episode()
        self.reset_model()

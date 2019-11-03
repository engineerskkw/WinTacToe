#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from reinforcement_learning.agents.abstract_agent import Agent
from reinforcement_learning.action import Action
from reinforcement_learning.action_value import ActionValue
from reinforcement_learning.episode import Episode
from reinforcement_learning.epsilon_greedy_policy import EpsilonGreedyPolicy
from reinforcement_learning.mdp import MDP
from reinforcement_learning.model import Model
from reinforcement_learning.policy import Policy
from reinforcement_learning.returns import Returns
from reinforcement_learning.state import State
from reinforcement_learning.stochastic_model import StochasticModel

import random
import numpy as np
from itertools import cycle


class BasicAgent(Agent):
    def __init__(self):
        # Agent's building blocks
        self.action_value = ActionValue()
        self.policy = EpsilonGreedyPolicy(self.action_value, None, 0.3)
        self.returns = Returns()
        self.last_episode = Episode()
        self.model = StochasticModel()

        # Auxiliary atributes
        self.last_state = None
        self.last_action = None
        self.last_MDP = None
        self.Gs = []

    # TODO: Random step

    # Interface implementation
    def step(self, state, allowed_actions):
        # TODO: self.policy.epsilon = epsilon

        # Choose action in epsilon-greedy way
        state = State(state)
        self.policy.allowed_actions = allowed_actions
        action = self.policy[state]
        if not tuple(action.array) in allowed_actions:
            action = Action(random.choice(allowed_actions))

        # Register model transition
        if self.last_state and self.last_action:
            self.model[self.last_state, self.last_action] = state
        self.last_state, self.last_action = state, action

        # Register state and action
        self.last_episode.append((state, action))

        return tuple(action.array)

    def reward(self, reward):
        self.last_episode.append(reward)

    def exit(self, termination_state):
        termination_state = State(termination_state)
        self.last_episode.append((termination_state, Action([]))) # TODO: do something elese than empty action
        self.last_episode.append(0) # TODO: do something else than just zero reward appending

        G = self.pass_episode()
        self.Gs.append(G)
        print(f"self Gs: {self.Gs}")

    # RL Monte Carlo algorithm
    def pass_episode(self):
        episode = self.last_episode
        print(f"EPISODE: {episode}")
        gamma = 0.9  # Discount factor
        G = 0  # Episode's accumulative discounted total reward/return
        steps_no = len(episode) // 2
        for t in reversed(range(steps_no)):
            S, A = episode[2 * t]  # This step's (state, action) pair
            R = episode[2 * t + 1]  # This step's reward

            G = gamma * G + R  # Calculate discounted return

            # Update rule according to the Monte Carlo first-step approach
            if not (S, A) in episode[0:2 * t]:
                # Policy evaluation
                self.returns[S, A].append(G)
                self.action_value[S, A] = np.mean(self.returns[S, A])  # Improve policy of both agents
                # Greedy policy improvement in the background (as a consequence of action_value change)
        #                 agent.policy[S] = agent.action_value.argmax_a(S)
        return G

    # Auxiliary methods
    def get_mdp(self):
        self.last_MDP = MDP(self.model, self.action_value, self.policy)
        return self.last_MDP

    def reset_policy(self):
        self.policy = Policy(self.env)

    def reset_action_value(self):
        self.action_value = ActionValue()

    def reset_returns(self):
        self.returns = Returns()

    def reset_episode(self):
        self.last_episode = Episode()
        self.last_state = None
        self.last_action = None

    def reset_model(self):
        self.model = Model()
        self.last_state = None
        self.last_action = None

    def reset_agent(self):
        self.reset_policy()
        self.reset_action_value()
        self.reset_returns()
        self.reset_episode()
        self.reset_model()

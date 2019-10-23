import random

from action import Action
from action_value import ActionValue
from episode import Episode
from epsilon_greedy_policy import EpsilonGreedyPolicy
from mdp import MDP
from model import Model
from policy import Policy
from returns import Returns
from state import State
from stochastic_model import StochasticModel

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
        if not action.array in allowed_actions:
            action = random.choice(allowed_actions)
        action = Action(action)

        # Register model transition
        if self.last_state and self.last_action:
            self.model[self.last_state, self.last_action] = state
        self.last_state, self.last_action = state, action

        # Register state and action
        self.last_episode.append((state, action))

        return action.array

    def reward(self, reward):
        self.last_episode.append(reward)

    def exit(self, termination_state):
        termination_state = State(termination_state)
        self.last_episode.append(termination_state)
        G = self.pass_episode()
        self.Gs.append(G)

    # RL Monte Carlo algorithm
    def pass_episode(self):
        episode = self.last_episode
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

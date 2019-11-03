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


class Agent:
    def __init__(self, environment, player):
        self.player = player
        self.env = environment

        self.action_value = ActionValue()
        self.policy = EpsilonGreedyPolicy(self.env, self.action_value, 0.3)
        self.returns = Returns()
        self.last_episode = Episode()
        self.model = StochasticModel()
        self.last_state = None
        self.last_action = None
        self.last_MDP = None

    def step(self, state, epsilon):

        # Choose action in epsilon-greedy way
        self.policy.epsilon = epsilon
        action = self.policy[state]
        self.last_episode.append((state, action))  # Register state and action
        raw_state, reward, done, _ = self.env.step(action.array, self.player)  # Take action

        # Register model transition
        if self.last_state and self.last_action:
            self.model[self.last_state, self.last_action] = state
        self.last_state, self.last_action = state, action

        self.last_episode.append(reward)  # Register reward
        return State(raw_state), done

    def random_step(self, state):
        action = Action(random.choice(self.env.possible_actions))  # Choose action
        self.last_episode.append((state, action))  # Register state and action
        raw_state, reward, done, _ = self.env.step(action.array, self.player)  # Take action

        # Register model transition
        if self.last_state and self.last_action:
            self.model[self.last_state, self.last_action] = state
        self.last_state, self.last_action = state, action

        self.last_episode.append(reward)  # Register reward
        return State(raw_state), done

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

# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import random
from scipy.special import softmax

from reinforcement_learning.base.base_policy import BasePolicy


class ActionValueDerivedPolicy(BasePolicy):
    def __init__(self, action_value):
        self.action_value = action_value

    def __getitem__(self, key: tuple):
        assert len(key) == 2, f"Invalid key: {key}, should be tuple(BaseState, BaseAction)..."

        state, action = key
        self.action_value[state, action]  # Initialize state action value by defaultdict
        expected_returns = self.action_value.action_returns(state)

        # Softmax on action returns gives the probability that they will be chosen
        softmax_returns = dict(zip(expected_returns.keys(), softmax(list(expected_returns.values()))))

        return softmax_returns[action]

    def epsilon_greedy(self, state, action_space, epsilon=0.1):
        if random.random() > epsilon:  # Choose action in the epsilon-greedy way
            greedy_actions = list(self.action_value.argmax(state))

            if greedy_actions:  # Check if there are any chosen possibilities
                action = random.choice(greedy_actions)  # Random drawback settlement

                if action in action_space:  # Check action validity
                    return action

        return action_space.random_action  # Otherwise (in each case) get a random action

    def __str__(self):
        return self.action_value.__str__()

    def __repr__(self):
        return self.__str__()

    def _repr_svg_(self):
        return self.action_value._repr_svg_()

    def view(self):
        return self.action_value.view()
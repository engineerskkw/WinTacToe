#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import random

from reinforcement_learning.agents.basic_mc_agent.state import State
from reinforcement_learning.agents.basic_mc_agent.action import Action
from reinforcement_learning.abstract.abstract_policy import AbstractPolicy
from reinforcement_learning.agents.basic_mc_agent.lazy_tabular_action_value import LazyTabularActionValue


class ActionValueDerivedPolicy(AbstractPolicy):
    def __init__(self, action_value, action_space):
        super().__init__()
        self.action_space = action_space
        self.action_value = action_value

    def __getitem__(self, key):
        # Expected return of the given action in the given state
        action_return = self.action_value[key]
        # Sum of expected returns of all possible actions in the given state
        sum_of_returns = sum(self.action_value.returns_of_actions(key[0]).values())
        return action_return/sum_of_returns

    def epsilon_greedy(self, state, action_space, epsilon=0.1):
        if random.random() >= epsilon: # Choose action in the epsilon-greedy way
            greedy_actions = self.action_value.argmax_over_actions(state)
            if greedy_actions:  # Check if there are any chosen possibilities
                action = random.choice(greedy_actions)  # Random drawback settlement
                if action in action_space:  # Check action validity
                    return action
        return action_space.random_action # Otherwise (in each case) get a random action

    # Representations
    def __str__(self):
        return self.action_value.__str__()

    def __repr__(self):
        return self.__str__()

    def _repr_svg_(self):
        return self.action_value._repr_svg_()

    def view(self):
        return self.action_value.view()

if __name__ == '__main__':
    av = LazyTabularActionValue()

    s = State([[-1, -1], [-1, 1]])

    a1 = Action([0, 0])
    a2 = Action([0, 1])
    a3 = Action([1, 0])

    av[s, a1] = 6
    av[s, a2] = 2.9
    av[s, a3] = -10

    egp = ActionValueDerivedPolicy(None, av, 0.3)

    print(egp)
    egp.view()
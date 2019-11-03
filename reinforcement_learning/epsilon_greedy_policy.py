#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import random

from reinforcement_learning.state import State
from reinforcement_learning.action import Action
from reinforcement_learning.action_value import ActionValue


class EpsilonGreedyPolicy:
    def __init__(self, action_value, allowed_actions, epsilon):
        self.allowed_actions = allowed_actions
        self.action_value = action_value
        self.epsilon = epsilon

    # Action-value and epsilon based action choosing
    def __getitem__(self, state):
        if random.random() >= self.epsilon:
            action = self.action_value.argmax_a(state)
            if action != Action([]):
                return action
        if self.allowed_actions:
            return Action(random.choice(self.allowed_actions))
        return Action([])

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
    av = ActionValue()

    s = State([[-1, -1], [-1, 1]])

    a1 = Action([0, 0])
    a2 = Action([0, 1])
    a3 = Action([1, 0])

    av[s, a1] = 6
    av[s, a2] = 2.9
    av[s, a3] = -10

    egp = EpsilonGreedyPolicy(None, av, 0.3)

    print(egp)
    egp.view()
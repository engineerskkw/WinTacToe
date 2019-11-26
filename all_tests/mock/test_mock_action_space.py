#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from reinforcement_learning.base.base_action_space import BaseActionSpace
from random import choice, randrange, sample


class MockActionSpace(BaseActionSpace):
    """
    actions: Set
    """
    def __init__(self, actions: set):
        self.actions = actions

    def __contains__(self, action):
        return action in self.actions

    def __len__(self):
        return len(self.actions)

    @property
    def random_action(self):
        return choice(list(self.actions))

    @property
    def random_actions(self, no_of_actions=None):
        no_of_actions = randrange(1, len(self.actions)) if not no_of_actions else no_of_actions
        return sample(list(self.actions), no_of_actions)

    def __eq__(self, other):
        return self.actions == other.actions

    def __str__(self):
        return str(self.actions)
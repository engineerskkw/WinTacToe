from reinforcement_learning.agents.common_building_blocks.base.base_action_space import BaseActionSpace
from random import choice, randrange, sample
from typing import Set

from dataclasses import dataclass

@dataclass(frozen=True)
class MockActionSpace(BaseActionSpace):
    actions: Set

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
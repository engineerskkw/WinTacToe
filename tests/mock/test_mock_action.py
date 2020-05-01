from reinforcement_learning.agents.common_building_blocks.base.base_action import BaseAction

from dataclasses import dataclass


@dataclass(frozen=True)
class MockAction(BaseAction):
    atr1: int
    atr2: int

    def flatten(self):
        return [self.atr1, self.atr2]

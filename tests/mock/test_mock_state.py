import numpy as np
from reinforcement_learning.agents.common_building_blocks.base.base_state import BaseState
from dataclasses import dataclass

@dataclass(frozen=True)
class MockState(BaseState):
    array: np.ndarray

    def __post_init__(self):
        self.array.flags.writeable = False

    def __hash__(self):
        return hash(self.array.data.tobytes())

    def __eq__(self, other):
        if isinstance(other, MockState):
            return hash(self) == hash(other)
        return False

    def flatten(self):
        return self.array.flatten()

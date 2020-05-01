import numpy as np
from reinforcement_learning.base.base_action import BaseAction

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class MockAction(BaseAction):
    atr1: int
    atr2: int

    def flatten(self):
        return [self.atr1, self.atr2]

#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#


import numpy as np
from reinforcement_learning.base.base_state import BaseState
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

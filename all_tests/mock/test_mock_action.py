#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

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

#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import numpy as np


class Action:
    def __init__(self, array):
        self.array = np.array(array)

    def __hash__(self):
        return hash(self.array.tostring())

    def __eq__(self, other):
        if not isinstance(other, Action):
            return NotImplemented
        return hash(self) == hash(other)

    def __str__(self):
        return str(self.array)

    def __repr__(self):
        return self.__str__()
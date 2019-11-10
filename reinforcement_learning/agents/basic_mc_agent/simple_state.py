#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#


import numpy as np
from reinforcement_learning.abstract.abstract_state import AbstractState

class SimpleState(AbstractState):
    def __init__(self, array):
        self.array = np.array(array)

    def __hash__(self):
        return hash(self.array.tostring())

    def __str__(self):
        representation = ''
        height, width = self.array.shape

        for h in range(height):
            for w in range(width):
                if self.array[h, w] == -1:
                    representation += '#'
                elif self.array[h, w] == 0:
                    representation += 'O'
                elif self.array[h, w] == 1:
                    representation += 'X'
                else:
                    print("Invalid mark code")
                    raise
            if h < height - 1:
                representation += '\n'
        return representation

    def __repr__(self):
        return self.__str__()
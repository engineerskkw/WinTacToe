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
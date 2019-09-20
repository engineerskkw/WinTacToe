import numpy as np


class State:
    def __init__(self, array):
        self.array = np.array(array)

    def __hash__(self):
        return hash(self.array.tostring())

    def __eq__(self, other):
        if not isinstance(other, State):
            return NotImplemented
        return hash(self) == hash(other)

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
# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from abc import ABC, abstractmethod
import numpy as np


class AbstractState(ABC):
    """
    Class implements reinforcement learning state of the environment

    It contains numpy array which is sufficiently general and convenient
    data structure that is able to represent wide variety of environmental
    states. Moreover it's easy to use with neural networks.

    Parameters
    ----------
    array : numpy array or python list
        State data.

    Methods
    -------
    __hash__()
        Get a unique hash value of the state.
    __eq__()
        Compare state with another. It's key feature of the state used
        by many reinforcement learning components.
    __str__()
        Get a string representation.
    """

    @abstractmethod
    def __hash__(self):
        """
        Get a unique hash value of the state.

        Returns
        -------
        Int
            Hash value.
        """
        # return hash(self.array.tostring())
        pass

    # TODO: remove after making sure you can do it
    def __eq__(self, other):
        """
        Compare the state with another.

        Returns
        -------
        Bool
            True if states are equal, false otherwise.
        """
        if not isinstance(other, AbstractState):
            return False
        return hash(self) == hash(other)

    @abstractmethod
    def __str__(self):
        """
        Get a string representation.

        Returns
        -------
        String
            String representation.
        """
        pass

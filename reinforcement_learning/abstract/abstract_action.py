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


class AbstractAction(ABC):
    """
    Class implements action taken by reinforcement learning agent.

    It contains numpy array which is sufficiently general and convenient
    data structure that is able to represent wide variety of agent's actions.
    Moreover it's easy to use with neural networks.

    Parameters
    ----------
    value : numpy array or python list
        State data.

    Methods
    -------
    __hash__()
        Get a unique hash value of the action.
    __eq__()
        Compare the action with another. It's key feature of the action used
        by many reinforcement learning components.
    __str__()
        Get a string representation.
    """

    def __init__(self, value):
        self.value = np.array(value)

    def __hash__(self):
        """
        Get a unique hash value of the action.

        Returns
        -------
        Int
            Hash value.
        """
        return hash(self.value.tostring())

    # TODO: remove after making sure you can do it
    def __eq__(self, other):
        """
        Compare the action with another.

        Returns
        -------
        Bool
            True if actions are equal, false otherwise.
        """
        if not isinstance(other, AbstractAction):
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

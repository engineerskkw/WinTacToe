# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from abc import ABC, abstractmethod


class BaseAction(ABC):
    """
    Class implements action taken by reinforcement learning agent.

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

    @abstractmethod
    def __hash__(self):
        """
        Get a unique hash value of the action.

        Returns
        -------
        Int
            Hash value.
        """
        pass

    # TODO: remove after making sure you can do it
    def __eq__(self, other):
        """
        Compare the action with another.

        Returns
        -------
        Bool
            True if actions are equal, false otherwise.
        """
        if not isinstance(other, BaseAction):
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

    @abstractmethod
    def flatten(self):
        """
        Get vectorized representation.

        Returns
        -------
        np.array[np.float64]
            Numpy array of floats
        """

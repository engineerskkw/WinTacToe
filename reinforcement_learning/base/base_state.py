# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class BaseState(ABC):
    """
    Class implements reinforcement learning state of the environment

    Methods
    -------
    __hash__()
        Get a unique hash value of the state.
    __eq__()
        Compare state with another. It's key feature of the state used
        by many reinforcement learning components.
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
        pass

    def __eq__(self, other):
        """
        Compare the state with another.

        Returns
        -------
        Bool
            True if states are equal, false otherwise.
        """
        if not isinstance(other, BaseState):
            return False
        return hash(self) == hash(other)

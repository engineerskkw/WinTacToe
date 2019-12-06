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
class BaseActionSpace(ABC):
    """
    Action space is an object that can be used for determining if given action
    is allowed to receive by the environment. Moreover it provides random action (which also is allowed).

    Methods
    -------
    __contains__(action)
        Check if action is allowed by the environment.
    random_action()
        Get random (but allowed by the environment) action.
    """
    @abstractmethod
    def __contains__(self, action):
        """
        Check if given action is allowed by the environment.

        Parameters
        ----------
        action : BaseAction
            Action of the reinforcement learning agent.

        Returns
        -------
        Bool
            True if action is allowed, false otherwise.
        """
        pass

    @abstractmethod
    def random_action(self):
        """
        Get random (but allowed by the environment) action.

        Returns
        -------
        BaseAction
            Random action allowed by the environment.
        """
        pass

    @abstractmethod
    def random_actions(self, no_of_actions):
        pass


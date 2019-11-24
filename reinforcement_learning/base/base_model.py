# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from abc import ABC, abstractmethod


class BaseModel(ABC):
    """
    Class implements reinforcement model.

    Model mimics the behavior of the environment, or more generally,
    allows inferences to be made about how the environment will behave.
    Given a state and action, the model might predict the resultant next
    state and next reward. Models are used for planning.

    Methods
    -------
    __getitem__(key)
        Returns next state and next reward, given state and action.
    __setitem__(key, value)
        Set the next state and the reward.
    __str__()
        Get a string representation.
    """

    def __init__(self):
        pass

    @abstractmethod
    def __getitem__(self, key):
        """
        Returns next state and next reward, given state and action.

        Parameters
        ----------
        key : Tuple(BaseState, BaseAction)
            Pair of the state and the action.

        Returns
        -------
        Tuple(BaseState, Int)
            Pair of the next state and the reward
        """
        pass

    @abstractmethod
    def __setitem__(self, key, value):
        """
        Set the next state and the reward for given state and action.

        Parameters
        ----------
        key : Tuple(BaseState, BaseAction)
            Pair of the state and the action.
        value : Tuple(BaseState, Double)
            Pair of the next state and the reward
        """
        pass

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

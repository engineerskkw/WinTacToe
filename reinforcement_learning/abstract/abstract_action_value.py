# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from abc import ABC, abstractmethod


class AbstractActionValue(ABC):
    """
    Class implements action value function of the reinforcement learning agent.

    It contains mapping (state, action) -> expected return.

    Methods
    -------
    __getitem__(key)
        Get an expected return for the given (state, action) pair.
    __setitem__()
        Set an expected return for the given (state, action) pair.
    max_over_actions(state)
        Get a maximum expected return for the given state and for all actions
        that are possible to choose in this state.
    argmax_over_actions(state)
        Get a set of actions for which the expected return is maximum in the given state.
    __str__()
        Get a string representation.
    """

    def __init__(self):
        pass

    @abstractmethod
    def __getitem__(self, key):
        """
        Get an expected return for the given (state, action) pair.

        Parameters
        ----------
        key : Tuple(AbstractState, AbstractAction)
            Pair of the state and action.

        Returns
        -------
        Double
            Expected return.
        """
        pass

    @abstractmethod
    def __setitem__(self, key, value):
        """
        Set an expected return for the given (state, action) pair.

        Parameters
        ----------
        key : Tuple(AbstractState, AbstractAction)
            Pair of the state and action.
        """
        pass

    @abstractmethod
    def max_over_actions(self, state):
        """
        Get a maximum expected return for the given state and for
        all actions that are possible to choose in this state.

        Parameters
        ----------
        state : AbstractState
            State of the environment.

        Returns
        -------
        Double
            Maximum expected return.
        """
        pass

    @abstractmethod
    def argmax_over_actions(self, state):
        """
        Get a set of actions for which the expected return
        is maximum in the given state.

        Parameters
        ----------
        state : AbstractState
            State of the environment.

        Returns
        -------
        Set[AbstractAction]
            Set of actions that maximize expected return.
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
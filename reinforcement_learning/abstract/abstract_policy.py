# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from abc import ABC, abstractmethod


class Policy(ABC):
    """Class implements reinforcement learning policy.

    A policy defines the learning agent’s way of behaving at a given time.
    Roughly speaking, a policy is a mapping from perceived states of the
    environment to actions to be taken when in those states. Formally,
    a policy is a mapping from states to probabilities of selecting each
    possible action.

    Methods
    -------
    __getitem__(key)
        Returns probability of taking the given action in the given state.
    epsilon_greedy(state, epsilon=None)
        Return epsilon-greedily chosen action.
    __str__()
        Get a string representation.
    """
    def __init__(self):
        pass

    @abstractmethod
    def __getitem__(self, key):
        """
        Get a probability of taking given action in given state.

        Parameters
        ----------
        key : Tuple(AbstractState, AbstractAction)
            Pair of the state and action.

        Returns
        -------
        Double
            Probability of taking given action in given state.
        """
        pass

    @abstractmethod
    def epsilon_greedy(self, state, epsilon=None):
        """
        Get an epsilon-greedily chosen action in the given state.

        Parameters
        ----------
        state : AbstractState
            State of the environment.
        epsilon : Double
            Epsilon - value used when determining the selection of a greedy
            or random action.

        Returns
        -------
        Double
            Probability of taking given action in given state.
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

# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from abc import ABC, abstractmethod


class AbstractReturns(ABC):
    """
    Class implements Returns data structure used in Reinforcement Learning Monte Carlo algorithms.

    It contains mapping (state, action) -> list[return].


    Methods
    -------
    __getitem__()
        Get a list of expected returns for the given (state, action) pair.
    __str__()
        Get a string representation.
    """

    @abstractmethod
    def __getitem__(self, key):
        """
        Get a list of expected returns for the given (state, action) pair.

        Parameters
        ----------
        key : Tuple(AbstractState, AbstractAction)
            Pair of the state and action.

        Returns
        -------
        list[Float]
            List of expected returns.
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

from abc import ABC, abstractmethod


class BaseReturns(ABC):
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
        key : Tuple(BaseState, BaseAction)
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

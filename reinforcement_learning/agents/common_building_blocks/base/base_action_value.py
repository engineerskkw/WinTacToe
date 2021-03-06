from abc import ABC, abstractmethod


class BaseActionValue(ABC):
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

    @abstractmethod
    def __getitem__(self, key):
        """
        Get an expected return for the given (state, action) pair.

        Parameters
        ----------
        key : Tuple(BaseState, BaseAction)
            Pair of the state and action.

        Returns
        -------
        Float
            Expected return.
        """
        pass

    # TODO: remove below method completely
    def __setitem__(self, key, value):
        """
        Set an expected return for the given (state, action) pair.

        Parameters
        ----------
        key : Tuple(BaseState, BaseAction)
            Pair of the state and action.
        value : Double
            Expected return.
        """
        pass

    # TODO: make below method abstract after removing above method
    def sample_update(self, **kwargs):
        """
        Given appropriate parameters, apply update to the action value

        Parameters
        ----------
        **kwargs : Arbitrary keyword arguments
        """
        pass

    @abstractmethod
    def max(self, state, action_space):
        """
        Get a maximum expected return for the given state and for
        all actions that are possible to choose in this state.

        Parameters
        ----------
        state : BaseState
            State of the environment.
        action_space : BaseActionSpace
            Action space for given state

        Returns
        -------
        Float
            Maximum expected return.
        """
        pass

    @abstractmethod
    def argmax(self, state, action_space):
        """
        Get a set of actions for which the expected return
        is maximum in the given state.

        Parameters
        ----------
        state : BaseState
            State of the environment.
        action_space : BaseActionSpace
            Action space for given state

        Returns
        -------
        Set[BaseAction]
            Set of actions that maximize expected return.
        """
        pass

    @abstractmethod
    def action_returns(self, state, action_space):
        """
        Get expected returns estimates of all possible actions in the given state.

        Parameters
        ----------
        state : BaseState
            State of the environment.
        action_space : BaseActionSpace
            Action space for given state

        Returns
        -------
        Dict[BaseAction:float]
            Dictionary of actions as keys and expected returns estimates as values.
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

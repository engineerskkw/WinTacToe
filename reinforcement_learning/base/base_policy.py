from abc import ABC, abstractmethod


class BasePolicy(ABC):
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

    @abstractmethod
    def __getitem__(self, key):
        """
        Get a probability of taking given action in given state.

        Parameters
        ----------
        key : Tuple(BaseState, BaseAction)
            Pair of the state and action.

        Returns
        -------
        Float
            Probability of taking given action in given state.
        """
        pass

    @abstractmethod
    def epsilon_greedy(self, state, action_space, epsilon):
        """
        Get an epsilon-greedily chosen action in the given state.

        Parameters
        ----------
        state : BaseState
            State of the environment.
        action_space : BaseActionSpace
            Space of all possible actions the in given state
        epsilon : Double
            Epsilon - value used when determining the selection of a greedy
            or random action.

        Returns
        -------
        BaseAction
            Greedy action
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

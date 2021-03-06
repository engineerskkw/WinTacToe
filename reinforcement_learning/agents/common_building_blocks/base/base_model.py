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

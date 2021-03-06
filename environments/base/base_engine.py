from abc import ABC, abstractmethod


class BaseEngine(ABC):
    @abstractmethod
    def current_player(self):
        """
        Get a current player.

        Returns
        -------
            BasePlayer
        """
        pass

    @abstractmethod
    def players(self):
        """
        Get a list of currently participating players.

        Returns
        -------
            list[BasePlayer]
        """
        pass

    @abstractmethod
    def current_state(self):
        """
        Get a current state of the environment.

        Returns
        -------
            BaseState
        """
        pass

    @abstractmethod
    def winnings(self):
        """
        Get winnings.

        Returns
        -------
            list[BaseWinning]
        """
        pass

    @abstractmethod
    def allowed_actions(self):
        """
        Get current allowed actions.

        Returns
        -------
            BaseActionSpace
        """
        pass

    @abstractmethod
    def rewards(self):
        """
        Get a rewards hash per player.

        Returns
        -------
            dict(BasePlayer: float)
        """

    @abstractmethod
    def ended(self):
        """
        Check if the episode or game has ended.

        Returns
        -------
            bool
        """
        pass

    @abstractmethod
    def make_move(self, action):
        """
        Take action.

        Parameters
        ----------
            action: BaseAction

        """
        pass

    def randomize(self, seed):
        """
        Randomize an initial state of the environment.

        Parameters
        ----------
        seed: int
            seed for randomization

        """
        pass

    def reset(self):
        """Reset the environment."""
        pass

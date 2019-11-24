import sys, os
from abc import ABC, abstractmethod

# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
REL_PROJECT_ROOT_PATH = "./../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#


class BaseEngine(ABC):
    @abstractmethod
    def current_player(self):
        """
        Get a current player.

        Returns
        -------
            AbstractPlayer(not implemented)
        """
        pass

    @abstractmethod
    def players(self):
        """
        Get list of currently participating players.

        Returns
        -------
            list[AbstractPlayer(not implemented)
        """
        pass

    @abstractmethod
    def current_state(self):
        """
        Get current state of the environment.

        Returns
        -------
            AbstractState
        """
        pass

    @abstractmethod
    def winnings(self):
        """
        Get winnings.

        Returns
        -------
            list[AbstractWinning (not implemented)]
        """
        pass

    @abstractmethod
    def allowed_actions(self):
        """
        Get current allowed actions

        Returns
        -------
            AbstractActionSpace
        """
        pass

    @abstractmethod
    def rewards(self):
        """
        Get rewards hash per player.

        Returns
        -------
            Hash(AbstractPlayer (not implemented): float)
        """

    @abstractmethod
    def ended(self):
        """
        Check if the episode or game has ended

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
        action: AbstractAction

        """
        pass

    def randomize(self, seed):
        """
        Randomizes initial state of the environment

        Parameters
        ----------
        seed: int
            seed for randomization

        """
        pass

    def reset(self):
        """Resets the environment"""
        pass

#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#


from abc import ABC, abstractmethod


class Agent(ABC):
    @abstractmethod
    def step(self, state, allowed_actions):
        """Make a step/move/action by an agent. 

        Parameters
        ----------
        state : np.array(dtype=int)
            An numpy array representing current state of the board.
        allowed_actions : list[(int, int)]
            list of tuples of the coordinates of the unoccupied fields on the board

        Returns
        -------
        (int, int)
            A tuple of the move coordinates in following order (y, x)
        """
        pass

    @abstractmethod
    def reward(self, reward):
        """Give the agent a reward. Should be overriden only in case of the RL Agent

        Parameters
        ----------
        reward : int
            A scalar value
        """
        pass

    @abstractmethod
    def exit(self, final_state):
        """This method allows agent to prepare for shutdown. It also provide final/termination state of the game/environment

        """
        pass
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
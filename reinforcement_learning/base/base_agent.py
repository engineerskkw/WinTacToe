# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from abc import ABC, abstractmethod
import pickle

class BaseAgent(ABC):
    @abstractmethod
    def take_action(self, state, allowed_actions):
        """
        Take an action based on the given state and allowed actions.

        Parameters
        ----------
        state : BaseState
            A state of the environment.
        allowed_actions : BaseActionSpace
            A list of the actions that agent can take.

        Returns
        -------
        BaseAction
            An action taken by the agent.
        """
        pass

    @abstractmethod
    def receive_reward(self, reward):
        """
        Give the agent a reward. Should be overridden only in case of the RL BaseAgent

        Parameters
        ----------
        reward : Float
            Reinforcement learning reward.
        """
        pass

    @abstractmethod
    def exit(self, terminal_state):
        """
        This method allows agent to prepare for shutdown.

        It also provide final/termination state of the game/environment.

        Parameters
        ----------
        terminal_state : BaseState
            Terminal state of the environment.
        """
        pass

    @abstractmethod
    def restart(self):
        """
        This method allows agent to prepare for restart of the environment.
        """
        pass

    def save(self, file_path):
        with open(file_path, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load(file_path):
        with open(file_path, 'rb') as file:
            return pickle.load(file)

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
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

from reinforcement_learning.agents.common.agent_utils import bucketify, gen_tempfile_path
from utils.common_utils import return_deepcopy

class BaseAgent(ABC):
    def __init__(self):
        self.episodes_actions_times = [[]]
        self.all_episodes_returns = []

    @abstractmethod
    @return_deepcopy
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

    def save(self, agent_file_path):
        with open(agent_file_path, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load(agent_file_path):
        # Load concrete instance of an agent
        with open(agent_file_path, 'rb') as file:
            agent = pickle.load(file)

        # Give a control of loading process to the concrete class of the agent
        agent.additional_load_handling(agent_file_path)

        return agent

    def additional_load_handling(self, agent_file_path):
        pass

    def _repr_svg_(self):
        # TODO seamlessly integrate matplotlib plot with ipython _repr_svg_
        self.visualize()

    def visualize(self, bucketing=True):
        if bucketing:
            er_n = len(self.all_episodes_returns)
            er_buckets_number = min(int(np.ceil(0.1*er_n)), 100)
            er_bucket_size = int(er_n/er_buckets_number)
            performance = (np.array(bucketify(self.all_episodes_returns, er_buckets_number, np.mean))+1)/2.0
        else:
            performance = self.all_episodes_returns
        mean_reward = np.mean(self.all_episodes_returns)

        ep_act_times_flatten = [item for sublist in self.episodes_actions_times for item in sublist]
        mean_action_time = np.mean(ep_act_times_flatten)
        if bucketing:
            at_n = len(ep_act_times_flatten)
            at_buckets_number = min(int(np.ceil(0.1*er_n)), 100)
            at_bucket_size = int(at_n / at_buckets_number)
            action_times = bucketify(ep_act_times_flatten, at_buckets_number, np.mean)
        else:
            action_times = ep_act_times_flatten

        fig = plt.figure(constrained_layout=True)
        fig.suptitle(f"{self.__class__.__name__}", fontsize=16, y=1.1)
        spec = gridspec.GridSpec(ncols=1, nrows=2, figure=fig)

        ax0 = fig.add_subplot(spec[0, 0])
        if bucketing:
            ax0.set_xlabel(f"Episodes buckets ({er_buckets_number} buckets of size {er_bucket_size})")
            ax0.set_ylabel("Percentage of winnings")
        else:
            ax0.set_ylabel("Mean return")
        ax0.set_title(f"Performance")
        ax0.plot(performance)

        ax1 = fig.add_subplot(spec[1, 0])
        if bucketing:
            ax1.set_xlabel(f"Actions buckets ({at_buckets_number} buckets of size {at_bucket_size})")
        ax1.set_ylabel("Mean action time [s]")
        ax1.set_title(f"Action times")
        ax1.plot(action_times)

        plt.show()

        # print(f"Number of played episodes: {er_n}")
        print(f"Mean reward: {'{0:0.6f}'.format(mean_reward)}")
        # print(f"Number of taken actions: {at_n}")
        print(f"Mean action time: {'{0:0.6f}'.format(mean_action_time)}")

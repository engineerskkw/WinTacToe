# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os

REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from environments.tic_tac_toe.tic_tac_toe_engine import TicTacToeEngine
from reinforcement_learning.new_agents.n_step_agent.n_step_agent import NStepAgent
from reinforcement_learning.new_agents.q_learning_agent.q_learning_agent import QLearningAgent

from reinforcement_learning.new_agents.random_agent.random_agent import RandomAgent
from reinforcement_learning.new_agents.common.lazy_tabular_action_value import LazyTabularActionValue
from reinforcement_learning.new_agents.common.linear_regression_action_value import LinearRegressionActionValue
from reinforcement_learning.new_agents.common.neural_network_action_value import NeuralNetworkActionValue
from reinforcement_learning.common.simple_training import SimpleTraining
from reinforcement_learning.new_agents.dqn_agent.dqn_agent import DQNAgent
from reinforcement_learning.agents.common.agent_utils import bucketify
from reinforcement_learning.base.base_agent import BaseAgent
import numpy as np
import matplotlib.pyplot as plt
import pickle

from copy import deepcopy

import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

if __name__ == '__main__':
    # To start a training you need an engine:
    engine = TicTacToeEngine(2, 3, 3)

    # # You can also load previously saved agents from files:
    agent_0_file_path = os.path.join(ABS_PROJECT_ROOT_PATH, "training_platform", "examples", "agent0.ai")
    agent_0_network_path = os.path.join(ABS_PROJECT_ROOT_PATH, "training_platform", "examples", "agent0_network.h5")
    agent_1_file_path = os.path.join(ABS_PROJECT_ROOT_PATH, "training_platform", "examples", "agent1.ai")
    agent_1_network_path = os.path.join(ABS_PROJECT_ROOT_PATH, "training_platform", "examples", "agent1_network.h5")

    # agents = [DQNAgent.load(agent_0_file_path, network_file_path=agent_0_network_path),
    #       DQNAgent.load(agent_1_file_path, network_file_path=agent_1_network_path)]

    agents = (BaseAgent.load(agent_0_file_path), BaseAgent.load(agent_1_file_path))

    number_of_episodes = 50000

    hyper_epsilon_starting_value = 0.3
    # x = np.linspace(0, final_epsilon_episode, int(final_epsilon_episode))
    x = np.linspace(0, 10*np.pi, int(0.9*number_of_episodes))
    # x = np.arange(1, int(final_epsilon_episode))
    # y = (np.sqrt(np.power(final_epsilon_episode, 2) - np.power(x, 2)) / final_epsilon_episode) \
    #     * hyper_epsilon_starting_value

    y = np.abs((np.sin(x)/x)) * hyper_epsilon_starting_value
    # y = np.sin(x)
    plt.plot(x, y)
    plt.show()
    # sys.exit()

    example_epsilon_iterator0 = iter(y)
    example_epsilon_iterator1 = iter(y)

    agents = [NStepAgent(5, 0.1, 0.2, 1),
              NStepAgent(5, 0.1, 0.2, 1)
    ]

    # agents[0].epsilon_iter = example_epsilon_iterator
    # agents[1].epsilon_iter = deepcopy(example_epsilon_iterator)

    # Training is as simple as it:
    with SimpleTraining(engine, agents) as st:  # using "with statement" is encouraged
        # assignment is necessary, because training doesn't modify agents provided in constructor
        agents = st.train(number_of_episodes, 10000)

    agents[0].visualize()
    # agents[1].visualize()

    # At the end you can save your trained agents
    # [agent.save(file_path) for (agent, file_path) in zip(agents, agents_file_paths)]
    agents[0].save(agent_0_file_path, network_file_path=agent_0_network_path)
    agents[1].save(agent_1_file_path, network_file_path=agent_1_network_path)
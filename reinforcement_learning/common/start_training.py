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

from reinforcement_learning.new_agents.common.epsilon_strategy import ConstantEpsilonStrategy, CircleEpsilonStrategy, DecayingSinusEpsilonStrategy

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

    # agents = (BaseAgent.load(agent_0_file_path), BaseAgent.load(agent_1_file_path))

    number_of_episodes = 1000

    agents = [
        NStepAgent(5, 0.1, DecayingSinusEpsilonStrategy(0.3, 0.7), 1),
        NStepAgent(5, 0.1, ConstantEpsilonStrategy(0.2),  1)
    ]

    # Training is as simple as this:
    with SimpleTraining(engine, agents) as st:  # using "with statement" is encouraged
        # assignment is necessary, because training doesn't modify agents provided in constructor
        agents = st.train(number_of_episodes, 10000)

    agents[0].visualize()
    # agents[1].visualize()

    # # At the end you can save your trained agents
    # # [agent.save(file_path) for (agent, file_path) in zip(agents, agents_file_paths)]
    # agents[0].save(agent_0_file_path, network_file_path=agent_0_network_path)
    # agents[1].save(agent_1_file_path, network_file_path=agent_1_network_path)
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
from reinforcement_learning.new_agents.common.epsilon_strategy import ConstantEpsilonStrategy, CircleEpsilonStrategy, DecayingSinusEpsilonStrategy

from copy import deepcopy

import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

if __name__ == '__main__':
    # To start a training you need an engine:
    engine = TicTacToeEngine(2, 3, 3)

    agent_0_file_path = os.path.join(ABS_PROJECT_ROOT_PATH, "reinforcement_learning", "common", "trained_agents", "agent0.ai")
    agent_1_file_path = os.path.join(ABS_PROJECT_ROOT_PATH, "reinforcement_learning", "common", "trained_agents", "agent1.ai")
    agents_file_paths = [agent_0_file_path, agent_1_file_path]
    agents = (BaseAgent.load(agent_0_file_path), BaseAgent.load(agent_1_file_path))

    agents = [
        NStepAgent(5, 0.1, CircleEpsilonStrategy(0.1, 0.7), 1),
        RandomAgent()
    ]

    number_of_episodes = 10000
    with SimpleTraining(engine, agents) as st:  # using "with statement" is encouraged
        # assignment is necessary, because training doesn't modify agents provided in constructor
        agents = st.train(number_of_episodes)

    agents[0].visualize()
    # agents[1].visualize()

    # At the end you can save your trained agents
    [agent.save(agent_file_path) for (agent, agent_file_path) in zip(agents, agents_file_paths)]

# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from unittest import TestCase
import numpy as np

from reinforcement_learning.new_agents.dqn_agent.dqn_agent import DQNAgent
from reinforcement_learning.common.simple_training import SimpleTraining
from environments.tic_tac_toe.tic_tac_toe_engine import TicTacToeEngine
from reinforcement_learning.new_agents.n_step_agent.n_step_agent import NStepAgent
from reinforcement_learning.base.base_agent import BaseAgent


class TestAgentsSavingAndLoading(TestCase):
    def setUp(self):
        self.engine = TicTacToeEngine(2, 3, 3)
        self.number_of_episodes = 10
        self.agent_path = os.path.join(ABS_PROJECT_ROOT_PATH, "all_tests", "reinforcement_learning", "agent.ai")

    def test_saving_and_loading_for_agent_with_model(self):
        hyper_epsilon_starting_value = 0.3
        x = np.linspace(0, 10 * np.pi, int(0.9 * self.number_of_episodes))
        y = np.abs((np.sin(x) / x)) * hyper_epsilon_starting_value
        example_epsilon_iterator0 = iter(y)
        example_epsilon_iterator1 = iter(y)

        agents = [DQNAgent(step_size=0.01,
                           epsilon_iter=example_epsilon_iterator0,
                           discount=1,
                           fit_period=4,
                           batch_size=4,
                           max_memory_size=4),
                  DQNAgent(step_size=0.01,
                           epsilon_iter=example_epsilon_iterator1,
                           discount=1,
                           fit_period=4,
                           batch_size=4,
                           max_memory_size=4)
                  ]

        with SimpleTraining(self.engine, agents) as st:
            agents = st.train(self.number_of_episodes)

        agent = agents[0]
        agent.save(self.agent_path)
        loaded_agent = BaseAgent.load(self.agent_path)
        self.assertTrue(np.all(np.isclose(loaded_agent.all_episodes_returns, agent.all_episodes_returns)))

    def test_saving_and_loading_for_agent_without_model(self):
        agents = [NStepAgent(5, 0.1, 0.2, 1),
                  NStepAgent(5, 0.1, 0.2, 1)
                  ]

        with SimpleTraining(self.engine, agents) as st:
            agents = st.train(self.number_of_episodes)

        agent = agents[0]
        agent.save(self.agent_path)
        loaded_agent = BaseAgent.load(self.agent_path)
        self.assertTrue(np.all(np.isclose(loaded_agent.all_episodes_returns, agent.all_episodes_returns)))
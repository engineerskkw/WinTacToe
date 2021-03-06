from unittest import TestCase
import numpy as np
import os
from global_constants import ABS_PROJECT_ROOT_PATH

from reinforcement_learning.agents.dqn_agent.dqn_agent import DQNAgent
from reinforcement_learning.simple_training import SimpleTraining
from environments.tic_tac_toe.tic_tac_toe_engine import TicTacToeEngine
from reinforcement_learning.agents.n_step_agent.n_step_agent import NStepAgent
from reinforcement_learning.agents.base_agent import BaseAgent
from reinforcement_learning.agents.common_building_blocks.epsilon_strategy import CircleEpsilonStrategy


class TestAgentsSavingAndLoading(TestCase):
    def setUp(self):
        self.engine = TicTacToeEngine(2, 3, 3)
        self.number_of_episodes = 10
        self.agent_path = os.path.join(ABS_PROJECT_ROOT_PATH, "tests", "test_reinforcement_learning", "agent.ai")

    def test_saving_and_loading_for_agent_with_model(self):
        agents = [DQNAgent(step_size=0.01,
                           discount=1,
                           epsilon_strategy=CircleEpsilonStrategy(0.1, 0.7),
                           fit_period=64,
                           batch_size=64,
                           max_memory_size=64),
                  DQNAgent(step_size=0.01,
                           discount=1,
                           epsilon_strategy=CircleEpsilonStrategy(0.1, 0.7),
                           fit_period=64,
                           batch_size=64,
                           max_memory_size=64)
                  ]

        with SimpleTraining(self.engine, agents) as st:
            agents = st.train(self.number_of_episodes)

        agent = agents[0]
        agent.save(self.agent_path)
        loaded_agent = BaseAgent.load(self.agent_path)
        self.assertTrue(np.all(np.isclose(loaded_agent.all_episodes_returns, agent.all_episodes_returns)))
        original_weights = loaded_agent.model.get_weights()
        loaded_weights = agent.model.get_weights()
        self.assertEqual(len(original_weights), len(loaded_weights))
        for i in range(len(original_weights)):
            self.assertTrue(np.all(np.isclose(original_weights[i], loaded_weights[i])))

    def test_saving_and_loading_for_agent_without_model(self):
        agents = [NStepAgent(5, 0.1, CircleEpsilonStrategy(0.1, 0.7), 1),
                  NStepAgent(5, 0.1, CircleEpsilonStrategy(0.1, 0.7), 1)
                  ]

        with SimpleTraining(self.engine, agents) as st:
            agents = st.train(self.number_of_episodes)

        agent = agents[0]
        agent.save(self.agent_path)
        loaded_agent = BaseAgent.load(self.agent_path)
        self.assertTrue(np.all(np.isclose(loaded_agent.all_episodes_returns, agent.all_episodes_returns)))

    def tearDown(self):
        os.remove(self.agent_path)

# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os

REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

# Engine
from environments.tic_tac_toe.tic_tac_toe_engine import TicTacToeEngine

#Agents
from reinforcement_learning.base.base_agent import BaseAgent
from reinforcement_learning.new_agents.n_step_agent.n_step_agent import NStepAgent
from reinforcement_learning.new_agents.random_agent.random_agent import RandomAgent
from reinforcement_learning.new_agents.dqn_agent.dqn_agent import DQNAgent
from reinforcement_learning.agents.basic_mc_agent.basic_mc_agent import BasicAgent

# Agents building blocks
from reinforcement_learning.new_agents.common.epsilon_strategy import ConstantEpsilonStrategy, CircleEpsilonStrategy, DecayingSinusEpsilonStrategy

# Training
from reinforcement_learning.common.simple_training import SimpleTraining

# Agents Database
from reinforcement_learning.agents_database.agents_db import AgentsDB

# To avoid warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

if __name__ == '__main__':
    engine = TicTacToeEngine(2, 3, 3)

    # agents = [NStepAgent(n=5,
    #                      step_size=0.1,
    #                      epsilon_strategy=CircleEpsilonStrategy(starting_epsilon_value=0.1, exploration_part=0.7),
    #                      discount=1),
    #           DQNAgent(step_size=0.01,
    #                    discount=1,
    #                    epsilon_strategy=DecayingSinusEpsilonStrategy(starting_epsilon_value=0.1, exploration_part=0.7),
    #                    fit_period=64,
    #                    batch_size=64,
    #                    max_memory_size=64)]

    # agents = [NStepAgent(n=5,
    #                      step_size=0.1,
    #                      epsilon_strategy=CircleEpsilonStrategy(starting_epsilon_value=0.1, exploration_part=0.7),
    #                      discount=1),
    #           NStepAgent(n=5,
    #                      step_size=0.1,
    #                      epsilon_strategy=CircleEpsilonStrategy(starting_epsilon_value=0.1, exploration_part=0.7),
    #                      discount=1)]

    agents = [BasicAgent(epsilon_strategy=ConstantEpsilonStrategy(0.1),
                         discount=1),
              BasicAgent(epsilon_strategy=ConstantEpsilonStrategy(0.1),
                         discount=1)]

    episodes_no = 10000
    with SimpleTraining(engine=engine, agents=agents) as st:
        agents = st.train(episodes_no=episodes_no,
                          auto_saving=True,
                          saving_description="MonteCarloAgent vs MonteCarloAgent from scratch, "
                                             "sConstantEpsilonStrategy(0.1), discount=1")

    [agent.visualize() for agent in agents]

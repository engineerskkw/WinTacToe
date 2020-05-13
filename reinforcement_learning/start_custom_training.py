# Engine
from environments.tic_tac_toe.tic_tac_toe_engine import TicTacToeEngine

#Agents
from reinforcement_learning.agents.monte_carlo_agent.monte_carlo_agent import MonteCarloAgent
from reinforcement_learning.agents.n_step_agent.n_step_agent import NStepAgent
from reinforcement_learning.agents.dyna_n_step_agent.dyna_n_step_agent import DynaNStepAgent
from reinforcement_learning.agents.dqn_agent.dqn_agent import DQNAgent

# Agents building blocks
from reinforcement_learning.agents.common_building_blocks.epsilon_strategy import ConstantEpsilonStrategy, CircleEpsilonStrategy, DecayingSinusEpsilonStrategy

# Training
from reinforcement_learning.simple_training import SimpleTraining

# Agents Database

# To avoid warnings
import os
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

    agents = [NStepAgent(n=5,
                         step_size=0.1,
                         epsilon_strategy=CircleEpsilonStrategy(starting_epsilon_value=0.1, exploration_part=0.7),
                         discount=1),
              DynaNStepAgent(n=5,
                         step_size=0.1,
                         epsilon_strategy=CircleEpsilonStrategy(starting_epsilon_value=0.1, exploration_part=0.7),
                         discount=1)]

    # agents = [MonteCarloAgent(epsilon_strategy=ConstantEpsilonStrategy(0.1),
    #                           discount=1),
    #           MonteCarloAgent(epsilon_strategy=ConstantEpsilonStrategy(0.1),
    #                           discount=1)]

    episodes_no = 1000
    with SimpleTraining(engine=engine, agents=agents) as st:
        agents = st.train(episodes_no=episodes_no,
                          auto_saving=True,
                          saving_description="dyna from scratch")

    [agent.visualize() for agent in agents]

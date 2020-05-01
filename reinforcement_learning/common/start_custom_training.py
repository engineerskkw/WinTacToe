# Engine
from environments.tic_tac_toe.tic_tac_toe_engine import TicTacToeEngine

#Agents
from reinforcement_learning.agents.monte_carlo_agent.monte_carlo_agent import MonteCarloAgent

# Agents building blocks
from reinforcement_learning.agents.common.epsilon_strategy import ConstantEpsilonStrategy

# Training
from reinforcement_learning.common.simple_training import SimpleTraining

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

    # agents = [NStepAgent(n=5,
    #                      step_size=0.1,
    #                      epsilon_strategy=CircleEpsilonStrategy(starting_epsilon_value=0.1, exploration_part=0.7),
    #                      discount=1),
    #           NStepAgent(n=5,
    #                      step_size=0.1,
    #                      epsilon_strategy=CircleEpsilonStrategy(starting_epsilon_value=0.1, exploration_part=0.7),
    #                      discount=1)]

    agents = [MonteCarloAgent(epsilon_strategy=ConstantEpsilonStrategy(0.1),
                              discount=1),
              MonteCarloAgent(epsilon_strategy=ConstantEpsilonStrategy(0.1),
                              discount=1)]

    episodes_no = 10000
    with SimpleTraining(engine=engine, agents=agents) as st:
        agents = st.train(episodes_no=episodes_no,
                          auto_saving=True,
                          saving_description="MonteCarloAgent vs MonteCarloAgent from scratch, "
                                             "sConstantEpsilonStrategy(0.1), discount=1")

    [agent.visualize() for agent in agents]

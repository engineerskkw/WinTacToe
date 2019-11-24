# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os

REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from environments.tic_tac_toe.tic_tac_toe_engine import TicTacToeEngine
from reinforcement_learning.base.base_agent import BaseAgent
from reinforcement_learning.agents.basic_mc_agent.basic_mc_agent import BasicAgent
from reinforcement_learning.agents.q_learning_agent.q_learning_agent import QLearningAgent
from reinforcement_learning.common.simple_training import SimpleTraining

if __name__ == '__main__':
    # To start a training you need an engine:
    engine = TicTacToeEngine(2, 3, 3)

    # ...and agents:
    agents = [BasicAgent(), QLearningAgent(0.3, 0.1, 0.9)]

    # You can also load previously saved agents from files:
    agent_0_file_path = os.path.join(ABS_PROJECT_ROOT_PATH, "training_platform", "examples", "agent0.ai")
    agent_1_file_path = os.path.join(ABS_PROJECT_ROOT_PATH, "training_platform", "examples", "agent1.ai")
    agents_file_paths = [agent_0_file_path, agent_1_file_path]
    agents = [BaseAgent.load(file_path) for file_path in agents_file_paths]

    # Training is as simple as it:
    number_of_episodes = 100
    with SimpleTraining(engine, agents) as st:  # using "with statement" is encouraged
        # assignment is necessary, because training doesn't modify agents provided in constructor
        agents = st.train(number_of_episodes)

    # At the end you can save your trained agents
    [agent.save(file_path) for (agent, file_path) in zip(agents, agents_file_paths)]
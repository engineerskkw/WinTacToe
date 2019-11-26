# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os

REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from environments.tic_tac_toe.tic_tac_toe_engine import TicTacToeEngine
from reinforcement_learning.agents.basic_mc_agent.basic_mc_agent import BasicAgent
from reinforcement_learning.agents.q_learning_agent.q_learning_agent import QLearningAgent
from reinforcement_learning.agents.n_step_agent.n_step_agent import NStepAgent
from training_platform import EnvironmentServer
from training_platform import AgentClient
from reinforcement_learning.base.base_agent import BaseAgent
from reinforcement_learning.agents.random_agent.random_agent import RandomAgent

if __name__ == '__main__':
    agent_0_file_path = os.path.join(ABS_PROJECT_ROOT_PATH, "training_platform", "examples", "agent0.ai")
    agent_1_file_path = os.path.join(ABS_PROJECT_ROOT_PATH, "training_platform", "examples", "agent1.ai")

    NStepAgent(4, 0.4, 0.1, 0.9).save(agent_0_file_path)
    QLearningAgent(0.1, 0.1, 0.1).save(agent_1_file_path)

    print("Agents created")
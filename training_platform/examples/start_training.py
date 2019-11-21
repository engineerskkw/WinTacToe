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
from training_platform import EnvironmentServer
from training_platform import AgentClient
from reinforcement_learning.abstract.abstract_agent import Agent

if __name__ == '__main__':
    server = EnvironmentServer(TicTacToeEngine(2, 3, 3))
    print("Environment Server has started!")

    players = server.players
    p0 = players[0]
    p1 = players[1]

    # agent_0_file_path = os.path.join(ABS_PROJECT_ROOT_PATH, "training_platform", "examples", "agent0.ai")
    # agent_1_file_path = os.path.join(ABS_PROJECT_ROOT_PATH, "training_platform", "examples", "agent1.ai")
    #
    # a0 = Agent.load(agent_0_file_path)
    # a1 = Agent.load(agent_1_file_path)

    c0 = AgentClient(QLearningAgent(0.1, 0.05, 0.9))
    c1 = AgentClient(QLearningAgent(0.1, 0.05, 0.9))

    server.join(c0, p0)
    server.join(c1, p1)
    print("Clients have joined server!")

    for i in range(100):
        print(f"Game number: {i}")
        server.start()
    print("All episodes finished")

    # c0.agent.save(agent_0_file_path)
    # c1.agent.save(agent_1_file_path)

    a0 = c0.agent
    a1 = c1.agent

    print(a0.performance_measure)
    print(a1.performance_measure)

    server.shutdown()
    print("Training platform has been shutdowned!")

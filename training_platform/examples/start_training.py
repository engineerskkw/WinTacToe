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
from training_platform import EnvironmentServer
from training_platform import AgentClient
from reinforcement_learning.base.base_agent import BaseAgent
import time

if __name__ == '__main__':
    server = EnvironmentServer(TicTacToeEngine(2, 3, 3))
    print("Environment Server has started!")

    players = server.players
    p0 = players[0]
    p1 = players[1]

    agent_0_file_path = os.path.join(ABS_PROJECT_ROOT_PATH, "training_platform", "examples", "agent0.ai")
    agent_1_file_path = os.path.join(ABS_PROJECT_ROOT_PATH, "training_platform", "examples", "agent1.ai")

    a0 = BaseAgent.load(agent_0_file_path)
    a1 = BaseAgent.load(agent_1_file_path)

    c0 = AgentClient(a0)
    c1 = AgentClient(a1)

    server.join(c0, p0)
    server.join(c1, p1)
    print("Clients have joined server!")

    start = time.time()
    episodes_number = 10
    print("Please wait...")
    for i in range(episodes_number):
        # print(f"Game number: {i}")
        server.start()
    end = time.time()
    print(f"{episodes_number} episodes finished in {end-start}")

    c0.agent.save(agent_0_file_path)
    c1.agent.save(agent_1_file_path)

    server.shutdown()
    print("Training platform has been shutdowned!")

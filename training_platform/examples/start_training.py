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

if __name__ == '__main__':
    server = EnvironmentServer(TicTacToeEngine(2, 3, 3))
    print("Environment Server has started!")

    players = server.players
    p0 = players[0]
    p1 = players[1]

    c0 = AgentClient(BasicAgent())
    c1 = AgentClient(BasicAgent())

    server.join(c0, p0)
    server.join(c1, p1)
    print("Clients have joined server!")

    for i in range(100):
        print(f"Game number: {i}")
        server.start()
    print("All episodes finished")

    server.shutdown()
    print("Server has been shutdowned!")

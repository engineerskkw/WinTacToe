# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os
REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from training_platform.server.environment_server import EnvironmentServer
from training_platform import AgentClient
from reinforcement_learning.agents.basic_mc_agent.basic_mc_agent import BasicAgent

if __name__ == '__main__':
    server = EnvironmentServer()
    p = server.players[0]
    c = AgentClient(BasicAgent())
    c.join(p)
    print("Agent Client has joind server!")

# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os

REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import unittest
from environments.tic_tac_toe.tic_tac_toe_engine import TicTacToeEngine
from reinforcement_learning.agents.basic_mc_agent.basic_mc_agent import BasicAgent
from training_platform import EnvironmentServer
from training_platform import AgentClient
from training_platform.server.environment_server import EnvironmentNotReadyToStartError, \
    AccessingUninitializedEnvServerError, \
    EnvServerReinitializingError, MatchMakerUninitializedMsg
from thespian.actors import ActorSystem, ActorExitRequest
from training_platform.clients.agent_client import MatchMakerUninitializedError
from training_platform.server.service import MatchMaker

import time
ACTOR_SYSTEM_CLEANUP_TIME = 1

# class EnvironmentServerInitializationTestCase(unittest.TestCase):
#     def test_accessing_uninitialize_env_server(self):
#         with self.assertRaises(AccessingUninitializedEnvServerError):
#             EnvironmentServer()
#
#     def test_env_server_reinitializing(self):
#         server = EnvironmentServer(TicTacToeEngine(2, 3, 3))
#         with self.assertRaises(EnvServerReinitializingError):
#             EnvironmentServer(TicTacToeEngine(2, 3, 3))
#         server.shutdown()
#         time.sleep(ACTOR_SYSTEM_CLEANUP_TIME)


class ClientPlayerJoiningTestCase(unittest.TestCase):
    def setUp(self):
        self.server = EnvironmentServer(TicTacToeEngine(2, 3, 3))
        players = self.server.players
        self.p0 = players[0]
        self.p1 = players[1]
        self.c0 = AgentClient(BasicAgent())
        self.c1 = AgentClient(BasicAgent())

    def test_proper_joinning_from_clients(self):
        self.assertTrue(self.c0.join(self.p0))
        self.assertTrue(self.c1.join(self.p1))

    # def test_join_match_maker_uninitialized(self):
    #     asys = ActorSystem('multiprocTCPBase')
    #     match_maker_addr = asys.createActor(MatchMaker, globalName="MatchMaker")
    #     asys.tell(match_maker_addr, ActorExitRequest()) # Exit an old initialized MatchMaker
    #     asys.createActor(MatchMaker, globalName="MatchMaker")  # Make instance of the new uninitialized MatchMaker
    #     with self.assertRaises(MatchMakerUninitializedError):
    #         print("aaa")
    #         self.c0.join(self.p0)

    # def test_proper_joinning_from_server(self):
    #     self.assertTrue(self.server.join(self.c0, self.p0))
    #     self.assertTrue(self.server.join(self.c1, self.p1))

    def tearDown(self):
        self.server.shutdown()
        time.sleep(ACTOR_SYSTEM_CLEANUP_TIME)

# class NonBlockingStartTestCase(unittest.TestCase):
#     def setUp(self):
#         self.server = EnvironmentServer(TicTacToeEngine(2, 3, 3))
#
#         players = self.server.players
#         p0, p1 = players[0], players[1]
#         c0, c1 = AgentClient(BasicAgent()), AgentClient(BasicAgent())
#
#         self.server.join(c0, p0)
#         self.server.join(c1, p1)
#
#     def test_nonblocking_start(self):
#         with self.assertRaises(EnvironmentNotReadyToStartError):
#             for i in range(5):
#                 self.server.start(False)
#
#     def tearDown(self):
#         self.server.shutdown()
#         time.sleep(ACTOR_SYSTEM_CLEANUP_TIME)


if __name__ == '__main__':
    unittest.main()

# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os

REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

# BEGIN---------------------CHANGING-ACTOR-SYSTEM-BASE-------------------------#
import configparser
config = configparser.RawConfigParser()
config_file_path = os.path.join(ABS_PROJECT_ROOT_PATH, "training_platform", "config.ini")

config.read(config_file_path)
old_actor_system_base_value = config["TRAINING PLATFORM PARAMETERS"]["actorsystembase"]

config.set("TRAINING PLATFORM PARAMETERS", "actorsystembase", "simpleSystemBase")
with open(config_file_path, 'w') as configfile:
    config.write(configfile)
# ---------------------------CHANGING-ACTOR-SYSTEM-BASE---------------------END#

import unittest

from training_platform.common import *
from environments.tic_tac_toe.tic_tac_toe_engine import TicTacToeEngine
from reinforcement_learning.agents.basic_mc_agent.basic_mc_agent import BasicAgent
from training_platform import EnvironmentServer
from training_platform import AgentClient
from training_platform.server.environment_server import EnvironmentNotReadyToStartError, \
                                                        AccessingUninitializedEnvServerError,\
                                                        EnvServerReinitializingError
from training_platform.clients.agent_client import InvalidPlayer,\
                                                   RejoiningError


class EnvironmentServerInitializationTestCase(unittest.TestCase):
    def test_accessing_uninitialize_env_server(self):
        with self.assertRaises(AccessingUninitializedEnvServerError):
            EnvironmentServer()

    def test_env_server_reinitializing(self):
        server = EnvironmentServer(TicTacToeEngine(2, 3, 3))
        with self.assertRaises(EnvServerReinitializingError):
            EnvironmentServer(TicTacToeEngine(2, 3, 3))
        server.shutdown()


class ClientPlayerTestCase(unittest.TestCase):
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

    # # Ultra cancer, I don't know how to make it fucking work
    # def test_join_match_maker_uninitialized(self):
    #     self.server.shutdown()
    #     with self.assertRaises(MatchMakerUninitializedError):
    #         self.c0.join(self.p0)
    #     self.server = EnvironmentServer(TicTacToeEngine(2, 3, 3))

    def test_joining_with_invalid_player(self):
        with self.assertRaises(InvalidPlayer):
            self.c0.join(None)

    def test_rejoining(self):
        self.assertTrue(self.c0.join(self.p0))
        with self.assertRaises(RejoiningError):
            self.assertTrue(self.c0.join(self.p0))

    def test_proper_joinning_from_server(self):
        self.assertTrue(self.server.join(self.c0, self.p0))
        self.assertTrue(self.server.join(self.c1, self.p1))

    def test_agent_getting(self):
        self.c0.join(self.p0)
        self.c1.join(self.p1)
        self.server.start()
        # If list of expected returns is not empty, agent has been updated
        self.assertTrue(self.c0.agent.Gs)

    def test_agent_multiple_games_expirience(self):
        self.c0.join(self.p0)
        self.c1.join(self.p1)
        for i in range(10):
            self.server.start()
        self.assertEqual(len(self.c0.agent.Gs), 10)
        self.assertEqual(len(self.c1.agent.Gs), 10)

    def tearDown(self):
        self.server.shutdown()


class EnvironmentServerTestCase(unittest.TestCase):
    def setUp(self):
        self.server = EnvironmentServer(TicTacToeEngine(2, 3, 3))

        players = self.server.players
        p0, p1 = players[0], players[1]
        c0, c1 = AgentClient(BasicAgent()), AgentClient(BasicAgent())

        self.server.join(c0, p0)
        self.server.join(c1, p1)

    def test_start_blocking(self):
        self.assertTrue(self.server.start())

    def test_start_non_blocking_(self):
        with self.assertRaises(EnvironmentNotReadyToStartError):
            for i in range(10):
                self.server.start(blocking=False)

    def test_restart_non_blocking(self):
        self.server.start(blocking=False)
        for i in range(10):
            self.server.restart(blocking=False)

    def test_restart_blocking(self):
        self.server.start(blocking=False)
        for i in range(10):
            self.server.restart()

    def tearDown(self):
        self.server.shutdown()


if __name__ == '__main__':
    unittest.main(exit=False)

    # BEGIN--------------------RESTORING-ACTOR-SYSTEM-BASE-------------------------#
    config.set("TRAINING PLATFORM PARAMETERS", "actorsystembase", old_actor_system_base_value)
    with open(config_file_path, 'w') as configfile:
        config.write(configfile)
    # -------------------------RESTORING-ACTOR-SYSTEM-BASE----------------------END#

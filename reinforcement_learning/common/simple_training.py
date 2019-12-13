# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import time
from progress.bar import IncrementalBar

from training_platform import EnvironmentServer
from training_platform import AgentClient



class AgentsNumberNotMatchPlayersNumber(Exception):
    def __str__(self):
        return "Number of players demanded by an engine doesn't match number of provided agents"


class InvalidUsage(Exception):
    def __init__(self, object):
        self.object = object

    def __str__(self):
        return f"This object: {self.object} should be used with the python's 'with statement' " \
               f"as it need some cleanup."


class SimpleTraining:
    def __init__(self, engine, agents):
        self.engine = engine
        self.agents = agents
        self._server = None
        self._clients = [AgentClient(agent) for agent in self.agents]

    def __enter__(self):
        self._server = EnvironmentServer(self.engine)
        print("Training platform has started!")
        players = self._server.players
        if not len(players) == len(self.agents):
            raise AgentsNumberNotMatchPlayersNumber
        [self._server.join(client, player) for (client, player) in zip(self._clients, players)]
        print("Clients have joined server!")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._server.shutdown()
        print("Training platform has been shutdown!")

    def train(self, episodes_no, saving_period=None):
        if self._server is None:
            raise InvalidUsage(self)

        # with IncrementalBar("Training", max=episodes_no, suffix='%(percent)d%%') as bar:
        for agent in self.agents:
            agent.epsilon_strategy.init_no_of_episodes(episodes_no)

        start = time.time()
        for i in range(episodes_no):
            for agent in self.agents:
                agent.update_epsilon()

            print(f"episode {i}") if i % 100 == 0 else None
            if saving_period is not None and i % saving_period == 0 and not i == 0:
                for agent in self.agents:
                    agent.save(agent.agent_path)
            self._server.start()
            # bar.next()
        end = time.time()
        print(f"Finished {episodes_no} episodes in {end-start}")

        return [client.agent for client in self._clients]

    def finish(self):
        self.__exit__(None, None, None)

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
from reinforcement_learning.agents_database.agents_db import AgentsDB


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

    def train(self, episodes_no, auto_saving=None, saving_description=None):
        """
        :param episodes_no: number of episodes to play
        :param auto_saving:
            if None or False-> nothing is saved
            if True -> All agents are saved at the and of the training
            if Integer -> All agents are saved every auto_saving episodes
        :param saving_description:
            if None -> All agents are saved with the same standard description: "{episodes_no} episodes"
            if string -> This string is used as description for saving for all agents
            if list(string) -> Each agent is saved with his own description from list
        :return: list of trained agents
        """
        # Error handling
        if not (isinstance(auto_saving, bool) or isinstance(auto_saving, int) or auto_saving is None):
            raise ValueError("Invalid auto_saving parameter. Allowed values: None, False, True, integer")

        if self._server is None:
            raise InvalidUsage(self)

        # with IncrementalBar("Training", max=episodes_no, suffix='%(percent)d%%') as bar:
        for agent in self.agents:
            agent.epsilon_strategy.init_no_of_episodes(episodes_no)

        # Description(s) handling
        if auto_saving is not None and saving_description is not None:
            if isinstance(saving_description, str):
                saving_descriptions = [saving_description for _ in range(len(self.agents))]
            elif isinstance(saving_description, list) or isinstance(saving_description, tuple):
                if len(saving_description) == len(self.agents):
                    saving_descriptions = saving_description
                else:
                    raise ValueError(
                        "If saving_description is a list of descriptions its length should be same as agents number")
            else:
                raise ValueError("Invalid saving_description parameter")
        else:
            saving_descriptions = [f"{episodes_no} episodes" for _ in range(len(self.agents))]

        start = time.time()
        for i in range(episodes_no):
            # Epsilon updating
            for agent in self.agents:
                agent.update_epsilon()

            # Pseudo progress bar
            print(f"episode {i}") if i % 100 == 0 else None

            # Periodic saving
            if isinstance(auto_saving, int) and not isinstance(auto_saving, bool) and \
                i % auto_saving == 0 and not i == 0:
                [AgentsDB.save(self.agents[i],
                               i,
                               self.engine._board_size,
                               self.engine._marks_required,
                               saving_descriptions[i]) for i in range(len(self.agents))]

            # Start episode
            self._server.start()
            # bar.next()
        end = time.time()

        # Finish log
        print(f"Finished {episodes_no} episodes in {end-start}")

        # Saving at the end
        if auto_saving:
            [AgentsDB.save(self.agents[i],
                           i,
                           self.engine._board_size,
                           self.engine._marks_required,
                           saving_descriptions[i]) for i in range(len(self.agents))]

        return [client.agent for client in self._clients]

    def finish(self):
        self.__exit__(None, None, None)

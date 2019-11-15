# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from thespian.actors import *
from training_platform.server.common import *
from training_platform.server.service import GameManager, MatchMaker


class UninitializedServerWithoutEngine(Exception):
    """Raised when uninitialized server is spawned without engine"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class InitializedServerWithEngine(Exception):
    """Raised when initialized server is spawned with engine"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)

class ServerNotReadyToStart(Exception):
    """Raised when server is called to start but it hasn't all player clients joined"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class Server:
    def __init__(self, engine=None):
        self.engine = engine
        self.asys = ActorSystem('multiprocTCPBase')
        self.game_manager_addr = self.asys.createActor(GameManager, globalName="GameManager")
        self.match_maker_addr = self.asys.createActor(MatchMaker, globalName="MatchMaker")
        response = self.asys.ask(self.game_manager_addr, AreYouInitializedMsg())

        if isinstance(response, IAmInitializedMsg):
            if self.engine is not None:
                raise InitializedServerWithEngine("Initialized server spawned with engine")

        if isinstance(response, IAmUninitializedMsg):
            if self.engine is None:
                raise UninitializedServerWithoutEngine("Uninitialized server spawned without engine")
            else:
                response = self.asys.ask(self.game_manager_addr, InitGameManagerMsg(self.engine))
                if not isinstance(response, IAmInitializedMsg):
                    raise

    @property
    def players(self):
        if self.engine is not None:
            return self.engine.players
        else:
            return None

    def join(self, client, player):
        return client.join(player)

    # TODO: rethink starting and restarting, blocking and  non-blocking, check corner cases
    def start(self, blocking=True):
        response = self.asys.ask(self.game_manager_addr, StartEnvMsg())
        if blocking:
            return self._start_blocking(response)
        else:
            return self._start_non_blocking(response)

    def _start_non_blocking(self, response):
        """Non-blocking call"""
        if isinstance(response, StartedMsg):
            return
        elif isinstance(response, NotReadyToStartMsg):
            raise ServerNotReadyToStart("Server not ready to start")
        else:
            raise

    def _start_blocking(self, response):
        """Blocking call"""
        while True:
            if isinstance(response, GameOverMsg):
                return
            elif isinstance(response, GameRestartedMsg):
                return
            elif isinstance(response, NotReadyToStartMsg):
                raise ServerNotReadyToStart("Server not ready to start")
            elif isinstance(response, StartedMsg):
                response = self.asys.listen()
            else:
                raise

    def restart(self, blocking=True):

        response = self.asys.ask(self.game_manager_addr, RestartEnvMsg())
        if blocking:
            return self._restart_blocking(response)
        else:
            return self._restart_non_blocking(response)

    def _restart_non_blocking(self, response):
        if isinstance(response, GameRestartedMsg):
            return
        else:
            raise

    def _restart_blocking(self, response):
        while True:
            if isinstance(response, GameOverMsg):

                return
            else:
                response = self.asys.listen()

    def shutdown(self):
        self.asys.shutdown()

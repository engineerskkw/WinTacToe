# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from thespian.actors import *
from training_platform.common import *
from training_platform.server.service import GameManager, MatchMaker
from training_platform.server.logger import Logger
from training_platform.common import LOGGING

class EnvironmentNotReadyToStartError(Exception):
    def __str__(self):
        return "EnvironmentServer not ready to start (not all clients have joined or game is already started)"


class AccessingUninitializedEnvServerError(Exception):
    def __str__(self):
        return "Attempt of getting access-object of uninitialized EnvironmentServer. " \
               "If you want initialize it try constructor EnvironmentServer(engine) " \
               "with engine parameter."


class EnvServerReinitializingError(Exception):
    def __str__(self):
        return "Attempt of reinitializing already initialized EnvironmentServer with new engine! " \
               "To get access-object to already initialized EnvironmentServer" \
               "try constructor EnvironmentServer() without engine parameter."


class EnvironmentServer:
    def __init__(self, engine=None):
        self.engine = engine
        self.asys = ActorSystem(ACTOR_SYSTEM_BASE)
        self.game_manager_addr = self.asys.createActor(GameManager, globalName="GameManager")
        self.match_maker_addr = self.asys.createActor(MatchMaker, globalName="MatchMaker")
        self.logger_addr = self.asys.createActor(Logger, globalName="Logger")
        self._connect()

    def log(self, text, logging_level=LoggingLevel.GAME_EVENTS):
        if not LOGGING:
            return
        if self.logger_addr is not None:
            self.asys.tell(self.logger_addr, LogMsg(text, f"EnvironmentServerEndpoint", logging_level))

    def tell(self, target_address, message):
        self.asys.tell(target_address, message)
        self.log(f"Sent {message} to {target_address}", LoggingLevel.PLATFORM_COMMUNICATION_MESSAGES)

    def listen(self):
        response = self.asys.listen()
        self.log(f"Received {response}", LoggingLevel.PLATFORM_COMMUNICATION_MESSAGES)
        return response

    def ask(self, target_address, message):
        self.tell(target_address, message)
        return self.listen()
    
    def _connect(self):
        response = self.ask(self.game_manager_addr, AreYouInitializedMsg())
        if self.engine is None:
            if isinstance(response, GameManagerInitializedMsg):
                self.engine = response.environment
            elif isinstance(response, GameManagerUninitializedMsg):
                raise AccessingUninitializedEnvServerError
            else:
                raise UnexpectedMessageError(response)
        else:
            if isinstance(response, GameManagerInitializedMsg):
                raise EnvServerReinitializingError
            elif isinstance(response, GameManagerUninitializedMsg):
                response = self.ask(self.game_manager_addr, InitGameManagerMsg(self.engine))
                if not isinstance(response, GameManagerInitializedMsg):
                    raise UnexpectedMessageError(response)
            else:
                raise UnexpectedMessageError(response)

    @property
    def players(self):
        self.log(f"Getting players")
        return self.engine.players


    def join(self, client, player):
        self.log(f"Started joining client {client} to player {player} on server")
        return client.join(player)

    def start(self, blocking=True):
        response = self.ask(self.game_manager_addr, StartEnvMsg(notify_on_end=blocking))
        if blocking:
            return self._start_blocking(response)
        else:
            return self._start_non_blocking(response)

    def _start_non_blocking(self, response):
        """Non-blocking call, returns immediately after EnvironmentServer has started environment"""
        if isinstance(response, EnvStartedMsg):
            return
        elif isinstance(response, EnvNotReadyToStartMsg):
            raise EnvironmentNotReadyToStartError
        raise UnexpectedMessageError(response)

    def _start_blocking(self, response):
        """Blocking call, returns after completing or restarting of the episode started by this access-object"""
        if isinstance(response, EnvNotReadyToStartMsg):
            raise EnvironmentNotReadyToStartError
        elif isinstance(response, EnvStartedMsg):
            response = self.listen()
            if isinstance(response, GameOverMsg) or isinstance(response, EnvRestartedMsg):
                return True
        raise UnexpectedMessageError(response)

    def restart(self, blocking=True):
        response = self.ask(self.game_manager_addr, RestartEnvMsg(notify_on_end=blocking))
        if blocking:
            return self._restart_blocking(response)
        else:
            return self._restart_non_blocking(response)

    def _restart_non_blocking(self, response):
        if isinstance(response, EnvRestartedMsg):
            return
        raise UnexpectedMessageError(response)

    def _restart_blocking(self, response):
        if isinstance(response, EnvRestartedMsg):
            response = self.listen()
            if isinstance(response, GameOverMsg) or isinstance(response, EnvRestartedMsg):
                return
        raise UnexpectedMessageError(response)

    def shutdown(self):
        self.log(f"Performing shutdown")
        self.asys.shutdown()

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
from training_platform.server.logger import Logger


class MonitorClient:
    def __init__(self):
        self.asys = ActorSystem(ACTOR_SYSTEM_BASE)
        self.match_maker_addr = self.asys.createActor(MatchMaker, globalName="MatchMaker")
        self.game_manager_addr = self.asys.createActor(GameManager, globalName="GameManager")
        self.logger_addr = self.asys.createActor(Logger, globalName="Logger")

    def start_monitoring(self):
        response = self.asys.ask(self.logger_addr, JoinMonitorMsg())
        if isinstance(response, MonitorJoinAcknowledgement):
            print("Succesfully joined logger")

        while True:
            msg = self.asys.listen()
            if isinstance(msg, LogMsg):
                print(msg)

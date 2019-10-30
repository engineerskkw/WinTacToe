#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
PROJECT_ROOT_PATH = "./../../"
sys.path.append(os.path.join(os.path.dirname(__file__), PROJECT_ROOT_PATH))
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from training_platform.server.common import *

class Logger(Actor):
    def __init__(self):
        super().__init__()
        self.history = []
        self.match_maker_addr = None
        self.game_manager_addr = None
        self.monitor_addr = None

    def receiveMessage(self, msg, sender):
        if isinstance(msg, InitLoggerMsg):
            self.match_maker_addr = self.createActor(MatchMaker, globalName="MatchMaker")
            self.game_manager_addr = self.createActor(MatchMaker, globalName="GameManager")

        elif isinstance(msg, JoinMonitorMsg):
            self.monitor_addr = sender
            for log_msg in self.history:
                self.send(self.monitor_addr, log_msg)

        elif isinstance(msg, LogMsg):
            self.history.append(msg)
            if self.monitor_addr:
                self.send(self.monitor_addr, self.history[-1])

        elif isinstance(msg, DetachMonitorMsg):
            self.monitor_addr = None
                


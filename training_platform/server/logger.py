#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from training_platform.server.common import *

class Logger(Actor):
    def __init__(self):
        super().__init__()
        self.history = []
        self.monitor_addr = None

    def receiveMessage(self, msg, sender):
        if isinstance(msg, InitLoggerMsg):
            pass

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
                


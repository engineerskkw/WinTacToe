from thespian.actors import *
from training_platform.common import *

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
            self.send(self.monitor_addr, MonitorJoinAcknowledgement())
            for log_msg in self.history:
                self.send(self.monitor_addr, log_msg)

        elif isinstance(msg, LogMsg):
            self.history.append(msg)
            if self.monitor_addr:
                self.send(self.monitor_addr, self.history[-1])

        elif isinstance(msg, DetachMonitorMsg):
            self.monitor_addr = None
                


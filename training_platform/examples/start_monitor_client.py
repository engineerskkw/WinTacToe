# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from training_platform import MonitorClient
from training_platform.server.common import LoggingLevel

if __name__ == '__main__':
    # Every log message has it logging level
    # There are few possible loging levels, e.g.:
    #   -> PLATFORM_COMMUNICATION_MESSAGES
    #   -> GAME_EVENTS
    #   -> DEBUG
    # Monitor client can work on different logging levels
    # It takes list of levels that it will log as an constructor parameter

    # For example
    logging_levels = list(LoggingLevel) # It's a list of all logging levels
    loggins_levels = [LoggingLevel.GAME_EVENTS] # It's a list containing only one logging level GAME_EVENTS
    monitor = MonitorClient(loggins_levels)
    print("Monitor Client has started!")
    monitor.start_monitoring()
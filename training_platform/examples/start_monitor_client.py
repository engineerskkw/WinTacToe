from training_platform import MonitorClient
from training_platform.common import LoggingLevel

if __name__ == '__main__':
    # Every log message has it's logging level
    # There are few possible loging levels, e.g.:
    #   -> PLATFORM_COMMUNICATION_MESSAGES
    #   -> GAME_EVENTS
    #   -> DEBUG
    # Monitor client can work on different logging levels
    # It takes list of levels that it will log as an constructor parameter

    # For example
    # logging_levels = list(LoggingLevel) # It's a list of all logging levels
    # It's a list containing only one logging level PLATFORM_COMMUNICATION_MESSAGES
    # logging_levels = [LoggingLevel.PLATFORM_COMMUNICATION_MESSAGES]
    # And it's example of list usefull for debuging
    # logging_levels = [LoggingLevel.PLATFORM_COMMUNICATION_MESSAGES, LoggingLevel.DEBUG]
    
    logging_levels = [LoggingLevel.GAME_EVENTS]
    monitor = MonitorClient(logging_levels)
    print("Monitor Client has started!")
    monitor.start_monitoring()

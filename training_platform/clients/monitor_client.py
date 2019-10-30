#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
PROJECT_ROOT_PATH = "./../../"
sys.path.append(os.path.join(os.path.dirname(__file__), PROJECT_ROOT_PATH))
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from training_platform.server.common import *
from training_platform.server.service import GameManager, MatchMaker
from training_platform.server.logger import Logger

import signal
import sys


def signal_handler(sig, frame):
    asys.tell(logger_addr, DetachMonitorMsg())
    print('\nDetached from logger')
    sys.exit(0)


if __name__ == '__main__':
    # signal.signal(signal.SIGINT, signal_handler)
    asys = ActorSystem('multiprocTCPBase')
    match_maker_addr = asys.createActor(MatchMaker, globalName="MatchMaker")
    game_manager_addr = asys.createActor(GameManager, globalName="GameManager")
    logger_addr = asys.createActor(Logger, globalName="Logger")

    # Server joining
    asys.tell(logger_addr, JoinMonitorMsg())

    # Messages dispatcher
    while True:
        msg = asys.listen()
        if isinstance(msg, LogMsg):
            print(msg)

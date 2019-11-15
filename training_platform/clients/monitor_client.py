#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import signal
import sys
from thespian.actors import *

from training_platform.server.common import *
from training_platform.server.service import GameManager, MatchMaker
from training_platform.server.logger import Logger


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

    # EnvironmentServer joining
    asys.tell(logger_addr, JoinMonitorMsg())

    # Messages dispatcher
    while True:
        msg = asys.listen()
        if isinstance(msg, LogMsg):
            print(msg)

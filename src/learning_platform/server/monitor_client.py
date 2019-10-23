from common import *
from service import GameManager, MatchMaker
import signal
import sys
from logger import Logger

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

from common import *
from service import *

if __name__ == '__main__':
    asys = ActorSystem('multiprocTCPBase')
    match_maker_addr = asys.createActor(MatchMaker, globalName="MatchMaker")
    game_manager_addr = asys.createActor(GameManager, globalName="GameManager")
    logger_addr = asys.createActor(GameManager, globalName="Logger")

    # Server joining
    asys.tell(logger_addr, JoinMonitorMsg())

    # Messages dispatcher
    while(True):
        msg = asys.listen()
        if isinstance(msg, LogMsg):
            print(msg)

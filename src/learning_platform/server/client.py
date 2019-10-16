from common import *
import sys

if __name__ == '__main__':
    player_name = sys.argv[1]
    player_mark = int(sys.argv[2])
    player = Player(player_name, player_mark)
    print(f"[Client]: Joining as: {player}")

    asys = ActorSystem('multiprocTCPBase')
    client0 = asys.createActor(Client)
    asys.tell(client0, InitClientMsg(player, Agent()))

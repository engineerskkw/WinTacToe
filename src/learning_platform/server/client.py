from common import *
import sys

if __name__ == '__main__':
    argc = len(sys.argv)
    if not argc == 3:
        print(f"Invalid arguments number: {argc-1} (should be 2)")
        print("Try again with following arguments:")
        print("python client.py <player_name> <player_mark>")
        exit()

    player_name = sys.argv[1]
    player_mark = int(sys.argv[2])
    player = Player(player_name, player_mark)
    print(f"[Client]: Joining as: {player}")

    asys = ActorSystem('multiprocTCPBase')
    client0 = asys.createActor(Client)
    asys.ask(client0, InitClientMsg(player, Agent()))


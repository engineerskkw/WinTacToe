from common import *
import sys

if __name__ == '__main__':
    argc = len(sys.argv)
    if not argc == 4:
        print(f"Invalid arguments number: {argc-1} (should be 3)")
        print("Try again with following arguments:")
        print("python start_server.py <no_of_players> <board_size> <marks_required> ")
        exit()
    no_of_players = int(sys.argv[1])
    board_size = int(sys.argv[2])
    marks_required = int(sys.argv[3])
    print("[Server]: starting with following engine parameters:")
    print(f"[Server]: no_of_players: {no_of_players}")
    print(f"[Server]: board_size: {board_size}")
    print(f"[Server]: marks_required: {marks_required}")

    asys = ActorSystem('multiprocTCPBase')
    game_manager = asys.createActor(GameManager, globalName="GameManager")
    asys.tell(game_manager, InitGameManagerMsg(TicTacToeEngine(no_of_players, board_size, marks_required)))
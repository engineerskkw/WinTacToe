

from environments.tic_tac_toe.tic_tac_toe_engine import TicTacToeEngine
from training_platform.common import *
from training_platform import EnvironmentServer


if __name__ == '__main__':
    # Commandline parameters parsing
    argc = len(sys.argv)
    if not argc == 4:
        print(f"Invalid arguments number: {argc-1} (should be 3)")
        print("Try again with following arguments:")
        print("python start_server.py <no_of_players> <board_size> <marks_required> ")
        exit()
    no_of_players = int(sys.argv[1])
    board_size = int(sys.argv[2])
    marks_required = int(sys.argv[3])

    server = EnvironmentServer(TicTacToeEngine(no_of_players, board_size, marks_required))

    input("Press ENTER after all players have joined")

    server.start()
    print("Episode has ended!")
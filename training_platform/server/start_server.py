#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from thespian.actors import *

from game_app.games.tic_tac_toe.engine.tic_tac_toe_engine import TicTacToeEngine
from training_platform.server.common import *
from training_platform.server.service import GameManager


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

    # Server starting
    asys = ActorSystem('multiprocTCPBase')
    game_manager = asys.createActor(GameManager, globalName="GameManager")
    asys.tell(game_manager, InitGameManagerMsg(TicTacToeEngine(no_of_players, board_size, marks_required)))
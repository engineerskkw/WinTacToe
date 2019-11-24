# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os
REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from training_platform import EnvironmentServer
from environments.tic_tac_toe.tic_tac_toe_engine import TicTacToeEngine

if __name__ == '__main__':
    server = EnvironmentServer(TicTacToeEngine(2, 3, 3))

    input("Press ENTER after all players have joined")

    for i in range(100):
        print(f"Game number: {i}")
        server.start()

    server.shutdown()
    print("Training platform has been shutdowned!")
# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from training_platform import EnvironmentServer
from training_platform.server.environment_server import AccessingUninitializedEnvServerError

if __name__ == '__main__':
    try:
        server = EnvironmentServer()
        server.shutdown()
        print("Training platform shutdown completed successfully!")
    except AccessingUninitializedEnvServerError:
        print("Nothing to shutdown.")


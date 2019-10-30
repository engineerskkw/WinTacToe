#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
PROJECT_ROOT_PATH = "./../../"
sys.path.append(os.path.join(os.path.dirname(__file__), PROJECT_ROOT_PATH))
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from training_platform.server.common import *

if __name__ == '__main__':
    ActorSystem('multiprocTCPBase').shutdown()

# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys
import os
REL_PROJECT_ROOT_PATH = "./../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from copy import deepcopy


def return_deepcopy(func):
    def deepcopy_wrapper(*args, **kwargs):
        return deepcopy(func(*args, **kwargs))

    return deepcopy_wrapper

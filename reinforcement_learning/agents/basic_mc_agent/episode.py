# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from reinforcement_learning.base.base_action import BaseAction
from reinforcement_learning.base.base_state import BaseState


class Episode(list):
    def __init__(self, the_list=[]):
        super().__init__(the_list)

    def __str__(self):
        representation = ''
        for element in self:
            if isinstance(element, float):
                representation += 'Reward:\n'
            elif isinstance(element, BaseState):
                representation += 'State:\n'
            elif isinstance(element, BaseAction):
                representation += 'Action:\n'
            else:
                raise Exception("Ivalid episode's element error")
            representation += str(element)
            representation += '\n\n'
        return representation

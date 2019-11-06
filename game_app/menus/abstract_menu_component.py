#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

from game_app.abstract_component import AbstractComponent


class AbstractMenuComponent(AbstractComponent):
    def __init__(self):
        self._scene = None
        self._logic = None

    def render(self):
        self._scene.render()

    def handle_event(self, event):
        self._logic.handle_event(event)

    def loop(self):
        pass

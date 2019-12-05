# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import time
from threading import Thread
from queue import SimpleQueue


class KillFakePlayerCommand:
    pass


class RestartFakePlayerCommand:
    def __init__(self, component):
        self.component = component


class ActionFakePlayerCommand:
    def __init__(self, action, component):
        self.action = action
        self.component = component


def agent_fake_player(commands_queue):
    while True:
        command = commands_queue.get(block=True, timeout=None)

        if isinstance(command, KillFakePlayerCommand):
            break

        if isinstance(command, RestartFakePlayerCommand):
            command.component.game_ended = False
            continue

        if isinstance(command, ActionFakePlayerCommand) and not command.component.game_ended:
            time.sleep(0.4)
            if not command.component.game_ended:
                command.action()

def init_agent_fake_player():
    commands_queue = SimpleQueue()
    agent_fake_player_thread = Thread(target=agent_fake_player, args=(commands_queue,))
    agent_fake_player_thread.start()
    return commands_queue

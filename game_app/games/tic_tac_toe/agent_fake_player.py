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
            command.component.show_match_ended = False
            continue

        if isinstance(command, ActionFakePlayerCommand) and not command.component.show_match_ended:
            for i in range(5):
                time.sleep(0.1)
                if command.component.next_moves_to_show != 0:
                    break
            while command.component.show_match_paused and not command.component.show_match_ended \
                    and command.component.next_moves_to_show == 0:
                time.sleep(0.1)
            if not command.component.show_match_ended:
                if command.component.next_moves_to_show != 0:
                    command.component.next_moves_to_show -= 1
                command.action()


def init_agent_fake_player():
    commands_queue = SimpleQueue()
    agent_fake_player_thread = Thread(target=agent_fake_player, args=(commands_queue,))
    agent_fake_player_thread.start()
    return commands_queue

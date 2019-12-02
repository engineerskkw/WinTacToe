# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

REL_PROJECT_ROOT_PATH = "./../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import time
import pygame
from enum import Enum
from pygame.mixer import Sound
from threading import Thread
from queue import SimpleQueue


class Hardness(Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2


class TurnState(Enum):
    NOT_YOUR_TURN = 0
    YOUR_TURN = 1


class Components(Enum):
    MAIN_MENU = 1
    TIC_TAC_TOE_LAUNCH_MENU = 2
    TIC_TAC_TOE = 3
    SETTINGS = 4


class Settings(Enum):
    COLOR = 1
    MUSIC = 2
    SOUNDS = 3


class ColorMode(Enum):
    LIGHT = 1
    DARK = 2


class SwitchMusicCommand:
    def __init__(self, music_file_path):
        self.music_file_path = music_file_path


class PlaySoundStoppingMusicCommand:
    def __init__(self, sound_file_path, music_on):
        self.sound = Sound(sound_file_path)
        self.music_on = music_on


class StopMusicCommand:
    pass


class StopMusicPlayerCommand:
    pass


def music_player(commands_queue):
    while True:
        command = commands_queue.get(block=True, timeout=None)

        if isinstance(command, SwitchMusicCommand):
            pygame.mixer.music.fadeout(700)
            pygame.mixer.music.load(command.music_file_path)
            pygame.mixer.music.play(loops=-1)

        if isinstance(command, PlaySoundStoppingMusicCommand):
            pygame.mixer.music.fadeout(600)
            time.sleep(0.3)
            sound_length = command.sound.get_length()
            command.sound.play()
            time.sleep(sound_length)
            if command.music_on:
                pygame.mixer.music.play(loops=-1)

        if isinstance(command, StopMusicCommand):
            pygame.mixer.music.stop()

        if isinstance(command, StopMusicPlayerCommand):
            break


def init_music_player():
    commands_queue = SimpleQueue()
    music_player_thread = Thread(target=music_player, args=(commands_queue,))
    music_player_thread.start()
    return commands_queue

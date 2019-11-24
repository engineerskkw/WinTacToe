# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

REL_PROJECT_ROOT_PATH = "./../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import time
import threading
import pygame
from enum import Enum
from pygame.mixer import Sound


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


class MusicSwitcher(threading.Thread):
    def __init__(self, file_path, music_on=True):
        threading.Thread.__init__(self)
        self._file_path = file_path
        self._music_on = music_on

    def run(self):
        pygame.mixer.music.fadeout(800)
        if self._music_on:
            pygame.mixer.music.load(self._file_path)
            pygame.mixer.music.play(loops=-1)


class SoundPlayer(threading.Thread):
    def __init__(self, sound_path, should_stop_music):
        threading.Thread.__init__(self)
        self._sound = Sound(sound_path)
        self._should_stop_music = should_stop_music

    def run(self):
        if self._should_stop_music:
            self.play_sound_stopping_music()
        else:
            self.play_sound()

    def play_sound_stopping_music(self):
        pygame.mixer.music.fadeout(600)
        time.sleep(0.3)
        self._sound.play()
        sound_length = self._sound.get_length()
        time.sleep(sound_length)
        pygame.mixer.music.play()

    def play_sound(self):
        self._sound.play()

#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
PROJECT_ROOT_PATH = "./../"
sys.path.append(os.path.join(os.path.dirname(__file__), PROJECT_ROOT_PATH))
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import time
import threading
import pygame
from enum import Enum
from pygame.mixer import Sound


class Components(Enum):
    MAIN_MENU = 1
    TIC_TAC_TOE = 2


class MusicSwitcher(threading.Thread):
    def __init__(self, file_path):
        threading.Thread.__init__(self)
        self._file_path = file_path

    def run(self):
        pygame.mixer.music.fadeout(800)
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


from enum import Enum
import threading
import pygame


class Extensions(Enum):
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

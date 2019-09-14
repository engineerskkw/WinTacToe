from ....common_helper import MusicSwitcher
from ...abstract_extension import AbstractExtension
from .main_menu_logic import MainMenuLogic
from .main_menu_scene import MainMenuScene
import pygame


class MainMenuExtension(AbstractExtension):
    def __init__(self, app):
        self.app = app
        self._logic = MainMenuLogic(self)
        self._scene = MainMenuScene(self)
        MusicSwitcher("resources/sounds/common/SneakySnitch.mp3").start()


    def render(self, screen):
        self._scene.render(screen)

    def handle_event(self, event):
        self._logic.handle_event(event)

    def get_buttons(self):
        return self._logic.buttons

    def loop(self):
        pass

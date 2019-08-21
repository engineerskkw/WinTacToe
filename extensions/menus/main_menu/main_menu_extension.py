from ...abstract_extension import AbstractExtension
from .main_menu_scene import MainMenuScene
from .main_menu_logic import MainMenuLogic


class MainMenuExtension(AbstractExtension):
    def __init__(self):
        self.scene = MainMenuScene()
        self.logic = MainMenuLogic()
        self.background_color = (55, 55, 55)

    def render(self, screen):
        self.scene.render(screen)

    def handle_event(self, event):
        print(event.type)




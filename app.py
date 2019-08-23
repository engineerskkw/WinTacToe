import sys
import pygame
from pygame import Color, Surface
from pygame.locals import *
from extensions.menus.main_menu import MainMenuExtension
from extensions.games.tic_tac_toe import tic_tac_toe_logic


class Player:
    pass


class TicTacToeLogic:
    pass




class App:
    def __init__(self):
        self.extension = MainMenuExtension()
        self.running = True
        self.screen = None
        self.size = self.weight, self.height = 1280, 720
        self.background_color = (55, 55, 55)

    def launch(self):
        pygame.init()
        # logo = pygame.image.load("../resources/images/common/logo.png")
        # pygame.display.set_icon(logo)
        pygame.display.set_caption("WinTacToe")
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.running = True

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

        self.extension.handle_event(event)


    def loop(self):
        pass

    def render(self):
        self.extension.render(self.screen)

    def cleanup(self):
        pygame.quit()

    def execute(self):
        print(3)
        self.launch()

        while self.running:

            for event in pygame.event.get():
                self.handle_event(event)

            self.loop()

            self.render()

        self.cleanup()


def main():
    print("2")
    App().execute()


if __name__ == "__main__":
    print("1")
    tic_tac_toe_logic.TicTacToeLogic()
    main()

import sys
import pygame
from pygame import Color, Surface
from pygame.locals import *


class Player:
    pass


class TicTacToeLogic:
    pass


class TicTacToeScene:
    def __init__(self):
        pass


class MenuScene:
    pass


class App:
    def __init__(self):
        self._scene = 1
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

    def loop(self):
        pass

    def render(self):
        print(pygame.display.get_surface().get_size())
        background = pygame.Surface(self.screen.get_size())
        background.fill(self.background_color)
        self.screen.blit(background, (0, 0))

        pygame.display.flip()

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
    main()

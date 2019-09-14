import pygame
from pygame.mixer import Sound
from .extensions import MainMenuExtension
from .extensions import TicTacToeExtension
from .common_helper import Extensions


class App:
    def __init__(self):
        self._extensions = {
            Extensions.MAIN_MENU: MainMenuExtension,
            Extensions.TIC_TAC_TOE: TicTacToeExtension,
        }
        self._current_extension = None
        self._running = False
        self._screen = None
        self._size = 1280, 720
        self._block_events = False

    def _launch(self):
        pygame.init()
        pygame.mixer.init()
        # xd = Sound("resources/sounds/tic_tac_toe/hitsound.wav")
        # xd.play()

        # logo = pygame.image.load("../resources/images/common/logo.png")
        # pygame.display.set_icon(logo)
        pygame.display.set_caption("WinTacToe")
        self._screen = pygame.display.set_mode(self._size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self._current_extension = MainMenuExtension(self)

    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if not self._block_events:
            self._current_extension.handle_event(event)

    def _loop(self):
        self._current_extension.loop()

    def _render(self):
        self._current_extension.render(self._screen)

    def _cleanup(self):
        pygame.quit()

    def switch_extension(self, extension):
        self._block_events = True
        self._current_extension = self._extensions[extension](self)
        pygame.event.clear()
        self._block_events = False

    def execute(self):
        self._launch()

        while self._running:
            for event in pygame.event.get():
                self._handle_event(event)
            self._loop()
            self._render()

        self._cleanup()

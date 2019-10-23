import pygame
from .components import MainMenuComponent, TicTacToeComponent
from .common_helper import Components


class Application:
    def __init__(self):
        self._components = {
            Components.MAIN_MENU: MainMenuComponent,

            Components.TIC_TAC_TOE: TicTacToeComponent,
        }
        self._current_component = None
        self._running = False
        self.screen = None
        self._size = 1280, 720
        self._block_events = False

    def _launch(self):
        pygame.mixer.init(buffer=256)
        pygame.init()

        logo = pygame.image.load("resources/images/common/logo.png")
        pygame.display.set_icon(logo)

        pygame.display.set_caption("WinTacToe")
        self.screen = pygame.display.set_mode(self._size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self._current_component = MainMenuComponent(self)

    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if not self._block_events:
            self._current_component.handle_event(event)

    def _loop(self):
        self._current_component.loop()

    def _render(self):
        self._current_component.render()

    def _cleanup(self):
        pygame.quit()

    def switch_component(self, component):
        self._block_events = True
        self._current_component = self._components[component](self)
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

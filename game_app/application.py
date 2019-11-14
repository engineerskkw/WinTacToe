#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import subprocess
from thespian.actors import ActorSystem

from game_app.games.tic_tac_toe.tic_tac_toe_component import TicTacToeComponent
from game_app.menus.main_menu.main_menu_component import MainMenuComponent
from game_app.menus.tic_tac_toe_launch_menu.tic_tac_toe_launch_menu_component import TicTacToeLaunchMenuComponent
from game_app.common_helper import Components
from training_platform.server.service import GameManager


class Application:
    def __init__(self):
        self._components = {
            Components.MAIN_MENU: MainMenuComponent,

            Components.TIC_TAC_TOE_LAUNCH_MENU: TicTacToeLaunchMenuComponent,
            Components.TIC_TAC_TOE: TicTacToeComponent,
        }
        self._current_component = None
        self._running = False
        self.screen = None
        self._size = 1280, 720
        self._block_events = False

        self.actorSystem = ActorSystem('multiprocTCPBase')
        self.tic_tac_toe_game_manager = self.actorSystem.createActor(GameManager, globalName="GameManager")

    def _launch(self):
        pygame.mixer.init(buffer=256)
        pygame.init()

        logo = pygame.image.load(os.path.join(ABS_PROJECT_ROOT_PATH, "game_app/resources/images/common/logo.png"))
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
        ActorSystem('multiprocTCPBase').shutdown()
        pygame.quit()

    def switch_component(self, component, **args):
        ev = pygame.event.Event(pygame.USEREVENT, {'new_game_state': 1})
        pygame.event.post(ev)
        self._block_events = True
        if args:
            self._current_component = self._components[component](self, **args)
        else:
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

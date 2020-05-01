import os
from global_constants import ABS_PROJECT_ROOT_PATH
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pickle
from game_app.games.tic_tac_toe.tic_tac_toe_component import TicTacToeComponent
from game_app.menus.main_menu.main_menu_component import MainMenuComponent
from game_app.menus.settings.settings_component import SettingsComponent
from game_app.menus.credits.credits_component import CreditsComponent
from game_app.menus.tic_tac_toe_launch_menu.tic_tac_toe_launch_menu_component import TicTacToeLaunchMenuComponent
from game_app.common.common_helper import Components, Settings, init_music_player, SwitchMusicCommand, StopMusicCommand, \
    StopMusicPlayerCommand, PlaySoundStoppingMusicCommand


class Application:
    def __init__(self):
        self._components = {
            Components.MAIN_MENU: MainMenuComponent,
            Components.SETTINGS: SettingsComponent,
            Components.CREDITS: CreditsComponent,
            Components.TIC_TAC_TOE_LAUNCH_MENU: TicTacToeLaunchMenuComponent,
            Components.TIC_TAC_TOE: TicTacToeComponent,
        }
        self._current_component = None
        self._running = False
        self.screen = None
        self._size = 1280, 720
        self._block_events = False
        with open(os.path.join(ABS_PROJECT_ROOT_PATH, "test_game_app/settings.cfg"), 'rb') as settings_file:
            self.settings = pickle.load(settings_file)
        self._music_player_commands_queue = init_music_player()

    def _launch(self):
        pygame.mixer.init(buffer=256)
        pygame.init()

        logo = pygame.image.load(os.path.join(ABS_PROJECT_ROOT_PATH, "test_game_app/resources/images/common_building_blocks/logo.png"))
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
        self._music_player_commands_queue.put(StopMusicPlayerCommand())
        if isinstance(self._current_component, TicTacToeComponent) and self._current_component.spectator_mode:
            self._current_component.kill_fake_player()
        pygame.quit()

    def exit_application(self):
        self._running = False

    def switch_component(self, component, **args):
        ev = pygame.event.Event(pygame.USEREVENT, {'new_game_state': 1})
        pygame.event.post(ev)
        self._block_events = True
        self._current_component = self._components[component](self, **args)
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

    def switch_music(self, music_file_path):
        if self.settings[Settings.MUSIC]:
            self._music_player_commands_queue.put(SwitchMusicCommand(music_file_path))
        else:
            self._music_player_commands_queue.put(StopMusicCommand())

    def play_sound_stopping_music(self, sound_file_path):
        if self.settings[Settings.SOUNDS]:
            self._music_player_commands_queue.put(
                PlaySoundStoppingMusicCommand(sound_file_path, self.settings[Settings.MUSIC]))

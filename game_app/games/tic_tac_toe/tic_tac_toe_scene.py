#BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
#-------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#


import pygame
from pygame.rect import Rect
from pygame.mixer import Sound

from game_app.common_helper import SoundPlayer


symbols = {
    0: 'X',
    1: 'O',
    2: 'A',
}


class TicTacToeScene:
    def __init__(self, component, screen, board_size):
        self._component = component
        self._screen = screen
        self._board_size = board_size

        self._background_color = (0, 0, 0)
        self._game_over_displayed = False
        self._winner = None

        self._background_displayed = False

        self._square_size = 720 // self._board_size
        self.buttons = []
        for row in range(self._board_size):
            self.buttons.append([])
            for column in range(self._board_size):
                self.buttons[row].append(TicTacToeButton(self._component,
                                                         (280 + column * self._square_size, row * self._square_size),
                                                         self._square_size,
                                                         (row, column)))
        self.restart_button = RectangularTextButton("Restart",
                                                    lambda: self._component.restart(),
                                                    (1040, 20),
                                                    (200, 50))

        self.main_menu_button = RectangularTextButton("MainMenu",
                                                      lambda: self._component.back_to_menu(),
                                                      (1040, 90),
                                                      (200, 50))

    def render(self):
        if not self._game_over_displayed and self._component.winnings:
            buttons = sum(self.buttons, [])
            [button.set_disabled() for button in buttons]
            for winning in self._component.winnings:
                [self.buttons[x][y].set_winning() for (x,y) in winning.points_included]

            font = pygame.font.Font(None, 50)
            self._winner = symbols[self._component.winnings[0].mark]
            self._screen.blit(font.render("The winner is: " + self._winner, True, (100, 100, 100)), (5, 5))
            self._game_over_displayed = True
            resource_path = os.path.join(ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/tic_tac_toe/victory.wav")
            SoundPlayer(resource_path, True).start()

        self._display_background(self._screen)

        for row in range(self._board_size):
            for column in range(self._board_size):
                figure = self.buttons[row][column].get_figure()
                figures_color = self.buttons[row][column].get_color(pygame.mouse.get_pos(),
                                                                    pygame.mouse.get_pressed()[0] == 1)
                pygame.draw.rect(self._screen, figures_color, figure)
                frame_size = max(min(self._square_size // 30, 5), 1)
                pygame.draw.rect(self._screen, self.buttons[row][column].get_frame_color(), figure, frame_size)
                self._screen.blit(self.buttons[row][column].text, self.buttons[row][column].get_text_position())

        restart_button_figure = self.restart_button.get_figure()
        restart_button_color = self.restart_button.get_color(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0] == 1)
        pygame.draw.rect(self._screen, restart_button_color, restart_button_figure)
        pygame.draw.rect(self._screen, self.restart_button.get_frame_color(), restart_button_figure, 3)
        self._screen.blit(self.restart_button.text, self.restart_button.get_text_position())

        main_menu_button_figure = self.main_menu_button.get_figure()
        main_menu_button_color = self.main_menu_button.get_color(pygame.mouse.get_pos(),
                                                                 pygame.mouse.get_pressed()[0] == 1)
        pygame.draw.rect(self._screen, main_menu_button_color, main_menu_button_figure)
        pygame.draw.rect(self._screen, self.main_menu_button.get_frame_color(), main_menu_button_figure, 3)
        self._screen.blit(self.main_menu_button.text, self.main_menu_button.get_text_position())

        pygame.display.flip()

    def _display_background(self, screen):
        if not self._background_displayed:
            background = pygame.Surface(screen.get_size())
            background.fill(self._background_color)
            screen.blit(background, (0, 0))
            self._background_displayed = True

    def handle_state_changed(self, new_game_state):
        for row in range(self._board_size):
            for col in range(self._board_size):
                if new_game_state[row, col] != self.buttons[row][col].mark:
                    self.buttons[row][col].marked_by_enemy(new_game_state[row, col])


class RectangularButton:
    def __init__(self, position, size):
        self._position = position
        self._size = size

        self._base_color = (0, 0, 0)
        self._hovered_color = (50, 50, 50)
        self._pressed_color = (40, 40, 40)
        self._frame_color = (255, 255, 255)

    def contains_point(self, point):
        return self._position[0] < point[0] < self._position[0] + self._size[0] \
               and self._position[1] < point[1] < self._position[1] + self._size[1]

    def get_figure(self):
        return Rect(self._position, self._size)

    def get_color(self, mouse_position, is_mouse_pressed):
        if not self.contains_point(mouse_position):
            return self._base_color
        return self._pressed_color if is_mouse_pressed else self._hovered_color

    def get_frame_color(self):
        return self._frame_color


class RectangularTextButton(RectangularButton):
    def __init__(self, text, action, position, size):
        super().__init__(position, size)
        self._action = action
        pygame.font.init()
        font = pygame.font.Font(None, 50)
        self.text = font.render(text, True, (255, 255, 255))
        resource_path = os.path.join(ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/tic_tac_toe/move_sound_1.wav")
        self.click_sound = Sound(resource_path)

    def get_text_position(self):
        x = self._position[0] + self._size[0] // 2 - self.text.get_width() // 2
        y = self._position[1] + self._size[1] // 2 - self.text.get_height() // 2
        return x, y

    def on_pressed(self):
        self.click_sound.play()
        self._action()


class TicTacToeButton(RectangularButton):
    def __init__(self, component, position, size, game_position):
        super().__init__(position, (size, size))
        pygame.font.init()
        self._component = component
        self._game_position = game_position
        self._is_disabled = False
        self._is_winning = False
        self._disabled_color = (0, 100, 0)
        self._winning_color = (100, 100, 100)
        self._mark_color = (255, 255, 255)
        self.mark = -1
        self.set_text("")

        self.players_sounds = {
            0: Sound(os.path.join(ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/tic_tac_toe/move_sound_1.wav")),
            1: Sound(os.path.join(ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/tic_tac_toe/move_sound_2.wav")),
            2: Sound(os.path.join(ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/tic_tac_toe/move_sound_1.wav")),
        }

    def on_pressed(self):
        if self._is_disabled:
            # TODO mozna zrobic dzwiek zlego zagrania
            return
        self.players_sounds[0].play()
        self._component.step(self._game_position)
        self.set_text(symbols[0])
        self.mark = 0
        self.set_disabled()

    def marked_by_enemy(self, enemy_mark):
        if enemy_mark == -1:
            self._is_disabled = False
            self.set_text("")
            self.mark = -1
            return
        if self._is_disabled:
            return
        self.set_text(symbols[1])
        self.mark = enemy_mark
        self.set_disabled()

    def set_text(self, text):
        font = pygame.font.Font(None, self._size[0])
        self.text = font.render(text, True, self._mark_color)

    def get_text_position(self):
        x = self._position[0] + self._size[0] // 2 - self.text.get_width() // 2
        y = self._position[1] + self._size[1] // 2 - self.text.get_height() // 2
        return x, y

    def get_color(self, mouse_position, is_mouse_pressed):
        if self._is_winning:
            return self._winning_color
        if self._is_disabled:
            return self._disabled_color
        return super().get_color(mouse_position, is_mouse_pressed)

    def set_disabled(self):
        self._is_disabled = True

    def set_winning(self):
        self._is_winning = True

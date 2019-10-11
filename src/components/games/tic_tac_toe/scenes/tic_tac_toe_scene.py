from pygame.mixer import Sound
from src.common_helper import SoundPlayer, Components
from pygame.rect import Rect
import pygame

symbols = {
    0: 'X',
    1: 'O',
    2: 'A',
}

players_sounds = (
    Sound("resources/sounds/tic_tac_toe/move_sound_1.wav"),
    Sound("resources/sounds/tic_tac_toe/move_sound_2.wav"),
    Sound("resources/sounds/tic_tac_toe/move_sound_1.wav"),
)


class TicTacToeScene:
    def __init__(self, env):
        self._env = env
        self._background_color = (0, 0, 0)  # (200, 200, 200)
        self._finished = False
        self._winner = None

        self._background_displayed = False

        board = self._env.env.board
        self.board_size = board.size

        self.square_size = 720 // self.board_size
        self.buttons = []
        for row in range(self.board_size):
            self.buttons.append([])
            for column in range(self.board_size):
                self.buttons[row].append(TicTacToeButton(self._env,
                                                         (280 + column * self.square_size, row * self.square_size),
                                                         self.square_size,
                                                         (row, column)))
        self.restart_button = RectangularTextButton("Restart",
                                                    lambda: self._env.reset(),
                                                    (1040, 20),
                                                    (200, 50))

        self.main_menu_button = RectangularTextButton("MainMenu",
                                                      lambda: self._env.app.switch_component(Components.MAIN_MENU),
                                                      (1040, 90),
                                                      (200, 50))

    def render(self, screen):
        if not self._finished and self._env.current_winnings:
            buttons = sum(self.buttons, [])
            [button.set_disabled() for button in buttons]
            for winning in self._env.current_winnings:
                xs = list(range(winning.starting_point[0], winning.ending_point[0] + 1)) \
                    if winning.starting_point[0] < winning.ending_point[0] \
                    else list(range(winning.starting_point[0], winning.ending_point[0] - 1, -1))
                ys = list(range(winning.starting_point[1], winning.ending_point[1] + 1)) \
                    if winning.starting_point[1] < winning.ending_point[1] \
                    else list(range(winning.starting_point[1], winning.ending_point[1] - 1, -1))
                xs = xs * len(ys) if len(xs) == 1 else xs
                ys = ys * len(xs) if len(ys) == 1 else ys
                [self.buttons[i][j].set_winning() for i, j in zip(xs, ys)]
            self._winner = symbols[self._env.current_winnings[0].mark]
            self._finished = True
            SoundPlayer("resources/sounds/tic_tac_toe/victory.wav", True).start()

        self._display_background(screen)

        for row in range(self.board_size):
            for column in range(self.board_size):
                figure = self.buttons[row][column].get_figure()
                figures_color = self.buttons[row][column].get_color(pygame.mouse.get_pos(),
                                                                    pygame.mouse.get_pressed()[0] == 1)
                pygame.draw.rect(screen, figures_color, figure)
                frame_size = max(min(self.square_size // 30, 5), 1)
                pygame.draw.rect(screen, self.buttons[row][column].get_frame_color(), figure, frame_size)
                screen.blit(self.buttons[row][column].text, self.buttons[row][column].get_text_position())

        if self._finished:
            font = pygame.font.Font(None, 50)
            screen.blit(font.render("The winner is: " + self._winner, True, (100, 100, 100)), (5, 5))

        restart_button_figure = self.restart_button.get_figure()
        restart_button_color = self.restart_button.get_color(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0] == 1)
        pygame.draw.rect(screen, restart_button_color, restart_button_figure)
        pygame.draw.rect(screen, self.restart_button.get_frame_color(), restart_button_figure, 3)
        screen.blit(self.restart_button.text, self.restart_button.get_text_position())

        main_menu_button_figure = self.main_menu_button.get_figure()
        main_menu_button_color = self.main_menu_button.get_color(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0] == 1)
        pygame.draw.rect(screen, main_menu_button_color, main_menu_button_figure)
        pygame.draw.rect(screen, self.main_menu_button.get_frame_color(), main_menu_button_figure, 3)
        screen.blit(self.main_menu_button.text, self.main_menu_button.get_text_position())

        pygame.display.flip()

    def _display_background(self, screen):
        if not self._background_displayed:
            background = pygame.Surface(screen.get_size())
            background.fill(self._background_color)
            screen.blit(background, (0, 0))
            self._background_displayed = True


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

    def get_text_position(self):
        x = self._position[0] + self._size[0] // 2 - self.text.get_width() // 2
        y = self._position[1] + self._size[1] // 2 - self.text.get_height() // 2
        return x, y

    def on_pressed(self):
        self._action()


class TicTacToeButton(RectangularButton):
    def __init__(self, env, position, size, game_position):
        super().__init__(position, (size, size))
        pygame.font.init()
        self._env = env
        self._game_position = game_position
        self._is_disabled = False
        self._is_winning = False
        self._disabled_color = (0, 0, 0)
        self._winning_color = (100, 100, 100)
        self._mark_color = (255, 255, 255)

        self.set_text("")

    def on_pressed(self):
        if self._is_disabled:
            return
        _, _, _, _, player = self._env.step(self._game_position, None)
        players_sounds[player.mark].play()
        self.set_text(symbols[player.mark])
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

# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os

REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#

import pygame
from pygame import Rect


class RectangularButton:
    def __init__(self, action, position, size):
        self._action = action
        self._position = position
        self._size = size

        self._base_color = (200, 0, 0)
        self._hovered_color = (255, 0, 0)
        self._pressed_color = (150, 0, 0)

    def contains_point(self, point):
        return self._position[0] < point[0] < self._position[0] + self._size[0] \
               and self._position[1] < point[1] < self._position[1] + self._size[1]

    def get_figure(self):
        return Rect(self._position, self._size)

    def get_color(self, mouse_position, is_mouse_pressed):
        if not self.contains_point(mouse_position):
            return self._base_color
        return self._pressed_color if is_mouse_pressed else self._hovered_color

    def on_pressed(self):
        self._action()


class RectangularTextButton(RectangularButton):
    def __init__(self, text, action, position, size):
        super().__init__(action, position, size)

        pygame.font.init()
        font = pygame.font.Font(None, 50)
        self.text = font.render(text, True, (255, 255, 255))

    def get_text_position(self):
        x = self._position[0] + self._size[0] // 2 - self.text.get_width() // 2
        y = self._position[1] + self._size[1] // 2 - self.text.get_height() // 2
        return x, y


class RectangularChoiceButton(RectangularTextButton):
    def __init__(self, text, action, position, size, chosen):
        super().__init__(text, action, position, size)
        self._chosen = chosen

        self._chosen_base_color = (0, 0, 0)
        self._chosen_hovered_color = (30, 0, 0)
        self._chosen_pressed_color = (50, 0, 0)

    def on_pressed(self):
        self._action()
        self._chosen = True

    def get_color(self, mouse_position, is_mouse_pressed):
        if self._chosen:
            if not self.contains_point(mouse_position):
                return self._chosen_base_color
            return self._chosen_pressed_color if is_mouse_pressed else self._chosen_hovered_color
        else:
            if not self.contains_point(mouse_position):
                return self._base_color
            return self._pressed_color if is_mouse_pressed else self._hovered_color

    def set_chosen(self, new_chosen):
        self._chosen = new_chosen

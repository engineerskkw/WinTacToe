import pygame
from pygame import Rect


class RectangularButton:
    def __init__(self, action, position, size):
        self._action = action
        self._position = position
        self._size = size

        self._base_color = (200, 0, 0)
        self._hovered_color = (255, 0, 0)
        self._pressed_color = (0, 0, 255)

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
        self.text = font.render(text, True, (0, 128, 0))

    def get_text_position(self):
        x = self._position[0] + self._size[0] // 2 - self.text.get_width() // 2
        y = self._position[1] + self._size[1] // 2 - self.text.get_height() // 2
        return x, y

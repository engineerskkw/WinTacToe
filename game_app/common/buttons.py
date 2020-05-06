import os
from global_constants import ABS_PROJECT_ROOT_PATH

import pygame
from pygame import Rect, gfxdraw
from pygame.mixer import Sound
from abc import ABC, abstractmethod
from game_app.common.common_helper import ColorMode, Settings


class AbstractButton(ABC):
    def __init__(self, action, app):
        self._action = action
        self._app = app

        self._dark_mode_on = app.settings[Settings.COLOR] == ColorMode.DARK
        self._base_color = (70, 70, 70) if self._dark_mode_on else (190, 190, 190)
        self._hovered_color = (60, 60, 60) if self._dark_mode_on else (170, 170, 170)
        self._pressed_color = (50, 50, 50) if self._dark_mode_on else (155, 155, 155)
        self._click_sound = Sound(os.path.join(
            ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/common/button_click_sound.wav"))

    @abstractmethod
    def contains_point(self, point):
        pass

    @abstractmethod
    def render(self, screen, mouse_position, is_mouse_pressed):
        pass

    def _get_color(self, mouse_position, is_mouse_pressed):
        if not self.contains_point(mouse_position):
            return self._base_color
        return self._pressed_color if is_mouse_pressed else self._hovered_color

    def on_pressed(self):
        if self._app.settings[Settings.SOUNDS]:
            self._click_sound.play()
        self._action()


class RectangularButton(AbstractButton):
    def __init__(self, action, app, position, size):
        super().__init__(action, app)
        self._position = position
        self._size = size

    def contains_point(self, point):
        return self._position[0] < point[0] < self._position[0] + self._size[0] \
               and self._position[1] < point[1] < self._position[1] + self._size[1]

    def render(self, screen, mouse_position, is_mouse_pressed):
        figure = Rect(self._position, self._size)
        color = self._get_color(mouse_position, is_mouse_pressed)
        pygame.draw.rect(screen, color, figure)


class RectangularTextButton(RectangularButton):
    def __init__(self, text, action, app, position, size):
        super().__init__(action, app, position, size)

        pygame.font.init()
        self._text_color = (230, 230, 230) if self._dark_mode_on else (25, 25, 25)
        self._font = pygame.font.Font(None, 47)
        self._text = self._font.render(text, True, self._text_color)

    def _get_text_position(self):
        x = self._position[0] + self._size[0] // 2 - self._text.get_width() // 2
        y = self._position[1] + self._size[1] // 2 - self._text.get_height() // 2
        return x, y

    def set_text(self, new_text):
        self._text = self._font.render(new_text, True, self._text_color)

    def render(self, screen, mouse_position, is_mouse_pressed):
        super().render(screen, mouse_position, is_mouse_pressed)
        screen.blit(self._text, self._get_text_position())


class DisableableRectangularTextButton(RectangularTextButton):
    def __init__(self, enabled_text, disabled_text, action, app, position, size, disabled):
        super().__init__(enabled_text, action, app, position, size)
        self._disabled = disabled
        self._disabled_color = (45, 45, 45) if self._dark_mode_on else (230, 230, 230)
        self._enabled_text = enabled_text
        self._disabled_text = disabled_text
        self._disabled_click_sound = Sound(os.path.join(
            ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/common/disabled_button_sound.wav"))

    def _get_color(self, mouse_position, is_mouse_pressed):
        if self._disabled:
            return self._disabled_color
        return super()._get_color(mouse_position, is_mouse_pressed)

    def set_disabled(self, new_disabled):
        self._disabled = new_disabled
        self.set_text(self._disabled_text if new_disabled else self._enabled_text)

    def on_pressed(self):
        if self._disabled:
            if self._app.settings[Settings.SOUNDS]:
                self._disabled_click_sound.play()
        else:
            super().on_pressed()


class RectangularChoiceButton(RectangularTextButton):
    def __init__(self, text, action, app, position, size, chosen):
        super().__init__(text, action, app, position, size)
        self._chosen = chosen

        self._chosen_base_color = (15, 15, 15) if self._dark_mode_on else (105, 105, 105)
        self._chosen_hovered_color = (0, 0, 0) if self._dark_mode_on else (90, 90, 90)
        self._chosen_pressed_color = (0, 0, 0) if self._dark_mode_on else (100, 100, 100)

    def _get_color(self, mouse_position, is_mouse_pressed):
        if self._chosen:
            if not self.contains_point(mouse_position):
                return self._chosen_base_color
            return self._chosen_pressed_color if is_mouse_pressed else self._chosen_hovered_color
        else:
            return super()._get_color(mouse_position, is_mouse_pressed)

    def set_chosen(self, new_chosen):
        self._chosen = new_chosen

    def on_pressed(self):
        super().on_pressed()
        self._chosen = True


class RectangularChoiceButtonWithSubtext(RectangularChoiceButton):
    def __init__(self, text, subtext, action, app, position, size, chosen):
        super().__init__(text, action, app, position, size, chosen)
        self._subtext_font = pygame.font.Font(None, 27)
        self._subtext = self._subtext_font.render(subtext, True, self._text_color)

    def _get_text_position(self):
        x = self._position[0] + self._size[0] // 2 - self._text.get_width() // 2
        y = self._position[1] + self._size[1] // 2 - self._subtext.get_height() // 2 - self._text.get_height() // 2
        return x, y

    def _get_subtext_position(self):
        x = self._position[0] + self._size[0] // 2 - self._subtext.get_width() // 2
        y = self._position[1] + self._size[1] // 2 + self._subtext.get_height() // 2
        return x, y

    def render(self, screen, mouse_position, is_mouse_pressed):
        super().render(screen, mouse_position, is_mouse_pressed)
        screen.blit(self._subtext, self._get_subtext_position())


class RectangularDisableableChoiceButton(RectangularChoiceButton):
    def __init__(self, text, action, app, position, size, chosen, enabled):
        super().__init__(text, action, app, position, size, chosen)
        self._enabled = enabled

        self.disabled_color = (52, 52, 52) if self._dark_mode_on else (215, 215, 215)
        self._disabled_click_sound = Sound(os.path.join(
            ABS_PROJECT_ROOT_PATH, "game_app/resources/sounds/common/disabled_button_sound.wav"))

    def _get_color(self, mouse_position, is_mouse_pressed):
        if self._enabled:
            return super()._get_color(mouse_position, is_mouse_pressed)
        return self.disabled_color

    def set_enabled(self, new_enabled):
        self._enabled = new_enabled

    def on_pressed(self):
        if self._enabled:
            super().on_pressed()
        elif self._app.settings[Settings.SOUNDS]:
            self._disabled_click_sound.play()


class RectangularTextButtonWithIcon(RectangularTextButton):
    def __init__(self, text, icon_path, action, app, position, size):
        super().__init__(text, action, app, position, size)
        self._icon = pygame.image.load(os.path.join(ABS_PROJECT_ROOT_PATH, icon_path))

    def _get_text_position(self):
        x = self._position[0] + self._size[0] // 2 - self._text.get_width() // 2 - self._icon.get_size()[0] // 2
        y = self._position[1] + self._size[1] // 2 - self._text.get_height() // 2
        return x, y

    def _get_icon_position(self):
        x = self._position[0] + self._size[0] - self._icon.get_size()[0] * 3 // 2
        y = self._position[1] + self._size[1] // 2 - self._icon.get_size()[1] // 2
        return x, y

    def render(self, screen, mouse_position, is_mouse_pressed):
        super().render(screen, mouse_position, is_mouse_pressed)
        screen.blit(self._icon, self._get_icon_position())


class RoundButton(AbstractButton):
    def __init__(self, action, app, center_position, radius):
        super().__init__(action, app)
        self._center_position = center_position
        self._radius = radius

    def contains_point(self, point):
        return (self._center_position[0] - point[0]) ** 2 + (
                self._center_position[1] - point[1]) ** 2 <= self._radius ** 2

    def render(self, screen, mouse_position, is_mouse_pressed):
        color = self._get_color(mouse_position, is_mouse_pressed)
        gfxdraw.filled_circle(screen, self._center_position[0], self._center_position[1], self._radius, color)


class RoundIconButton(RoundButton):
    def __init__(self, icon_path, action, app, center_position, radius):
        super().__init__(action, app, center_position, radius)
        self._icon = pygame.image.load(os.path.join(ABS_PROJECT_ROOT_PATH, icon_path))

    def _get_icon_position(self):
        x = self._center_position[0] - self._icon.get_size()[0] // 2
        y = self._center_position[1] - self._icon.get_size()[1] // 2
        return x, y

    def render(self, screen, mouse_position, is_mouse_pressed):
        super().render(screen, mouse_position, is_mouse_pressed)
        screen.blit(self._icon, self._get_icon_position())

    def set_icon(self, new_icon_path):
        self._icon = pygame.image.load(os.path.join(ABS_PROJECT_ROOT_PATH, new_icon_path))


class RoundIconButtonWithDescription(RoundIconButton):
    def __init__(self, icon_path, description, action, app, center_position, radius):
        super().__init__(icon_path, action, app, center_position, radius)
        pygame.font.init()
        self._description_color = (230, 230, 230) if app.settings[Settings.COLOR] == ColorMode.DARK else (25, 25, 25)
        self._description_font = pygame.font.Font(None, 21)
        self._description = self._description_font.render(description, True, self._description_color)
        self._description_rendered = False

    def _get_description_position(self):
        x = self._center_position[0] - self._description.get_width() // 2
        y = self._center_position[1] + self._radius + self._description.get_height() // 2
        return x, y

    def render(self, screen, mouse_position, is_mouse_pressed):
        super().render(screen, mouse_position, is_mouse_pressed)
        if not self._description_rendered:
            screen.blit(self._description, self._get_description_position())
            self._description_rendered = True


class RoundMutedIconButtonWithDescription(RoundIconButtonWithDescription):
    def __init__(self, icon_path, description, sub_description, action, app, center_position, radius):
        super().__init__(icon_path, description, action, app, center_position, radius)
        self._sub_description = self._description_font.render(sub_description, True, self._description_color)
        self._sub_description_rendered = False

    def _get_sub_description_position(self):
        x = self._center_position[0] - self._sub_description.get_width() // 2
        y = self._center_position[1] + self._radius + self._description.get_height() * 8 // 5
        return x, y

    def render(self, screen, mouse_position, is_mouse_pressed):
        super().render(screen, mouse_position, is_mouse_pressed)
        if not self._sub_description_rendered:
            screen.blit(self._sub_description, self._get_sub_description_position())
            self._sub_description_rendered = True

    def on_pressed(self):
        self._action()

import pygame


class MainMenuScene:
    def __init__(self):
        self.background_color = (55, 55, 55)

    def render(self, screen):
        # print(pygame.display.get_surface().get_size())
        background = pygame.Surface(screen.get_size())
        background.fill(self.background_color)
        screen.blit(background, (0, 0))

        pygame.display.flip()

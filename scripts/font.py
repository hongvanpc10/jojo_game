import pygame


class Font:
    def __init__(self, font_in, font_out, size=32):
        self.font_in = pygame.font.Font(font_in, size)
        self.font_out = pygame.font.Font(font_out, size)

    def render(self, text, in_color=(255, 255, 255), out_color=(0, 0, 0)):
        out_surface = self.font_out.render(text, True, out_color)
        in_surface = self.font_in.render(text, True, in_color)
        out_surface.blit(in_surface, (0, 0))
        return out_surface

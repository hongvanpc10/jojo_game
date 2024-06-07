import pygame


class ScreenTransition:
    def __init__(self, width, height, speed=10):
        self.transition = -255
        self.speed = speed
        self.transitioning = False
        self.transition_surf = pygame.Surface((width, height))
        self.transition_surf.fill((0, 0, 0))
        self.done = 0

    def update(self):
        if self.transitioning:
            self.transition += self.speed
            if self.transition >= 0:
                self.done += 1
            if self.transition > 255:
                self.transition = -255
                self.transitioning = False
                self.done = 0

    def render(self, surf):
        if self.transitioning:
            self.transition_surf.set_alpha(255 - abs(self.transition))
            surf.blit(self.transition_surf, (0, 0))

    def start(self):
        self.transitioning = True

    def is_done(self):
        return self.done == 1

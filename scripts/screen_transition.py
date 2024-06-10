import pygame


class ScreenTransition:
    '''
    A screen transition effect that will be rendered on top of the screen. It can be used to transition between scenes.
    '''

    def __init__(self, width, height, speed=10):
        '''
        Create a new ScreenTransition object.

        Parameters:
            width (int): The width of the transition surface.
            height (int): The height of the transition surface.
            speed (int): The speed of the transition effect. Default is 10.
        '''

        self.transition = -255
        self.speed = speed
        self.transitioning = False
        self.transition_surf = pygame.Surface((width, height))
        self.transition_surf.fill((0, 0, 0))
        self.done = 0

    def update(self):
        '''
        Update the transition effect.
        '''

        if self.transitioning:
            self.transition += self.speed
            if self.transition >= 0:
                self.done += 1
            if self.transition > 255:
                self.transition = -255
                self.transitioning = False
                self.done = 0

    def render(self, surf):
        '''
        Render the transition effect on the screen.

        Parameters:
            surf (pygame.Surface): The surface to render the transition effect.
        '''

        if self.transitioning:
            self.transition_surf.set_alpha(255 - abs(self.transition))
            surf.blit(self.transition_surf, (0, 0))

    def start(self):
        '''
        Start the transition effect.
        '''

        self.transitioning = True

    def is_done(self):
        '''
        Check if the transition effect is done.
        '''

        return self.done == 1

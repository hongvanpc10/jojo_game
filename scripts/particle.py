import pygame


class Particle:
    '''
    A particle object. It is used to create animations in the game.
    '''

    def __init__(
        self,
        animation,
        type,
        pos,
        velocity,
        frame=0,
    ):
        '''
        Create a new Particle object.

        Parameters:
            animation (Animation): The animation of the particle.
            type (str): The type of the particle.
            pos (tuple[int, int]): The position of the particle.
            velocity (tuple[float, float]): The velocity of the particle.
            frame (int): The start frame of the animation. Default is 0.
        '''

        self.type = type
        self.pos = list(pos)
        self.velocity = list(velocity)
        self.animation = animation.copy()
        self.animation.frame = frame

    def update(self):
        '''
        Update the particle position and animation.

        Returns:
            bool: If the particle should be removed or not.
        '''

        kill = False
        if self.animation.done:
            kill = True

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        self.animation.update()

        return kill

    def render(self, surf: pygame.Surface, offset: tuple[int, int] = (0, 0)):
        '''
        Render the particle on the screen.

        Parameters:
            surf (pygame.Surface): The surface to render the particle.
            offset (tuple[int, int]): The offset of the screen, used to render the particle in the correct position. Default is (0, 0).
        '''

        image = self.animation.image
        surf.blit(
            image,
            (
                self.pos[0] - offset[0] - image.get_width() // 2,
                self.pos[1] - offset[1] - image.get_height() // 2,
            ),
        )

    @property
    def frame(self):
        '''
        Get the current frame of the particle.

        Returns:
            int: The current frame of the particle.


        '''

        return self.animation.frame

    @property
    def done(self):
        '''
        Get if the particle animation is done.

        Returns:
            bool: If the particle animation is done or not.
            
        '''

        return self.animation.done

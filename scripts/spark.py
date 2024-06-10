import math
import pygame


class Spark:
    '''
    A spark object that is a effect of the projectile when it hits something. It will be rendered in the game.
    '''

    def __init__(self, pos: tuple, angle: float, speed: float):
        '''
        Create a new Spark object.

        Parameters:
            pos (tuple[float, float]): The position of the spark.
            angle (float): The angle of the spark will move. It should be in radians.
            speed (float): The speed of the spark. 
        '''

        self.pos = list(pos)
        self.angle = angle
        self.speed = speed

    def update(self):
        '''
        Update the spark position.

        Returns:
            bool: If the spark should be removed or not.
        '''

        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed

        self.speed = max(0, self.speed - 0.1)
        return not self.speed

    def render(self, surf: pygame.Surface, offset: tuple[float, float] = (0, 0)):
        '''
        Render the spark on the screen.

        Parameters:
            surf (pygame.Surface): The surface to render the spark.
            offset (tuple[float, float]): The offset of the screen, used to render the spark in the correct position. Default is (0, 0).

            
        '''

        render_points = [
            (
                self.pos[0] + math.cos(self.angle) * self.speed * 2 - offset[0],
                self.pos[1] + math.sin(self.angle) * self.speed * 2 - offset[1],
            ),
            (
                self.pos[0]
                + math.cos(self.angle + math.pi * 0.5) * self.speed * 0.5
                - offset[0],
                self.pos[1]
                + math.sin(self.angle + math.pi * 0.5) * self.speed * 0.5
                - offset[1],
            ),
            (
                self.pos[0]
                + math.cos(self.angle + math.pi) * self.speed * 2
                - offset[0],
                self.pos[1]
                + math.sin(self.angle + math.pi) * self.speed * 2
                - offset[1],
            ),
            (
                self.pos[0]
                + math.cos(self.angle - math.pi * 0.5) * self.speed * 0.5
                - offset[0],
                self.pos[1]
                + math.sin(self.angle - math.pi * 0.5) * self.speed * 0.5
                - offset[1],
            ),
        ]

        pygame.draw.polygon(surf, (255, 255, 255), render_points)

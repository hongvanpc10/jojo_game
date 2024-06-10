import random
import math
import pygame
from .spark import Spark


class Projectile:
    """
    A projectile object that will be rendered in the game. It can be used for the player or the enemies.
    """

    def __init__(
        self,
        animation,
        type,
        pos,
        size,
        direction,
    ):
        """
        Create a new Projectile object.

        Parameters:
            animation (Animation): The animation of the projectile.
            type (str): The type of the projectile.
            pos (tuple[float, float]): The position of the projectile.
            size (tuple[float, float]): The size of the projectile.
            direction (float): The direction of the projectile. It should be 1 for right and -1 for left.
        """

        self.animation = animation.copy()
        self.type = type
        self.pos = list(pos)
        self.size = size
        self.direction = direction
        self.animation_offsets = (-2, -2)
        self.sparks = []
        self.is_removed = False
        for _ in range(4):
            self.sparks.append(
                Spark(
                    self.pos,
                    random.random() - 0.5 + (math.pi if self.direction < 0 else 0),
                    1.5 + random.random(),
                )
            )

    def update(self):
        """
        Update the projectile position and animation.

        Returns:
            bool: If the projectile should be removed or not.
        """

        if self.is_removed and not self.sparks:
            return True

        if not self.is_removed:
            self.animation.update()
            self.pos[0] += self.direction

        return self.animation.done

    def render(self, surf: pygame.Surface, offset: tuple[float, float]):
        """
        Render the projectile on the screen.

        Parameters:
            surf (pygame.Surface): The surface to render the projectile.
            offset (tuple[float, float]): The offset of the screen, used to render the projectile in the correct position.
        """

        if not self.is_removed:
            surf.blit(
                pygame.transform.flip(self.animation.image, self.direction < 0, False),
                (
                    self.pos[0] - self.animation.image.get_width() / 2 - offset[0],
                    self.pos[1] - self.animation.image.get_height() / 2 - offset[1],
                ),
            )

        for spark in self.sparks.copy():
            kill = spark.update()
            spark.render(surf, offset=offset)
            if kill:
                self.sparks.remove(spark)

    @property
    def rect(self):
        """
        Get the rectangle of the projectile.

        Returns:
            pygame.Rect: The rectangle of the projectile.
        """

        return pygame.Rect(
            self.pos[0] - self.size[0] / 2,
            self.pos[1] - self.size[1] / 2,
            self.size[0],
            self.size[1],
        )

    def remove(self, sfx=None):
        """
        Remove the projectile from the game.

        Parameters:
            sfx (pygame.mixer.Sound): The sound effect to play when the projectile is removed. Default is None.
        """

        if not self.is_removed:
            if sfx:
                sfx.play()

            for _ in range(4):
                self.sparks.append(
                    Spark(
                        self.pos,
                        random.random() - 0.5 + (math.pi if self.direction > 0 else 0),
                        1.5 + random.random(),
                    )
                )
            self.is_removed = True

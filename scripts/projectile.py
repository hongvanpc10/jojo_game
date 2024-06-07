import random
import math
import pygame
from .spark import Spark


class Projectile:
    def __init__(
        self,
        animation,
        type,
        pos,
        size,
        direction,
    ):
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
        if self.is_removed and not self.sparks:
            return True

        if not self.is_removed:
            self.animation.update()
            self.pos[0] += self.direction

        return self.animation.done

    def render(self, surf: pygame.Surface, offset: tuple[float, float]):
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
        return pygame.Rect(
            self.pos[0] - self.size[0] / 2,
            self.pos[1] - self.size[1] / 2,
            self.size[0],
            self.size[1],
        )

    def remove(self):
        if not self.is_removed:
            for _ in range(4):
                self.sparks.append(
                    Spark(
                        self.pos,
                        random.random() - 0.5 + (math.pi if self.direction > 0 else 0),
                        1.5 + random.random(),
                    )
                )
            self.is_removed = True

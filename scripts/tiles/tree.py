import pygame
import random
import math
from .tile import Tile
from ..particle import Particle


class Tree(Tile):
    def __init__(self, assets, variant, pos, leaf_animation):
        super().__init__(assets[variant], pos, "tree", variant, 16, True)
        if variant == 0:
            self.leave_spawner = pygame.Rect(self.pos[0] + 7, self.pos[1] + 4, 34, 21)
        elif variant == 1:
            self.leave_spawner = pygame.Rect(self.pos[0] + 5, self.pos[1] + 4, 29, 20)
        self.particles = []
        self.leaf_animation = leaf_animation

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset)
        for particle in self.particles:
            particle.render(surf, offset)

    def update(self):
        if (
            random.random() * 49999
            < self.leave_spawner.width * self.leave_spawner.height
        ):
            pos = (
                self.leave_spawner.x + random.random() * self.leave_spawner.width,
                self.leave_spawner.y + random.random() * self.leave_spawner.height,
            )
            self.particles.append(
                Particle(
                    self.leaf_animation,
                    "leaf",
                    pos,
                    (-0.1, 0.3),
                    frame=random.randint(0, 20),
                )
            )

        for particle in self.particles.copy():
            kill = particle.update()
            particle.pos[0] += math.sin(particle.frame * 0.035) * 0.3
            if kill:
                self.particles.remove(particle)

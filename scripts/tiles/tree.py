import pygame
import random
import math
from .tile import Tile
from ..particle import Particle


class Tree(Tile):
    """
    A tree tile. It has a leave spawner that creates leaf particles.
    """

    def __init__(self, assets, variant, pos, leaf_animation):
        """
        Create a new Tree object.

        Parameters:
            assets (list): The assets of the tree. It should contain the images of the tree. The first element should be the tree with the variant 0 and the second element should be the tree with the variant 1.
            variant (int): The variant of the tree.
            pos (tuple[int, int]): The position of the tree.
            leaf_animation (Animation): The animation of the leaf particles that the tree will spawn. It should be an Animation object.
        """

        super().__init__(assets[variant], pos, "tree", variant, 16, True)
        if variant == 0:
            self.leave_spawner = pygame.Rect(self.pos[0] + 7, self.pos[1] + 4, 34, 21)
        elif variant == 1:
            self.leave_spawner = pygame.Rect(self.pos[0] + 5, self.pos[1] + 4, 29, 20)
        self.particles = []
        self.leaf_animation = leaf_animation

    def render(self, surf, offset=(0, 0)):
        """
        Render the tree on the screen.

        Parameters:
            surf (pygame.Surface): The surface to render the tree.
            offset (tuple[int, int]): The offset of the screen, used to render the tree in the correct position. Default is (0, 0).
        """

        super().render(surf, offset)
        for particle in self.particles:
            particle.render(surf, offset)

    def update(self):
        """
        Update the tree. It will spawn leaf particles.
        """

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

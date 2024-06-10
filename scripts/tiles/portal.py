import random
from .tile import Tile
from ..particle import Particle


class Portal(Tile):
    """
    A portal tile, which can spawn enemies. It has a smoke explosion when destroyed.
    """

    def __init__(self, assets, pos, variant, size, smoke_animation):
        """
        Create a new Portal object.

        Parameters:
            assets (list): The assets of the portal. It should contain the images of the portal. The first element should be the portal with the variant 0 and the second element should be the portal with the variant 1.
            pos (tuple[int, int]): The position of the portal.
            variant (int): The variant of the portal.
            size (int): The size of the portal.
            smoke_animation (Animation): The animation of the smoke particles that will appear when the portal is destroyed. It should be an Animation object.
        """

        super().__init__(assets[variant], pos, "portal", variant, size, offgrid=True)
        self.assets = assets
        self.durability = 300
        self.smoke_explosion = None
        self.smoke_animation = smoke_animation

    def render(self, surf, offset):
        """
        Render the portal on the screen.

        Parameters:
            surf (pygame.Surface): The surface to render the portal.
            offset (tuple[int, int]): The offset of the screen, used to render the portal in the correct position.
        """

        super().render(surf, offset)

        if self.smoke_explosion:
            self.smoke_explosion.render(surf, offset=offset)

    def update(self, player):
        """
        Update the portal. It will spawn enemies if the player is close to it.

        Parameters:
            player (Player): The player object.

        Returns:
            bool: If the portal should be destroyed or not.
        """

        if self.smoke_explosion:
            kill = self.smoke_explosion.update()
            if kill:
                self.smoke_explosion = None

        if (
            self.variant == 0
            and abs(player.rect.centerx - self.rect.centerx) < self.size * 10
        ):
            if random.random() < 0.003:
                return True
        return False

    def destroy(self):
        """
        Destroy the portal.

        Returns:
            bool: If the portal is destroyed or not.
        """

        if self.durability > 0:
            self.durability -= 1
            if self.durability <= 0:
                self.variant = 1
                self.image = self.assets[1]
                self.smoke_explosion = Particle(
                    self.smoke_animation,
                    "smoke",
                    self.rect.center,
                    (0, 0),
                    frame=0,
                )

        return self.durability <= 0

    @property
    def destroyed(self):
        """
        If the portal is destroyed or not.
        """

        return self.durability <= 0

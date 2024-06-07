import random
from .tile import Tile
from ..particle import Particle


class Portal(Tile):
    def __init__(self, assets, pos, variant, size, smoke_animation):
        super().__init__(assets[variant], pos, "portal", variant, size, offgrid=True)
        self.assets = assets
        self.durability = 300
        self.smoke_explosion = None
        self.smoke_animation = smoke_animation

    def render(self, surf, offset):
        super().render(surf, offset)

        if self.smoke_explosion:
            self.smoke_explosion.render(surf, offset=offset)

    def update(self, player):
        if self.smoke_explosion:
            kill = self.smoke_explosion.update()
            if kill:
                self.smoke_explosion = None

        if (
            self.variant == 0
            and abs(player.rect.centerx - self.rect.centerx) < self.size * 30
        ):
            if random.random() < 0.003:
                return True
        return False

    def destroy(self):
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
        return self.durability <= 0

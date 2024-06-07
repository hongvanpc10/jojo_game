import pygame
from .tile import Tile
from ..particle import Particle


class Barrel(Tile):
    def __init__(self, image, pos, variant, size, smoke_animation):
        super().__init__(image, pos, "barrel", variant, size, False)
        self.smoke_explosion = None
        self.exploded = False
        self.smoke_animation = smoke_animation

    def render(self, surf, offset):
        if not self.exploded:
            super().render(surf, offset)

        if self.exploded:
            self.smoke_explosion.render(surf, offset=offset)

    def update(self, tilemap, player, enemies):
        if self.exploded:
            kill = self.smoke_explosion.update()
            if kill:
                self.smoke_explosions = None

            done = self.smoke_explosion.done

            rect = pygame.Rect(
                (
                    self.pos[0] * tilemap.tile_size - tilemap.tile_size * 2,
                    self.pos[1] * tilemap.tile_size - tilemap.tile_size * 2,
                    tilemap.tile_size * 5,
                    tilemap.tile_size * 5,
                )
            )

            for tile, _ in tilemap.tiles_around(
                (
                    self.pos[0] * tilemap.tile_size,
                    self.pos[1] * tilemap.tile_size,
                )
            ):
                if tile.type == "barrel" :
                    tile.explode()
                else:
                    tilemap.remove_tile(
                        tile.pos,
                        self.pos,
                        offgrid=False,
                    )

            if rect.colliderect(player.rect):
                player.kill(1)

            for enemy in enemies.copy():
                if rect.colliderect(enemy.rect):
                    enemy.dead = True

            if done:
                tilemap.remove_tile(self.pos, self.pos, offgrid=False)

    def explode(self):
        if not self.exploded:
            self.smoke_explosion = Particle(
                self.smoke_animation,
                "smoke",
                (self.pos[0] * self.size, self.pos[1] * self.size),
                (0, 0),
                frame=0,
            )
            self.exploded = True

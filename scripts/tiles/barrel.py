import pygame
from .tile import Tile
from ..particle import Particle


class Barrel(Tile):
    """
    A barrel tile. It can explode and create a smoke explosion that kills the player and enemies around it.
    """

    def __init__(self, image, pos, variant, size, smoke_animation):
        """
        Create a new Barrel object.

        Parameters:
            image (pygame.Surface): The image of the barrel.
            pos (tuple[int, int]): The position of the barrel.
            variant (int): The variant of the barrel.
            size (int): The size of the barrel.
            smoke_animation (Animation): The animation of the smoke particles that will appear when the barrel explodes. It should be an Animation object.
        """

        super().__init__(image, pos, "barrel", variant, size, False)
        self.smoke_explosion = None
        self.exploded = False
        self.smoke_animation = smoke_animation
        self.killed = False

    def render(self, surf, offset):
        """
        Render the barrel on the screen.

        Parameters:
            surf (pygame.Surface): The surface to render the barrel.
            offset (tuple[int, int]): The offset of the screen, used to render the barrel in the correct position.
        """

        if not self.exploded:
            super().render(surf, offset)

        if self.exploded:
            self.smoke_explosion.render(surf, offset=offset)

    def update(self, tilemap, player, enemies):
        """
        Update the barrel. It will explode if it is destroyed. The explosion will kill the player and enemies and destroy the tiles around it.

        Parameters:
            tilemap (Tilemap): The tilemap object where the barrel is.
            player (Player): The player object.
            enemies (list[Enemy]): The list of enemies.
        """

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
                if tile.type == "barrel":
                    tile.explode()
                else:
                    tilemap.remove_tile(
                        tile.pos,
                        self.pos,
                        offgrid=False,
                    )
            if not self.killed:
                if rect.colliderect(player.rect):
                    player.kill(1)

                for enemy in enemies.copy():
                    if rect.colliderect(enemy.rect):
                        enemy.dead = True
                self.killed = True

            if done:
                tilemap.remove_tile(self.pos, self.pos, offgrid=False)

    def explode(self, sfx=None):
        """
        Explode the barrel. It will create a smoke explosion that will kill the player and enemies around it.

        Parameters:
            sfx (pygame.mixer.Sound): The sound effect to play when the barrel explodes. Default is None.

        Returns:
            bool: If the barrel is exploded or not.
        """

        if not self.exploded:
            if sfx:
                sfx.play()
            self.smoke_explosion = Particle(
                self.smoke_animation,
                "smoke",
                (self.pos[0] * self.size, self.pos[1] * self.size),
                (0, 0),
                frame=0,
            )
            self.exploded = True

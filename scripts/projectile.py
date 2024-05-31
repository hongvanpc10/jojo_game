import pygame


class Projectile:
    def __init__(
        self,
        game,
        type: str,
        pos: tuple[float, float],
        size: tuple[float, float],
        direction: int,
    ):
        self.game = game
        self.type = type
        self.pos = list(pos)
        self.size = size
        self.direction = direction
        self.collisions = {
            "top": False,
            "bottom": False,
            "left": False,
            "right": False,
        }
        self.animation = self.game.assets["projectile/" + self.type].copy()
        self.animation_offsets = (-2, -2)

    def update(self):
        self.animation.update()
        self.pos[0] += self.direction
        return self.animation.done

    def render(self, surf: pygame.Surface, offset: tuple[float, float]):
        surf.blit(
            pygame.transform.flip(self.animation.image, self.direction < 0, False),
            (
                self.pos[0] - self.animation.image.get_width() / 2 - offset[0],
                self.pos[1] - self.animation.image.get_height() / 2 - offset[1],
            ),
        )

    @property
    def rect(self):
        return pygame.Rect(
            self.pos[0] - self.size[0] / 2,
            self.pos[1] - self.size[1] / 2,
            self.size[0],
            self.size[1],
        )

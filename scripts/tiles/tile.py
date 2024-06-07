import pygame


class Tile:
    @staticmethod
    def from_json(assets, data):
        return Tile(
            assets[data["type"]][data["variant"]],
            tuple(data["pos"]),
            data["type"],
            data["variant"],
            data["size"],
            data["offgrid"],
        )

    def __init__(self, image, pos, type, variant, size, offgrid=False):
        self.image = image
        self.pos = list(pos)
        self.type = type
        self.variant = variant
        self.size = size
        self.offgrid = offgrid

    def render(self, surf, offset=(0, 0)):
        if self.offgrid:
            surf.blit(self.image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        else:
            surf.blit(
                self.image,
                (
                    self.pos[0] * self.size - offset[0],
                    self.pos[1] * self.size - offset[1],
                ),
            )

    def to_json(self):
        return {
            "type": self.type,
            "pos": self.pos,
            "variant": self.variant,
            "size": self.size,
            "offgrid": self.offgrid,
        }

    def copy(self):
        return Tile(
            self.image, self.pos, self.type, self.variant, self.size, self.offgrid
        )

    @property
    def key(self):
        return str(self.pos[0]) + ";" + str(self.pos[1])

    @property
    def rect(self):
        if self.offgrid:
            return pygame.Rect(
                self.pos[0],
                self.pos[1],
                self.image.get_width(),
                self.image.get_height(),
            )

        return pygame.Rect(
            self.pos[0] * self.size,
            self.pos[1] * self.size,
            self.size,
            self.size,
        )

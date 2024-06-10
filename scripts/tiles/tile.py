import pygame


class Tile:
    """
    A class to represent a tile. A tile is a single image that is rendered on the screen. It can be on the grid or off the grid.
    """

    @staticmethod
    def from_json(assets, data):
        """
        Create a new Tile object from a JSON object.

        Parameters:
            assets (dict): The assets of the game. It should contain the images for the tiles. Each key should be the type of the tile and the value should be a dictionary with the variant as the key and the image as the value.
            data (dict): The JSON object with the data of the tile. It should contain the type, pos, variant, size, and offgrid.

        Returns:
            Tile: A new Tile object with the data from the JSON object.
        """

        return Tile(
            assets[data["type"]][data["variant"]],
            tuple(data["pos"]),
            data["type"],
            data["variant"],
            data["size"],
            data["offgrid"],
        )

    def __init__(self, image, pos, type, variant, size, offgrid=False):
        """
        Create a new Tile object.

        Parameters:
            image (pygame.Surface): The image of the tile.
            pos (tuple[int, int]): The position of the tile.
            type (str): The type of the tile. It should be the same as the key in the assets dict.
            variant (str): The variant of the tile.
            size (int): The size of the tile.
            offgrid (bool): If the tile is off the grid or not. If True, the tile will be rendered at the exact position. Default is False.
        """

        self.image = image
        self.pos = list(pos)
        self.type = type
        self.variant = variant
        self.size = size
        self.offgrid = offgrid

    def render(self, surf, offset=(0, 0)):
        """
        Render the tile on the screen.

        Parameters:
            surf (pygame.Surface): The surface to render the tile.
            offset (tuple[int, int]): The offset of the screen, used to render the tile in the correct position. Default is (0, 0).
        """

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
        """
        Convert the tile to a JSON object.

        Returns:
            dict: A JSON object with the data of the tile.
        """

        return {
            "type": self.type,
            "pos": self.pos,
            "variant": self.variant,
            "size": self.size,
            "offgrid": self.offgrid,
        }

    def copy(self):
        """
        Create a copy of the tile.

        Returns:
            Tile: A new Tile object with the same data as the current tile.
        """

        return Tile(
            self.image, self.pos, self.type, self.variant, self.size, self.offgrid
        )

    @property
    def key(self):
        """
        Get the key of the tile in tilemap. The key is the position of the tile in the format "x;y".
        """

        return str(self.pos[0]) + ";" + str(self.pos[1])

    @property
    def rect(self):
        """
        Get the rect of the tile.

        Returns:
            pygame.Rect: The rect of the tile.

        """

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

import pygame
import json
from .tiles import Tile, Tree, Barrel


NEIGHBORS_OFFSETS = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (0, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
]


AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (1, 0)])): 0,
    tuple(sorted([(-1, 0), (1, 0), (0, 1)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (1, 0), (0, -1)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted(((0, -1), (-1, 0), (0, 1), (1, 0)))): 8,
    tuple(): 9,
    tuple(sorted([(0, 1)])): 10,
    tuple(sorted([(0, 1), (0, -1)])): 11,
    tuple(sorted([(0, -1)])): 12,
    tuple(sorted([(1, 0)])): 13,
    tuple(sorted([(1, 0), (-1, 0)])): 14,
    tuple(sorted([(-1, 0)])): 15,
}


class Tilemap:
    """
    A class to represent the tilemap of the game. It will store the tiles and offgrid tiles of the game. It will also handle the rendering and updating of the tiles.
    """

    def __init__(self, config):
        """
        Create a new Tilemap object.

        Parameters:
            config (Config): The config object of the game.
        """

        self.tile_size = config.tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        self.assets = config.tiles_assets
        self.trees = []
        self.config = config

    def tiles_around(self, pos):
        """
        Get the tiles around a position.

        Parameters:
            pos (tuple[float, float]): The position to check.

        Yields:
            tuple[Tile, tuple[int, int]]: A tuple with the tile and the offset of the tile.

        """

        tile_loc = (
            int(pos[0] // self.tile_size),
            int(pos[1] // self.tile_size),
        )
        for offset in NEIGHBORS_OFFSETS:
            check_loc = (
                str(tile_loc[0] + offset[0]) + ";" + str(tile_loc[1] + offset[1])
            )
            if check_loc in self.tilemap:

                yield self.tilemap[check_loc], offset

    def physics_rects_around(self, pos):
        """
        Get the physics rects around a position.

        Parameters:
            pos (tuple[float, float]): The position to check.

        Yields:
            pygame.Rect: A rectangle with the physics tile.

        """

        for tile, _ in self.tiles_around(pos):
            if tile.type in self.config.physics_tiles:
                yield tile.rect

    def add_tile(self, pos, type, variant):
        '''
        Add a new tile to the tilemap.

        Parameters:
            pos (tuple[int, int]): The position of the tile.
            type (str): The type of the tile.
            variant (int): The variant of the tile.


        '''

        tile = Tile(
            self.assets[type][variant],
            pos,
            type,
            variant,
            self.tile_size,
            offgrid=False,
        )
        self.tilemap[tile.key] = tile

    def add_offgrid_tile(self, pos, tile, variant):
        '''
        Add a new offgrid tile to the tilemap.

        Parameters:
            pos (tuple[int, int]): The position of the tile.
            tile (str): The type of the tile.
            variant (int): The variant of the tile.
        '''

        self.offgrid_tiles.append(
            Tile(
                self.assets[tile][variant],
                pos,
                tile,
                variant,
                self.tile_size,
                offgrid=True,
            )
        )

    def remove_tile(
        self,
        pos,
        mouse_pos,
        offset=(0, 0),
        offgrid=True,
    ):
        '''
        Remove a tile from the tilemap.

        Parameters:
            pos (tuple[int, int]): The position of the tile to remove.
            mouse_pos (tuple[int, int]): The position of the mouse.
            offset (tuple[int, int]): The offset of the screen.
            offgrid (bool): If the tile is offgrid or not. Default is True.


        '''

        loc = str(pos[0]) + ";" + str(pos[1])
        if loc in self.tilemap:
            del self.tilemap[loc]

        if offgrid:
            for tile in self.offgrid_tiles.copy():
                tile_rect = pygame.Rect(
                    tile.pos[0] - offset[0],
                    tile.pos[1] - offset[1],
                    tile.rect.width,
                    tile.rect.height,
                )

                if tile_rect.collidepoint(mouse_pos):
                    self.offgrid_tiles.remove(tile)

    def solid_check(self, pos):
        '''
        Check if a position is solid or not.

        Parameters:
            pos (tuple[int, int]): The position to check.

        Returns:
            Tile: The tile that is solid or None if there is no solid tile.
        '''

        tile_loc = (
            str(int(pos[0] // self.tile_size))
            + ";"
            + str(int(pos[1] // self.tile_size))
        )
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc].type in self.config.physics_tiles:
                return self.tilemap[tile_loc]

    def autotile(self):
        '''
        Update the autotile tiles.
        '''

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                check_loc = (
                    str(tile.pos[0] + offset[0]) + ";" + str(tile.pos[1] + offset[1])
                )
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc].type == tile.type:
                        neighbors.add(offset)
                    else:
                        if self.tilemap[check_loc].type in self.config.autotile_tiles:
                            neighbors.add(offset)

            neighbors = tuple(sorted(neighbors))
            if tile.type in self.config.autotile_tiles and neighbors in AUTOTILE_MAP:
                tile.variant = AUTOTILE_MAP[neighbors]
                tile.image = self.assets[tile.type][tile.variant]

    def render(self, surf, offset=(0, 0)):
        '''
        Render the tilemap on the screen.

        Parameters:
            surf (pygame.Surface): The surface to render the tilemap.
            offset (tuple[int, int]): The offset of the screen, used to render the tilemap in the correct position. Default is (0, 0).
        '''

        for tile in self.offgrid_tiles:
            tile.render(surf, offset)

        for x in range(
            offset[0] // self.tile_size,
            (offset[0] + surf.get_width()) // self.tile_size + 1,
        ):
            for y in range(
                offset[1] // self.tile_size,
                (offset[1] + surf.get_height()) // self.tile_size + 1,
            ):
                loc = str(x) + ";" + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    tile.render(surf, offset)

    def update(self):
        '''
        Update the tilemap. It will update the autotile tiles and the trees.
        '''

        self.autotile()
        for tree in self.trees:
            tree.update()

    def save(self, path):
        '''
        Save the tilemap to a file.

        Parameters:
            path (str): The path to save the tilemap.
        '''

        tilemap = {loc: tile.to_json() for loc, tile in self.tilemap.items()}
        offgrid_tiles = [tile.to_json() for tile in self.offgrid_tiles]

        with open(path, "w") as file:
            json.dump(
                {
                    "tilemap": tilemap,
                    "offgrid_tiles": offgrid_tiles,
                    "tile_size": self.tile_size,
                },
                file,
            )

    def load(self, path):
        '''
        Load the tilemap from a file.

        Parameters:
            path (str): The path to load the tilemap.
        '''

        self.tilemap = {}
        self.offgrid_tiles = []
        self.trees = []

        try:
            with open(path, "r") as file:
                data = json.load(file)
                self.tilemap = {
                    loc: Tile.from_json(self.assets, tile)
                    for loc, tile in data["tilemap"].items()
                }
                self.offgrid_tiles = [
                    Tile.from_json(self.assets, tile) for tile in data["offgrid_tiles"]
                ]
                self.tile_size = data["tile_size"]

                for tree in self.extract([("tree", 0), ("tree", 1)], keep=False):
                    self.trees.append(
                        Tree(
                            self.assets["tree"],
                            tree.variant,
                            tree.pos,
                            self.config.particles_assets["leaf"],
                        )
                    )
                    self.offgrid_tiles.append(self.trees[-1])

                for barrel in self.extract([("barrel", 0), ("barrel", 1)]):
                    barrel.pos[0] //= self.tile_size
                    barrel.pos[1] //= self.tile_size
                    self.tilemap[barrel.key] = Barrel(
                        self.assets["barrel"][barrel.variant],
                        barrel.pos,
                        barrel.variant,
                        barrel.size,
                        self.config.particles_assets["smoke"],
                    )

        except FileNotFoundError:
            pass

    def extract(self, id_pairs: list[tuple[str, int]], keep=True):
        '''
        Extract tiles from the tilemap.

        Parameters:
            id_pairs (list[tuple[str, int]]): The list of id pairs to extract. The id pairs should be a tuple with the type and variant of the tile.
            keep (bool): If the tiles should be kept in the tilemap or not. Default is True.

        Returns:
            list[Tile]: The list of tiles extracted from the tilemap.
        '''



        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile.type, tile.variant) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile.type, tile.variant) in id_pairs:
                matches.append(tile.copy())
                matches[-1].pos = matches[-1].pos.copy()
                matches[-1].pos[0] *= self.tile_size
                matches[-1].pos[1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]

        return matches

    def tile_at(self, pos):
        '''
        Get the tile at a position.

        Parameters:
            pos (tuple[int, int]): The position to check.

        Returns:
            Tile: The tile at the position or None if there is no tile.
        '''

        loc = (
            str(int(pos[0] // self.tile_size))
            + ";"
            + str(int(pos[1] // self.tile_size))
        )
        return self.tilemap[loc]

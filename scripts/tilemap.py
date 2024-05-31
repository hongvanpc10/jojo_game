import pygame
import json


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

PHYSICS_TILES = {
    "grass",
    "stone",
    "obstacle",
}

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
}

AUTOTILE_TYPES = {"grass", "stone"}


class Tilemap:
    def __init__(self, game, tile_size=16):
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        self.game = game

    def tiles_around(self, pos: tuple[int, int]):
        tile_loc = (
            int(pos[0] // self.tile_size),
            int(pos[1] // self.tile_size),
        )
        for offset in NEIGHBORS_OFFSETS:
            check_loc = (
                str(tile_loc[0] + offset[0]) + ";" + str(tile_loc[1] + offset[1])
            )
            if check_loc in self.tilemap:
                yield self.tilemap[check_loc]

    def physics_rects_around(self, pos: tuple[int, int]):
        for tile in self.tiles_around(pos):
            if tile["type"] in PHYSICS_TILES:
                yield pygame.Rect(
                    tile["pos"][0] * self.tile_size,
                    tile["pos"][1] * self.tile_size,
                    self.tile_size,
                    self.tile_size,
                )

    def add_tile(self, pos: tuple[int, int], tile: str, variant: int):
        self.tilemap[str(pos[0]) + ";" + str(pos[1])] = {
            "pos": pos,
            "type": tile,
            "variant": variant,
        }

    def add_offgrid_tile(self, pos: tuple[int, int], tile: str, variant: int):
        self.offgrid_tiles.append({"pos": pos, "type": tile, "variant": variant})

    def remove_tile(
        self,
        pos: tuple[int, int],
        mouse_pos: tuple[float, float],
        offset: tuple[float, float] = (0, 0),
    ):
        loc = str(pos[0]) + ";" + str(pos[1])
        if loc in self.tilemap:
            del self.tilemap[loc]

        for tile in self.offgrid_tiles.copy():
            tile_image = self.game.assets[tile["type"]][tile["variant"]]
            tile_rect = pygame.Rect(
                tile["pos"][0] - offset[0],
                tile["pos"][1] - offset[1],
                tile_image.get_width(),
                tile_image.get_height(),
            )
            if tile_rect.collidepoint(mouse_pos):
                self.offgrid_tiles.remove(tile)

    def solid_check(self, pos: tuple[float, float]):
        tile_loc = (
            str(int(pos[0] // self.tile_size))
            + ";"
            + str(int(pos[1] // self.tile_size))
        )
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]["type"] in PHYSICS_TILES:
                return self.tilemap[tile_loc]

    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                check_loc = (
                    str(tile["pos"][0] + offset[0])
                    + ";"
                    + str(tile["pos"][1] + offset[1])
                )
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]["type"] == tile["type"]:
                        neighbors.add(offset)
                    else:
                        if self.tilemap[check_loc]["type"] in AUTOTILE_TYPES:
                            neighbors.add(offset)

            neighbors = tuple(sorted(neighbors))
            if tile["type"] in AUTOTILE_TYPES and neighbors in AUTOTILE_MAP:
                tile["variant"] = AUTOTILE_MAP[neighbors]

    def render(self, surf: pygame.Surface, offset: tuple[int, int] = (0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(
                self.game.assets[tile["type"]][tile["variant"]],
                (tile["pos"][0] - offset[0], tile["pos"][1] - offset[1]),
            )

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
                    surf.blit(
                        self.game.assets[tile["type"]][tile["variant"]],
                        (
                            tile["pos"][0] * self.tile_size - offset[0],
                            tile["pos"][1] * self.tile_size - offset[1],
                        ),
                    )

    def save(self, path: str):
        with open(path, "w") as file:
            json.dump(
                {
                    "tilemap": self.tilemap,
                    "offgrid_tiles": self.offgrid_tiles,
                    "tile_size": self.tile_size,
                },
                file,
            )

    def load(self, path: str):
        try:
            with open(path, "r") as file:
                data = json.load(file)
                self.tilemap = data["tilemap"]
                self.offgrid_tiles = data["offgrid_tiles"]
                self.tile_size = data["tile_size"]

        except FileNotFoundError:
            pass

    def extract(self, id_pairs: list[tuple[str, int]], keep=True):
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile["type"], tile["variant"]) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile["type"], tile["variant"]) in id_pairs:
                matches.append(tile.copy())
                matches[-1]["pos"] = matches[-1]["pos"].copy()
                matches[-1]["pos"][0] *= self.tile_size
                matches[-1]["pos"][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]

        return matches

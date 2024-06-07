import pygame
from scripts.utils import Animation, load_images, load_image


class Config:
    def __init__(self):
        self.base_images_path = "assets/images/"

        self.player_assets = {
            "player/idle": Animation(
                load_images(self.base_images_path + "entities/player/idle"), duration=10
            ),
            "player/run": Animation(
                load_images(self.base_images_path + "entities/player/run"), duration=4
            ),
            "player/jump": Animation(
                load_images(self.base_images_path + "entities/player/jump"),
                duration=2,
                loop=False,
            ),
            "player/wall_slide": Animation(
                load_images(self.base_images_path + "entities/player/wall_slide"),
                duration=10,
            ),
            "player/stand_shoot": Animation(
                load_images(self.base_images_path + "entities/player/stand_shoot"),
                duration=4,
            ),
            "player/run_shoot": Animation(
                load_images(self.base_images_path + "entities/player/run_shoot"),
                duration=4,
            ),
            "player/dead": Animation(
                load_images(self.base_images_path + "entities/player/dead"),
                duration=2,
                loop=False,
            ),
        }

        self.tiles_assets = {
            "grass": load_images(self.base_images_path + "tiles/grass"),
            "obstacle": load_images(self.base_images_path + "tiles/obstacle"),
            "barrel": load_images(self.base_images_path + "tiles/barrel"),
            "bridge": load_images(self.base_images_path + "tiles/bridge"),
            "ladder": load_images(self.base_images_path + "tiles/ladder"),
            "trap": load_images(self.base_images_path + "tiles/trap"),
            "decor": load_images(self.base_images_path + "tiles/decor"),
            "tree": load_images(self.base_images_path + "tiles/tree"),
            "spawner": load_images(self.base_images_path + "tiles/spawner"),
            "portal": load_images(self.base_images_path + "tiles/portal"),
            "cave": load_images(self.base_images_path + "tiles/cave"),
            "checkpoint": load_images(self.base_images_path + "tiles/checkpoint"),
        }

        self.enemy_assets = {
            "enemy/idle": Animation(
                load_images(self.base_images_path + "entities/enemy/idle"), duration=10
            ),
            "enemy/run": Animation(
                load_images(self.base_images_path + "entities/enemy/run"), duration=8
            ),
            "enemy/shoot": Animation(
                load_images(self.base_images_path + "entities/enemy/shoot"), duration=1
            ),
            "enemy/dead": Animation(
                load_images(self.base_images_path + "entities/enemy/dead"),
                duration=2,
                loop=False,
            ),
        }

        self.projectile_assets = {
            "player": Animation(
                load_images(self.base_images_path + "projectiles/player"),
                duration=8,
                loop=False,
            ),
            "enemy": Animation(
                load_images(self.base_images_path + "projectiles/enemy"),
                duration=8,
                loop=False,
            ),
        }

        self.particles_assets = {
            "particle": Animation(
                load_images(self.base_images_path + "particles/particle"),
                duration=6,
                loop=False,
            ),
            "leaf": Animation(
                load_images(self.base_images_path + "particles/leaf"),
                duration=20,
                loop=False,
            ),
            "smoke": Animation(
                load_images(self.base_images_path + "particles/smoke"),
                duration=4,
                loop=False,
            ),
        }

        self.cloud_assets = load_images(self.base_images_path + "cloud")

        self.background_image = load_image(self.base_images_path + "background.png")
        self.title_image = load_image(self.base_images_path + "title.png")
        self.player_dead_image = load_image(
            self.base_images_path + "entities/player/dead/9.png"
        )

        self.tile_size = 16

        self.offgrid_tiles = {
            "decor",
            "tree",
            "spawner",
            "portal",
            "cave",
            "checkpoint",
        }

        self.player_icon = load_image(self.base_images_path + "ui/player_icon.png")

        self.live_images = load_images(self.base_images_path + "ui/live")

        self.physics_tiles = {"grass", "stone", "obstacle", "bridge", "barrel"}

        self.autotile_tiles = {"grass"}

        self.font_18 = pygame.font.Font("assets/fonts/PressStart2P.ttf", 18)
        self.font_16 = pygame.font.Font("assets/fonts/PressStart2P.ttf", 16)
        self.font_32 = pygame.font.Font("assets/fonts/PressStart2P.ttf", 32)

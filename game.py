import pygame
import random
from scripts.tilemap import Tilemap
from scripts.utils import load_images, Animation
from scripts.entities import Player, Enemy
from scripts.particle import Particle
from scripts.spark import Spark
import math


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 380))
        pygame.display.set_caption("Jojo")
        self.clock = pygame.time.Clock()
        self.display = pygame.Surface((320, 180))

        self.assets = {
            "decor": load_images("tiles/decor"),
            "obstacle": load_images("tiles/obstacle"),
            "tree": load_images("tiles/tree"),
            "grass": load_images("tiles/grass"),
            "stone": load_images("tiles/stone"),
            "player/idle": Animation(load_images("entities/player/idle"), duration=15),
            "player/run": Animation(load_images("entities/player/run"), duration=8),
            "player/jump": Animation(
                load_images("entities/player/jump"), duration=2, loop=False
            ),
            "player/wall_slide": Animation(
                load_images("entities/player/wall_slide"), duration=10
            ),
            "player/stand_shoot": Animation(
                load_images("entities/player/stand_shoot"), duration=4
            ),
            "player/run_shoot": Animation(
                load_images("entities/player/run_shoot"), duration=4
            ),
            "player/dead": Animation(
                load_images("entities/player/dead"), duration=2, loop=False
            ),
            "particle/leaf": Animation(
                load_images("particles/leaf"), duration=20, loop=False
            ),
            "particle/particle": Animation(
                load_images("particles/particle"), duration=6, loop=False
            ),
            "particle/smoke": Animation(
                load_images("particles/smoke"), duration=4, loop=False
            ),
            "spawner": load_images("tiles/spawner"),
            "enemy/idle": Animation(load_images("entities/enemy/idle"), duration=10),
            "enemy/run": Animation(load_images("entities/enemy/run"), duration=8),
            "enemy/shoot": Animation(load_images("entities/enemy/shoot"), duration=1),
            "enemy/dead": Animation(
                load_images("entities/enemy/dead"), duration=2, loop=False
            ),
            "projectile/enemy": Animation(
                load_images("projectiles/enemy"), duration=12, loop=False
            ),
            "projectile/player": Animation(
                load_images("projectiles/player"), duration=12, loop=False
            ),
        }

        self.movement = [False, False]

        self.player = Player(self, (20, 50), (12, 18))

        self.tilemap = Tilemap(self, tile_size=16)

        self.level = 0
        self.load_level(self.level)

        self.shoot = False

        self.screenshake = 0

    def load_level(self, map_id: int):
        # self.tilemap.load("data/maps/" + str(map_id) + ".json")
        self.tilemap.load("map.json")

        self.scroll = [0, 0]

        self.leaves_spawners = []
        for tree in self.tilemap.extract([("tree", 0)]):
            self.leaves_spawners.append(
                pygame.Rect(tree["pos"][0] + 7, tree["pos"][1] + 4, 34, 21)
            )
        for tree in self.tilemap.extract([("tree", 1)]):
            self.leaves_spawners.append(
                pygame.Rect(tree["pos"][0] + 5, tree["pos"][1] + 4, 29, 20)
            )

        self.particles = []

        self.enemies = []

        for spawner in self.tilemap.extract(
            [("spawner", 0), ("spawner", 1)], keep=False
        ):
            if spawner["variant"] == 0:
                self.player.pos = spawner["pos"]
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner["pos"], (12, 18)))

        self.enemy_projectiles = []
        self.player_projectiles = []

        self.sparks = []

        self.smoke_explosions = []

    def run(self):
        running = True
        while running:
            self.display.fill((82, 168, 255))

            self.screenshake = max(0, self.screenshake - 1)

            self.scroll[0] += (
                self.player.rect.centerx
                - self.display.get_width() * 1 / 3
                - self.scroll[0]
            ) / 30
            self.scroll[1] += (
                self.player.rect.centery
                - self.display.get_height() * 2 / 3
                - self.scroll[1]
            ) / 30
            render_scroll = (
                int(self.scroll[0]),
                int(self.scroll[1]),
            )

            for rect in self.leaves_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (
                        rect.x + random.random() * rect.width,
                        rect.y + random.random() * rect.height,
                    )
                    self.particles.append(
                        Particle(
                            self,
                            "leaf",
                            pos,
                            (-0.1, 0.3),
                            frame=random.randint(0, 20),
                        )
                    )

            self.tilemap.render(self.display, offset=render_scroll)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == "leaf":
                    particle.pos[0] += math.sin(particle.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)

            for smoke in self.smoke_explosions.copy():

                kill = smoke.update()
                smoke.render(self.display, offset=render_scroll)
                if kill:
                    self.smoke_explosions.remove(smoke)

            for projectile in self.enemy_projectiles.copy():
                kill = projectile.update()
                projectile.render(self.display, offset=render_scroll)
                if kill:
                    self.enemy_projectiles.remove(projectile)
                elif self.tilemap.solid_check(
                    (
                        projectile.rect.centerx
                        + 2 * (1 if projectile.direction > 0 else -1),
                        projectile.rect.centery,
                    )
                ):
                    self.enemy_projectiles.remove(projectile)
                    for _ in range(4):
                        self.sparks.append(
                            Spark(
                                projectile.pos,
                                random.random()
                                - 0.5
                                + (math.pi if projectile.direction > 0 else 0),
                                1.5 + random.random(),
                            )
                        )
                elif self.player.rect.colliderect(projectile.rect):
                    self.enemy_projectiles.remove(projectile)
                    self.player.kill(projectile.direction)
                    self.screenshake = max(16, self.screenshake)

            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, movement=(0, 0))
                enemy.render(self.display, render_scroll)
                if kill:
                    self.enemies.remove(enemy)

            self.player.update(
                self.tilemap, movement=(self.movement[1] - self.movement[0], 0)
            )
            self.player.render(self.display, offset=render_scroll)

            if self.shoot:
                self.player.shoot()
                self.screenshake = max(4, self.screenshake)

            for projectile in self.player_projectiles.copy():
                kill = projectile.update()
                projectile.render(self.display, offset=render_scroll)
                if kill:
                    self.player_projectiles.remove(projectile)
                    break
                collision = self.tilemap.solid_check(
                    (
                        projectile.rect.centerx
                        + 3 * (1 if projectile.direction > 0 else -1),
                        projectile.rect.centery,
                    )
                )
                if collision:
                    self.player_projectiles.remove(projectile)
                    for _ in range(4):
                        self.sparks.append(
                            Spark(
                                projectile.pos,
                                random.random()
                                - 0.5
                                + (math.pi if projectile.direction > 0 else 0),
                                1.5 + random.random(),
                            )
                        )

                    if collision["type"] == "obstacle" and collision["variant"] in [
                        1,
                        2,
                    ]:
                        self.smoke_explosions.append(
                            Particle(
                                self,
                                "smoke",
                                (
                                    collision["pos"][0] * self.tilemap.tile_size,
                                    collision["pos"][1] * self.tilemap.tile_size,
                                ),
                                (0, 0),
                                frame=0,
                            )
                        )

                        rect = pygame.Rect(
                            (
                                collision["pos"][0] * self.tilemap.tile_size
                                - self.tilemap.tile_size * 2,
                                collision["pos"][1] * self.tilemap.tile_size
                                - self.tilemap.tile_size * 2,
                                self.tilemap.tile_size * 5,
                                self.tilemap.tile_size * 5,
                            )
                        )

                        if rect.colliderect(self.player.rect):
                            self.player.kill(projectile.direction)

                        for enemy in self.enemies.copy():
                            if rect.colliderect(enemy.rect):
                                enemy.dead = True

                        for tile in self.tilemap.physics_rects_around(
                            (
                                collision["pos"][0] * self.tilemap.tile_size,
                                collision["pos"][1] * self.tilemap.tile_size,
                            )
                        ):
                            if rect.colliderect(tile):
                                self.tilemap.remove_tile(
                                    (
                                        tile.x // self.tilemap.tile_size,
                                        tile.y // self.tilemap.tile_size,
                                    ),
                                    projectile.rect.center,
                                )
                                self.tilemap.autotile()

                        self.tilemap.remove_tile(
                            collision["pos"], projectile.rect.center
                        )

                        self.screenshake = max(20, self.screenshake)
                    else:
                        self.screenshake = max(10, self.screenshake)

                    break

                for enemy in self.enemies.copy():
                    if projectile.rect.colliderect(enemy.rect):
                        self.player_projectiles.remove(projectile)
                        enemy.dead = True
                        self.screenshake = max(16, self.screenshake)
                        break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True

                    if event.key == pygame.K_UP:
                        self.player.jump()
                    if event.key == pygame.K_c:
                        self.player.dash()
                    if event.key == pygame.K_x:
                        self.shoot = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_x:
                        self.shoot = False

            screenshake_offset = (
                random.random() * self.screenshake - self.screenshake / 2,
                random.random() * self.screenshake - self.screenshake / 2,
            )
            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()),
                screenshake_offset,
            )

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    Game().run()

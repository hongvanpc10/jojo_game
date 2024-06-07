import pygame
import random
from scripts.tilemap import Tilemap
from scripts.entities import Player, Enemy
from scripts.tiles import Portal
from config import Config
from scripts.clouds import Clouds
from scripts.screen_transition import ScreenTransition
from scripts.menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 360))
        pygame.display.set_caption("Jojo")

        self.config = Config()
        self.clock = pygame.time.Clock()

        self.display = pygame.Surface((320, 180))
        self.overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)

        self.game_state = 0

        self.movement = [False, False]

        self.tilemap = Tilemap(self.config)

        self.level = 0

        self.load_level(self.level)

        self.shoot = False

        self.screenshake = 0

        self.menu_select = [0]

        self.screen_transition = ScreenTransition(*self.screen.get_size())

    def load_level(self, map_id: int):
        # self.tilemap.load("data/maps/" + str(map_id) + ".json")
        self.tilemap.load("map.json")

        self.scroll = [0, 0]

        self.clouds = Clouds(self.config.cloud_assets, count=8)


        self.enemies = []

        self.player = Player(
            self.config.player_assets,
            (20, 50),
            (12, 18),
            self.config.projectile_assets["player"],
            self.config.particles_assets["particle"],
        )

        self.scores = 0

        for spawner in self.tilemap.extract(
            [("spawner", 0), ("spawner", 1)], keep=False
        ):
            if spawner.variant == 0:
                self.player = Player(
                    self.config.player_assets,
                    spawner.pos,
                    (12, 18),
                    self.config.projectile_assets["player"],
                    self.config.particles_assets["particle"],
                )
            else:
                self.enemies.append(
                    Enemy(
                        self.config.enemy_assets,
                        spawner.pos,
                        (12, 18),
                        self.config.projectile_assets["enemy"],
                    )
                )

        self.portals = []
        for portal in self.tilemap.extract([("portal", 0), ("portal", 1)], keep=False):
            self.portals.append(
                Portal(
                    self.config.tiles_assets["portal"],
                    portal.pos,
                    portal.variant,
                    self.config.tile_size,
                    self.config.particles_assets["smoke"],
                )
            )

        self.enemy_projectiles = []
        self.player_projectiles = []

        self.dead_delay = 60
        self.dead = False

        self.lives = 1

    def run(self):
        running = True

        def exit():
            nonlocal running
            running = False

        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            if self.game_state == 0:
                self.game_start(events, exit)
            elif self.game_state == 1:
                self.game_play(events)
            elif self.game_state == 2:
                self.game_over(events, exit)

            self.screen_transition.update()
            self.screen_transition.render(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def game_start(self, events, exit):
        if self.screen_transition.is_done():
            self.game_state = 1
            return

        menu = Menu(
            ["CONTINUE", "NEW GAME", "EXIT"], self.config.font_18, self.menu_select
        )

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if menu.selected[0] == 0:
                        self.screen_transition.start()
                    elif menu.selected[0] == 2:
                        exit()

        self.display.blit(
            self.config.background_image,
            (0, 0),
        )

        self.display.blit(
            self.config.title_image,
            (
                self.display.get_width() / 2 - self.config.title_image.get_width() / 2,
                16,
            ),
        )

        self.screen.blit(
            pygame.transform.scale(self.display, self.screen.get_size()),
            (0, 0),
        )

        menu.render(self.screen)
        menu.update(events)

    def game_play(self, events):
        if self.screen_transition.is_done():
            self.menu_select[0] = 0
            self.game_state = 2
            return

        self.display.fill((82, 168, 255))

        self.overlay.fill((0, 0, 0, 0))

        scores_surf = self.config.font_16.render(
            "Scores: " + str(self.scores).rjust(5, "0"), True, (255, 255, 255)
        )
        self.overlay.blit(
            scores_surf,
            (self.overlay.get_width() - scores_surf.get_width() - 16, 8),
        )

        self.overlay.blit(
            pygame.transform.scale_by(self.config.player_icon, 2.5), (16, 16)
        )

        for i in range(3):
            surf = pygame.transform.scale_by(
                self.config.live_images[1 if i < self.lives else 0], 3
            )
            self.overlay.blit(
                surf,
                (
                    16
                    + self.config.player_icon.get_width() * 2.5
                    + 8
                    + (surf.get_width() + 4) * i,
                    16,
                ),
            )

        self.clouds.update()
        self.clouds.render(self.display, self.scroll)

        self.screenshake = max(0, self.screenshake - 1)

        self.scroll[0] += (
            self.player.rect.centerx - self.display.get_width() * 1 / 3 - self.scroll[0]
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

        if self.dead:
            if self.dead_delay > 0:
                self.dead_delay -= 1

        if self.dead_delay <= 0:
            self.screen_transition.start()

        self.tilemap.render(self.display, offset=render_scroll)
        self.tilemap.update()

        for barrel in self.tilemap.extract([("barrel", 0), ("barrel", 1)]):
            self.tilemap.tile_at(barrel.pos).update(
                self.tilemap, self.player, self.enemies
            )

        for projectile in self.enemy_projectiles.copy():
            if self.tilemap.solid_check(
                (
                    projectile.rect.centerx
                    + 2 * (1 if projectile.direction > 0 else -1),
                    projectile.rect.centery,
                )
            ):
                projectile.remove()

            elif self.player.rect.colliderect(projectile.rect):
                projectile.remove()
                self.player.kill(projectile.direction)
                self.dead = True
                self.screenshake = max(16, self.screenshake)

            kill = projectile.update()
            projectile.render(self.display, offset=render_scroll)
            if kill:
                self.enemy_projectiles.remove(projectile)

        for portal in self.portals:
            portal.render(self.display, render_scroll)
            if portal.update(self.player):
                self.enemies.append(
                    Enemy(
                        self.config.enemy_assets,
                        portal.pos,
                        (12, 18),
                        self.config.projectile_assets["enemy"],
                    )
                )

        for enemy in self.enemies.copy():
            kill = enemy.update(
                self.tilemap,
                self.enemy_projectiles.append,
                self.player,
                movement=(0, 0),
            )
            enemy.render(self.display, render_scroll)
            if kill:
                self.scores += 10
                self.enemies.remove(enemy)

        self.player.update(
            self.tilemap,
            movement=(self.movement[1] - self.movement[0], 0),
        )
        self.player.render(self.display, offset=render_scroll)

        if self.player.dead:
            self.dead = True

        if self.shoot:
            self.player.shoot(self.player_projectiles.append)
            self.screenshake = max(4, self.screenshake)

        for projectile in self.player_projectiles.copy():
            collision = self.tilemap.solid_check(
                (
                    projectile.rect.centerx
                    + 3 * (1 if projectile.direction > 0 else -1),
                    projectile.rect.centery,
                )
            )

            if collision:
                projectile.remove()
                if collision.type == "barrel":
                    collision.explode()
                    self.screenshake = max(25, self.screenshake)

                else:
                    self.screenshake = max(8, self.screenshake)
            else:
                for enemy in self.enemies.copy():
                    if projectile.rect.colliderect(enemy.rect):
                        projectile.remove()
                        enemy.dead = True
                        self.screenshake = max(16, self.screenshake)
                        break
                else:
                    for portal in self.portals:
                        if not portal.destroyed and projectile.rect.colliderect(
                            portal.rect
                        ):
                            destroyed = portal.destroy()

                            if destroyed:
                                self.screenshake = max(25, self.screenshake)
                                self.scores += 50
                            else:
                                projectile.remove()
                                self.screenshake = max(8, self.screenshake)
                            break

            kill = projectile.update()
            projectile.render(self.display, offset=render_scroll)
            if kill:
                self.player_projectiles.remove(projectile)

        if not self.dead:
            for trap in self.tilemap.extract([("trap", 0)]):
                player_rect = pygame.Rect(
                    self.player.rect.centerx - self.config.tile_size / 2,
                    self.player.rect.bottom - self.config.tile_size / 2,
                    self.config.tile_size,
                    self.config.tile_size / 2,
                )

                trap_rect = pygame.Rect(
                    trap.pos[0],
                    trap.pos[1],
                    trap.size,
                    trap.size,
                )
                if player_rect.colliderect(trap_rect):
                    self.player.kill(0)
                    self.dead = True
                    self.screenshake = max(25, self.screenshake)

        for event in events:
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
        self.screen.blit(self.overlay, (0, 0))

    def game_over(self, events, exit):
        menu = Menu(["RESTART", "BACK", "EXIT"], self.config.font_18, self.menu_select)

        if self.screen_transition.is_done():
            if menu.selected[0] == 0:
                self.game_state = 1
            elif menu.selected[0] == 1:
                self.game_state = 0
            self.menu_select[0] = 0
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if menu.selected[0] == 0:
                        self.load_level(self.level)
                        self.screen_transition.start()
                    elif menu.selected[0] == 1:
                        self.load_level(self.level)
                        self.screen_transition.start()

                    elif menu.selected[0] == 2:
                        exit()

        mission_failed_text = self.config.font_32.render(
            "MISSION FAILED", True, (255, 255, 255)
        )

        self.screen.blit(
            pygame.transform.scale(
                self.config.background_image, self.screen.get_size()
            ),
            (0, 0),
        )

        self.screen.blit(
            mission_failed_text,
            (
                (self.screen.get_width() - mission_failed_text.get_width()) / 2,
                64,
            ),
        )

        player_image = pygame.transform.scale_by(
            self.config.player_dead_image.copy(), 2
        )

        self.screen.blit(
            player_image,
            (
                (self.screen.get_width() - mission_failed_text.get_width()) / 2 + 16,
                64 - player_image.get_height(),
            ),
        )

        menu.render(self.screen)
        menu.update(events)

    def start_transition(self):
        self.transition = -255


if __name__ == "__main__":
    Game().run()

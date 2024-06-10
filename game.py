import pygame
import random
import os
from scripts.tilemap import Tilemap
from scripts.entities import Player, Enemy
from scripts.tiles import Portal
from config import Config
from scripts.clouds import Clouds
from scripts.screen_transition import ScreenTransition
from scripts.menu import Menu


class Game:
    """
    Game class is used to create the main game loop and manage the game states.
    """

    def __init__(self):
        """
        Create a new Game object.
        """

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
        self.is_new = True

        self.load_level()
        self.load_map(self.level)

        self.shoot = False

        self.screenshake = 0

        self.menu_select = [0]

        self.screen_transition = ScreenTransition(*self.screen.get_size(), 15)

    def load_level(self):
        """
        Load the level from the file.
        """

        if os.path.exists(self.config.level_file):
            with open(self.config.level_file, "r") as file:
                self.level = int(file.read())
            self.is_new = False
        else:
            self.level = 0
            self.is_new = True

    def save_level(self):
        """
        Save the level to the file.
        """

        with open(self.config.level_file, "w") as file:
            file.write(str(self.level))

    def load_map(self, map_id: int):
        """
        Load the map from the file.

        Parameters:
            map_id (int): The id of the map to load.
        """

        self.tilemap.load(self.config.map_path + str(map_id) + ".json")
        # self.tilemap.load("map.json")

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

        self.next_level_delay = 60
        self.next_level = False

        self.lives = 1

    def run(self):
        """
        Run the game loop.
        """

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
            elif self.game_state == 3:
                self.game_pause(events, exit)
            elif self.game_state == 4:
                self.mission_completed(events, exit)

            self.screen_transition.update()
            self.screen_transition.render(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def game_start(self, events, exit):
        """
        Show the game start screen.

        Parameters:
            events (list): The list of events.
            exit (function): The function to exit the game.
        """

        if not pygame.mixer.music.get_busy():
            self.play_music(self.config.theme_music)

        if self.screen_transition.is_done():
            self.game_state = 1
            pygame.mixer.music.stop()
            return

        menu = Menu(
            (
                ["CONTINUE", "NEW GAME", "EXIT"]
                if not self.is_new
                else ["NEW GAME", "EXIT"]
            ),
            self.config.font_18,
            self.menu_select,
        )

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if self.is_new:
                        if menu.selected[0] == 0:
                            self.screen_transition.start()
                            with open(self.config.level_file, "w") as file:
                                file.write("0")
                        elif menu.selected[0] == 1:
                            exit()
                    else:
                        if menu.selected[0] == 0:
                            self.screen_transition.start()
                        elif menu.selected[0] == 1:
                            self.level = 0
                            self.save_level()
                            self.load_map(self.level)
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
        """
        Play the game.

        Parameters:
            events (list): The list of events.

        """

        if not pygame.mixer.music.get_busy():
            self.play_music(self.config.ambience_music, 0.1)

        if self.screen_transition.is_done():
            if self.next_level:
                if self.level < len(os.listdir(self.config.map_path)) - 1:
                    self.level += 1
                    self.save_level()
                    self.load_map(self.level)
                else:
                    self.game_state = 4
            elif self.dead:
                self.menu_select[0] = 0
                self.game_state = 2

            pygame.mixer.music.stop()

            return

        self.display.fill((82, 168, 255))

        self.overlay.fill((0, 0, 0, 0))

        scores_surf = self.config.font_16.render(
            "SCORES " + str(self.scores).rjust(5, "0"), True, (255, 255, 255)
        )
        self.overlay.blit(
            scores_surf,
            (self.overlay.get_width() - scores_surf.get_width() - 16, 16),
        )

        level_surf = self.config.font_16.render(
            "LEVEL " + str(self.level + 1).rjust(2, "0"), True, (255, 255, 255)
        )
        self.overlay.blit(
            level_surf,
            (
                self.overlay.get_width()
                - scores_surf.get_width()
                - 16
                - level_surf.get_width()
                - 32,
                16,
            ),
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
            self.player.rect.centery - self.display.get_height() / 2 - self.scroll[1]
        ) / 30
        render_scroll = (
            int(self.scroll[0]),
            int(self.scroll[1]),
        )

        if self.dead:
            if self.dead_delay > 0:
                self.dead_delay -= 1

        if self.dead_delay <= 0:
            self.lives -= 1
            if self.lives > 0:
                self.player = Player(
                    self.config.player_assets,
                    (self.player.pos[0], self.player.pos[1] - 14),
                    (12, 18),
                    self.config.projectile_assets["player"],
                    self.config.particles_assets["particle"],
                )
                self.config.sfx["select"].play()
                self.dead = False
                self.dead_delay = 60
            else:
                self.screen_transition.start()

        if self.next_level:
            if self.next_level_delay > 0:
                self.next_level_delay -= 1

        if self.next_level_delay <= 0:
            self.screen_transition.start()

        self.tilemap.render(self.display, offset=render_scroll)
        self.tilemap.update()

        for barrel in self.tilemap.extract([("barrel", 0), ("barrel", 1)]):
            self.tilemap.tile_at(barrel.pos).update(
                self.tilemap, self.player, self.enemies
            )

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
                self.player.kill(projectile.direction, self.config.sfx["hurt"])
                self.dead = True
                self.screenshake = max(16, self.screenshake)

            kill = projectile.update()
            projectile.render(self.display, offset=render_scroll)
            if kill:
                self.enemy_projectiles.remove(projectile)

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

        if self.dead == True:
            self.movement = [False, False]

        if self.shoot:
            if self.player.shoot(self.player_projectiles.append):
                self.config.sfx["shoot"].play()
                self.screenshake = max(4, self.screenshake)

        for ammo in self.tilemap.extract([("ammo", 0)]).copy():
            if self.player.rect.colliderect(ammo.rect):
                self.config.sfx["select"].play()
                self.lives = min(3, 1 + self.lives)
                self.tilemap.remove_tile(
                    ammo.pos,
                    (ammo.pos[0] - self.scroll[0], ammo.pos[1] - self.scroll[1]),
                    self.scroll,
                )

        for checkpoint in self.tilemap.extract([("checkpoint", 0)]).copy():
            if self.player.rect.colliderect(checkpoint.rect):
                self.next_level = True
                self.screenshake = max(30, self.screenshake)

        for projectile in self.player_projectiles.copy():
            collision = self.tilemap.solid_check(
                (
                    projectile.rect.centerx
                    + 3 * (1 if projectile.direction > 0 else -1),
                    projectile.rect.centery,
                )
            )

            if collision:
                projectile.remove(self.config.sfx["hit"])

                if collision.type == "barrel":
                    collision.explode(self.config.sfx["bomb"])

                    self.screenshake = max(25, self.screenshake)
                else:
                    self.screenshake = max(8, self.screenshake)

            else:
                for enemy in self.enemies.copy():
                    if projectile.rect.colliderect(enemy.rect):
                        projectile.remove(self.config.sfx["explosion"])
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
                                self.config.sfx["bomb"].play()
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
                    self.player.kill(0, self.config.sfx["hurt"])
                    self.dead = True
                    self.screenshake = max(25, self.screenshake)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.movement[0] = True
                if event.key == pygame.K_RIGHT:
                    self.movement[1] = True

                if event.key == pygame.K_UP:
                    if self.player.jump():
                        self.config.sfx["jump"].play()
                if event.key == pygame.K_c:
                    if self.player.dash():
                        self.config.sfx["dash"].play()

                if event.key == pygame.K_x:
                    self.shoot = True

                if event.key == pygame.K_ESCAPE:
                    self.game_state = 3

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
        """
        Show the game over screen.

        Parameters:
            events (list): The list of events.
            exit (function): The function to exit the game.
        """

        if not pygame.mixer.music.get_busy():
            self.play_music(self.config.end_music)

        menu = Menu(["RESTART", "BACK", "EXIT"], self.config.font_18, self.menu_select)

        if self.screen_transition.is_done():
            if menu.selected[0] == 0:
                self.game_state = 1
            elif menu.selected[0] == 1:
                self.game_state = 0
            self.menu_select[0] = 0

            pygame.mixer.music.stop()

            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if menu.selected[0] == 0:
                        self.load_map(self.level)
                        self.screen_transition.start()
                    elif menu.selected[0] == 1:
                        self.load_map(self.level)
                        self.screen_transition.start()
                    elif menu.selected[0] == 2:
                        exit()

        title = self.config.font_32.render("MISSION FAILED", True, (255, 255, 255))

        self.screen.blit(
            pygame.transform.scale(
                self.config.background_image, self.screen.get_size()
            ),
            (0, 0),
        )

        self.screen.blit(
            title,
            (
                (self.screen.get_width() - title.get_width()) / 2,
                64,
            ),
        )

        player_image = pygame.transform.scale_by(
            self.config.player_dead_image.copy(), 2
        )

        self.screen.blit(
            player_image,
            (
                (self.screen.get_width() - title.get_width()) / 2 + 16,
                64 - player_image.get_height(),
            ),
        )

        menu.render(self.screen)
        menu.update(events)

    def game_pause(self, events, exit):
        """
        Show the game pause screen.

        Parameters:
            events (list): The list of events.
            exit (function): The function to exit the game.
        """

        if not pygame.mixer.music.get_busy():
            self.play_music(self.config.theme_music, 0.1)

        menu = Menu(["RESUME", "BACK", "EXIT"], self.config.font_18, self.menu_select)

        if self.screen_transition.is_done():
            if menu.selected[0] == 0:
                self.game_state = 1
            elif menu.selected[0] == 1:
                self.game_state = 0
            self.menu_select[0] = 0

            pygame.mixer.music.stop()
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if menu.selected[0] == 0:
                        self.screen_transition.start()
                    elif menu.selected[0] == 1:
                        self.load_map(self.level)
                        self.screen_transition.start()
                    elif menu.selected[0] == 2:
                        exit()

        title = self.config.font_32.render("GAME PAUSE", True, (255, 255, 255))

        self.screen.blit(
            pygame.transform.scale(
                self.config.background_image, self.screen.get_size()
            ),
            (0, 0),
        )

        self.screen.blit(
            title,
            (
                (self.screen.get_width() - title.get_width()) / 2,
                64,
            ),
        )

        player_image = pygame.transform.scale_by(
            self.config.player_dead_image.copy(), 2
        )

        self.screen.blit(
            player_image,
            (
                (self.screen.get_width() - title.get_width()) / 2 + 16,
                64 - player_image.get_height(),
            ),
        )

        menu.render(self.screen)
        menu.update(events)

    def mission_completed(self, events, exit):
        """
        Show the mission completed screen.

        Parameters:
            events (list): The list of events.
            exit (function): The function to exit the game.
        """

        if not pygame.mixer.music.get_busy():
            self.play_music(self.config.end_music)

        menu = Menu(
            ["RESTART", "START NEW", "BACK", "EXIT"],
            self.config.font_18,
            self.menu_select,
        )

        if self.screen_transition.is_done():
            if menu.selected[0] == 0:
                self.game_state = 1
            elif menu.selected[0] == 1:
                self.game_state = 1
            elif menu.selected[0] == 2:
                self.game_state = 0
            self.menu_select[0] = 0
            pygame.mixer.music.stop()
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if menu.selected[0] == 0:
                        self.load_map(self.level)
                        self.screen_transition.start()
                    elif menu.selected[0] == 1:
                        self.level = 0
                        self.save_level()
                        self.load_map(self.level)
                        self.screen_transition.start()
                    elif menu.selected[0] == 2:
                        self.load_map(self.level)
                        self.screen_transition.start()
                    elif menu.selected[0] == 3:
                        exit()

        title = self.config.font_32.render("MISSION COMPLETED", True, (255, 255, 255))

        self.screen.blit(
            pygame.transform.scale(
                self.config.background_image, self.screen.get_size()
            ),
            (0, 0),
        )

        self.screen.blit(
            title,
            (
                (self.screen.get_width() - title.get_width()) / 2,
                64,
            ),
        )

        player_image = pygame.transform.scale_by(
            self.config.player_dead_image.copy(), 2
        )

        self.screen.blit(
            player_image,
            (
                (self.screen.get_width() - title.get_width()) / 2 + 16,
                64 - player_image.get_height(),
            ),
        )

        menu.render(self.screen)
        menu.update(events)

    def play_music(self, path, volume=0.3):
        """
        Play the music.

        Parameters:
            path (str): The path to the music file.
            volume (float): The volume of the music. Default is 0.3.
        """

        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)


if __name__ == "__main__":
    Game().run()

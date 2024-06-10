import pygame
from scripts.tilemap import Tilemap
from config import Config

RENDER_SCALE = 2.0


class Editor:
    """
    Editor class is used to create a level editor for the game. It allows the user to create and edit the levels.
    """

    def __init__(self):
        """
        Create a new Editor object.
        """

        pygame.init()
        self.screen = pygame.display.set_mode((640, 360))
        pygame.display.set_caption("Editor")
        self.clock = pygame.time.Clock()
        self.display = pygame.Surface((320, 180))
        self.config = Config()
        self.assets = self.config.tiles_assets.copy()
        self.movement = [False, False, False, False]

        self.tilemap = Tilemap(self.config)
        self.tilemap.load("map.json")

        self.scroll = [0, 0]

        self.tiles_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.click = False
        self.right_click = False
        self.shift = False

        self.ongrid = self.tiles_list[self.tile_group] not in self.config.offgrid_tiles

    def run(self):
        '''
        Run the editor.

        This method will run the editor and allow the user to create and edit the levels.
        '''

        running = True
        while running:
            self.display.fill((82, 168, 255))

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)
            self.tilemap.update()

            current_tile_image = self.assets[self.tiles_list[self.tile_group]][
                self.tile_variant
            ].copy()

            current_tile_image.set_alpha(100)

            self.display.blit(current_tile_image, (5, 5))

            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (mouse_pos[0] / RENDER_SCALE, mouse_pos[1] / RENDER_SCALE)
            tile_pos = (
                int((mouse_pos[0] + render_scroll[0]) // self.tilemap.tile_size),
                int((mouse_pos[1] + render_scroll[1]) // self.tilemap.tile_size),
            )

            if self.ongrid:
                self.display.blit(
                    current_tile_image,
                    (
                        tile_pos[0] * self.tilemap.tile_size - render_scroll[0],
                        tile_pos[1] * self.tilemap.tile_size - render_scroll[1],
                    ),
                )
            else:
                self.display.blit(
                    current_tile_image,
                    mouse_pos,
                )

            if self.click and self.ongrid:
                self.tilemap.add_tile(
                    tile_pos, self.tiles_list[self.tile_group], self.tile_variant
                )
            if self.right_click:
                self.tilemap.remove_tile(tile_pos, mouse_pos, self.scroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True
                    if event.button == 3:
                        self.right_click = True

                    if not self.shift:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(
                                self.tiles_list
                            )

                            self.ongrid = (
                                self.tiles_list[self.tile_group]
                                not in self.config.offgrid_tiles
                            )

                            self.tile_variant = 0

                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(
                                self.tiles_list
                            )

                            self.ongrid = (
                                self.tiles_list[self.tile_group]
                                not in self.config.offgrid_tiles
                            )

                            self.tile_variant = 0

                    else:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(
                                self.assets[self.tiles_list[self.tile_group]]
                            )
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(
                                self.assets[self.tiles_list[self.tile_group]]
                            )

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.click = False
                        if not self.ongrid:
                            self.tilemap.add_offgrid_tile(
                                (
                                    mouse_pos[0] + self.scroll[0],
                                    mouse_pos[1] + self.scroll[1],
                                ),
                                self.tiles_list[self.tile_group],
                                self.tile_variant,
                            )
                    if event.button == 3:
                        self.right_click = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True

                    if event.key == pygame.K_LSHIFT:
                        self.shift = True

                    if event.key == pygame.K_o:
                        self.tilemap.save("map.json")

                    if event.key == pygame.K_t:
                        self.tilemap.autotile()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False

                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    Editor().run()

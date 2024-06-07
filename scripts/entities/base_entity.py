import pygame


class PhysicsEntity:
    def __init__(
        self, assets, type: str, pos: tuple[float, float], size: tuple[float, float]
    ):
        self.assets = assets
        self.type = type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {
            "top": False,
            "bottom": False,
            "left": False,
            "right": False,
        }

        self.action = ""
        self.animation_offsets = (-7, -4)
        self.flip = False
        self.set_action("idle")
        self.last_movement = [0, 0]

    def set_action(self, action: str):
        if self.action != action:
            self.action = action
            self.animation = self.assets[self.type + "/" + action].copy()

    def update(self, tilemap, movement: tuple[float, float] = (0, 0)):
        self.collisions = {
            "top": False,
            "bottom": False,
            "left": False,
            "right": False,
        }

        frame_movement = [
            movement[0] + self.velocity[0],
            movement[1] + self.velocity[1],
        ]

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions["right"] = True
                elif frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions["left"] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top + 1
                    self.collisions["bottom"] = True
                elif frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions["top"] = True
                self.pos[1] = entity_rect.y

        if movement[0] < 0:
            self.flip = True
        elif movement[0] > 0:
            self.flip = False

        self.last_movement = movement

        self.velocity[1] = min(5, self.velocity[1] + 0.15)

        if self.collisions["bottom"] or self.collisions["top"]:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surf: pygame.Surface, offset: tuple[int, int] = (0, 0)):
        surf.blit(
            pygame.transform.flip(self.animation.image, self.flip, False),
            (
                self.pos[0] - offset[0] + self.animation_offsets[0],
                self.pos[1] - offset[1] + self.animation_offsets[1],
            ),
        )

    @property
    def rect(self):
        return pygame.Rect(
            self.pos[0],
            self.pos[1],
            self.size[0],
            self.size[1],
        )

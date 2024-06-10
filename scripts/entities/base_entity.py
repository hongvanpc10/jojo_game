import pygame


class PhysicsEntity:
    """
    Base class for all entities that have physics and animations such as the player and enemies.
    """

    def __init__(
        self, assets, type: str, pos: tuple[float, float], size: tuple[float, float]
    ):
        """
        Create a new PhysicsEntity object.

        Parameters:
            assets (dict): The assets of the entity. It should contain the animations for the entity. Each key should be the type of the animation and the value should be an Animation object.
            type (str): The type of the entity. It should be the same as the key in the assets dict.
            pos (tuple[float, float]): The position of the entity.
            size (tuple[float, float]): The size of the entity.
        """

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
        """
        Set the current action of the entity. This will change the current animation of the entity.

        Parameters:
            action (str): The action to set. It should be the same as the key in the assets dict.
        """

        if self.action != action:
            self.action = action
            self.animation = self.assets[self.type + "/" + action].copy()

    def update(self, tilemap, movement: tuple[float, float] = (0, 0)):
        """
        Update the entity.

        Parameters:
            tilemap (Tilemap): The tilemap object where the entity is.
            movement (tuple[float, float]): The movement of the entity. It should be a tuple with the x and y movement. Default is (0, 0).
        """

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
        """
        Render the entity to the screen.

        Parameters:
            surf (pygame.Surface): The surface to render the entity.
            offset (tuple[int, int]): The offset to render the entity, relative to the screen. Default is (0, 0).
        """

        surf.blit(
            pygame.transform.flip(self.animation.image, self.flip, False),
            (
                self.pos[0] - offset[0] + self.animation_offsets[0],
                self.pos[1] - offset[1] + self.animation_offsets[1],
            ),
        )

    @property
    def rect(self):
        """
        Get the rect of the entity.

        Returns:
            pygame.Rect: The rect of the entity.
        """

        return pygame.Rect(
            self.pos[0],
            self.pos[1],
            self.size[0],
            self.size[1],
        )

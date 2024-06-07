import random
from .base_entity import PhysicsEntity
from ..projectile import Projectile


class Enemy(PhysicsEntity):
    def __init__(
        self,
        assets,
        pos: tuple[float, float],
        size: tuple[float, float],
        projectile_animation,
    ):
        super().__init__(
            assets,
            "enemy",
            pos,
            size,
        )
        self.walking = 0
        self.shooting = 0
        self.dead = False
        self.projectile_animation = projectile_animation

    def update(
        self,
        tilemap,
        add_projectile,
        player,
        movement: tuple[float, float] = (0, 0),
    ):
        if self.dead:
            self.set_action("dead")
            super().update(tilemap, movement)
            return self.animation.done

        if self.walking:
            if tilemap.solid_check(
                (self.rect.centerx + (-7 if self.flip else 7), self.pos[1] + 20)
            ):
                if self.collisions["left"] or self.collisions["right"]:
                    self.flip = not self.flip
                movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip

            self.walking = max(0, self.walking - 1)

            if not self.walking and not player.dead:
                dis = (
                    player.pos[0] - self.pos[0],
                    player.pos[1] - self.pos[1],
                )
                if abs(dis[1]) < 16:
                    if self.flip and dis[0] < 0:
                        add_projectile(
                            Projectile(
                                self.projectile_animation,
                                "enemy",
                                (self.rect.centerx - 10, self.rect.centery + 2),
                                (4, 4),
                                -3,
                            )
                        )
                        self.shooting = 20
                    if not self.flip and dis[0] > 0:
                        add_projectile(
                            Projectile(
                                self.projectile_animation,
                                "enemy",
                                (self.rect.centerx + 10, self.rect.centery + 2),
                                (4, 4),
                                3,
                            )
                        )
                        self.shooting = 20

        elif random.random() < 0.05:
            self.walking = random.randint(30, 120)

        self.shooting = max(0, self.shooting - 1)

        if self.shooting:
            self.set_action("shoot")
        elif movement[0] != 0:
            self.set_action("run")
        else:
            self.set_action("idle")

        super().update(tilemap, movement)

        return False

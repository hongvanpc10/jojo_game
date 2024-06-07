import random
import math
from .base_entity import PhysicsEntity
from ..particle import Particle
from ..projectile import Projectile
import pygame


class Player(PhysicsEntity):
    def __init__(
        self,
        assets,
        pos,
        size,
        projectile_animation,
        particle_animation,
    ):
        super().__init__(assets, "player", pos, size)
        self.air_time = 0
        self.jumps = 1
        self.wall_slide = False
        self.dashing = 0
        self.shooting = 0
        self.dead = False
        self.dead_direction = 1
        self.particles = []
        self.projectile_animation = projectile_animation
        self.particle_animation = particle_animation

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset)
        for particle in self.particles.copy():
            kill = particle.update()
            particle.render(surf, offset=offset)

            if kill:
                self.particles.remove(particle)

    def update(self, tilemap, movement: tuple[float, float] = (0, 0)):
        if self.dead:
            self.set_action("dead")
            super().update(tilemap, movement=(0, 0))
            return

        super().update(tilemap, movement)

        self.air_time += 1
        if self.collisions["bottom"]:
            self.air_time = 0
            self.jumps = 1

        if self.air_time > 120:
            self.kill(1)

        self.wall_slide = False
        if (self.collisions["left"] or self.collisions["right"]) and self.air_time > 4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)
            if self.collisions["right"]:
                self.flip = False
            else:
                self.flip = True
            self.set_action("wall_slide")

        if not self.wall_slide:
            if self.air_time > 4:
                self.set_action("jump")
            elif movement[0] != 0:
                if self.shooting:
                    self.set_action("run_shoot")
                else:
                    self.set_action("run")
            else:
                if self.shooting:
                    self.set_action("stand_shoot")
                else:
                    self.set_action("idle")

            for tile, offset in tilemap.tiles_around(self.rect.midtop):
                if tile.type == "ladder" and offset[0] == 0:
                    self.velocity[1] = 0
                    self.air_time = 0
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_UP]:
                        self.velocity[1] = -1
                    elif keys[pygame.K_DOWN]:
                        self.velocity[1] = 1

        if abs(self.dashing) in {50, 60}:
            for _ in range(20):
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                particle_velocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.particles.append(
                    Particle(
                        self.particle_animation,
                        "particle",
                        self.rect.center,
                        particle_velocity,
                        frame=random.randint(0, 7),
                    )
                )

        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        elif self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)

        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1
            particle_velocity = [
                abs(self.dashing) / self.dashing * random.random() * 3,
                0,
            ]
            self.particles.append(
                Particle(
                    self.particle_animation,
                    "particle",
                    self.rect.center,
                    particle_velocity,
                    frame=random.randint(0, 7),
                )
            )

        if self.velocity[0] > 0:
            self.velocity[0] = max(0, self.velocity[0] - 0.1)
        elif self.velocity[0] < 0:
            self.velocity[0] = min(0, self.velocity[0] + 0.1)

        self.shooting = max(0, self.shooting - 1)

    def jump(self):
        if self.dead:
            return

        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 2
                self.velocity[1] = -3
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -2
                self.velocity[1] = -3
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
        elif self.jumps:
            self.velocity[1] = -2.75
            self.jumps -= 1
            self.air_time = 5
            return True

        return False

    def dash(self):
        if not self.dead and not self.dashing:
            if self.flip:
                self.dashing = -60
            else:
                self.dashing = 60

    def shoot(self, add_projectile):
        if not self.dead and not self.shooting:
            self.shooting = 8
            add_projectile(
                Projectile(
                    self.projectile_animation,
                    "player",
                    (
                        self.rect.centerx + 10 * (-1 if self.flip else 1),
                        self.rect.centery + 2,
                    ),
                    (4, 4),
                    -3 if self.flip else 3,
                )
            )

    def kill(self, direction: int):
        self.dead = True
        self.dead_direction = direction

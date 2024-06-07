import pygame


class Particle:
    def __init__(
        self,
        animation,
        type,
        pos,
        velocity,
        frame=0,
    ):
        self.type = type
        self.pos = list(pos)
        self.velocity = list(velocity)
        self.animation = animation.copy()
        self.animation.frame = frame

    def update(self):
        kill = False
        if self.animation.done:
            kill = True

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        self.animation.update()

        return kill

    def render(self, surf: pygame.Surface, offset: tuple[int, int] = (0, 0)):
        image = self.animation.image
        surf.blit(
            image,
            (
                self.pos[0] - offset[0] - image.get_width() // 2,
                self.pos[1] - offset[1] - image.get_height() // 2,
            ),
        )

    @property
    def frame(self):
        return self.animation.frame

    @property
    def done(self):
        return self.animation.done

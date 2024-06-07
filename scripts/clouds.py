import random


class Cloud:
    def __init__(self, image, pos, speed, depth):
        self.image = image
        self.pos = list(pos)
        self.speed = speed
        self.depth = depth

    def update(self):
        self.pos[0] += self.speed

    def render(self, surf, offset):
        render_pos = (
            self.pos[0] - offset[0] * self.depth,
            self.pos[1] - offset[1] * self.depth,
        )
        surf.blit(
            self.image,
            (
                render_pos[0] % (surf.get_width() + self.image.get_width())
                - self.image.get_width(),
                render_pos[1] % (surf.get_height() + self.image.get_height())
                - self.image.get_height(),
            ),
        )


class Clouds:
    def __init__(self, assets, count=16):
        self.clouds = []
        for _ in range(count):
            self.clouds.append(
                Cloud(
                    random.choice(assets),
                    (random.random() * 99999, random.random() * 99999),
                    random.random() * 0.04 + 0.02,
                    random.random() * 0.5 + 0.1,
                )
            )

        self.clouds.sort(key=lambda x: x.depth)

    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def render(self, surf, offset):
        for cloud in self.clouds:
            cloud.render(surf, offset)

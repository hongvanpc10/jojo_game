import pygame, os
import re


BASE_IMAGE_PATH = "assets/images/"


def load_image(path: str):
    image = pygame.image.load(BASE_IMAGE_PATH + path).convert_alpha()
    image.set_colorkey((0, 0, 0))
    return image


def load_images(path: str):
    images = []
    for file in sorted(os.listdir(BASE_IMAGE_PATH + path)):
        if re.match(r".*\.(png|jpg|jpeg|gif|bmp)", file):
            images.append(load_image(path + "/" + file))

    return images


class Animation:
    def __init__(self, images: list[pygame.Surface], duration=5, loop=True):
        self.images = images
        self.duration = duration
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (len(self.images) * self.duration)
        else:
            self.frame = min(self.frame + 1, self.duration * len(self.images) - 1)
            if self.frame == len(self.images) * self.duration - 1:
                self.done = True

    @property
    def image(self):
        return self.images[self.frame // self.duration]

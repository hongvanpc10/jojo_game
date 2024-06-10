import pygame
import os
import re


def load_image(path: str):
    '''
    Load an image from a file.

    Parameters:
        path (str): The path to the image file.

    Returns:
        pygame.Surface: The image loaded from the file.
    '''

    image = pygame.image.load(path).convert_alpha()
    image.set_colorkey((0, 0, 0))
    return image


def load_images(path: str):
    '''
    Load a list of images from a directory.

    Parameters:
        path (str): The path to the directory containing the images.

    Returns:
        list[pygame.Surface]: A list of images loaded from the directory.
    '''

    images = []
    for file in sorted(os.listdir(path)):
        if re.match(r".*\.(png|jpg|jpeg|gif|bmp)", file):
            images.append(load_image(path + "/" + file))

    return images


class Animation:
    '''
    An animation object. It is used to create animations in the game.
    '''

    def __init__(self, images: list[pygame.Surface], duration=5, loop=True):
        '''
        Create a new Animation object.

        Parameters:
            images (list[pygame.Surface]): The images of the animation.
            duration (int): The duration of each frame. Default is 5.
            loop (bool): If the animation should loop or not. Default is True.
        '''

        self.images = images
        self.duration = duration
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        '''
        Create a copy of the animation.

        Returns:
            Animation: A new Animation object with the same images, duration, and loop as the original.
        '''

        return Animation(self.images, self.duration, self.loop)

    def update(self):
        '''
        Update the animation frame.
        '''

        if self.loop:
            self.frame = (self.frame + 1) % (len(self.images) * self.duration)
        else:
            self.frame = min(self.frame + 1, self.duration * len(self.images) - 1)
            if self.frame == len(self.images) * self.duration - 1:
                self.done = True

    @property
    def image(self):
        '''
        Get the current image of the animation.

        Returns:
            pygame.Surface: The current image of the animation.
        '''

        return self.images[self.frame // self.duration]

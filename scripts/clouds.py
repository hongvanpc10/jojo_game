import random


class Cloud:
    '''
    A cloud object that will be rendered in the background.
    '''

    def __init__(self, image, pos, speed, depth):
        '''
        Create a new Cloud object.

        Parameters:
            image (pygame.Surface): The image of the cloud.
            pos (tuple[int, int]): The position of the cloud.
            speed (float): The speed of the cloud. 
            depth (float): The depth of the cloud. It should be between 0 and 1.
        '''

        self.image = image
        self.pos = list(pos)
        self.speed = speed
        self.depth = depth

    def update(self):
        '''
        Update the cloud position.
        '''

        self.pos[0] += self.speed

    def render(self, surf, offset):
        '''
        Render the cloud on the screen.

        Parameters:
            surf (pygame.Surface): The surface to render the cloud.
            offset (tuple[int, int]): The offset of the screen, used to render the cloud in the correct position.
        '''

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
    '''
    A collection of cloud objects that will be rendered in the background.
    '''

    def __init__(self, assets, count=16):
        '''
        Create a new Clouds object.

        Parameters:
            assets (list): The assets of the clouds. It should contain the images of the clouds.
            count (int): The number of clouds to create. Default is 16.
        '''

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
        '''
        Update the clouds position.
        
        '''

        for cloud in self.clouds:
            cloud.update()

    def render(self, surf, offset):
        '''
        Render the clouds on the screen.

        Parameters:
            surf (pygame.Surface): The surface to render the clouds.
            offset (tuple[int, int]): The offset of the screen, used to render the clouds in the correct position.
        '''

        for cloud in self.clouds:
            cloud.render(surf, offset)

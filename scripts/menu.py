import pygame


class Menu:
    """
    A menu object that will be rendered on the screen. A menu can have multiple items and a selected item. The selected item will be highlighted.
    """

    def __init__(self, items, font, selected):
        """
        Create a new Menu object.

        Parameters:
            items (list[str]): The items of the menu.
            font (pygame.font.Font): The font of the menu.
            selected (list[int]): The selected item of the menu.
        """

        self.items = []
        self.selected = selected
        for item in items:
            self.items.append(font.render(item, True, (255, 255, 255)))

    def render(self, surf):
        """
        Render the menu on the screen.

        Parameters:
            surf (pygame.Surface): The surface to render the menu.
        """

        max_width = 0
        height = 0
        for i, item in enumerate(self.items):
            item_surf = item.copy()
            if i == self.selected[0]:
                text_surf = pygame.transform.scale_by(item_surf, 1.4)
                item_surf = pygame.Surface(
                    (text_surf.get_width() + 8, text_surf.get_height() + 8),
                    pygame.SRCALPHA,
                )
                item_surf.fill((0, 0, 0, 128))
                item_surf.blit(
                    text_surf,
                    (
                        (item_surf.get_width() - text_surf.get_width()) / 2,
                        (item_surf.get_height() - text_surf.get_height()) / 2,
                    ),
                )

            max_width = max(max_width, item_surf.get_width())

            surf.blit(
                item_surf,
                (
                    (surf.get_width() - max_width + (max_width - item_surf.get_width()))
                    / 2,
                    surf.get_height() / 2 + height - (24 if len(self.items) > 3 else 0),
                ),
            )
            height += item_surf.get_height() + 24

    def update(self, events):
        """
        Update the menu. It will change the selected item based on the input.

        Parameters:
            events (list[pygame.event.Event]): The events to update the menu.

        """

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected[0] = (self.selected[0] - 1) % len(self.items)
                if event.key == pygame.K_DOWN:
                    self.selected[0] = (self.selected[0] + 1) % len(self.items)

import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, surf: pygame.Surface, groups: pygame.sprite.Group):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

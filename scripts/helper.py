import pygame

from scripts.utils import load_font


class Helper(pygame.sprite.Sprite):
    def __init__(self, game, assets, *groups):
        super().__init__(groups)
        self.game = game
        self.assets = assets
        self.image = pygame.image.load("./data/images/helper/helper.png")
        self.text_image = pygame.image.load("./data/images/ui/helper.png")
        self.rect = self.image.get_rect()
        self.display_width = game.display.get_width()
        self.display_height = game.display.get_height()

        self.name_font = load_font(14)
        self.description_font = load_font(16)

    def update(self, platforms_group: pygame.sprite.Group):
        pass

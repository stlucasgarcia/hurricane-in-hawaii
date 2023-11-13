import pygame

from scripts.common.utils import load_font


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


class RunawayHelper(Helper):
    def __init__(self, game, assets, *groups):
        super().__init__(game, assets, groups)
        self.disappear_time = pygame.time.get_ticks() + 2 * 60 * 1000

    def update(self, platforms_group: pygame.sprite.Group):
        current_time = pygame.time.get_ticks()

        if current_time >= self.disappear_time:
            return

        title = self.name_font.render("Bob", False, (0, 0, 0))
        description = self.description_font.render(
            "Encontre um local seguro",
            False,
            (0, 0, 0),
        )

        self.game.display.blit(
            self.text_image, (self.display_width // 2 - 140, self.display_height - 50)
        )
        self.game.display.blit(
            self.image, (self.display_width // 2 - 137, self.display_height - 58)
        )

        self.game.display.blit(
            title, (self.display_width // 2 - 120, self.display_height - 46)
        )
        self.game.display.blit(
            description, (self.display_width // 2 - 137, self.display_height - 37)
        )


class AwareHelper(Helper):
    def __init__(self, game, assets, *groups):
        super().__init__(game, assets, groups)
        self.disappear_time = pygame.time.get_ticks() + 2 * 60 * 1000

    def update(self, platforms_group: pygame.sprite.Group):
        current_time = pygame.time.get_ticks()

        if current_time >= self.disappear_time:
            return

        title = self.name_font.render("Bob", False, (0, 0, 0))
        description = self.description_font.render(
            "Preste atenção ao seu redor",
            False,
            (0, 0, 0),
        )

        self.game.display.blit(
            self.text_image, (self.display_width // 2 - 140, self.display_height - 50)
        )
        self.game.display.blit(
            self.image, (self.display_width // 2 - 137, self.display_height - 58)
        )

        self.game.display.blit(
            title, (self.display_width // 2 - 120, self.display_height - 46)
        )
        self.game.display.blit(
            description, (self.display_width // 2 - 137, self.display_height - 37)
        )

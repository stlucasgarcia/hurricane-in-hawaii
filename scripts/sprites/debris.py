import pygame
import random

from scripts.common.utils import State


# Define debris class
class Debris(pygame.sprite.Sprite):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        self.groups_remove = groups
        self.image = game.assets["brick_box"]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(320)
        self.rect.y = -30  # Start above the screen

    def update(self, **kwargs: dict[str, pygame.sprite.Group]):
        self.rect.y += 3  # Adjust falling speed
        if self.rect.y > 240:
            self.rect.y = -30
            self.rect.x = random.randrange(320)

        self.check_collision_y(kwargs["platforms"], kwargs["players"])

    def check_collision_y(
        self,
        platforms_group: pygame.sprite.Group,
        player_group: pygame.sprite.Group,
    ):
        hits = pygame.sprite.spritecollide(self, platforms_group, False)
        if len(hits) > 0:
            # TODO: add animation
            self.kill()

        hits = pygame.sprite.spritecollide(self, player_group, False)
        for hit in hits:
            if self.rect.y > 0:
                hit.is_alive = False
                hit.game.set_state(State.GAME_OVER)
                self.kill()

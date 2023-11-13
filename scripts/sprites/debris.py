import pygame
import random

from scripts.common.utils import State


class Debris(pygame.sprite.Sprite):
    def __init__(self, game, player_x, *groups):
        super().__init__(*groups)
        self.game = game
        self.image = game.assets["brick_box"]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(player_x - 50, player_x + 100)
        self.rect.y = -30
        self.velocity = random.randrange(1, 3)

    def update(self, **kwargs: dict[str, pygame.sprite.Group]):
        self.rect.y += self.velocity
        if self.rect.y > 300:
            self.kill()

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
                self.game.set_state(State.GAME_OVER)
                self.kill()

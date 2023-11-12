import pygame

from scripts.utils import State

PLAYER_SPEED = 1
JUMP_HEIGHT = 7
GRAVITY = 0.5


class Player(pygame.sprite.Sprite):
    def __init__(self, game, assets, *groups):
        super().__init__(groups)
        self.game = game
        self.assets = assets
        self.image = pygame.image.load("./data/images/player/player.png")
        self.rect = self.image.get_rect()
        self.rect.x = 100

        self.velocity = pygame.Vector2(0, 0)
        self.can_jump = False

        self.is_alive = True

        self.action = ""
        self.anim_offset = (+2, +2)
        self.flip = False

        self.set_action("idle")

    def update(
        self,
        platforms_group: pygame.sprite.Group,
        next_level_group: pygame.sprite.Group,
    ):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = PLAYER_SPEED

        self.velocity.y += GRAVITY
        self.rect.x += self.velocity.x
        self.check_collision_x(platforms_group, next_level_group)

        self.rect.y += self.velocity.y
        self.check_collision_y(platforms_group, next_level_group)

        if self.velocity.x > 0:
            self.flip = False
            self.set_action("run")

        if self.velocity.x < 0:
            self.flip = True
            self.set_action("run")

        if self.velocity.x == 0:
            self.set_action("idle")

        if self.velocity.y > 80:
            self.is_alive = False
            self.game.set_state(State.GAME_OVER)

        self.image = pygame.transform.flip(self.animation.img(), self.flip, False)
        self.animation.update()

    def check_collision_x(
        self,
        platforms_group: pygame.sprite.Group,
        next_level_group: pygame.sprite.Group,
    ):
        hits = pygame.sprite.spritecollide(self, platforms_group, False)
        for hit in hits:
            if self.velocity.x > 0:
                self.rect.right = hit.rect.left
            elif self.velocity.x < 0:
                self.rect.left = hit.rect.right

        hits = pygame.sprite.spritecollide(self, next_level_group, False)
        for hit in hits:
            if self.velocity.x != 0:
                self.game.set_state(State.NEXT_LEVEL)

    def check_collision_y(
        self,
        platforms_group: pygame.sprite.Group,
        next_level_group: pygame.sprite.Group,
    ):
        hits = pygame.sprite.spritecollide(self, platforms_group, False)
        for hit in hits:
            if self.velocity.y > 0:
                self.rect.bottom = hit.rect.top
                self.velocity.y = 0
                self.can_jump = True
            elif self.velocity.y < 0:
                self.rect.top = hit.rect.bottom
                self.velocity.y = 0

        hits = pygame.sprite.spritecollide(self, next_level_group, False)
        for hit in hits:
            if self.velocity.y != 0:
                self.game.set_state(State.NEXT_LEVEL)

    def jump(self):
        if self.can_jump:
            self.velocity.y = -JUMP_HEIGHT
            self.can_jump = False
            self.set_action("jump")

    def set_action(self, action: str) -> None:
        if self.action != action:
            self.action = action
            self.animation = self.assets["player/" + action].copy()

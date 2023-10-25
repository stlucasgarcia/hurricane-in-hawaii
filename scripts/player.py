import pygame

PLAYER_SPEED = 1
JUMP_HEIGHT = 7
GRAVITY = 0.5


class Player(pygame.sprite.Sprite):
    def __init__(self, assets, *groups):
        super().__init__(groups)
        self.assets = assets
        self.image = pygame.image.load("./data/images/player.png")
        self.rect = self.image.get_rect()
        self.rect.x = 100

        self.velocity = pygame.Vector2(0, 0)
        self.can_jump = False

        self.action = ""
        self.anim_offset = (+2, +2)
        self.flip = False
        self.set_action("idle")

    def update(self, platforms_group: pygame.sprite.Group):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = PLAYER_SPEED

        self.velocity.y += GRAVITY
        self.rect.x += self.velocity.x
        self.check_collision_x(platforms_group)

        self.rect.y += self.velocity.y
        self.check_collision_y(platforms_group)

        if self.velocity.x > 0:
            self.flip = False
            self.set_action("run")

        if self.velocity.x < 0:
            self.flip = True
            self.set_action("run")

        if self.velocity.x == 0:
            self.set_action("idle")

        self.image = pygame.transform.flip(self.animation.img(), self.flip, False)
        self.animation.update()

        self.can_jump = True

    def check_collision_x(self, platforms_group: pygame.sprite.Group):
        hits = pygame.sprite.spritecollide(self, platforms_group, False)
        for hit in hits:
            if self.velocity.x > 0:
                self.rect.right = hit.rect.left
            elif self.velocity.x < 0:
                self.rect.left = hit.rect.right

    def check_collision_y(self, platforms_group: pygame.sprite.Group):
        hits = pygame.sprite.spritecollide(self, platforms_group, False)
        for hit in hits:
            if self.velocity.y > 0:
                self.rect.bottom = hit.rect.top
                self.velocity.y = 0
            elif self.velocity.y < 0:
                self.rect.top = hit.rect.bottom
                self.velocity.y = 0

    def jump(self):
        if self.can_jump:
            self.velocity.y = -JUMP_HEIGHT
            self.can_jump = False

    def set_action(self, action: str) -> None:
        if self.action != action:
            self.action = action
            self.animation = self.assets["player/" + action].copy()
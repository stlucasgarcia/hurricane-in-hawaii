import pygame

PLAYER_SPEED = 1
JUMP_HEIGHT = 7
GRAVITY = 0.5


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(groups)
        self.image = pygame.image.load("./data/images/player.png")
        self.rect = self.image.get_rect()
        self.rect.x = 100

        self.velocity = pygame.Vector2(0, 0)
        self.can_jump = False

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

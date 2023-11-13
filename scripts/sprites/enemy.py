import pygame


PLAYER_SPEED = 1
GRAVITY = 0.5
ATTACK_DISTANCE = 5  # Adjust as needed


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, assets, *groups):
        super().__init__(groups)
        self.game = game
        self.assets = assets
        self.image = pygame.image.load("./data/images/enemy/enemy.png")
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.sounds = game.sounds

        self.velocity = pygame.Vector2(0, 0)
        self.can_jump = False

        self.is_alive = True
        self.is_attacking = False

        self.action = ""
        self.anim_offset = (-2, -2)
        self.flip = False

        self.animation = None

        self.game.channels["enemy_run"].set_volume(0.1)
        self.game.channels["enemy_run"].play(self.sounds["player/run"], loops=-1)
        self.game.channels["enemy_run"].pause()

        self.set_action("idle")

    def update(
        self,
        **kwargs: dict[str, pygame.sprite.Group],
    ):
        player = kwargs["players"].sprites()[0]

        if self.is_alive:
            # Simple AI: Move towards the player
            if player.rect.x < self.rect.x:
                self.velocity.x = -PLAYER_SPEED
                self.flip = True
                self.set_action("run")
            elif player.rect.x > self.rect.x:
                self.velocity.x = PLAYER_SPEED
                self.flip = False
                self.set_action("run")
            else:
                self.velocity.x = 0
                self.set_action("idle")

            # Check if the enemy is close enough to attack
            if (
                abs(player.rect.x - self.rect.x) < ATTACK_DISTANCE
                and (player.rect.y - self.rect.y) == 16
            ):
                self.set_action("attack", player)

            # Update movement and collisions
            self.velocity.y += GRAVITY
            self.rect.x += self.velocity.x
            self.check_collision_x(kwargs["platforms"])

            self.rect.y += self.velocity.y
            self.check_collision_y(kwargs["platforms"])

            # Update animation
            self.image = pygame.transform.flip(self.animation.img(), self.flip, False)
            self.animation.update()

    def check_collision_x(
        self,
        platforms_group: pygame.sprite.Group,
    ):
        hits = pygame.sprite.spritecollide(self, platforms_group, False)
        for hit in hits:
            if self.velocity.x > 0:
                self.rect.right = hit.rect.left
            elif self.velocity.x < 0:
                self.rect.left = hit.rect.right

    def check_collision_y(
        self,
        platforms_group: pygame.sprite.Group,
    ):
        hits = pygame.sprite.spritecollide(self, platforms_group, False)
        for hit in hits:
            if self.velocity.y > 0:
                self.rect.bottom = hit.rect.top
                self.velocity.y = 0
            elif self.velocity.y < 0:
                self.rect.top = hit.rect.bottom
                self.velocity.y = 0

    def set_action(self, action: str, player=None) -> None:
        if (self.action != action or action == "attack") and (
            self.animation is None or (self.animation.done or self.animation.loop)
        ):
            self.action = action
            self.animation = self.assets["enemy/" + action].copy()

            if action == "attack" and player:
                player.hit()

            if self.game.sound_enabled:
                sound = self.sounds.get("enemy/" + action)

                if action == "run":
                    self.game.channels["enemy_run"].unpause()
                elif action == "idle":
                    self.game.channels["enemy_run"].pause()
                elif action == "attack":
                    self.game.channels["enemy_run"].pause()
                    self.game.channels["enemy"].set_volume(0.4)
                    self.game.channels["enemy"].play(sound)
            else:
                self.game.channels["enemy_run"].pause()

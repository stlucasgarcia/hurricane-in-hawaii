import pygame

from scripts.clouds import Clouds
from scripts.player import Player
from scripts.tilemap import Tilemap

TIME_LIMIT = 5 * 60  # 5 minutes in seconds
JUMP_KEYS = [pygame.K_SPACE, pygame.K_UP, pygame.K_w]


class Level1:
    def __init__(self, game) -> None:
        self.game = game

        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()

        self.clouds = Clouds(self.game.assets["clouds"], 10)

        self.tilemap = Tilemap(
            "./data/levels/1.tmx", self.all_sprites, self.platforms
        ).render()
        self.player = Player(self.game.assets, self.all_sprites)
        self.scroll = [0, 0]

        self.start_time = pygame.time.get_ticks()

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key in JUMP_KEYS:
                self.player.jump()

    def update(self):
        # Camera movement
        self.scroll[0] += (
            self.player.rect.centerx
            - self.game.display.get_width() / 2
            - self.scroll[0]
        ) / 30
        self.scroll[1] += (
            self.player.rect.centery
            - self.game.display.get_height() / 2
            - self.scroll[1]
        ) / 30
        render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

        # Sprites
        self.clouds.update()
        self.clouds.render(self.game.display, offset=render_scroll)

        if self.game.is_running():
            self.all_sprites.update(self.platforms)

        for sprite in self.all_sprites:
            animation_offset = (0, 0)

            if hasattr(sprite, "anim_offset"):
                animation_offset = sprite.anim_offset

            self.game.display.blit(
                sprite.image,
                (
                    sprite.rect.x - render_scroll[0] + animation_offset[0],
                    sprite.rect.y - render_scroll[1] + animation_offset[1],
                ),
            )

        elapsed_time = (
            pygame.time.get_ticks() - self.start_time
        ) // 1000  # Convert to seconds

        if elapsed_time >= TIME_LIMIT:
            print("Time's up! Game over.")
            pygame.quit()
            exit()

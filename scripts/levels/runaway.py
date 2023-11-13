import pygame

from scripts.sprites.clouds import Clouds
from scripts.sprites.helper import Helper
from scripts.sprites.player import Player
from scripts.common.tilemap import Tilemap
from scripts.common.utils import State, load_font

TIME_LIMIT = 3 * 60  # 5 minutes in seconds
JUMP_KEYS = [pygame.K_SPACE, pygame.K_UP, pygame.K_w]


class LevelHelper(Helper):
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


class RunawayLevel:
    def __init__(self, game) -> None:
        self.game = game
        self.name = "runaway"

        self.font = load_font(24)

        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.helpers = pygame.sprite.Group()
        self.next = pygame.sprite.Group()

        self.clouds = Clouds(self.game.assets["clouds"], 10)

        self.tilemap = Tilemap(
            "./data/levels/runaway.tmx", self.all_sprites, self.platforms, self.next
        ).render()
        self.player = Player(self.game, self.game.assets, self.all_sprites)
        self.scroll = [0, 0]

        self.start_time = pygame.time.get_ticks()
        self.helper = LevelHelper(self.game, self.game.assets, self.helpers)
        self.points = 0
        self.is_completed = False

        self.ambient_music = self.game.sounds["ambient/runaway"]
        self.ambient_music.set_volume(0.1)

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
            self.all_sprites.update(self.platforms, self.next)

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

        elapsed_time_text = self.font.render(
            f"{TIME_LIMIT - elapsed_time}",
            False,
            (0, 0, 0),
        )

        self.points = TIME_LIMIT - elapsed_time

        self.game.display.blit(elapsed_time_text, (145, 5))

        self.helper.update(self.platforms)

        if elapsed_time >= TIME_LIMIT:
            self.game.set_state(State.GAME_OVER)

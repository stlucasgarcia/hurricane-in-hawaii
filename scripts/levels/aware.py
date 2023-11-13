import pygame

from scripts.sprites.clouds import Clouds
from scripts.sprites.debris import Debris
from scripts.sprites.helper import AwareHelper
from scripts.sprites.player import Player
from scripts.common.tilemap import Tilemap
from scripts.common.utils import load_font

TIME_LIMIT = 3 * 60  # 5 minutes in seconds
JUMP_KEYS = [pygame.K_SPACE, pygame.K_UP, pygame.K_w]


class AwareLevel:
    def __init__(self, game) -> None:
        self.name = "aware"
        self.game = game

        self.font = load_font(24)

        self.sprite_groups: dict[str, pygame.sprite.Group] = {
            "all_sprites": pygame.sprite.Group(),
            "platforms": pygame.sprite.Group(),
            "helpers": pygame.sprite.Group(),
            "next": pygame.sprite.Group(),
            "players": pygame.sprite.Group(),
            "debris": pygame.sprite.Group(),
        }

        self.clouds = Clouds(self.game.assets["clouds"], 10)

        self.tilemap = Tilemap("./data/levels/aware.tmx", **self.sprite_groups).render()
        self.player = Player(
            self.game,
            self.game.assets,
            [self.sprite_groups["all_sprites"], self.sprite_groups["players"]],
        )
        self.scroll = [0, 0]

        self.helper = AwareHelper(
            self.game, self.game.assets, self.sprite_groups["helpers"]
        )
        self.points = 0
        self.is_completed = False

        self.ambient_music = self.game.sounds["ambient/runaway"]
        self.ambient_music.set_volume(0.1)

        for _ in range(10):  # Adjust the number of debris
            Debris(
                game, [self.sprite_groups["all_sprites"], self.sprite_groups["debris"]]
            )

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
            self.sprite_groups["all_sprites"].update(**self.sprite_groups)

        for sprite in self.sprite_groups["all_sprites"]:
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

        # # Check for collisions (you can add more logic here)
        # collisions = pygame.sprite.spritecollide(self.debris, self.debris, False)
        # for debris in collisions:
        #     debris.rect.y = -30
        #     debris.rect.x = random.randrange(320)

        self.points = 1

        self.helper.update(self.sprite_groups["platforms"])

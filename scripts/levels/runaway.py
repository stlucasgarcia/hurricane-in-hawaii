import pygame

from scripts.sprites.clouds import Clouds
from scripts.sprites.helper import RunawayHelper
from scripts.sprites.player import Player
from scripts.common.tilemap import Tilemap
from scripts.common.utils import State, load_font
from scripts.ui.menu import InstructionRunawayMenu

TIME_LIMIT = 3 * 60  # 5 minutes in seconds
JUMP_KEYS = [pygame.K_SPACE, pygame.K_UP, pygame.K_w]


class RunawayLevel:
    def __init__(self, game) -> None:
        self.name = "runaway"
        self.game = game

        self.font = load_font(24)

        self.sprite_groups: dict[str, pygame.sprite.Group] = {
            "all_sprites": pygame.sprite.Group(),
            "platforms": pygame.sprite.Group(),
            "helpers": pygame.sprite.Group(),
            "next": pygame.sprite.Group(),
        }

        self.clouds = Clouds(self.game.assets["clouds"], 10)

        self.tilemap = Tilemap(
            "./data/levels/runaway.tmx", **self.sprite_groups
        ).render()
        self.player = Player(
            self.game, self.game.assets, self.sprite_groups["all_sprites"]
        )
        self.scroll = [0, 0]

        self.start_time = pygame.time.get_ticks()
        self.helper = RunawayHelper(
            self.game, self.game.assets, self.sprite_groups["helpers"]
        )
        self.points = 0
        self.is_completed = False

        self.ambient_music = self.game.sounds["ambient/runaway"]
        self.ambient_music.set_volume(0.1)

        self.instructions_menu = InstructionRunawayMenu(game)
        self.instructions = True

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key in JUMP_KEYS:
                self.player.jump()

        if self.instructions:
            self.instructions_menu.handle_events(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.instructions_menu.play_menu_select_sound()
                    self.instructions = False

    def update(self):
        if self.instructions:
            self.instructions_menu.render()
            return

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

        self.helper.update(self.sprite_groups["platforms"])

        if elapsed_time >= TIME_LIMIT:
            self.game.set_state(State.GAME_OVER)

import pygame

from scripts.clouds import Clouds
from scripts.player import Player
from scripts.tilemap import Tilemap
from scripts.utils import Animation, load_image, load_images


JUMP_KEYS = [pygame.K_SPACE, pygame.K_UP, pygame.K_w]

TIME_LIMIT = 5 * 60  # 5 minutes in seconds


class Game:
    def __init__(self) -> None:
        pygame.init()

        pygame.display.set_caption("Py Game")

        self.screen = pygame.display.set_mode((640, 480))

        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.assets = {
            "background": load_image("background.png"),
            "clouds": load_images("clouds"),
            "player/idle": Animation(load_images("player/idle"), img_dur=120),
            "player/run": Animation(load_images("player/run"), img_dur=8),
        }

        self.clouds = Clouds(self.assets["clouds"], 10)

        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()

        self.tilemap = Tilemap(
            "./data/levels/1.tmx", self.all_sprites, self.platforms
        ).render()
        self.player = Player(self.assets, self.all_sprites)
        self.scroll = [0, 0]

        self.start_time = pygame.time.get_ticks()

    def run(self) -> None:
        while True:
            self.display.blit(self.assets["background"], (0, 0))

            # Camera movement
            self.scroll[0] += (
                self.player.rect.centerx - self.display.get_width() / 2 - self.scroll[0]
            ) / 30
            self.scroll[1] += (
                self.player.rect.centery
                - self.display.get_height() / 2
                - self.scroll[1]
            ) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            # Sprites
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.all_sprites.update(self.platforms)

            for sprite in self.all_sprites:
                animation_offset = (0, 0)

                if hasattr(sprite, "anim_offset"):
                    animation_offset = sprite.anim_offset

                self.display.blit(
                    sprite.image,
                    (
                        sprite.rect.x - render_scroll[0] + animation_offset[0],
                        sprite.rect.y - render_scroll[1] + animation_offset[1],
                    ),
                )

            # Player inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key in JUMP_KEYS:
                        self.player.jump()

            elapsed_time = (
                pygame.time.get_ticks() - self.start_time
            ) // 1000  # Convert to seconds

            if elapsed_time >= TIME_LIMIT:
                print("Time's up! Game over.")
                pygame.quit()
                exit()

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()

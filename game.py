import pygame

from scripts.clouds import Clouds
from scripts.player import Player
from scripts.tilemap import Tilemap
from scripts.utils import load_image, load_images


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
        }

        self.clouds = Clouds(self.assets["clouds"], 16)

        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()

        self.tilemap = Tilemap(
            "./data/levels/1.tmx", self.all_sprites, self.platforms
        ).render()
        self.player = Player(self.all_sprites)
        self.scroll = [0, 0]

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
                self.display.blit(
                    sprite.image,
                    (
                        sprite.rect.x - render_scroll[0],
                        sprite.rect.y - render_scroll[1],
                    ),
                )

            # Player inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if (
                        event.key == pygame.K_SPACE
                        or event.key == pygame.K_UP
                        or event.key == pygame.K_w
                    ):
                        self.player.jump()

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()

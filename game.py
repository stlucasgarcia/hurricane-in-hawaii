import pygame

from scripts.clouds import Clouds
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

        self.tilemap = Tilemap("./data/levels/0.tmx")

    def run(self) -> None:
        while True:
            self.display.blit(self.assets["background"], (0, 0))

            self.clouds.update()
            self.clouds.render(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.tilemap.sprite_group.draw(self.display)

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()

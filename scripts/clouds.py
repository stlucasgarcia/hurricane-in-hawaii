from random import choice, random

import pygame


class Cloud(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, image, speed, depth, groups) -> None:
        super().__init__(groups)

        self.pos = list(pos)
        self.image = image
        self.rect = self.image.get_rect(topleft=self.pos)
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        self.speed = speed
        self.depth = depth

    def update(self):
        self.pos[0] += self.speed

    def render(self, surf: pygame.Surface, offset=(0, 0)):
        render_pos = (
            self.pos[0] - offset[0] * self.depth,
            self.pos[1] - offset[1] * self.depth,
        )
        surf.blit(
            self.image,
            (
                render_pos[0] % (surf.get_width() + self.image.get_width())
                - self.image.get_width(),
                render_pos[1] % (surf.get_height() + self.image.get_height())
                - self.image.get_height(),
            ),
        )


class Clouds:
    def __init__(self, cloud_images: list, count: int = 10) -> None:
        self.clouds = pygame.sprite.Group()

        for i in range(count):
            Cloud(
                (random() * 99999, random() * 99999),
                choice(cloud_images),
                random() * 0.05 + 0.05,
                random() * 0.6 + 0.2,
                self.clouds,
            )

    def update(self):
        self.clouds.update()

    def render(self, surf: pygame.Surface, offset=(0, 0)):
        for cloud in self.clouds:
            cloud.render(surf, offset=offset)

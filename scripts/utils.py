import pygame
import os

BASE_IMG_PATH = "data/images/"


def load_image(path: str) -> pygame.Surface:
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


def load_images(path: str) -> list[pygame.Surface]:
    return [
        load_image(path + "/" + img_name)
        for img_name in sorted(os.listdir(BASE_IMG_PATH + path))
    ]


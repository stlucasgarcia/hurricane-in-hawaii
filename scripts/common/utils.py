import pygame
import os

from enum import Enum

BASE_IMG_PATH = "data/images/"
BASE_SOUND_PATH = "data/audio/"


def load_image(path: str) -> pygame.Surface:
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


def load_images(path: str) -> list[pygame.Surface]:
    return [
        load_image(path + "/" + img_name)
        for img_name in sorted(os.listdir(BASE_IMG_PATH + path))
    ]


def load_font(size: int) -> pygame.font.Font:
    return pygame.font.Font("./data/fonts/Silver.ttf", size)


def load_sound(path: str) -> pygame.mixer.Sound:
    return pygame.mixer.Sound(BASE_SOUND_PATH + path)


class Animation:
    def __init__(self, images, img_dur=5, loop=True) -> None:
        self.images = images
        self.img_duration = img_dur
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self) -> "Animation":
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (len(self.images) * self.img_duration)
        else:
            self.frame = min(self.frame + 1, len(self.images) * self.img_duration - 1)

            if self.frame >= len(self.images) * self.img_duration - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]


class State(str, Enum):
    START = "start"
    PAUSED = "paused"
    RUNNING = "running"
    NEXT_LEVEL = "next_level"
    GAME_OVER = "game_over"
    FINISHED = "finished"
    LEADERBOARD = "leaderboard"


class MixerChannels(int, Enum):
    BACKGROUND = 0
    AMBIENT = 1
    MENU = 2
    PLAYER = 3
    PLAYER_RUN = 4

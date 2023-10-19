import pygame

from pytmx.util_pygame import load_pygame
from scripts.tile import Tile


class Tilemap:
    def __init__(self, path: str) -> None:
        self.game_map = load_pygame(path, pixelalpha=True)
        self.sprite_group = pygame.sprite.Group()

        self.render()

    def render(self) -> None:
        for layer in self.game_map.visible_layers:
            print(layer.name)
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    pos = (x * self.game_map.tilewidth, y * self.game_map.tileheight)
                    Tile(pos, surf, groups=self.sprite_group)

        for obj in self.game_map.objects:
            pos = obj.x, obj.y
            Tile(pos, obj.image, groups=self.sprite_group)

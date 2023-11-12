import pygame

from pytmx.util_pygame import load_pygame
from scripts.tile import Tile


class Tilemap:
    def __init__(
        self,
        path: str,
        all_sprites: pygame.sprite.Group,
        platforms: pygame.sprite.Group,
        next_level: pygame.sprite.Group,
    ) -> None:
        self.game_map = load_pygame(path, pixelalpha=True)
        self.all_sprites = all_sprites
        self.platforms = platforms
        self.next_level = next_level

    def render(self) -> None:
        for layer in self.game_map.visible_layers:
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    pos = (x * self.game_map.tilewidth, y * self.game_map.tileheight)
                    groups = [self.all_sprites]

                    if layer.name == "terrain":
                        groups.append(self.platforms)

                    Tile(
                        pos,
                        surf,
                        groups=groups,
                    )

        for obj in self.game_map.objects:
            pos = obj.x, obj.y

            if obj.properties.get("type") == "next":
                Tile(pos, obj.image, [self.next_level, self.all_sprites])
                continue

            Tile(pos, obj.image, groups=self.all_sprites)

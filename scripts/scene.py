import pygame
from scripts.level import Level1
from scripts.menu import PauseMenu

from scripts.utils import State


class Scene:
    def __init__(self, game) -> None:
        self.game = game

        self.levels = {
            "level_1": Level1(self.game),
        }
        self.current_level = self.levels["level_1"]
        self.pause_menu = PauseMenu(game, self)

    def create_level(self, level_name: str):
        if level_name == "level_1":
            return Level1(self.game)

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.set_state(State.PAUSED)

        if self.game.is_running():
            self.current_level.handle_events(event)

        self.pause_menu.handle_events(event)

    def update(self):
        self.current_level.update()

        self.pause_menu.render(self.game.is_paused())

    def reset(self):
        self.current_level = self.create_level("level_1")

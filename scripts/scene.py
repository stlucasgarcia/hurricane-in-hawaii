import pygame

from scripts.level import Level1
from scripts.menu import PauseMenu, StartMenu

from scripts.utils import State


class Scene:
    def __init__(self, game) -> None:
        self.game = game

        self.pause_menu = PauseMenu(game, self)
        self.start_menu = StartMenu(game)

        self.levels = {
            "level_1": Level1(self.game),
            "level_2": "Level 2",
            "level_3": "Level 3",
        }

        self.current_level = self.levels["level_1"]

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
        self.start_menu.handle_events(event)

    def update(self):
        self.current_level.update()

        self.pause_menu.render(self.game.is_paused())
        self.start_menu.render(self.game.is_start())

    def reset(self):
        self.current_level = self.create_level("level_1")

import pygame
from scripts.levels.aware import AwareLevel

from scripts.levels.runaway import RunawayLevel
from scripts.ui.menu import GameOverMenu, PauseMenu, StartMenu

from scripts.common.utils import State


class Scene:
    def __init__(self, game) -> None:
        self.game = game

        self.pause_menu = PauseMenu(game, self)
        self.start_menu = StartMenu(game)
        self.game_over_menu = GameOverMenu(game)

        self.levels = {
            "runaway": RunawayLevel(self.game),
            "aware": AwareLevel(self.game),
            "final": "final",
        }

        self.current_level = self.levels["runaway"]
        self.channel = game.channels["ambient"]

        self.is_alive = True

    def create_level(self, level_name: str):
        if level_name == "runaway":
            return RunawayLevel(self.game)
        elif level_name == "aware":
            return AwareLevel(self.game)

    def next_level(self):
        if self.current_level.name == "runaway":
            self.current_level = self.create_level("aware")
        if self.current_level.name == "aware":
            self.current_level = self.create_level("final")
        if self.current_level.name == "final":
            self.game.set_state(State.FINISHED)

    def get_points(self):
        points = 0

        for level in self.levels.values():
            if level.is_completed:
                points += level.points

        return points

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.set_state(State.PAUSED)

        if self.game.is_running():
            self.current_level.handle_events(event)

        if self.game.is_paused():
            self.pause_menu.handle_events(event)

        if self.game.is_start():
            self.start_menu.handle_events(event)

        if self.game.is_game_over():
            self.game_over_menu.handle_events(event)

    def play_ambient_music(self):
        if not self.game.sound_enabled:
            return

        if not self.channel.get_busy():
            self.channel.play(self.current_level.ambient_music, loops=-1)

    def update(self):
        if self.game.is_running():
            self.current_level.update()
            self.play_ambient_music()

        else:
            self.channel.stop()

        self.pause_menu.render(self.game.is_paused())
        self.start_menu.render(self.game.is_start())
        self.game_over_menu.render(self.game.is_game_over(), self.get_points())

    def reset(self):
        self.current_level = self.create_level("level_1")

import pygame

from scripts.levels.aware import AwareLevel
from scripts.levels.final import FinalLevel

from scripts.levels.runaway import RunawayLevel
from scripts.ui.menu import GameOverMenu, LeaderboardMenu, PauseMenu, StartMenu

from scripts.common.utils import State


class Scene:
    def __init__(self, game) -> None:
        self.game = game

        self.pause_menu = PauseMenu(game, self)
        self.start_menu = StartMenu(game)
        self.game_over_menu = GameOverMenu(game)
        self.leaderboard_menu = LeaderboardMenu(game)

        self.levels = {
            "runaway": RunawayLevel(self.game),
            "aware": AwareLevel(self.game),
            "final": FinalLevel(self.game),
        }

        self.current_level = self.levels["runaway"]
        self.channel = game.channels["ambient"]

        self.is_alive = True

    def create_level(self, level_name: str):
        if self.current_level.name != level_name:
            self.current_level.is_completed = True

        if level_name == "runaway":
            self.levels["runaway"] = RunawayLevel(self.game)
            self.current_level = self.levels["runaway"]
        elif level_name == "aware":
            self.levels["aware"] = AwareLevel(self.game)
            self.current_level = self.levels["aware"]
        elif level_name == "final":
            self.levels["final"] = FinalLevel(self.game)
            self.current_level = self.levels["final"]

    def next_level(self):
        if not self.current_level:
            self.create_level("runaway")
        elif self.current_level.name == "runaway":
            self.create_level("aware")
        elif self.current_level.name == "aware":
            self.create_level("final")
        elif self.current_level.name == "final":
            self.current_level.is_completed = True
            self.current_level.points += 500
            self.game.set_state(State.LEADERBOARD)

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

        if self.game.is_leaderboard():
            self.leaderboard_menu.handle_events(event)

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
        self.leaderboard_menu.render(self.game.is_leaderboard())

    def reset(self):
        self.create_level(self.current_level.name)

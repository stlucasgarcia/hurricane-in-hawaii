import pygame

from scripts.utils import load_font

SILVER = (128, 128, 128, 220)  # Silver color with alpha for transparency


class Menu:
    def __init__(self, game) -> None:
        self.game = game
        self.display_width = game.display.get_width()
        self.display_height = game.display.get_height()
        self.display = game.display

        self.font = load_font(36)

    def render(self, show: bool = False) -> None:
        raise NotImplementedError


class PauseMenu(Menu):
    def __init__(self, game, scene) -> None:
        super().__init__(game)
        self.scene = scene

        self.subtitle_font = load_font(24)
        self.controls_font = load_font(14)

    def render(self, show: bool = False) -> None:
        if not show:
            return

        menu_text = self.font.render("Paused", True, (0, 0, 0))

        game_menu_controls = self.subtitle_font.render(
            "Game Controls:", True, (0, 0, 0)
        )
        game_menu_controls_text = self.controls_font.render(
            "left arrow / a - Move left\nright arrow / d - Move right\nup arrow / space - Jump\nesc - Pause the game",  # noqa: E501
            True,
            (0, 0, 0),
        )

        pause_menu_controls = self.subtitle_font.render(
            "Menu Controls:", True, (0, 0, 0)
        )
        pause_menu_controls_text = self.controls_font.render(
            "r - Restart level\nspace - Go to start\nq - Quit the game\nf - Fullscreen",  # noqa: E501
            True,
            (0, 0, 0),
        )

        # Draw a silver filter
        silver_filter = pygame.Surface(
            (self.display_width, self.display_height),
            pygame.SRCALPHA,
        )
        silver_filter.fill(SILVER)
        self.display.blit(silver_filter, (0, 0))

        self.display.blit(menu_text, (self.display_width // 2 - 32, 10))

        self.display.blit(game_menu_controls, (self.display_width // 2 - 150, 60))
        self.display.blit(game_menu_controls_text, (self.display_width // 2 - 150, 90))

        self.display.blit(pause_menu_controls, (self.display_width // 2 + 50, 60))
        self.display.blit(pause_menu_controls_text, (self.display_width // 2 + 50, 90))

    def handle_events(self, event: pygame.event.Event) -> None:
        if not self.scene.game.is_paused():
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.scene.reset()
            if event.key == pygame.K_q:
                pygame.quit()
                exit()
            if event.key == pygame.K_f:
                self.game.toggle_fullscreen()

import pygame

from scripts.utils import State, load_font

SILVER = (128, 128, 128, 220)
LIGHT_SILVER = (192, 192, 192, 220)


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
            "r - Restart level\ni - Go to start\nq - Quit the game\nf - Fullscreen",  # noqa: E501
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.scene.reset()
            if event.key == pygame.K_q:
                pygame.quit()
                exit()
            if event.key == pygame.K_f:
                self.game.toggle_fullscreen()
            if event.key == pygame.K_i:
                self.game.set_state(State.START)


class StartMenu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.title_font = load_font(48)
        self.show_subtitle = True

        self.font_fade = pygame.USEREVENT + 1
        pygame.time.set_timer(self.font_fade, 800)

    def render(self, show: bool = False) -> None:
        if not show:
            return

        menu_text = self.title_font.render("Earthquake in Hawaii ", True, (0, 0, 0))
        subtitle_text = self.font.render("Press space to start", True, (0, 0, 0))

        # Draw a silver filter
        silver_filter = pygame.Surface(
            (self.display_width, self.display_height),
            pygame.SRCALPHA,
        )
        silver_filter.fill(LIGHT_SILVER)
        self.display.blit(silver_filter, (0, 0))

        self.display.blit(menu_text, (self.display_width // 2 - 140, 15))

        # make it blink
        if self.show_subtitle:
            self.display.blit(subtitle_text, (self.display_width // 2 - 115, 180))

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == self.font_fade:
            self.show_subtitle = not self.show_subtitle

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.set_state(State.RUNNING)


class GameOverMenu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.title_font = load_font(50)
        self.show_subtitle = True
        self.small_font = load_font(20)

        self.font_fade = pygame.USEREVENT + 1
        pygame.time.set_timer(self.font_fade, 800)

    def render(self, show: bool = False, points: int = 0) -> None:
        if not show:
            return

        menu_text = self.title_font.render("GAME OVER", True, (139, 0, 0))
        points_text = self.small_font.render(f"{points} points", True, (0, 0, 0))
        subtitle_text = self.font.render("Press space to restart", True, (0, 0, 0))

        # Draw a silver filter
        silver_filter = pygame.Surface(
            (self.display_width, self.display_height),
            pygame.SRCALPHA,
        )
        silver_filter.fill(LIGHT_SILVER)
        self.display.blit(silver_filter, (0, 0))

        self.display.blit(menu_text, (self.display_width // 2 - 65, 15))
        self.display.blit(points_text, (self.display_width // 2 - 25, 60))

        # make it blink
        if self.show_subtitle:
            self.display.blit(subtitle_text, (self.display_width // 2 - 125, 180))

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == self.font_fade:
            self.show_subtitle = not self.show_subtitle

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.set_state(State.START)

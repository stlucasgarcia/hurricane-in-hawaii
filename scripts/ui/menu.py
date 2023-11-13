import pygame
from random import randint

from scripts.common.utils import State, load_font

SILVER = (128, 128, 128, 220)
LIGHT_SILVER = (192, 192, 192, 220)


class Menu:
    def __init__(self, game) -> None:
        self.game = game
        self.display_width = game.display.get_width()
        self.display_height = game.display.get_height()
        self.display = game.display
        self.sounds = game.sounds

        self.channel = game.channels["menu"]
        self.channel.set_volume(0.2)

        self.font = load_font(36)

    def render(self, show: bool = False) -> None:
        raise NotImplementedError

    def play_menu_select_sound(self, variant: int = None) -> None:
        if not self.game.sound_enabled:
            return

        if not variant:
            variant = randint(0, 1)

        if variant == 0:
            self.channel.play(self.sounds["ui/select"])
        else:
            self.channel.play(self.sounds["ui/select_alternative"])

    def play_game_over_sound(self) -> None:
        if not self.game.sound_enabled:
            return

        self.channel.play(self.sounds["ui/game_over"])


class PauseMenu(Menu):
    def __init__(self, game, scene) -> None:
        super().__init__(game)
        self.scene = scene

        self.subtitle_font = load_font(24)
        self.controls_font = load_font(14)

    def render(self, show: bool = False) -> None:
        if not show:
            return

        menu_text = self.font.render("Pause", False, (0, 0, 0))

        game_menu_controls = self.subtitle_font.render(
            "Controle jogo:", False, (0, 0, 0)
        )
        game_menu_controls_text = self.controls_font.render(
            "seta esquerda / a - Movimentar esquerda\nseta direita / d - Movimentar direita\nseta cima / space - Pular\nesc - Pausar o jogo",  # noqa: E501
            False,
            (0, 0, 0),
        )

        pause_menu_controls = self.subtitle_font.render(
            "Controle pause:", False, (0, 0, 0)
        )
        pause_menu_controls_text = self.controls_font.render(
            "r - Reiniciar o nível\ni - Ir para o início\nq - Sair do jogo\nf - Tela cheia\ns - Tirar o som",  # noqa: E501
            False,
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
                self.play_menu_select_sound()
                self.scene.reset()
            if event.key == pygame.K_q:
                self.play_game_over_sound()
                pygame.quit()
                exit()
            if event.key == pygame.K_f:
                self.play_menu_select_sound()
                self.game.toggle_fullscreen()
            if event.key == pygame.K_i:
                self.play_menu_select_sound()
                self.game.set_state(State.START)
            if event.key == pygame.K_s:
                self.game.toggle_sound_enabled()


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

        menu_text = self.title_font.render("Terremoto no Havaí", False, (0, 0, 0))
        subtitle_text = self.font.render("Press space to start", False, (0, 0, 0))

        # Draw a silver filter
        silver_filter = pygame.Surface(
            (self.display_width, self.display_height),
            pygame.SRCALPHA,
        )
        silver_filter.fill(LIGHT_SILVER)
        self.display.blit(silver_filter, (0, 0))

        self.display.blit(menu_text, (self.display_width // 2 - 132, 15))

        # make it blink
        if self.show_subtitle:
            self.display.blit(subtitle_text, (self.display_width // 2 - 115, 180))

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == self.font_fade:
            self.show_subtitle = not self.show_subtitle

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.play_menu_select_sound()
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

        menu_text = self.title_font.render("GAME OVER", False, (139, 0, 0))
        points_text = self.small_font.render(f"{points} points", False, (0, 0, 0))
        subtitle_text = self.font.render("Press space to restart", False, (0, 0, 0))

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
                self.play_menu_select_sound()
                self.game.set_state(State.START)

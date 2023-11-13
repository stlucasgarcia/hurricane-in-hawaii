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
            "r - Reiniciar o nível\ni - Ir para o início\nq - Sair do jogo\nf - Tela cheia\ns - Tirar o som\nl - Leaderboard",  # noqa: E501
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
            if event.key == pygame.K_l:
                self.play_menu_select_sound()
                self.game.set_state(State.LEADERBOARD)


class StartMenu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.title_font = load_font(48)
        self.small_font = load_font(24)
        self.smaller_font = load_font(20)
        self.show_subtitle = True

        self.font_fade = pygame.USEREVENT + 1
        pygame.time.set_timer(self.font_fade, 800)

        self.player_name = "Digite o seu nome"

    def render(self, show: bool = False) -> None:
        if not show:
            return

        menu_text = self.title_font.render("Terremoto no Havaí", False, (0, 0, 0))
        subtitle_text = self.font.render("Press space to start", False, (0, 0, 0))
        player_title_text = self.small_font.render("Player", False, (0, 0, 0))
        player_name_text = self.smaller_font.render(self.player_name, False, (0, 0, 0))

        # Draw a silver filter
        silver_filter = pygame.Surface(
            (self.display_width, self.display_height),
            pygame.SRCALPHA,
        )
        silver_filter.fill(LIGHT_SILVER)
        self.display.blit(silver_filter, (0, 0))

        self.display.blit(menu_text, (self.display_width // 2 - 132, 15))
        self.display.blit(player_title_text, (self.display_width // 2 - 132, 60))
        self.display.blit(player_name_text, (self.display_width // 2 - 132, 80))

        # make it blink
        if self.show_subtitle:
            self.display.blit(subtitle_text, (self.display_width // 2 - 115, 180))

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == self.font_fade:
            self.show_subtitle = not self.show_subtitle

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                self.game.player_data["name"] = self.player_name
                self.play_menu_select_sound()
                self.game.set_state(State.RUNNING)

            if event.key == pygame.K_ESCAPE:
                self.player_name = ""
            elif event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            else:
                self.player_name += event.unicode


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


class InstructionRunawayMenu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.title_font = load_font(30)
        self.show_subtitle = True
        self.small_font = load_font(20)

        self.font_fade = pygame.USEREVENT + 1
        pygame.time.set_timer(self.font_fade, 800)

    def render(self) -> None:
        menu_text = self.title_font.render("Instruções", False, (139, 0, 0))
        tip_text = self.small_font.render(
            "Mantenha-se calmo e encontre uma rota de fuga", False, (0, 0, 0)
        )
        tip_time_text = self.small_font.render("Cuidado com o tempo!", False, (0, 0, 0))
        subtitle_text = self.font.render("Press space to continue", False, (0, 0, 0))

        # Draw a silver filter
        silver_filter = pygame.Surface(
            (self.display_width, self.display_height),
            pygame.SRCALPHA,
        )
        silver_filter.fill(LIGHT_SILVER)
        self.display.blit(silver_filter, (0, 0))

        self.display.blit(menu_text, (self.display_width // 2 - 60, 15))
        self.display.blit(tip_text, (self.display_width // 2 - 150, 60))
        self.display.blit(tip_time_text, (self.display_width // 2 - 150, 80))

        # make it blink
        if self.show_subtitle:
            self.display.blit(subtitle_text, (self.display_width // 2 - 125, 180))

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == self.font_fade:
            self.show_subtitle = not self.show_subtitle


class InstructionAwareMenu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.title_font = load_font(30)
        self.show_subtitle = True
        self.small_font = load_font(20)

        self.font_fade = pygame.USEREVENT + 1
        pygame.time.set_timer(self.font_fade, 800)

    def render(self) -> None:
        menu_text = self.title_font.render("Instruções", False, (139, 0, 0))
        tip_text = self.small_font.render(
            "Preste atenção ao seu redor", False, (0, 0, 0)
        )
        tip_time_text = self.small_font.render(
            "Cuidado com objetos caindo!", False, (0, 0, 0)
        )
        subtitle_text = self.font.render("Press space to continue", False, (0, 0, 0))

        # Draw a silver filter
        silver_filter = pygame.Surface(
            (self.display_width, self.display_height),
            pygame.SRCALPHA,
        )
        silver_filter.fill(LIGHT_SILVER)
        self.display.blit(silver_filter, (0, 0))

        self.display.blit(menu_text, (self.display_width // 2 - 60, 15))
        self.display.blit(tip_text, (self.display_width // 2 - 150, 60))
        self.display.blit(tip_time_text, (self.display_width // 2 - 150, 80))

        # make it blink
        if self.show_subtitle:
            self.display.blit(subtitle_text, (self.display_width // 2 - 125, 180))

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == self.font_fade:
            self.show_subtitle = not self.show_subtitle


class InstructionFinalMenu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.title_font = load_font(30)
        self.show_subtitle = True
        self.small_font = load_font(20)

        self.font_fade = pygame.USEREVENT + 1
        pygame.time.set_timer(self.font_fade, 800)

    def render(self) -> None:
        menu_text = self.title_font.render("Instruções", False, (139, 0, 0))
        tip_text = self.small_font.render("Corra e procure abrigo", False, (0, 0, 0))
        tip_time_text = self.small_font.render("Fuja do terremoto!", False, (0, 0, 0))
        subtitle_text = self.font.render("Press space to continue", False, (0, 0, 0))

        # Draw a silver filter
        silver_filter = pygame.Surface(
            (self.display_width, self.display_height),
            pygame.SRCALPHA,
        )
        silver_filter.fill(LIGHT_SILVER)
        self.display.blit(silver_filter, (0, 0))

        self.display.blit(menu_text, (self.display_width // 2 - 60, 15))
        self.display.blit(tip_text, (self.display_width // 2 - 150, 60))
        self.display.blit(tip_time_text, (self.display_width // 2 - 150, 80))

        # make it blink
        if self.show_subtitle:
            self.display.blit(subtitle_text, (self.display_width // 2 - 125, 180))

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == self.font_fade:
            self.show_subtitle = not self.show_subtitle


class LeaderboardMenu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.title_font = load_font(30)
        self.show_subtitle = True
        self.small_font = load_font(20)

        self.font_fade = pygame.USEREVENT + 1
        pygame.time.set_timer(self.font_fade, 800)

        self.leaderboard_data = sorted(
            self.game.leaderboard["players"], key=lambda x: x["score"], reverse=True
        )[:5]

    def render(self, show: bool) -> None:
        if not show:
            return

        self.leaderboard_data = sorted(
            self.game.leaderboard["players"], key=lambda x: x["score"], reverse=True
        )[:5]

        menu_text = self.title_font.render("Leaderboard", False, (25, 25, 112))

        subtitle_text = self.font.render("Press i to go to start", False, (0, 0, 0))

        # Draw a silver filter
        silver_filter = pygame.Surface(
            (self.display_width, self.display_height),
            pygame.SRCALPHA,
        )
        silver_filter.fill(LIGHT_SILVER)
        self.display.blit(silver_filter, (0, 0))

        self.display.blit(menu_text, (self.display_width // 2 - 60, 15))

        # make it blink
        if self.show_subtitle:
            self.display.blit(subtitle_text, (self.display_width // 2 - 120, 180))

        y = 60
        for player in self.leaderboard_data:
            text = self.small_font.render(
                f"{player['name']}: {player['score']} points", False, (0, 0, 0)
            )
            self.display.blit(text, (self.display_width // 2 - 132, y))
            y += 20

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == self.font_fade:
            self.show_subtitle = not self.show_subtitle

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                self.play_menu_select_sound()
                self.game.set_state(State.START)

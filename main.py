import pygame

from scripts.common.scene import Scene
from scripts.common.utils import (
    Animation,
    MixerChannels,
    State,
    load_image,
    load_images,
    load_sound,
)


class Game:
    def __init__(self) -> None:
        pygame.init()

        pygame.display.set_caption("Terremoto no Havaí")

        self.screen = pygame.display.set_mode((640, 480), pygame.SCALED)
        self.is_fullscreen = False

        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        pygame.mixer.set_num_channels(10)
        self.sound_enabled = True

        self.assets = {
            "background": load_image("background.png"),
            "clouds": load_images("clouds"),
            "player/idle": Animation(load_images("player/idle"), img_dur=120),
            "player/run": Animation(load_images("player/run"), img_dur=8),
            "player/jump": Animation(load_images("player/jump"), img_dur=1),
        }

        self.sounds: dict[str, pygame.mixer.Sound] = {
            "ui/select": load_sound("ui/select.wav"),
            "ui/select_alternative": load_sound("ui/select_2.wav"),
            "ui/game_over": load_sound("ui/game_over.wav"),
            "ui/menu_in": load_sound("ui/menu_in.wav"),
            "ui/menu_out": load_sound("ui/menu_out.wav"),
            "player/jump": load_sound("player/jump.wav"),
            "player/run": load_sound("player/run.wav"),
            "background/runaway": load_sound("background/runaway.wav"),
        }

        self.channels = {
            "background": pygame.mixer.Channel(MixerChannels.BACKGROUND),
            "menu": pygame.mixer.Channel(MixerChannels.MENU),
            "player": pygame.mixer.Channel(MixerChannels.PLAYER),
            "player_run": pygame.mixer.Channel(MixerChannels.PLAYER_RUN),
        }

        self.scene = Scene(self)

        self.state = State.START

    def set_state(self, state: State):
        if state == State.PAUSED:
            if self.state == State.RUNNING:
                self.channels["menu"].play(self.sounds["ui/menu_in"])
                self.state = state

            elif self.state == State.PAUSED:
                self.channels["menu"].play(self.sounds["ui/menu_out"])
                self.state = State.RUNNING

        elif state == State.START:
            self.scene = Scene(self)
            self.state = state

        elif state == State.GAME_OVER:
            self.channels["menu"].play(self.sounds["ui/game_over"])
            self.state = state

        else:
            self.state = state

    def is_paused(self) -> bool:
        return self.state == State.PAUSED

    def is_running(self) -> bool:
        return self.state == State.RUNNING

    def is_start(self) -> bool:
        return self.state == State.START

    def is_game_over(self) -> bool:
        return self.state == State.GAME_OVER

    def toggle_fullscreen(self):
        if self.is_fullscreen:
            pygame.display.set_mode((640, 480), pygame.SCALED)
            self.is_fullscreen = False

        else:
            pygame.display.set_mode((640, 480), pygame.FULLSCREEN)
            self.is_fullscreen = True

    def run(self) -> None:
        while True:
            self.display.blit(self.assets["background"], (0, 0))

            # Player inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                self.scene.handle_events(event)

            self.scene.update()

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()

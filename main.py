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
            "brick_box": load_image("objects/brick_box.png"),
            "enemy/idle": Animation(load_images("enemy/idle"), img_dur=60),
            "enemy/run": Animation(load_images("enemy/run"), img_dur=8),
            "enemy/attack": Animation(load_images("enemy/attack"), img_dur=1),
        }

        self.sounds: dict[str, pygame.mixer.Sound] = {
            "ui/select": load_sound("ui/select.wav"),
            "ui/select_alternative": load_sound("ui/select_2.wav"),
            "ui/game_over": load_sound("ui/game_over.wav"),
            "ui/menu_in": load_sound("ui/menu_in.wav"),
            "ui/menu_out": load_sound("ui/menu_out.wav"),
            "player/jump": load_sound("player/jump.wav"),
            "player/run": load_sound("player/run.wav"),
            "ambient/runaway": load_sound("ambient/runaway.wav"),
            "background/game": load_sound("background/game.mp3"),
            "background/presentation": load_sound("background/presentation.mp3"),
        }

        self.channels = {
            "background": pygame.mixer.Channel(MixerChannels.BACKGROUND),
            "ambient": pygame.mixer.Channel(MixerChannels.AMBIENT),
            "menu": pygame.mixer.Channel(MixerChannels.MENU),
            "player": pygame.mixer.Channel(MixerChannels.PLAYER),
            "player_run": pygame.mixer.Channel(MixerChannels.PLAYER_RUN),
        }
        self.channels["background"].set_volume(0.3)
        self.channels["background"].play(
            self.sounds["background/presentation"], loops=-1
        )

        self.scene = Scene(self)

        self.state = State.START

    def play_state_sound(self, channel, sound_name: str):
        if not self.sound_enabled:
            return

        channel.play(self.sounds[sound_name])

    def set_state(self, state: State):
        if state == State.PAUSED:
            if self.state == State.RUNNING:
                self.play_state_sound(self.channels["menu"], "ui/menu_in")
                self.channels["player_run"].pause()
                self.state = state

            elif self.state == State.PAUSED:
                self.play_state_sound(self.channels["menu"], "ui/menu_out")
                self.channels["player_run"].unpause()
                self.state = State.RUNNING

        elif state == State.START:
            self.scene = Scene(self)
            self.state = state
            self.play_state_sound(
                self.channels["background"], "background/presentation"
            )

        elif state == State.GAME_OVER:
            self.channels["menu"].set_volume(1)
            self.play_state_sound(self.channels["menu"], "ui/game_over")
            self.state = state

        elif state == State.RUNNING:
            self.state = state
            self.play_state_sound(self.channels["background"], "background/game")

        elif state == State.NEXT_LEVEL:
            self.scene.next_level()
            self.state = State.RUNNING

        else:
            self.state = state

    def toggle_sound_enabled(self):
        self.sound_enabled = not self.sound_enabled

        if not self.sound_enabled:
            for channel in self.channels.values():
                channel.pause()

        else:
            for channel in self.channels.values():
                channel.unpause()

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

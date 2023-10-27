import pygame

from scripts.scene import Scene
from scripts.utils import Animation, State, load_image, load_images


class Game:
    def __init__(self) -> None:
        pygame.init()

        pygame.display.set_caption("Py Game")

        self.screen = pygame.display.set_mode((640, 480), pygame.SCALED)
        self.is_fullscreen = False

        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.assets = {
            "background": load_image("background.png"),
            "clouds": load_images("clouds"),
            "player/idle": Animation(load_images("player/idle"), img_dur=120),
            "player/run": Animation(load_images("player/run"), img_dur=8),
        }

        self.scene = Scene(self)

        self.state = State.START

    def set_state(self, state: State):
        if state == State.PAUSED:
            if self.state == State.RUNNING:
                self.state = state

            elif self.state == State.PAUSED:
                self.state = State.RUNNING

        else:
            self.state = state

    def is_paused(self) -> bool:
        return self.state == State.PAUSED

    def is_running(self) -> bool:
        return self.state == State.RUNNING

    def is_start(self) -> bool:
        return self.state == State.START

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

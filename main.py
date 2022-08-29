import retro
import pygame

from constants import *


class MarioKart:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("MARIO KART")

        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.fps_clock = pygame.time.Clock()
        self.running = True

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def run(self):
        env = retro.make('SuperMarioKart-Snes')
        env.reset()

        while self.running:
            self.window.fill(WHITE)

            ram = env.get_ram()
            action = env.action_space.sample()
            buttons = env.buttons

            print(buttons)
            print(action)

            action = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            env.step(action)
            env.render()

            pygame.display.update()
            self.fps_clock.tick(MAX_FPS)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game = MarioKart()
    game.run()

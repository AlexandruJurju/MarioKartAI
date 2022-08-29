import retro
import pygame


class MarioKart:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("MARIO KART")
        self.fps_clock = pygame.time.Clock()

    def run(self):
        env = retro.make('SuperMarioKart-Snes')
        env.reset()

        while True:
            ram = env.get_ram()

            action = env.action_space.sample()
            env.step(action)
            env.render()

            pygame.display.update()
            self.fps_clock.tick(50)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game = MarioKart()
    game.run()

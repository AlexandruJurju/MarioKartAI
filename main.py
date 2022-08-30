import math

import cv2
import numpy as np
import retro
import pygame
from PIL import ImageGrab
from matplotlib import pyplot as plt

from constants import *

pressed_key = [1, 0, 0, 0, 0, 0, 0, 0, 0]


def gray_conversion(image):
    height, width, channel = image.shape
    for i in range(0, height):
        for j in range(0, width):
            blue_component = image[i][j][0]
            green_component = image[i][j][1]
            red_component = image[i][j][2]
            gray_value = 0.07 * blue_component + 0.72 * green_component + 0.21 * red_component
            image[i][j] = gray_value
    return image


def smech_gray(val, min, max):
    if val > max:
        val = max
    if val < min:
        val = min
    g = math.floor((val - min) / (max - min) * 255)
    return g, g, g


class MarioKart:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("MARIO KART")

        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.fps_clock = pygame.time.Clock()
        self.running = True

        self.env = retro.make('SuperMarioKart-Snes')
        self.env.reset()

    def process_events(self):
        global pressed_key
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_UP:
                    pressed_key = [1, 0, 0, 0, 0, 0, 0, 0, 0]
                if event.key == pygame.K_RIGHT:
                    pressed_key = [1, 0, 0, 0, 0, 0, 0, 1, 0]
                if event.key == pygame.K_LEFT:
                    pressed_key = [1, 0, 0, 0, 0, 0, 1, 0, 0]

    def run(self):
        while self.running:
            self.window.fill(WHITE)

            self.process_events()
            self.env.step(pressed_key)
            rgb_array = self.env.render(mode="rgb_array")
            self.draw_game_windows(rgb_array)

            pygame.display.update()
            self.fps_clock.tick(MAX_FPS)

    def draw_game_windows(self, rgb_array):
        # draw game window from np array
        game_window = np.swapaxes(rgb_array, 0, 1)
        new_surf = pygame.pixelcopy.make_surface(game_window)
        new_surf = pygame.transform.scale2x(new_surf)
        self.window.blit(new_surf, (25, 25))

        # draw input image , grayscale and resized to 17x17
        gray = rgb_array[:][25:70][:]
        gray = cv2.resize(gray, (17, 17))
        gray = gray_conversion(gray)
        gray_window = np.swapaxes(gray, 0, 1)
        gray_surf = pygame.pixelcopy.make_surface(gray_window)
        gray_surf = pygame.transform.scale(gray_surf, (200, 200))
        self.window.blit(gray_surf, (650, 200))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game = MarioKart()
    game.run()

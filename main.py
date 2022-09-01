import math

import cv2
import numpy as np
import retro
import pygame
from PIL import ImageGrab
from matplotlib import pyplot as plt

from constants import *

player_action = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


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


class MarioKart:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("MARIO KART")

        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.fps_clock = pygame.time.Clock()
        self.running = True

        self.env = retro.make('SuperMarioKart-Snes')
        observation = self.env.reset()
        print(self.env.buttons)

    def process_events(self):
        global player_action
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_UP:
                    player_action = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                if event.key == pygame.K_RIGHT:
                    player_action = [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
                if event.key == pygame.K_LEFT:
                    player_action = [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]

    def run(self):
        while self.running:
            self.window.fill(WHITE)
            self.process_events()

            self.draw_snes_controller(player_action)
            observation, reward, done, info = self.env.step(player_action)
            rgb_array = self.env.render(mode="rgb_array")
            self.draw_game_windows(observation)

            pygame.display.update()
            self.fps_clock.tick(MAX_FPS)

    def draw_game_windows(self, rgb_array):
        # draw game window from np array
        game_window = np.swapaxes(rgb_array, 0, 1)
        new_surf = pygame.pixelcopy.make_surface(game_window)
        new_surf = pygame.transform.scale2x(new_surf)
        self.window.blit(new_surf, (25, 25))

        # draw input image , grayscale and resized to 17x17
        # gray = rgb_array[:][25:70][:]
        # gray = cv2.resize(gray, (17, 17))
        # gray = gray_conversion(gray)
        # gray_window = np.swapaxes(gray, 0, 1)
        # gray_surf = pygame.pixelcopy.make_surface(gray_window)
        # gray_surf = pygame.transform.scale(gray_surf, (200, 200))
        # self.window.blit(gray_surf, (650, 200))

    def draw_snes_controller(self, action: []):
        square_base_x = 600
        square_base_y = 500
        square_width = 35
        square_height = 50
        square_distance = 60

        circle_base_x = square_base_x + square_distance * 4
        circle_base_y = square_base_y + 25
        circle_radius = 20
        circle_distance = 65

        controller_left_corner = (square_base_x - 25, square_base_y - 100)
        controller_width_height = ((circle_base_x + circle_distance) - square_base_x + square_distance + circle_distance, square_height * 5)

        pygame.draw.rect(self.window, (0, 125, 200), pygame.Rect(controller_left_corner, controller_width_height))

        # get a map of form BUTTON : 0 if buttons is not pressed, 1 if button is pressed
        buttons = self.env.buttons
        colors = {}
        for i, button in enumerate(buttons):
            # colors[button] = action[i]
            if action[i] == 1:
                colors[button] = GREEN
            else:
                colors[button] = BLACK

        # LEFT
        pygame.draw.rect(self.window, colors["LEFT"], pygame.Rect(square_base_x, square_base_y, square_width, square_height))

        # RIGHT
        pygame.draw.rect(self.window, colors["RIGHT"], pygame.Rect(square_base_x + square_distance * 2, square_base_y, square_width, square_height))

        # UP
        pygame.draw.rect(self.window, colors["UP"], pygame.Rect(square_base_x + square_distance, square_base_y - square_distance, square_width, square_height))

        # DOWN
        pygame.draw.rect(self.window, colors["DOWN"], pygame.Rect(square_base_x + square_distance, square_base_y + square_distance, square_width, square_height))

        # Y CIRCLE
        pygame.draw.circle(self.window, colors["Y"], (circle_base_x, circle_base_y), circle_radius)

        # X CIRCLE
        pygame.draw.circle(self.window, colors["X"], (circle_base_x + circle_distance, circle_base_y - circle_distance), circle_radius)

        # B CIRCLE
        pygame.draw.circle(self.window, colors["B"], (circle_base_x + circle_distance, circle_base_y + circle_distance), circle_radius)

        # A CIRCLE
        pygame.draw.circle(self.window, colors["Y"], (circle_base_x + circle_distance + circle_distance, circle_base_y), circle_radius)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game = MarioKart()
    game.run()

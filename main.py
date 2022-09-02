import typing

import numpy
import numpy as np
import retro
import pygame
from enum import Enum

from constants import *

player_action = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# ENUM for items ???
# nothing = (0,60)
# mushroom = (0,52)
# feather = (1,52)
# star = (2,56)
# banana = (3,56)
# green shell = (4,48)
# red shell = (5,52)
# coin = (7,56)
# lightning = (8,56)
# selecting/spinning = (0-8,?)
items = (0x0D70, 0x0C69)

# Enum for statuses ?
# on the ground = 0
# jump/hop/ramp = 2
# fallen off edge = 4
# in lava = 6
# in deep water = 8
status_flag = 0x10A0


class Statuses(Enum):
    on_ground = 0
    jump_hop_ram = 2
    fallen_off_edge = 4
    in_lava = 6
    in_deep_water = 8


# Lap number, two variables, both unsigned bytes:
# byte 7E10C1 = lap you're currently on
# byte 7E10F9 = maximum lap you've reached
# 0 = 127
# 1 = 128
# 2 = 129
# 3 = 130
# 4 = 131
# 5 = 132
# finished = 133
lapnumber_code = 0x10C1
lapsize = 0x0148

checkpoint = 0x10C0
clock = 0x0101
coins = 0x0E00
camera_facing_angle = 0x95
race_position = 0x1040
is_going_backward = 0x10B
game_mode = 0x00B5
max_speed = 0x10D6
player_speed = 0x10EA
spinout_code = 0x10A6
track_number = 0x0124
race_cc = 0x0030


# ENUM for surfaces
# unused power up square = 20
# deep water = 34
# mario circuit road / ghost valley road / used power up square / rainbow road = 64
# bowser castle = 68
# doughnut plains track = 70
# koopa beach sand = 74
# choco island track = 76
# ghost valley rough bit / bowser castle rough bit / ice = 78
# choco island bridges = 80
# choco island slightly rough bit of track = 82
# mario circuit off-road = 84
# choco island off-road = 86
# snow = 88
# koopa beach bushes / doughnut plains grass = 90
# shallow-water = 92
# mud puddle = 94
class SurfaceTypes(Enum):
    jump_pad = 0x10, 1.5
    choco_bump = 0x12, 0.75
    powerup_box = 0x14, 1.5
    speed_boost = 0x16, 2
    oil_spill = 0x18, -0.75
    coin = 0x1A, 1.25
    choco_bump2 = 0x1C, 0.75
    starting_line = 0x1E, 1
    pit = 0x20, -2
    deep_water = 0x22, -1
    lava = 0x24, -2
    oob_grass = 0x26, -1.5
    undefined = 0x28, -1
    road = 0x40, 1
    ghost_road = 0x42, 1
    castle_road = 0x44, 1
    dirt_road = 0x46, 0.75
    wet_sand = 0x48, 0.75
    sand_road = 0x4A, 1
    choco_road = 0x4C, 1
    light_ghost_road = 0x4E, 1
    wood_bridge = 0x50, 1
    loose_dirt = 0x52, 0.5
    dirt = 0x54, 0
    choco_dirt = 0x56, -0.5
    snow = 0x58, 0
    lily_pad_grass = 0x5A, 0
    shallow_water = 0x5C, 0
    mud = 0x5E, 0.5
    wall = 0x80, -1.5
    ghost_house_border = 0x82, -1.5
    ice_blocks = 0x84, -1.5


surface_type = 0x10AE
tile_surface_type_table = 0x0B00
tile_sprite_map = 0x10000

top_global_x = 0x0088
top_global_y = 0x008C
bottom_global_x = 0x008A
bottom_global_y = 0x008E

tile_size = 32


def get_position(player: int, ram: np.ndarray):
    if player == 1:
        kart_x = ram[top_global_x]
        kart_y = ram[top_global_y]

        kart_direction = ram[camera_facing_angle]
        kart_speed = ram[player_speed]

    else:
        kart_x = ram[top_global_x]
        kart_y = ram[top_global_y]

        kart_direction = ram[camera_facing_angle]
        kart_speed = ram[player_speed]

    return kart_x, kart_y


def get_track_number(ram: np.ndarray) -> int:
    return ram[track_number]


def get_lap(ram: np.ndarray) -> int:
    return ram[lapnumber_code] - 127


def get_surface_name(tile: int) -> SurfaceTypes:
    for surface in SurfaceTypes:
        if tile == surface.value[0]:
            return surface


def get_surface_physics(tile: int) -> int:
    for surface in SurfaceTypes:
        if tile == surface.value[0]:
            return surface.value[1]


def is_going_backwards(ram: np.ndarray) -> bool:
    kart_flow = ram[is_going_backward]
    if kart_flow == 0:
        return False
    else:
        return True


def get_camera_facing_angle(ram: np.ndarray) -> int:
    direction = ram[camera_facing_angle]
    return direction


def get_course_model(ram: np.ndarray) -> {}:
    course = {}
    for i in range(1, 128):
        for j in range(81, 209):
            tile = ram[tile_sprite_map + ((i - 1) + (j - 1) * 128)]
            course[(i - 1, j - 81)] = get_surface_physics(ram[tile_surface_type_table + tile])

    model = numpy.zeros((127, 127))

    for i in range(127):
        for j in range(127):
            model[i][j] = course[(i, j)]

    return model


def get_info_kart_position(info: {}):
    return info["kart1_X"], info["kart1_Y"]


def get_info_kart_position_to_matrix_index(info: {}):
    position = get_info_kart_position(info)

    return position[0] // tile_size, position[1] // tile_size


def get_info_current_frame(info: {}):
    return info["getFrame"]


def get_info_current_checkpoint(info: {}):
    return info["current_checkpoint"]


def get_info_prev_checkpoint(info: {}):
    return info["prevCheckpoint"]


class MarioKart:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("MARIO KART")

        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.fps_clock = pygame.time.Clock()
        self.running = True

        self.env = retro.make('SuperMarioKart-Snes', state="MarioCircuit_M")
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
        model = get_course_model(self.env.get_ram())

        while self.running:
            self.window.fill(BLUE)
            self.process_events()

            observation, reward, done, info = self.env.step(player_action)
            ram = self.env.get_ram()
            rgb_array = self.env.render(mode="rgb_array")

            self.draw_game_windows(observation)
            self.draw_minimal_view(model, get_info_kart_position_to_matrix_index(info))
            # self.draw_snes_controller(player_action)

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
        square_width = 50
        square_height = 50
        square_distance = 65

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

    def draw_model(self, model: []):
        for i in range(127):
            for j in range(127):
                if model[i][j] < 0:
                    pygame.draw.rect(self.window, (255, 0, 0), pygame.Rect(650 + 2 * i, 200 + 2 * j, 2, 2))
                elif model[i][j] == 0:
                    pygame.draw.rect(self.window, (128, 128, 128), pygame.Rect(650 + 2 * i, 200 + 2 * j, 2, 2))
                else:
                    pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(650 + 2 * i, 200 + 2 * j, 2, 2))

    def draw_minimal_view(self, model: [], mario_position: typing.Tuple):
        square_size = 3
        for x in range(-10, 10):
            for y in range(15):
                map_x = mario_position[0] + x
                map_y = mario_position[1] + y

                if model[map_x][map_y] > 1:
                    pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(650 + square_size * x, 200 + square_size * y, square_size, square_size))
                if model[map_x][map_y] == 0:
                    pygame.draw.rect(self.window, (128, 128, 128), pygame.Rect(650 + square_size * x, 200 + square_size * y, square_size, square_size))
                if model[map_x][map_y] < 0:
                    pygame.draw.rect(self.window, (255, 0, 0), pygame.Rect(650 + square_size * x, 200 + square_size * y, square_size, square_size))


if __name__ == '__main__':
    game = MarioKart()
    game.run()

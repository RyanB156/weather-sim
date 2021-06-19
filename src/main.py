import math

import pygame
import os

from ViewMode import ViewMode
from WeatherConfLoader import WeatherConfLoader
from WeatherMap import WeatherMap
from ViewState import ViewState


class WeatherSim:

    def __init__(self):
        # Load config data
        self.weather_config = WeatherConfLoader.get_conf()
        self.grid_size = self.weather_config['world']['gridSize']
        self.max_elevation = self.weather_config['world']['zMax']

        pygame.init()
        self.display_size = (800, 600)
        (self.width, self.height) = self.display_size

        self.game_display = pygame.display.set_mode(self.display_size)
        self.game_display_rect = self.game_display.get_rect()
        pygame.display.set_caption('Weather')

        # Init and create weather data
        # Load image and use it to set world size
        map_image_path = os.path.join('..', 'assets', 'pixel_map.png')
        self.map_image = pygame.image.load(map_image_path)
        (self.map_width, self.map_height) = self.map_image.get_size()

        # Set background
        self.background = pygame.Surface(self.game_display.get_size())
        self.background_color = (50, 50, 50)
        background_rect = pygame.Rect(0, 0, self.display_size[0], self.display_size[1])
        pygame.draw.rect(self.background, self.background_color, background_rect)

        # Set logging area
        log_surface = pygame.Surface(self.game_display.get_size())

        # Set grid
        self.grid_surface = pygame.Surface(self.game_display.get_size(), pygame.SRCALPHA)
        grid_color = (128, 128, 128)

        for x in range(0, self.map_width, self.grid_size):
            pygame.draw.line(self.grid_surface, grid_color, (x, 0), (x, self.map_height))
        for y in range(0, self.map_height, self.grid_size):
            pygame.draw.line(self.grid_surface, grid_color, (0, y), (self.map_width, y))

        self.game_display.blit(self.map_image, (0, 0))
        boolean_map = self.get_boolean_map(self.game_display)
        self.weather_data = WeatherMap(self.map_width, self.map_height, self.max_elevation, boolean_map)

        # app state
        self.view_state = ViewState(ViewMode.WIND)

        # Weather view surface
        self.weather_surface = pygame.Surface(self.game_display.get_size())

    def get_boolean_map(self, surface):
        """
        Get a 2D array denoting whether the cell is over land or water

        Args:
            surface - pygame surface - The surface containing the land/ocean map
        Returns:
            map - boolean[][] - A 2D boolean map of land vs water
        """
        b_map = []
        for x in range(0, self.width // self.grid_size):
            b_map.append([])
            for y in range(0, self.height // self.grid_size):
                g = surface.get_at((self.grid_size * x + (self.grid_size // 2),
                                    self.grid_size * y + (self.grid_size // 2)))[1]
                b_map[x].append(g > 0)
        return b_map

    def draw_wind(self):
        vector_color = (255, 0, 0)
        for x in range(self.map_width // self.grid_size):
            for y in range(self.map_height // self.grid_size):
                start = [x * self.grid_size + (self.grid_size // 2), y * self.grid_size + (self.grid_size // 2)]

                v = self.weather_data.samples[self.view_state.elevation][x][y].wind
                angle = math.atan2(v[1], v[0])

                magnitude = (v[0] * v[0] + v[1] * v[1]) ** 0.5

                scaled_dist = magnitude * 3
                head_length = scaled_dist / 3

                end = [start[0] + scaled_dist * math.cos(angle), start[1] - scaled_dist * math.sin(angle)]

                pygame.draw.line(self.game_display, vector_color, start, end)

                arrow_head_start = end
                arrow_angle = angle - math.pi

                arrow_left_end = [arrow_head_start[0] + head_length * math.cos(arrow_angle - math.pi / 6),
                                  arrow_head_start[1] - head_length * math.sin(arrow_angle - math.pi / 6)]

                pygame.draw.line(self.game_display, vector_color, end, arrow_left_end)

                arrow_right_end = [arrow_head_start[0] + head_length * math.cos(arrow_angle + math.pi / 6),
                                   arrow_head_start[1] - head_length * math.sin(arrow_angle + math.pi / 6)]

                pygame.draw.line(self.game_display, vector_color, end, arrow_right_end)

    def run_simulation(self):

        self.weather_data.simulate(0.0)

        log_text = ''
        font = pygame.font.SysFont('consolas', 15)

        crashed = False
        while not crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True

                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[0] < self.map_width - 1 and mouse_pos[1] < self.map_height - 1:
                        cell = [mouse_pos[0] // self.grid_size, mouse_pos[1] // self.grid_size]

                        try:
                            sample = self.weather_data.samples[self.view_state.elevation][cell[0]][cell[1]]
                        except IndexError:
                            continue

                        log_text = f'Sample - temperature: {int(sample.temperature * 100) / 100}, ' \
                                   f'humidity: {int(sample.humidity * 100) / 100}, '\
                                   f'pressure: {int(sample.pressure * 100) / 100}, ' \
                                   f'wind: {[int(sample.wind[0] * 100) / 100, int(sample.wind[1] * 100) / 100]} '

            self.game_display.fill(self.background_color)
            self.game_display.blit(self.background, (0, 0))
            self.game_display.blit(self.map_image, (0, 0))
            self.game_display.blit(self.grid_surface, (0, 0))

            if self.view_state.view_mode == ViewMode.WIND:
                self.draw_wind()

            text_surface = font.render(log_text, False, (255, 255, 255))
            self.game_display.blit(text_surface, (0, self.map_height + 10))

            pygame.display.update()

        pygame.quit()
        quit()


sim = WeatherSim()
sim.run_simulation()



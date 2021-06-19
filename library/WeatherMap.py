from Weather import WeatherSample
from WeatherConfLoader import WeatherConfLoader
import math
import random


class WeatherMap:

    def __init__(self, x_extent, y_extent, z_extent, world_map):
        self.weather_config = WeatherConfLoader.get_conf()

        # Pressure
        self.pressureStart = self.weather_config['init']['pressure']['start']
        self.pressureConstant = self.weather_config['coefficients']['pressureConstant']
        self.zScale = self.weather_config['world']['zScale']

        self.grid_size = self.weather_config['world']['gridSize']

        self.world_map = world_map

        self.neighbours = [[0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1]]

        self.samples = []
        for z in range(z_extent):
            self.samples.append([])
            for x in range(x_extent // self.grid_size):
                self.samples[z].append([])
                for y in range(y_extent // self.grid_size):
                    self.samples[z][x].append(self.init_weather_cell(x, x_extent, y, y_extent, z, z_extent, world_map))

    def init_weather_cell(self, x, x_extent, y, y_extent, z, z_extent, world_map):

        # Scale initial temperature by latitude.
        # TODO: Scale by elevation ???
        temperature = self.weather_config['init']['temperature']['pole'] \
                      + self.weather_config['init']['temperature']['equator'] \
                      * math.sin(2 * math.pi * (y / y_extent))

        # Humidity proportional to elevation.
        if world_map[x][y]:
            humidity = self.weather_config['init']['humidity']['land']['start'] \
                       + self.weather_config['init']['humidity']['land']['end'] * z / z_extent
        else:
            humidity = self.weather_config['init']['humidity']['water']['start'] \
                       + self.weather_config['init']['humidity']['water']['end'] * z / z_extent

        # P_h = P_0 * e^(-mgh / kT).
        z *= self.zScale
        abs_temperature = temperature + 237

        pressure = self.pressureStart - 0.2 * self.pressureConstant * math.exp(-z / abs_temperature)

        if world_map[x][y]:
            pressure += 100
        else:
            pressure += 0

        return WeatherSample(temperature, humidity, pressure)

    def set_wind(self, elevation):
        width = len(self.samples[elevation])
        height = len(self.samples[elevation][1])
        for x in range(1, width - 1):
            for y in range(1, height - 1):

                current_pressure = self.samples[elevation][x][y].pressure
                v = [0, 0]
                mag = 0
                for neighbour in self.neighbours:
                    neighbour_pressure = self.samples[elevation][x + neighbour[0]][y + neighbour[1]].pressure
                    angle = math.atan2(neighbour[1], neighbour[0])

                    mag += current_pressure - neighbour_pressure
                    v[0] += math.cos(angle) * (v[0] + neighbour_pressure - current_pressure)
                    v[1] += math.sin(angle) * (v[1] + neighbour_pressure - current_pressure)

                if mag != 0:
                    v[0] /= mag
                    v[1] /= mag

                self.samples[elevation][x][y].wind = v

                # print(f'Wind ({x}, {y}): {v}')

    def simulate(self, time_delta):
        for h in range(len(self.samples)):
            self.set_wind(h)





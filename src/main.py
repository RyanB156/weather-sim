import pygame
import os
from WeatherConfLoader import WeatherConfLoader
from WeatherMap import WeatherMap


def get_boolean_map(surface, g_size, w, h):
    b_map = []
    for x in range(0, w):
        b_map.append([])
        for y in range(0, h):
            g = surface.get_at((g_size * x, g_size * y))[1]
            b_map[x].append(g > 0)
    return b_map


weather_config = WeatherConfLoader.get_conf()
grid_size = weather_config['world']['gridSize']

pygame.init()

display_size = (800, 600)

game_display = pygame.display.set_mode(display_size)
pygame.display.set_caption('Weather')

map_image_path = os.path.join('..', 'assets', 'pixel_map.png')
map_image = pygame.image.load(map_image_path)

game_display.blit(map_image, (0, 0))

(x_extent, y_extent) = map_image.get_size()

boolean_map = get_boolean_map(game_display, grid_size, x_extent // grid_size, y_extent // grid_size)

height = 10

weatherData = WeatherMap(x_extent, y_extent, height, boolean_map)

print(weatherData)

crashed = False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    pygame.display.update()

pygame.quit()
quit()

"""
for (let x = 0; x < width / gridSize; x ++) {
      for (let y = 0; y < height / gridSize; y ++) {
        ctx.beginPath();
        let xPos = x * gridSize + (gridSize / 2);
        let yPos = y * gridSize + (gridSize / 2);
        ctx.moveTo(xPos, yPos);

        let radAngle = this.angle / 180 * Math.PI;

        let v = weatherData.samples[elevation][x][y].wind;
        
        let magnitude = (v[0] * v[0] + v[1] * v[1]) ** 0.5;
        let scaledDist = magnitude * 10;
        let headLength = scaledDist / 3;

        let end = [xPos + scaledDist * Math.cos(radAngle), 
                   yPos - scaledDist * Math.sin(radAngle)];

        console.log(`Drawing from (${xPos}, ${yPos}) to (${end[0]}, ${end[1]})`);

        // Main body.
        ctx.lineTo(end[0], end[1]);

        // Arrow head.
        let arrowHeadStart = end;
        let arrowAngle = radAngle - Math.PI;

        let arrowLeftEnd = [arrowHeadStart[0] + headLength * Math.cos(arrowAngle - Math.PI / 6), 
                            arrowHeadStart[1] - headLength * Math.sin(arrowAngle - Math.PI / 6)];
        ctx.lineTo(arrowLeftEnd[0], arrowLeftEnd[1]);

        let arrowRightEnd = [arrowHeadStart[0] + headLength * Math.cos(arrowAngle + Math.PI / 6), 
                            arrowHeadStart[1] - headLength * Math.sin(arrowAngle + Math.PI / 6)];
        ctx.moveTo(end[0], end[1]);
        ctx.lineTo(arrowRightEnd[0], arrowRightEnd[1]);

        ctx.stroke();
      }
    }
  }"""


from Precipitation import Precipitation


class WeatherSample:

    def __init__(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.precipitation = Precipitation().none
        self.wind = [0, 0]



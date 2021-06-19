from Precipitation import Precipitation


class WeatherSample:

    def __init__(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.precipitation = Precipitation.NONE
        self.wind = [0, 0]



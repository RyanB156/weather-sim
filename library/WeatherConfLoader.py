import json
import os


class WeatherConfLoader:
    @staticmethod
    def get_conf():
        """
        Get weather config json object
        Returns:
            weather_config - json object - The weather config data
        """
        config_path = os.path.join('..', 'assets', 'weather-config.json')
        with open(config_path) as config_file:
            return json.load(config_file)


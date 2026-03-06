# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737
'''
Testing all (probably closer to 70%) of all the code across
all the different modules
'''

import unittest
import LastFM 
import OpenWeather
import WebAPI


class Test_TestingAPIs(unittest.TestCase):
    def test_openweather(self):
        open_weather = OpenWeather.OpenWeather()
        open_weather.set_apikey("REDACTED")
        open_weather.load_data()
        result = open_weather.transclude("Testing the weather: @weather")
        assert "@weather" not in result

    def test_openweather(self):
        last_fm = LastFM.LastFM()
        last_fm.set_apikey("REDACTED")
        last_fm.load_data()
        result = last_fm.transclude("Testing lastFM: @lastfm")
        assert "@lastfm" not in result


if __name__ == "__main__":
    open_weather = OpenWeather.OpenWeather()
    open_weather.load_data()
#     unittest.main()
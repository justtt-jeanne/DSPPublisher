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
    def test_openweather_set_api(self):
        open_weather = OpenWeather.OpenWeather()
        open_weather.set_apikey("REDACTED")
        assert open_weather._apikey == "REDACTED"

    def test_lastfm_set_api(self):
        last_fm = LastFM.LastFM()
        last_fm.set_apikey("REDACTED")
        assert last_fm._apikey == "REDACTED"

    def test_openweather_url(self):
        open_weather = OpenWeather.OpenWeather()
        open_weather.set_apikey("REDACTED")
        open_weather.load_data()
        assert open_weather.url == ("http://api.openweathermap.org"
                                    "/data/2.5/weather"
                                    "?zip=92697,US&appid"
                                    "=REDACTED")

    def test_lastfm_url(self):
        last_fm = LastFM.LastFM()
        last_fm.set_apikey("REDACTED")
        last_fm.load_data()
        assert last_fm.url == ("http://ws.audioscrobbler.com/2.0/"
                               "?method=chart.gettopartists&api_key"
                               "=REDACTED"
                               "&format=json")

    def test_openweather_transclude(self):
        open_weather = OpenWeather.OpenWeather()
        open_weather.set_apikey("REDACTED")
        open_weather.load_data()
        result = open_weather.transclude("Testing the weather: @weather")
        assert "@weather" not in result

    def test_lastfm_transclude(self):
        last_fm = LastFM.LastFM()
        last_fm.set_apikey("REDACTED")
        last_fm.load_data()
        result = last_fm.transclude("Testing lastFM: @lastfm")
        assert "@lastfm" not in result


# if __name__ == "__main__":
#     unittest.main()
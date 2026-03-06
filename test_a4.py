# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737
# pylint: disable=invalid-name, protected-access
'''
Testing all (probably closer to 70%) of all the code across
all the different modules
'''

import unittest
import LastFM
import OpenWeather
import a4


class Test_TestingAPIs(unittest.TestCase):
    '''
    Testing class that tests any API related information/
    OpenWeather and LastFM.
    '''
    def test_openweather_set_api(self):
        '''
        @private
        Makes sure the apikey is set correctly in OpenWeather
        '''
        open_weather = OpenWeather.OpenWeather()
        open_weather.set_apikey("REDACTED")
        assert open_weather._apikey == "REDACTED"

    def test_lastfm_set_api(self):
        '''
        @private
        Makes sure the apikey is set correctly in LastFM
        '''
        last_fm = LastFM.LastFM()
        last_fm.set_apikey("REDACTED")
        assert last_fm._apikey == "REDACTED"

    def test_openweather_url(self):
        '''
        @private
        Makes sure the url is set correctly in OpenWeather
        '''
        open_weather = OpenWeather.OpenWeather()
        open_weather.set_apikey("REDACTED")
        open_weather.load_data()
        assert open_weather.url == ("http://api.openweathermap.org"
                                    "/data/2.5/weather"
                                    "?zip=92697,US&appid"
                                    "=REDACTED")

    def test_lastfm_url(self):
        '''
        @private
        Makes sure the url is set correctly in LastFM
        '''
        last_fm = LastFM.LastFM()
        last_fm.set_apikey("REDACTED")
        last_fm.load_data()
        assert last_fm.url == ("http://ws.audioscrobbler.com/2.0/"
                               "?method=chart.gettopartists&api_key"
                               "=REDACTED"
                               "&format=json")

    def test_openweather_invalid_api(self):
        '''
        @private
        Makes sure an error is caught in OpenWeather
        '''
        open_weather = OpenWeather.OpenWeather()
        open_weather.set_apikey("123")
        open_weather.load_data()
        assert open_weather.description is None

    def test_lastfm_invalid_api(self):
        '''
        @private
        Makes sure an error is caught in LastFM
        '''
        last_fm = LastFM.LastFM()
        last_fm.set_apikey("123")
        last_fm.load_data()
        assert last_fm.artist is None

    def test_openweather_transclude(self):
        '''
        @private
        Makes sure the transclusion is succesful in OpenWeather
        '''
        open_weather = OpenWeather.OpenWeather()
        open_weather.set_apikey("REDACTED")
        open_weather.load_data()
        result = open_weather.transclude("Testing the weather: @weather")
        assert "@weather" not in result

    def test_lastfm_transclude(self):
        '''
        @private
        Makes sure the transclusion is succesful in OpenWeather
        '''
        last_fm = LastFM.LastFM()
        last_fm.set_apikey("REDACTED")
        last_fm.load_data()
        result = last_fm.transclude("Testing lastFM: @lastfm")
        assert "@lastfm" not in result


class Test_TestingCommandParsing(unittest.TestCase):
    def test_empty_command_l(self):
        assert a4.parse_command_l("") is None

    def test_missing_e_command_l(self):
        assert a4.parse_command_l("-e") is None
    
    def test_missing_s_command_l(self):
        assert a4.parse_command_l("-s") is None

    def test_invalid_flag_command_l(self):
        assert a4.parse_command_l("-t") is None

    def test_valid_command_l(self):
        assert a4.parse_command_l("-r") == {"-r": True}

    def test_empty_command_e(self):
        assert a4.parse_command_e("") is None

    def test_empty_command_p(self):
        assert a4.parse_command_p("") is None


# if __name__ == "__main__":
#     unittest.main()

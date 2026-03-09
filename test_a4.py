# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737
# pylint: disable=invalid-name, protected-access
'''
Testing all (probably closer to 70%) of all the code across
all the different modules.
'''

from pathlib import Path
import unittest
import LastFM
import OpenWeather
import a4
import ui
import ds_client
import ds_protocol


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
    '''
    Testing class that tests any command parsing
    related functions.
    '''
    def test_empty_command_l(self):
        '''
        @private
        Tests that an empty string for the l
        command in the a4.py module will return None
        '''
        assert a4.parse_command_l("") is None

    def test_missing_e_command_l(self):
        '''
        @private
        Tests that a string that's missing an
        argument for the -e flag in a4.py
        will return None
        '''
        assert a4.parse_command_l("-e") is None

    def test_missing_s_command_l(self):
        '''
        @private
        Tests that a string that's missing an
        argument for the -s flag in a4.py
        will return None
        '''
        assert a4.parse_command_l("-s") is None

    def test_invalid_flag_command_l(self):
        '''
        @private
        Tests that a string that with an
        invalid flag for the l command in a4.py
        will return None
        '''
        assert a4.parse_command_l("-t") is None

    def test_valid_command_l(self):
        '''
        @private
        Tests that a valid l command will return
        the correct corresponding dictionary
        '''
        assert a4.parse_command_l("-r") == {"-r": True}

    def test_empty_command_e(self):
        '''
        @private
        Tests that an empty string for the e
        command in the a4.py module will return None
        '''
        assert a4.parse_command_e("") is None

    def test_missing_arg_command_e(self):
        '''
        @private
        Tests that a string sent to the
        e command that's missing an
        argument for any of the flags that
        need one in a4.py will return None
        '''
        assert a4.parse_command_e("-usr") is None

    def test_invalid_flag_command_e(self):
        '''
        @private
        Tests that a string that with an
        invalid flag for the e command in a4.py
        will return None
        '''
        assert a4.parse_command_e("-p") is None

    def test_valid_command_e(self):
        '''
        @private
        Tests that a valid e command will return
        the correct corresponding dictionary
        '''
        assert a4.parse_command_e("-usr \"hi there\"") == {
            "-usr": "hithere"
        }

    def test_empty_command_p(self):
        '''
        @private
        Tests that an empty string for the p
        command in the a4.py module will return None
        '''
        assert a4.parse_command_p("") is None

    def test_missing_arg_command_p(self):
        '''
        @private
        Tests that a string sent to the
        e command that's missing an
        argument for any of the flags that
        need one in a4.py will return None
        '''
        assert a4.parse_command_p("-post") is None

    def test_invalid_flag_command_p(self):
        '''
        @private
        Tests that a string that with an
        invalid flag for the p command in a4.py
        will return None
        '''
        assert a4.parse_command_p("-p") is None

    def test_valid_command_p(self):
        '''
        @private
        Tests that a valid p command will return
        the correct corresponding dictionary
        '''
        assert a4.parse_command_p("-post 1 -usr") == {
            "-post": "1", "-usr": True
        }

    def test_quoted_ui(self):
        '''
        @private
        Tests that a string in quotes will return the
        correct corresponding output
        '''
        assert ui.parse_quotes("'hi'", 0) == (" h i ", 4)


class Test_TestingTryingChecking(unittest.TestCase):
    '''
    Testing class that tests any function that checks things
    '''
    def test_check_path(self):
        '''
        @private
        Tests that an invalid path will return path.
        Does not test a valid path because I cannot
        guarantee what path is on the person's computer.
        '''
        assert a4.check_path(Path("abcdef")) is False

    def test_try_valid_attribute(self):
        '''
        @private
        Tests that a valid command returns true
        through the trying_attribute function
        '''
        assert ui.trying_attribute(print("HI")) is True

    def test_check_ow_and_lastfm_no_keyword(self):
        '''
        @private
        Tests that checking the transpose function
        works on a string that doesn't contain a keyword.
        '''
        assert ui.check_ow_and_lastfm("Hi there") == "Hi there"

    def test_invalid_port(self):
        '''
        @private
        Tests that an invalid port/server will return False.
        '''
        assert ds_client.send(
            "clotho.ics.uci.edu",
            1234,
            "joseph",
            "there",
            "Hi"
            ) is False

    def test_valid_send(self):
        '''
        @private
        Tests that valid information will return True.
        '''
        assert ds_client.send(
            "clotho.ics.uci.edu",
            2021,
            "joseph",
            "there",
            "Hi"
            ) is True


class Test_TestingJsons(unittest.TestCase):
    '''
    Testing class that test different Jsons
    sent to ds_protocol will return the right thing.
    '''
    def test_ok_json(self):
        '''
        @private
        Test that an ok Json will return the correct
        namedtuple information
        '''
        assert ds_protocol.extract_server_json(
            "{\"response\": "
            "{\"type\": \"ok\", "
            "\"message\": \"Awesome Sauce\", "
            "\"token\": \"abcdefg\"}}"
        ) == ("ok",
              "Awesome Sauce",
              "abcdefg")

    def test_error_json(self):
        '''
        @private
        Test that an error Json will return the correct
        namedtuple information
        '''
        assert ds_protocol.extract_server_json(
            "{\"response\": "
            "{\"type\": \"error\", "
            "\"message\": \"An error "
            "message will be contained here.\"}}"
        ) == ("error",
              "An error message will be contained here.",
              "None")

    def test_invalid_json(self):
        '''
        @private
        Test that an invalid Json will return None
        '''
        assert ds_protocol.extract_server_json("") is None

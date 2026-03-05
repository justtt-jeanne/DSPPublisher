# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737

import LastFM 
import OpenWeather
import WebAPI


def test_api(message:str, apikey:str, webapi:WebAPI):
    webapi.set_apikey(apikey)
    webapi.load_data()
    result = webapi.transclude(message)
    print(result)


open_weather = OpenWeather.OpenWeather() #notice there are no params here...HINT: be sure to use parameter defaults!!!
last_fm = LastFM.LastFM()

test_api("Testing the weather: @weather", "REDACTED", open_weather)
# expected output should include the original message transcluded with the default weather value for the @weather keyword.

test_api("Testing lastFM: @lastfm", "REDACTED", last_fm)
# expected output include the original message transcluded with the default music data assigned to the @lastfm keyword
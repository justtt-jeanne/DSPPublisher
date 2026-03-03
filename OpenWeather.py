# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737
'''
Handles Weather API and FM API,  as well as the function to get
the JSON from the urls.
'''

import json
import urllib.request
import urllib.error
import ds_protocol


class OpenWeather:
    '''
    Creating class that will store weather information
    '''
    def __init__(self, zipcode, ccode):
        '''
        Initializing self variables
        '''
        self._zipcode = zipcode
        self._ccode = ccode
        self._apikey = None
        self._url = None
        self._city = None
        self._temperature = 0
        self._high_temperature = 0
        self._low_temperature = 0
        self._longitude = 0
        self._latitude = 0
        self._description = None
        self._humidity = 0
        self._sunset = None


    def _download_url(self) -> dict:
        response = None
        r_obj = None
        try:
            response = urllib.request.urlopen(self._url)
            json_results = response.read()
            r_obj = json.loads(json_results)
            response.close()
        except urllib.error.HTTPError as e:
            print('Failed to download contents of URL')
            print('Status code: {}'.format(e.code))
        except ConnectionError:
            print("Loss of internet.")    
        return r_obj


    def set_apikey(self, apikey):
        self._apikey = apikey
        self._url = f"http://api.openweathermap.org/data/2.5/weather" + \
                    f"?zip={self._zipcode},{self._ccode}&appid={self._apikey}"


def main() -> None:
    zip = "92697"
    ccode = "US"
    apikey = "REDACTED"
    openweather = OpenWeather(zip, ccode)
    openweather.set_apikey(apikey)
    weather_obj = openweather._download_url()
    print(weather_obj)


if __name__ == '__main__':
    main()
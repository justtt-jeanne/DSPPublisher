# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737
'''
Handles OpenWeather API by making a class instance that gets
the JSON from the url.
'''

import sys
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
        self.zipcode = zipcode
        self.ccode = ccode
        self._apikey = None
        self.url = None
        self._json = None
        self.city = None
        self.temperature = 0
        self.high_temperature = 0
        self.low_temperature = 0
        self.longitude = 0
        self.latitude = 0
        self.description = None
        self.humidity = 0
        self.sunset = None


    def _download_url(self) -> None:
        '''
        Callable method tha opens the url and gets the json from the url.
        Stores the json so it can be used later.
        '''
        response = None
        try:
            response = urllib.request.urlopen(self.url)
            json_results = response.read()
            self._json = json.loads(json_results)
            response.close()
        except urllib.error.HTTPError as e:
            raise urllib.error.HTTPError('Failed to download contents of URL\n'
                                         'Status code: {}'.format(e.code))
        except ConnectionError:
            raise ConnectionError("Loss of internet.")


    def set_apikey(self, apikey):
        '''
        Sets the api key for the instance.
        '''
        self._apikey = apikey
        self.url = f"http://api.openweathermap.org/data/2.5/weather" + \
                    f"?zip={self.zipcode},{self.ccode}&appid={self._apikey}"


    def load_data(self):
        '''
        Sets instance variables after calling _download_url from the instance json.
        '''
        self._download_url()
        try:
            self.city = self._json['name']
            self.temperature = self._json['main']['temp']
            self.high_temperature = self._json['main']['temp_max']
            self.low_temperature = self._json['main']['temp_min']
            self.longitude = self._json['coord']['lon']
            self.latitude = self._json['coord']['lat']
            self.description = self._json['weather'][0]['description']
            self.humidity = self._json['main']['humidity']
            self.sunset = self._json['sys']['sunset']
        except TypeError:
            raise TypeError("Server did not return a json.")
        except KeyError:
            raise KeyError("Server did not send a valid json.")


def main() -> None:
    '''
    Test case with exceptions.
    '''
    zipcode = "92697"
    ccode = "US"
    apikey = "REDACTED"
    open_weather = OpenWeather(zipcode, ccode)
    open_weather.set_apikey(apikey)
    try:
        open_weather.load_data()
    except urllib.error.HTTPError as e:
        print(e)
        sys.exit(0)
    except ConnectionError as e:
        print(e)
        sys.exit(0)
    except TypeError as e:
        print(e)
        sys.exit(0)
    except KeyError as e:
        print(e)
        sys.exit(0)

    try:
        print(f"The temperature for {zipcode} is {open_weather.temperature} degrees")
        print(f"The high for today in {zipcode} will be {open_weather.high_temperature} degrees")
        print(f"The low for today in {zipcode} will be {open_weather.low_temperature} degrees")
        print(f"The coordinates for {zipcode} are {open_weather.longitude} longitude and {open_weather.latitude} latitude")
        print(f"The current weather for {zipcode} is {open_weather.description}")
        print(f"The current humidity for {zipcode} is {open_weather.humidity}")
        print(f"The sun will set in {open_weather.city} at {open_weather.sunset}")
    except AttributeError:
        print("Asked for an unknown attribute.")
        sys.exit(0)


if __name__ == '__main__':
    main()
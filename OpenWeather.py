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
            print('Failed to download contents of URL\n'
                  'Status code: {}'.format(e.code))
            sys.exit(0)
        except ConnectionError:
            print("Loss of internet.")
            sys.exit(0)


    def set_apikey(self, apikey):
        '''
        Sets the api key for the instance.
        :param apikey: The apikey to set
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
            self.temperature = round(((1.8 * (float(self._json['main']['temp']) - 273)) + 32), 2)
            self.high_temperature = round(((1.8 * (float(self._json['main']['temp_max']) - 273)) + 32), 2)
            self.low_temperature = round(((1.8 * (float(self._json['main']['temp_min']) - 273)) + 32), 2)
            self.longitude = self._json['coord']['lon']
            self.latitude = self._json['coord']['lat']
            self.description = self._json['weather'][0]['description']
            self.humidity = self._json['main']['humidity']
            self.sunset = self._json['sys']['sunset']
        except TypeError:
            print("Server did not return a json.")
            sys.exit(0)
        except KeyError:
            print("Server did not send a valid json.")
            sys.exit(0)


    def transclude(self, message: str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude

        :returns: The transcluded message
        '''
        new_message = message.replace("@weather", self.description)
        return new_message


def main() -> None:
    '''
    Test case with exceptions.
    '''
    zipcode = "92697"
    ccode = "US"
    apikey = "REDACTED"
    open_weather = OpenWeather(zipcode, ccode)
    open_weather.set_apikey(apikey)
    open_weather.load_data()
    try:
        print(f"The temperature for {zipcode} is {open_weather.temperature} degrees")
        print(f"The high for today in {zipcode} will be {open_weather.high_temperature} degrees")
        print(f"The low for today in {zipcode} will be {open_weather.low_temperature} degrees")
        print(f"The coordinates for {zipcode} are {open_weather.longitude} "
              f"longitude and {open_weather.latitude} latitude")
        print(f"The current weather for {zipcode} is {open_weather.description}")
        print(f"The current humidity for {zipcode} is {open_weather.humidity}")
        print(f"The sun will set in {open_weather.city} at {open_weather.sunset}")
    except AttributeError:
        print("Asked for an unknown attribute.")
        sys.exit(0)
    my_message = open_weather.transclude("Hello World! Today is the first day of the rest of my life. "
                                         "It is outside @weather and I am thrilled!")
    print(my_message)


if __name__ == '__main__':
    main()
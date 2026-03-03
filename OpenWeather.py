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


    def _download_url(self) -> dict:
        response = None
        try:
            response = urllib.request.urlopen(self.url)
            json_results = response.read()
            self._json = json.loads(json_results)
            response.close()
        except urllib.error.HTTPError as e:
            print('Failed to download contents of URL')
            print('Status code: {}'.format(e.code))
        except ConnectionError:
            print("Loss of internet.")


    def set_apikey(self, apikey):
        self._apikey = apikey
        self.url = f"http://api.openweathermap.org/data/2.5/weather" + \
                    f"?zip={self.zipcode},{self.ccode}&appid={self._apikey}"


    def load_data(self):
        response = None
        try:
            response = urllib.request.urlopen(self.url)
            json_results = response.read()
            self._json = json.loads(json_results)
            response.close()
        except urllib.error.HTTPError as e:
            print('Failed to download contents of URL')
            print('Status code: {}'.format(e.code))
        except ConnectionError:
            print("Loss of internet.")    
        self.city = self._json['name']
        self.temperature = self._json['main']['temp']
        self.high_temperature = self._json['main']['temp_max']
        self.low_temperature = self._json['main']['temp_min']
        self.longitude = self._json['coord']['lon']
        self.latitude = self._json['coord']['lat']
        self.description = self._json['weather'][0]['description']
        self.humidity = self._json['main']['humidity']
        self.sunset = self._json['sys']['sunset']


def main() -> None:
    zipcode = "92697"
    ccode = "US"
    apikey = "REDACTED"
    open_weather = OpenWeather(zipcode, ccode)
    open_weather.set_apikey(apikey)
    open_weather.load_data()
    
    print(f"The temperature for {zipcode} is {open_weather.temperature} degrees")
    print(f"The high for today in {zipcode} will be {open_weather.high_temperature} degrees")
    print(f"The low for today in {zipcode} will be {open_weather.low_temperature} degrees")
    print(f"The coordinates for {zipcode} are {open_weather.longitude} longitude and {open_weather.latitude} latitude")
    print(f"The current weather for {zipcode} is {open_weather.description}")
    print(f"The current humidity for {zipcode} is {open_weather.humidity}")
    print(f"The sun will set in {open_weather.city} at {open_weather.sunset}")


if __name__ == '__main__':
    main()
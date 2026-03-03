# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737
'''
Handles Weather API and FM API,  as well as the function to get
the JSON from the urls.
'''

import ds_protocol


def OpenWeather():
    '''
    Creating class that will store 
    '''
    def __init__(self):
        '''
        Initializing self variables
        '''
        self._apikey = None
        self._city = None
        self._temperature = 0
        self._high_temperature = 0
        self._low_temperature = 0
        self._longitude = 0
        self._latitude = 0
        self._description = None
        self._humidity = 0
        self._sunset = None


def main() -> None:
    zip = "92697"
    ccode = "US"
    apikey = "REDACTED"
    url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip},{ccode}&appid={apikey}"

    weather_obj = ds_protocol._download_url(url)
    if weather_obj is not None:
        # ['weather'][0]['description']
        print(weather_obj)


if __name__ == '__main__':
    main()
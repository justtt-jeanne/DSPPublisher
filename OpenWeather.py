# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737
# pylint: disable=invalid-name
# apikey = "REDACTED"
'''
Handles OpenWeather API by making a class instance that gets
the JSON from the url.
'''

from WebAPI import WebAPI


class OpenWeather(WebAPI):
    '''
    Creating class that will store weather information
    '''
    def __init__(self, zipcode="92697", ccode="US"):
        '''
        @private
        Initializing self variables
        '''
        self.zipcode = zipcode
        self.ccode = ccode
        self.city = None
        self.description = None
        self.humidity = 0
        self.sunset = None
        super().__init__("http://api.openweathermap.org/data/2.5/weather" +
                         f"?zip={self.zipcode},{self.ccode}&appid=APIKEY")

    def load_data(self):
        '''
        Sets instance variables after
        calling _download_url from the instance json.
        '''
        my_json = self._download_url(self.url)
        if my_json is not None:
            try:
                self.city = my_json['name']
                self.description = my_json['weather'][0]['description']
                self.humidity = my_json['main']['humidity']
                self.sunset = my_json['sys']['sunset']
            except TypeError:
                print("Server did not return a json.")
            except KeyError:
                print("Server did not send a valid json.")

    def transclude(self, message: str) -> str:
        '''
        Replaces keywords in a message with associated API description.
        :param message: The message to transclude
        :returns: The transcluded message
        '''
        new_message = message.replace("@weather", self.description)
        return new_message

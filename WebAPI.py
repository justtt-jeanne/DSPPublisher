# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737
# pylint: disable=invalid-name
'''
Makes the super class for OpenWeather and LastFM with modules
the classes instantiated in those modules can inherit.
'''

from abc import ABC
from abc import abstractmethod
import urllib.request
import urllib.error
import json


class WebAPI(ABC):
    '''
    The WebAPI class is an abstract class that allows child classes
    to inherit modules.
    '''
    def __init__(self, url):
        '''
        Initializes class variables.
        Apikey = None
        Json = None
        Url = whatever the url parameter is
        '''
        self._apikey = None
        self.url = url
        self._json = None

    def _download_url(self, url: str) -> dict:
        '''
        Callable method that opens the url and gets the json from the url.
        Stores the json so it can be used later.
        '''
        response = None
        try:
            with urllib.request.urlopen(url) as response:
                json_results = response.read()
                my_json = json.loads(json_results)
        except urllib.error.HTTPError as e:
            print('Failed to download contents of URL\n' +
                  f'Status code: {e.code}')
            return None
        except ConnectionError:
            print("Loss of internet.")
            return None
        return my_json

    def set_apikey(self, apikey: str) -> None:
        '''
        Sets the api key for the instance.
        :param apikey: The apikey to set
        '''
        self._apikey = apikey
        url = self.url
        self.url = url.replace("APIKEY", self._apikey)

    @abstractmethod
    def load_data(self):
        '''
        @private
        The load_data method is an abstract method that changes
        through each instance of the WebAPI class
        '''

    @abstractmethod
    def transclude(self, message: str) -> str:
        '''
        @private
        The transclude method is an abstract method that changes
        through each instance of the WebAPI class
        '''

# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737

from abc import ABC
from abc import abstractmethod
import urllib.request
import urllib.error
import json
import sys


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
        Callable method tha opens the url and gets the json from the url.
        Stores the json so it can be used later.
        '''
        response = None
        try:
            response = urllib.request.urlopen(url)
            json_results = response.read()
            my_json = json.loads(json_results)
            response.close()
        except urllib.error.HTTPError as e:
            print('Failed to download contents of URL\n'
                  'Status code: {}'.format(e.code))
            sys.exit(0)
        except ConnectionError:
            print("Loss of internet.")
            sys.exit(0)
        return my_json


    def set_apikey(self, apikey:str) -> None:
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
        The load_data method is an abstract method that changes
        through each instance of the WebAPI class
        '''
        pass


    @abstractmethod
    def transclude(self, message:str) -> str:
        '''
        The transclude method is an abstract method that changes
        through each instance of the WebAPI class
        '''
        pass

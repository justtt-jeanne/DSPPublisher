# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737
'''
Handles LastFM API by making a class instance that gets
the JSON from the url.
'''

import sys
import json
import urllib.request
import urllib.error


class LastFM:
    '''
    Creating class that will store artist information
    '''
    def __init__(self):
        '''
        Initializing self variables
        '''
        self._apikey = None
        self.url = None
        self._json = None
        self.artist = None
        self.playcount = 0
        self.listeners = 0


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
        '''
        self._apikey = apikey
        self.url = f"http://ws.audioscrobbler.com/2.0/?method=chart." \
                   f"gettopartists&api_key={apikey}&format=json"


    def load_data(self):
        '''
        Sets instance variables after calling _download_url from the instance json.
        '''
        self._download_url()
        try:
            self.artist = self._json["artists"]["artist"][0]["name"]
            self.playcount = self._json["artists"]["artist"][0]["playcount"]
            self.listeners = self._json["artists"]["artist"][0]["listeners"]
        except TypeError:
            print("Server did not return a json.")
            sys.exit(0)
        except KeyError:
            print("Server did not send a valid json.")
            sys.exit(0)


def main() -> None:
    apikey = "REDACTED"
    fm_obj = LastFM()
    fm_obj.set_apikey(apikey)
    fm_obj.load_data()
    print(f"The top artist is {fm_obj.artist}")
    print(f"{fm_obj.artist}'s total playcount is {fm_obj.playcount}")
    print(f"{fm_obj.artist}'s amount of listeners is {fm_obj.listeners}")


if __name__ == '__main__':
    main()

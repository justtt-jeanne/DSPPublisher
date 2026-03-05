# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737
# pylint: disable=invalid-name
# apikey = "REDACTED"
'''
Handles LastFM API by making a class instance that gets
the JSON from the url.
'''

from WebAPI import WebAPI


class LastFM(WebAPI):
    '''
    Creating class that will store artist information
    '''
    def __init__(self):
        '''
        Initializing self variables
        '''
        self.artist = None
        self.playcount = 0
        self.listeners = 0
        super().__init__("http://ws.audioscrobbler.com/2.0/?method=chart." +
                         "gettopartists&api_key=APIKEY&format=json")

    def load_data(self):
        '''
        Sets instance variables after
        calling _download_url from the instance json.
        '''
        my_json = self._download_url(self.url)
        if my_json is not None:
            try:
                self.artist = my_json["artists"]["artist"][0]["name"]
                self.playcount = my_json["artists"]["artist"][0]["playcount"]
                self.listeners = my_json["artists"]["artist"][0]["listeners"]
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
        new_message = message.replace("@lastfm", self.artist)
        return new_message

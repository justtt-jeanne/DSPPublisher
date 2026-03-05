# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737
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
        super().__init__(f"http://ws.audioscrobbler.com/2.0/?method=chart." + \
                       f"gettopartists&api_key=APIKEY&format=json")


    def load_data(self):
        '''
        Sets instance variables after calling _download_url from the instance json.
        '''
        my_json = self._download_url(self.url)
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


def main() -> None:
    apikey = "REDACTED"
    fm_obj = LastFM()
    fm_obj.set_apikey(apikey)
    fm_obj.load_data()
    print(f"The top artist is {fm_obj.artist}")
    print(f"{fm_obj.artist}'s total playcount is {fm_obj.playcount}")
    print(f"{fm_obj.artist}'s amount of listeners is {fm_obj.listeners}")
    my_message = fm_obj.transclude("My favorite arist right now is @lastfm!")
    print(my_message)


if __name__ == '__main__':
    main()

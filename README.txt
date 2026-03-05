ICS32 Assignment 3: Publishing Online

Has the same functionality as Assignment 2 but allows the user to publish their posts to the web as well as modify their bio.


a4.py : Calls on ui.py to manage commands. Directly copied from a2.py (no changes were made). Tells the user what commands they can use and tells them how to use it. Relatively user friendly. If you do something wrong within a command, it keeps asking you until you get it right, you cannot quit from a command once you have already initiated it.
ui.py : Code from assignment 2. Is "admin mode" ([COMMAND] [INPUT] [[-]OPTION] [INPUT]). Now asks the user if they want to publish online if they do -addpost or -bio.
        Manages keywords @weather and @lastfm and calls on OpenWeather.py and LastFM.py to transclude those keywords.
        Can't run on it's own, since there is no "if __name__ == "__main__":" block.
WebAPI.py : Creates a superclass called WebAPI with default methods download_url and set_apikey and abstract methods load_data and transclude.
LastFM.py : Uses an API key from https://www.last.fm/api#getting-started and sets the keyword to the top artist right now.
            Calls on WebAPI.py to create the class.
OpenWeather.py : Uses an API key from https://openweathermap.org/ and sets the keyword to the location's weather description right now.
                Calls on WebAPI.py to create the class.
ds_client.py : Communicates with the server and sends JSON string to add posts or change bio.
ds_protocol.py : The protocol for the DSP server/client. Breaks down the JSON the server sent.
Profile.py : File for managing saving and loading of user data. Do not edit.
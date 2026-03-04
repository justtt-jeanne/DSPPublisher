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


def _download_url(url_to_download: str) -> dict:
    response = None
    r_obj = None

    try:
        response = urllib.request.urlopen(url_to_download)
        json_results = response.read()
        r_obj = json.loads(json_results)

    except urllib.error.HTTPError as e:
        print('Failed to download contents of URL')
        print('Status code: {}'.format(e.code))

    finally:
        if response != None:
            response.close()
    
    return r_obj


def main() -> None:
    apikey = "REDACTED"
    url = f" http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key={apikey}&format=json"

    fm_obj = _download_url(url)
    print(fm_obj["artists"]["artist"][0]["name"])
    print(fm_obj["artists"]["artist"][0]["playcount"])
    print(fm_obj["artists"]["artist"][0]["listeners"])


if __name__ == '__main__':
    main()

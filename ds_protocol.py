# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737

'''
Protocol for ds client and server
for receiving messages from the server
'''

import json
import urllib.request
import urllib.error
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])


def _extract_server_json(json_msg: str) -> DataTuple:
    '''
    Call the json.loads function on a json
    string and convert it to a DataTuple object
    '''
    try:
        json_obj = json.loads(json_msg)
        resp = json_obj['response']
        if resp.get('type') == "ok":
            return DataTuple(
                type=resp.get('type'),
                message=resp.get('message'),
                token=resp.get('token'),
                )
        return DataTuple(
            type=resp.get('type'),
            message=resp.get('message'),
            token="None"
        )
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return None
    

def _download_url(url_to_download: str) -> dict:
    response = None
    r_obj = None

    try:
        # url_request = urllib.request.Request(url_to_download)
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

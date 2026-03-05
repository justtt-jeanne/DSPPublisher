# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737

'''
Protocol for ds client and server
for receiving messages from the server
'''

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])


def extract_server_json(json_msg: str) -> DataTuple:
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

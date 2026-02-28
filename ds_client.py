# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737

import socket
import ds_protocol
import Profile

token = None
current_profile = None


def send(server: str, port: int, username: str,
         password: str, message: str, bio: str = None):
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''
    # Returns either True or False
    # depending on results of required operation
    global token
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server, port))
    except ConnectionError:
        print("Server/Port does not exist")
        return False
    except socket.gaierror:
        print("Server/Port does not exist")
        return False
    except ConnectionRefusedError:
        print("Server rejected client.")
        return False
    except TimeoutError:
        print("Timed out.")
        return False
    recv, send = join_json(client, username, password)
    resp = ds_protocol.extract_json(recv.readline())
    print(resp.message)
    try:
        if resp.type != "ok":
            return False
        else:
            if not token:
                token = resp.token
            if message is not None:
                recv, send = post_json(send, recv, message)
                resp = ds_protocol.extract_json(recv.readline())
                print(resp.message)
            if bio is not None:
                recv, send = bio_json(send, recv, bio)
                resp = ds_protocol.extract_json(recv.readline())
                print(resp.message)
    except AttributeError:
        print("Error")
        client.close()
        return False
    client.close()
    return True

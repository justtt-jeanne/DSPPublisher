# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737
# pylint: disable=global-statement
# pylint: disable=too-many-arguments, too-many-positional-arguments

'''
Connects a client to the server and sends posts or bios
to the server to post or update bios
'''

import socket
import ds_protocol
import Profile

TOKEN = None
CURRENT_PROFILE = None


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
    global TOKEN
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server, port))
    except ConnectionError:
        print("Server/Port does not exist")
        return False
    except socket.gaierror:
        print("Server/Port does not exist")
        return False
    except TimeoutError:
        print("Timed out.")
        return False
    recv, sender = join_json(client, username, password)
    resp = ds_protocol.extract_server_json(recv.readline())
    print(resp.message)
    try:
        if resp.type != "ok":
            return False
        if not TOKEN:
            TOKEN = resp.token
        if message is not None:
            recv, sender = post_json(sender, recv, message)
            resp = ds_protocol.extract_server_json(recv.readline())
            print(resp.message)
        if bio is not None:
            recv, sender = bio_json(sender, recv, bio)
            resp = ds_protocol.extract_server_json(recv.readline())
            print(resp.message)
    except AttributeError:
        print("Error")
        client.close()
        return False
    client.close()
    return True


def join_json(client, username, password):
    '''
    Formats a json string to send to the server to allow
    the client to join the server
    '''
    global CURRENT_PROFILE
    profile = Profile.Profile()
    profile.username = username
    profile.password = password
    CURRENT_PROFILE = profile
    join_msg = (
        f"{{\"join\": {{\"username\":\"{username}\"" +
        f",\"password\":\"{password}\", \"token\":\"\"}}}}")
    sender = client.makefile('w')
    recv = client.makefile('r')
    sender.write(join_msg + '\r\n')
    sender.flush()
    return recv, sender


def post_json(sender, recv, message):
    '''
    Formats a json string to send to the server to post something
    '''
    post = Profile.Post()
    post.set_entry(message)
    post_msg = (
        f"{{\"token\":\"{TOKEN}\", \"post\": {{\"entry\": " +
        f"\"{post.get_entry()}\", \"timestamp\": {post.get_time()}" + "}}")
    CURRENT_PROFILE.add_post(post)
    sender.write(post_msg + '\r\n')
    sender.flush()
    return recv, sender


def bio_json(sender, recv, bio):
    '''
    Formats a json string to send to the server to update the bio
    '''
    bio_msg = (
        f"{{\"token\":\"{TOKEN}\", \"bio\": {{\"entry\": \""
        + f"{bio}\", \"timestamp\": \"\"" + "}}")
    CURRENT_PROFILE.bio = bio
    sender.write(bio_msg + '\r\n')
    sender.flush()
    return recv, sender

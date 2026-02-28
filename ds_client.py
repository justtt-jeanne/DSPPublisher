# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737

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
            if not TOKEN:
                TOKEN = resp.token
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


def join_json(client, username, password):
    global CURRENT_PROFILE
    profile = Profile.Profile()
    profile.username = username
    profile.password = password
    CURRENT_PROFILE = profile
    join_msg = (
        f"{{\"join\": {{\"username\":\"{username}\"" +
        f",\"password\":\"{password}\", \"token\":\"\"}}}}")
    send = client.makefile('w')
    recv = client.makefile('r')
    send.write(join_msg + '\r\n')
    send.flush()
    return recv, send


def post_json(send, recv, message):
    post = Profile.Post()
    post.set_entry(message)
    post_msg = (
        f"{{\"token\":\"{TOKEN}\", \"post\": {{\"entry\": " +
        f"\"{post.get_entry()}\", \"timestamp\": {post.get_time()}" + "}}")
    CURRENT_PROFILE.add_post(post)
    send.write(post_msg + '\r\n')
    send.flush()
    return recv, send


def bio_json(send, recv, bio):
    bio_msg = (
        f"{{\"token\":\"{TOKEN}\", \"bio\": {{\"entry\": \""
        + f"{bio}\", \"timestamp\": \"\"" + "}}")
    CURRENT_PROFILE.bio = bio
    send.write(bio_msg + '\r\n')
    send.flush()
    return recv, send

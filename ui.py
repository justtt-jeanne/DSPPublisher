# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737
'''
The underlying user interface for a4.py, the "admin mode".
Has different functionst that a4.py calls on to execute
what the user wants.
'''

from pathlib import Path
import socket
import Profile
import ds_client
import OpenWeather
import LastFM

valid_flags = {"-r", "-f", "-s", "-e", "-n", "-posts", "-post",
               "-usr", "-pwd", "-bio", "-addpost", "-delpost", "-all"}
flags_with_parts = {"-s", "-n", "-usr", "-pwd",
                    "-bio", "-addpost", "-delpost"}
CURRENT_PROFILE = None
CURRENT_PATH = None
CURRENT_PORT = None


def check_num_posts():
    '''
    Returns the number of posts in the profile.
    Not called within this module.
    '''
    return len(CURRENT_PROFILE.get_posts())


def trying_attribute(profile_command):
    '''
    A profile command (usually printing something)
    is tried and if that attribute does not exist
    in the profile, it will error.
    '''
    try:
        profile_command
        return True
    except AttributeError:
        print("No Profile loaded. Please try again.")
        return False


def parse_command():
    '''
    Splits the initial command, calls on some other splitting
    commands for redundancy's sake.
    '''
    tokens = input().split()
    if not tokens:
        return None
    cmd = tokens[0].upper()
    flags = {}
    i = 1
    path, i = parse_path(tokens, i)
    while i < len(tokens):
        flag = tokens[i]
        if flag in flags_with_parts and cmd != "P":
            i += 1
            if i >= len(tokens) or (tokens[i] in valid_flags):
                print(f"Missing argument for {flag}")
                return None
            value_parts = []
            if tokens[i].startswith('"') or tokens[i].startswith("'"):
                value, i = parse_quotes(tokens, i)
            else:
                while i < len(tokens) and (not tokens[i] in valid_flags):
                    value_parts.append(tokens[i])
                    i += 1
                value = " ".join(value_parts)
            if flag in {"-usr", "-pwd"}:
                value = value.replace(" ", "")
            flags[flag] = value
            continue
        if flag == "-e":
            if i + 1 >= len(tokens):
                print("Missing argument for -e")
                return None
            flags["-e"] = tokens[i + 1]
            i += 2
            continue
        if flag == "-post":
            if i + 1 >= len(tokens):
                print("Missing argument for -post")
                return None
            flags["-post"] = tokens[i + 1]
            i += 2
            continue
        if cmd == "P" and flag in {"-usr", "-pwd", "-bio"}:
            flags[flag] = True
            i += 1
            continue
        if flag in {"-r", "-f", "-posts", "-all"}:
            flags[flag] = True
            i += 1
            continue
        print(f"Invalid token {flag}")
        return None
    return cmd, path, flags


def parse_path(tokens, i):
    '''
    Called in parse_command(), get the the path.
    '''
    path_parts = []
    while (i < len(tokens)) and (not tokens[i] in valid_flags):
        path_parts.append(tokens[i])
        i += 1
    path = Path(" ".join(path_parts))
    return path, i


def parse_quotes(tokens, i):
    '''
    Called in parse_command(), get the message in
    any argument that has a message that should be surrounded
    by quotation marks.
    '''
    value_parts = []
    if tokens[i].startswith('"') or tokens[i].startswith("'"):
        quote = tokens[i][0]
        part = tokens[i][1:]
        if part.endswith(quote):
            value_parts.append(part[:-1])
            i += 1
        else:
            value_parts.append(part)
            i += 1
            while i < len(tokens):
                if tokens[i].endswith(quote):
                    value_parts.append(tokens[i][:-1])
                    i += 1
                    break
                value_parts.append(tokens[i])
                i += 1
    else:
        value_parts.append(tokens[i])
        i += 1
    value = " ".join(value_parts)
    return value, i


def list_directory(directory, flags):
    '''
    Lists the directory if the first command is L.
    Handles -f, -s, -e, and -r.
    '''
    if not directory.is_dir():
        print("Path does not exist. Please try again.")
        return
    if "-s" in flags:
        target_name = flags["-s"]
    files = []
    folders = []
    for item in directory.iterdir():
        if item.is_file():
            files.append(item)
        else:
            folders.append(item)
    for fle in files:
        if "-s" in flags:
            if fle.name == target_name:
                print(fle)
        elif "-e" in flags:
            if fle.suffix == f".{flags['-e']}":
                print(fle)
        else:
            print(fle)
    only_recursive = flags == {"-r": True}
    if "-r" in flags:
        for folder in folders:
            if only_recursive:
                print(folder)
            list_directory(folder, flags)
    else:
        if "-f" not in flags and "-s" not in flags and "-e" not in flags:
            for folder in folders:
                print(folder)


def create_file(directory, flags):
    '''
    Instantiates a new Profile object.
    Only creates dsu files.
    '''
    global CURRENT_PROFILE, CURRENT_PATH, CURRENT_PORT
    file_created = False
    if not directory.is_dir():
        print("Path does not exist. Please try again.")
        return None
    try:
        fle = flags["-n"]
    except KeyError:
        print("Wrong flag used. Please try again.")
        return None
    file_path = Path(fle + ".dsu")
    full_path = directory / file_path
    CURRENT_PATH = full_path
    if CURRENT_PATH.exists():
        print(f"{CURRENT_PATH} already exists, switching to load mode.")
        file_handler("O", CURRENT_PATH)
        return None
    CURRENT_PROFILE = Profile.Profile()
    print("Please enter a dsuserver: ")
    server = input().split()
    while len(server) > 1:
        print("Servers cannot have spaces. Please try again.")
        server = input().split()
    true_server = "".join(server)
    if CURRENT_PORT is None:
        print("Please enter a port: ")
        try:
            CURRENT_PORT = int(input())
        except TypeError:
            print("Invalid Port.")
            return None
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((true_server, CURRENT_PORT))
        client.close()
    except socket.gaierror:
        print("Server/Port does not exist.")
        CURRENT_PORT = None
        return None
    except ConnectionRefusedError:
        print("Server rejected client.")
        CURRENT_PORT = None
        return None
    CURRENT_PROFILE.dsuserver = true_server
    print("Please enter a username: ")
    username = input().split()
    while not username:
        print("Username must be at least 1 character. Please try again.")
        username = input().split()
    CURRENT_PROFILE.username = "".join(username)
    print("Please enter a password: ")
    password = input().split()
    while not password:
        print("Password must be at least 1 character. Please try again.")
        password = input().split()
    CURRENT_PROFILE.password = "".join(password)
    print("Please enter a bio: ")
    bio = input()
    while not bio:
        print("Bio must be at least 1 character. Please try again.")
        bio = input().split()
    bio = check_ow_and_lastfm(bio)
    if bio is None:
        return None
    CURRENT_PROFILE.bio = bio
    try:
        with open(CURRENT_PATH, "w", encoding="utf-8") as file:
            pass
        CURRENT_PROFILE.save_profile(str(CURRENT_PATH))
    except Profile.DsuFileError as e:
        print(e)
        return None
    except Profile.DsuProfileError:
        print("Profile does not exist. Please try again.")
        return None
    if CURRENT_PATH.is_file():
        print(CURRENT_PATH)
        file_created = True
    return file_created


def file_handler(command, directory):
    '''
    Deletes, reads, or opens a dsu file.
    '''
    global CURRENT_PATH, CURRENT_PROFILE, CURRENT_PORT
    if not directory.is_file():
        print("Path does not exist. Please try again.")
        return
    if directory.suffix != ".dsu":
        print("ERROR")
        return
    if command == "D":
        directory.unlink()
        print(f"{directory} DELETED")
    elif command == "R":
        with open(directory, "r", encoding="utf-8") as file:
            first_char = file.read(1)
            file.seek(0)
            if not first_char:
                print("EMPTY")
            else:
                for line in file.readlines():
                    print(line)
    else:
        if CURRENT_PORT is None:
            print("Please enter a port: ")
            CURRENT_PORT = int(input())
        CURRENT_PROFILE = Profile.Profile()
        try:
            CURRENT_PATH = directory
            CURRENT_PROFILE.load_profile(CURRENT_PATH)
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((CURRENT_PROFILE.dsuserver, CURRENT_PORT))
                client.close()
            except socket.gaierror:
                print("Server/Port does not exist")
                CURRENT_PORT = None
                return
            except ConnectionRefusedError:
                print("Server rejected client.")
                CURRENT_PORT = None
                return
            print("File successfully loaded.\n")
        except Profile.DsuFileError as e:
            print(e)
            return
        except Profile.DsuProfileError:
            print("Profile does not exist. Please try again.\n")
            return


def edit_profile(flags):
    '''
    Edits the current dsu profile.
    Handles -usr, -pwd, -bio, -addpost, and -delpost.
    Also asks the user if they would like to post their bio or post
    to the web.
    '''
    global CURRENT_PROFILE
    required_flags = ["-usr", "-pwd", "-bio", "-addpost", "-delpost"]
    for flag in required_flags:
        if flag in flags and not flags[flag]:
            print(f"Missing argument for {flag}. Please try again.")
            return
    try:
        if "-usr" in flags:
            if not flags["-usr"]:
                print("Username must be at least 1 character.")
                return
            CURRENT_PROFILE.username = flags["-usr"]
            print("Username updated.")
        if "-pwd" in flags:
            if not flags["-pwd"]:
                print("Password must be at least 1 character.")
                return
            CURRENT_PROFILE.password = flags["-pwd"]
            print("Password updated.")
        if "-bio" in flags:
            if not flags["-bio"].strip():
                print("Bio cannot be empty.")
                return
            bio = flags["-bio"]
            bio = check_ow_and_lastfm(bio)
            if bio is not None:
                print("Would you like to change bio online (y/n)?")
                bio_online = input().lower()
                if bio_online == "y":
                    ds_client.send(CURRENT_PROFILE.dsuserver, CURRENT_PORT,
                                   CURRENT_PROFILE.username,
                                   CURRENT_PROFILE.password,
                                   "None", bio)
                elif bio_online != "n":
                    print("Invalid option. Quitting proccess.")
                CURRENT_PROFILE.bio = bio
                print("Bio updated in file.")
        if "-addpost" in flags:
            post = Profile.Post()
            entry = flags["-addpost"]
            if not entry.strip():
                print("Post cannot be empty.")
                return
            entry = check_ow_and_lastfm(entry)
            if entry is not None:
                print("Would you like to post online (y/n)?")
                online = input().lower()
                if online == "y":
                    ds_client.send(CURRENT_PROFILE.dsuserver, CURRENT_PORT,
                                   CURRENT_PROFILE.username,
                                   CURRENT_PROFILE.password,
                                   entry, None)
                elif online != "n":
                    print("Invalid option. Quitting proccess.")
                post.set_entry(entry)
                CURRENT_PROFILE.add_post(post)
                print("Post added in file.")
        if "-delpost" in flags:
            try:
                delete_id = int(flags["-delpost"]) - 1
            except ValueError:
                print("Must be a valid integer. Please try again.")
                return
            deleted = CURRENT_PROFILE.del_post(int(delete_id))
            print("Post deleted.")
            if not deleted:
                print("Invalid index. Please try again.")
                return
    except AttributeError:
        print("No Profile loaded. Please try again.")
        return
    try:
        CURRENT_PROFILE.save_profile(str(CURRENT_PATH))
    except Profile.DsuFileError as e:
        print(e)
    except Profile.DsuProfileError:
        print("Profile does not exist. Please try again.")


def check_ow_and_lastfm(entry):
    '''
    Checks if the string attached to a flag
    has keywords in it, then calls on other
    functions to replace the keywords and
    returns that string.
    '''
    if "@weather" in entry:
        entry = check_transclude_ow(entry)
    elif "@lastfm" in entry:
        entry = check_transclude_lastfm(entry)
    return entry


def check_transclude_ow(entry):
    '''
    Asks user if they want to change their location
    and for their API key for OpenWeather, and then
    transcludes the keyword to the location's
    description.
    '''
    print("Would you like to change your location?")
    location = input()
    print("Please enter an API key for OpenWeather.")
    apikey = input()
    if location == "y":
        print("Please enter a zipcode.")
        zipcode = input()
        print("Please enter a country code.")
        ccode = input()
        open_weather = OpenWeather.OpenWeather(zipcode, ccode)
    elif location == "n":
        open_weather = OpenWeather.OpenWeather()
    else:
        print("Invalid option.")
        return None
    open_weather.set_apikey(apikey)
    open_weather.load_data()
    if open_weather.description is None:
        return None
    return open_weather.transclude(entry)


def check_transclude_lastfm(entry):
    '''
    Asks userfor their API key for LastFM, and then
    transcludes the keyword to the top artist name.
    '''
    print("Please enter an API key for LastFM.")
    apikey = input()
    last_fm = LastFM.LastFM()
    last_fm.set_apikey(apikey)
    last_fm.load_data()
    if last_fm.artist is None:
        return None
    return last_fm.transclude(entry)


def print_profile(flags):
    '''
    Prints the current dsu profile.
    Handles -usr, -pwd, -bio, -addpost, and -delpost.
    Also asks the user if they would like to post their bio or post
    to the web.
    '''
    global CURRENT_PROFILE, CURRENT_PATH
    if "-usr" in flags:
        successful = trying_attribute(print(CURRENT_PROFILE.username))
        if not successful:
            return
    if "-pwd" in flags:
        successful = trying_attribute(print(CURRENT_PROFILE.password))
        if not successful:
            return
    if "-bio" in flags:
        successful = trying_attribute(print(CURRENT_PROFILE.bio))
        if not successful:
            return
        print("Would you like this bio to be online (y/n)?")
        bio_online = input().lower()
        if bio_online == "y":
            ds_client.send(CURRENT_PROFILE.dsuserver, CURRENT_PORT,
                           CURRENT_PROFILE.username,
                           CURRENT_PROFILE.password,
                           None, CURRENT_PROFILE.bio)
        elif bio_online != "n":
            print("Invalid option. Quitting proccess.")
    if "-posts" in flags:
        posts = CURRENT_PROFILE.get_posts()
        for item in posts:
            print(item.get_entry())
    if "-post" in flags:
        single_id = flags["-post"]
        try:
            post_id = int(single_id) - 1
        except ValueError:
            print("ERROR: Post ID must be an integer")
            return
        posts = CURRENT_PROFILE.get_posts()
        if post_id < 0 or post_id >= len(posts):
            print("ERROR: Invalid post ID")
            return
        print(posts[post_id].get_entry())
        print("Would you like this post to be online (y/n)?")
        online = input().lower()
        if online == "y":
            ds_client.send(CURRENT_PROFILE.dsuserver, CURRENT_PORT,
                           CURRENT_PROFILE.username,
                           CURRENT_PROFILE.password,
                           posts[post_id].get_entry(), None)
        elif online != "n":
            print("Invalid option. Quitting proccess.")
    if "-all" in flags:
        print(f"DsuServer: {CURRENT_PROFILE.dsuserver}")
        print(f"Username: {CURRENT_PROFILE.username}")
        print(f"Password: {CURRENT_PROFILE.password}")
        print(f"Bio: {CURRENT_PROFILE.bio}")
        posts = CURRENT_PROFILE.get_posts()
        print("Posts: ", end="")
        for item in posts:
            print(item.get_entry(), end=" ")
        print()


def run():
    '''
    Admin mode. Finds the first command and does the
    corresponding function.
    '''
    while True:
        parsed = parse_command()
        if not parsed:
            continue
        cmd, path, flags = parsed
        if not path.parts and cmd not in {"Q", "E", "P"}:
            print("ERROR")
            continue
        if cmd == "Q":
            return
        if cmd == "L":
            list_directory(path, flags)
        elif cmd == "C":
            create_file(path, flags)
        elif cmd in ("D", "R", "O"):
            file_handler(cmd, path)
        elif cmd == "E":
            if CURRENT_PROFILE is None:
                print("ERROR")
                continue
            try:
                edit_profile(flags)
            except Profile.DsuFileError:
                print("ERROR")
                continue
            except Profile.DsuProfileError:
                print("ERROR")
                continue
        elif cmd == "P":
            if CURRENT_PROFILE is None:
                print("ERROR")
                continue
            try:
                print_profile(flags)
            except Profile.DsuFileError:
                print("ERROR")
                continue
            except Profile.DsuProfileError:
                print("ERROR")
                continue
        else:
            print("Invalid command. Please try again.")
            continue

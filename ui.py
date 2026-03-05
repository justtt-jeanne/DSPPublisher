# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737

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
current_profile = None
current_path = None
current_port = None


def trying_attribute(profile_command):
    try:
        profile_command
    except AttributeError:
        print("No Profile loaded. Please try again.")
        return


def parse_command():
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
    path_parts = []
    while (i < len(tokens)) and (not tokens[i] in valid_flags):
        path_parts.append(tokens[i])
        i += 1
    path = Path(" ".join(path_parts))
    return path, i


def parse_quotes(tokens, i):
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
    global current_profile, current_path, current_port
    file_created = False
    if not directory.is_dir():
        print("Path does not exist. Please try again.")
        return
    try:
        fle = flags["-n"]
    except KeyError:
        print("Wrong flag used. Please try again.")
        return
    full_file = fle + ".dsu"
    file_path = Path(full_file)
    full_path = directory / file_path
    current_path = full_path
    if current_path.exists():
        print(f"{current_path} already exists, switching to load mode.")
        file_handler("O", current_path)
        return
    user_info = Profile.Profile()
    current_profile = user_info
    print("Please enter a dsuserver: ")
    server = input().split()
    while len(server) > 1:
        print("Servers cannot have spaces. Please try again.")
        server = input().split()
    true_server = "".join(server)
    if current_port is None:
        print("Please enter a port: ")
        current_port = int(input())
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((true_server, current_port))
        client.close()
    except socket.gaierror:
        print("Server/Port does not exist.")
        current_port = None
        return
    except ConnectionRefusedError:
        print("Server rejected client.")
        current_port = None
        return
    current_profile.dsuserver = true_server
    print("Please enter a username: ")
    username = input().split()
    while not username:
        print("Username must be at least 1 character. Please try again.")
        username = input().split()
    current_profile.username = "".join(username)
    print("Please enter a password: ")
    password = input().split()
    while not password:
        print("Password must be at least 1 character. Please try again.")
        password = input().split()
    current_profile.password = "".join(password)
    print("Please enter a bio: ")
    bio = input()
    while not bio:
        print("Bio must be at least 1 character. Please try again.")
        bio = input().split()
    bio = check_ow_and_lastfm(bio)
    current_profile.bio = bio
    try:
        with open(current_path, "w") as file:
            pass
        current_profile.save_profile(str(current_path))
    except Profile.DsuFileError as e:
        print(e)
        return
    except Profile.DsuProfileError:
        print("Profile does not exist. Please try again.")
        return
    if current_path.is_file():
        print(current_path)
        file_created = True
        return file_created


def file_handler(command, directory):
    global current_path, current_profile, current_port
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
        if current_port is None:
            print("Please enter a port: ")
            current_port = int(input())
        current_profile = Profile.Profile()
        try:
            current_path = directory
            current_profile.load_profile(current_path)
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((current_profile.dsuserver, current_port))
                client.close()
            except socket.gaierror:
                print("Server/Port does not exist")
                current_port = None
                return
            except ConnectionRefusedError:
                print("Server rejected client.")
                current_port = None
                return
            print("File successfully loaded.\n")
        except Profile.DsuFileError as e:
            print(e)
            return
        except Profile.DsuProfileError:
            print("Profile does not exist. Please try again.\n")
            return


def edit_profile(flags):
    global current_profile, current_path
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
            current_profile.username = flags["-usr"]
            print("Username updated.")
        if "-pwd" in flags:
            if not flags["-pwd"]:
                print("Username must be at least 1 character.")
                return
            current_profile.password = flags["-pwd"]
            print("Password updated.")
        if "-bio" in flags:
            if not flags["-bio"].strip():
                print("Bio cannot be empty.")
                return
            entry = check_ow_and_lastfm(entry)
            print("Would you like to change bio online (y/n)?")
            bio_online = input().lower()
            if bio_online == "y":
                bio = flags["-bio"]
                ds_client.send(current_profile.dsuserver, current_port,
                               current_profile.username,
                               current_profile.password,
                               None, bio)
            elif bio_online != "n":
                print("Invalid option. Quitting proccess.")
            current_profile.bio = flags["-bio"]
            print("Bio updated in file.")
        if "-addpost" in flags:
            post = Profile.Post()
            entry = flags["-addpost"]
            if not entry.strip():
                print("Post cannot be empty.")
                return
            entry = check_ow_and_lastfm(entry)
            print("Would you like to post online (y/n)?")
            online = input().lower()
            if online == "y":
                ds_client.send(current_profile.dsuserver, current_port,
                               current_profile.username,
                               current_profile.password,
                               entry, None)
            elif online != "n":
                print("Invalid option. Quitting proccess.")
            post.set_entry(entry)
            current_profile.add_post(post)
            print("Post added in file.")
        if "-delpost" in flags:
            try:
                delete_id = int(flags["-delpost"]) - 1
                print("Post deleted.")
            except ValueError:
                print("Must be a valid integer. Please try again.")
                return
            deleted = current_profile.del_post(int(delete_id))
            if not deleted:
                print("Invalid index. Please try again.")
                return
    except AttributeError:
        print("No Profile loaded. Please try again.")
        return
    try:
        current_profile.save_profile(str(current_path))
    except Profile.DsuFileError as e:
        print(e)
    except Profile.DsuProfileError:
        print("Profile does not exist. Please try again.")


def check_ow_and_lastfm(entry):
    if "@weather" in entry:
        entry = check_transclude_ow(entry)
    elif "@lastfm" in entry:
        entry = check_transclude_lastfm(entry)
    return entry


def check_transclude_ow(entry):
    print("Would you like to change your location?")
    location = input()
    if location == "y":
        print("Please enter a zipcode.")
        zipcode = input()
        print(f"\"{zipcode}\"")
        print("Please enter a country code.")
        ccode = input()
        print(f"\"{zipcode}\"")
    elif location != "n":
        print("Invalid option.")
        return
    print("Please enter an API key for OpenWeather.")
    apikey = input()
    open_weather = OpenWeather.OpenWeather()
    open_weather.set_apikey(apikey)
    open_weather.load_data()
    if open_weather.description is None:
        return
    return open_weather.transclude(entry)


def check_transclude_lastfm(entry):
    pass



def print_profile(flags):
    global current_profile, current_path
    if "-usr" in flags:
        trying_attribute(print(current_profile.username))
    if "-pwd" in flags:
        print(current_profile.password)
    if "-bio" in flags:
        print(current_profile.bio)
        print("Would you like this bio to be online (y/n)?")
        bio_online = input().lower()
        if bio_online == "y":
            bio = flags["-bio"]
            ds_client.send(current_profile.dsuserver, current_port,
                            current_profile.username,
                            current_profile.password,
                            None, current_profile.bio)
        elif bio_online != "n":
            print("Invalid option. Quitting proccess.")
    if "-posts" in flags:
        posts = current_profile.get_posts()
        for item in posts:
            print(item.get_entry())
    if "-post" in flags:
        id = flags["-post"]
        try:
            post_id = int(id) - 1
        except ValueError:
            print("ERROR: Post ID must be an integer")
            return
        posts = current_profile.get_posts()
        if post_id < 0 or post_id >= len(posts):
            print("ERROR: Invalid post ID")
            return
        print(posts[post_id].get_entry())
        print("Would you like this post to be online (y/n)?")
        online = input().lower()
        if online == "y":
            ds_client.send(current_profile.dsuserver, current_port,
                            current_profile.username,
                            current_profile.password,
                            posts[post_id].get_entry(), None)
        elif online != "n":
                print("Invalid option. Quitting proccess.")
    if "-all" in flags:
        print(f"DsuServer: {current_profile.dsuserver}")
        print(f"Username: {current_profile.username}")
        print(f"Password: {current_profile.password}")
        print(f"Bio: {current_profile.bio}")
        posts = current_profile.get_posts()
        print("Posts: ", end="")
        for item in posts:
            print(item.get_entry(), end=" ")
        print()


def run():
    global current_path, current_profile
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
            if current_profile is None:
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
            if current_profile is None:
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

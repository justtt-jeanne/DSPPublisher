# JEANNE NGUYEN
# jeannen2@uci.edu
# 57923737
'''
User friendly code that allows the user to
explore their computer and also post things
to a website.
'''

from pathlib import Path
import ui

E_SUBCOMMANDS = {"-usr", "-post", "-pwd",
                 "-bio", "-addpost", "-delpost"}


def print_options():
    '''
    Prints menu of commands for the user
    '''
    print("Here are the commands you can input:\r\n"
          "L: List all the contents in a given directory."
          " (More options available if chosen)\r\n"
          "C: Create a new dsu file\r\n"
          "O: Load an existing dsu file\r\n"
          "E: Edit information on the file loaded through"
          " C or O. (More options available"
          " if chosen.)\r\n"
          "P: Print information on the file loaded through"
          " C or O. (More options available"
          " if chosen.)\r\n"
          "R: Read an existing dsu file\r\n"
          "D: Delete an existing dsu file\r\n"
          "Q: Quit\r\n"
          "admin: Enter admin mode, must input any "
          "command in this format: [COMMAND] [INPUT] [[-]OPTION] [INPUT]")
    return input().strip()


def parse_command_l(command):
    '''
    Splits whatever the user inputs if they chose the "L" command
    '''
    tokens = command.split()
    if not tokens:
        print("ERROR")
        return None
    flags = {}
    i = 0
    while i < len(tokens):
        flag = tokens[i]
        if flag == "-s":
            i += 1
            if i >= len(tokens) or tokens[i].startswith("-"):
                print(f"Missing argument for {flag}")
                return None
            value, i = parse_quotes(tokens, i)
            flags[flag] = value
            continue
        if flag == "-e":
            if i + 1 >= len(tokens):
                print("Missing argument for -e")
                return None
            flags["-e"] = tokens[i + 1]
            i += 2
            continue
        if flag in {"-r", "-f"}:
            flags[flag] = True
            i += 1
            continue
        print(f"Invalid token {flag}")
        return None
    return flags


def parse_command_e(command):
    '''
    Splits whatever the user inputs if they chose the "E" command
    '''
    tokens = command.split()
    if not tokens:
        print("ERROR")
        return None
    flags = {}
    i = 0
    while i < len(tokens):
        flag = tokens[i]
        if flag in E_SUBCOMMANDS:
            i += 1
            if i >= len(tokens) or tokens[i].startswith("-"):
                print(f"Missing argument for {flag}")
                return None
            value_parts = []
            if tokens[i].startswith('"') or tokens[i].startswith("'"):
                value, i = parse_quotes(tokens, i)
            else:
                while i < len(tokens) and (not tokens[i] in E_SUBCOMMANDS):
                    value_parts.append(tokens[i])
                    i += 1
                value = " ".join(value_parts)
            if flag in {"-usr", "-pwd"}:
                value = value.replace(" ", "")
            flags[flag] = value
            continue
        print(f"Invalid token {flag}")
        return None
    return flags


def parse_command_p(command):
    '''
    Splits whatever the user inputs if they chose the "P" command
    '''
    tokens = command.split()
    if not tokens:
        return None
    flags = {}
    i = 0
    while i < len(tokens):
        flag = tokens[i]
        if flag == "-post":
            if i + 1 >= len(tokens):
                print("Missing argument for -post")
                return None
            flags["-post"] = tokens[i + 1]
            i += 2
            continue
        if flag in {"-usr", "-pwd", "-bio", "-posts", "-all"}:
            flags[flag] = True
            i += 1
            continue
        print(f"Invalid token {flag}")
        return None
    return flags


def parse_quotes(tokens, i):
    '''
    Splits part of whatever the user inputed
    in commands if it should have quotes around it
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


def check_path(directory):
    '''
    Checks if the path input is a valid path
    '''
    return directory.exists()


def ask_path_again():
    '''
    Asks the user to input another path because the last
    one was invlaid.
    '''
    print("Invalid path. Please try again.\r")
    path = input("What is the full name (path included)"
                 " of the file you would like to load?\r\n")
    directory = Path(path)
    return directory


def command_l():
    '''
    After the user inputs "L", it goes here and lists
    more options that the user can do to list things in
    a path.
    '''
    print("Entered L mode!")
    path = input("What is the full name (path included)"
                 " of the file you would like to load?\r\n")
    directory = Path(path)
    while not check_path(directory):
        directory = ask_path_again()
    subcommands = input("Would you like to use subcommands "
                        "with this (y/n)?\r\n"
                        "Subcommands can specify what "
                        "you want to see.\r\n"
                        "For example, only files or files "
                        "with a certain extension.\r\n")
    while subcommands.lower() not in {"y", "n"}:
        subcommands = input("Invalid command. Please try again.\r\n")
    if subcommands == "y":
        print("Here are the commands you can use:\r\n"
              "-f: List only the files in the path\r\n"
              "-s [file]: Lists files with the matching file name\r\n"
              "-e [extenstion]: Lists files with the matching file "
              "extension. Please do not include the period with it.\r\n"
              "-r: Lists everything in a path recursively "
              "(meaning, it will open folders in the path and"
              " list what's in those as well.) Can be used "
              "with any of the previous commands.")
        command = input("Please input the command(s)"
                        " you would like to use.\r\n")
        flags = parse_command_l(command)
        if not flags:
            while not flags:
                command = input("Please input the command(s) you"
                                " would like to use.\r\n")
                flags = parse_command_l(command)
    else:
        flags = {}
    ui.list_directory(directory, flags)


def command_c():
    '''
    After the user inputs "C", it goes here and creates a file.
    '''
    path = input("Entered C mode! What is the name of the "
                 "path where you would like to create a file?\r\n")
    directory = Path(path)
    while not check_path(directory):
        directory = ask_path_again()
    flags = {}
    file_name = input("Path processed. What would you"
                      " like to name your file? Do not"
                      " include the extension.\r\n")
    flags["-n"] = file_name
    print("Creating file...")
    file_create = ui.create_file(directory, flags)
    if file_create:
        print("File created succesfully!\r\n")


def command_o():
    '''
    After the user inputs "O", it goes here and loads
    an existing dsu file.
    '''
    print("Entered O mode!")
    path = input("What is the full name (path included)"
                 " of the file you would like to load?\r\n")
    directory = Path(path)
    ui.file_handler("O", directory)


def command_e():
    '''
    After the user inputs "E", it goes here and provides
    the user more options to edit their existing DSU file.
    '''
    print("Entered E mode!")
    print("Here are the commands you can use:\r\n"
          "-usr \"username\": Change your username.\r\n"
          "-pwd \"password\": Change your password.\r\n"
          "-bio \"bio\": Change your bio. You can choose"
          " to change your bio online (given you've"
          " posted something).\r\n"
          "-addpost \"new post\": Add post to your posts."
          " You can choose to post the added post online.\r\n"
          "-delpost [ID]: Delete post given its ID.")
    command = input("Please input the command(s)"
                    " you would like to use.\r\n")
    flags = parse_command_e(command)
    if not flags:
        while not flags:
            command = input("Please input the command(s) you"
                            " would like to use.\r\n")
            flags = parse_command_e(command)
    ui.edit_profile(flags)


def command_p():
    '''
    After the user inputs "P", it goes here and provides
    the user more options to print parts of their 
    existing DSU file.
    '''
    print("Entered P mode!")
    print("Here are the commands you can use:\r\n"
          "-usr: Print the current username.\r\n"
          "-pwd: Print the current password.\r\n"
          "-bio: Print the current bio. You can"
          " choose to display this bio online (given"
          " you've posted something).\r\n"
          "-posts: Print all current posts.\r\n"
          "-post [ID]: Print post identified by ID."
          " You can choose to post these specific posts online.\r\n"
          "-all: Print everything currently in the Profile.\r")
    command = input("Please input the command(s)"
                    " you would like to use.\r\n")
    flags = parse_command_p(command)
    if not flags:
        while not flags:
            command = input("Please input the command(s) you"
                            " would like to use.\r\n")
            flags = parse_command_p(command)
    ui.print_profile(flags)


def command_r():
    '''
    After the user inputs "R", it goes here and asks the
    user for a file that they would like to read the
    contents of.
    '''
    print("Entered R mode!")
    path = input("What is the full name (path included)"
                 " of the file you would like to load?\r\n")
    directory = Path(path)
    ui.file_handler("R", directory)


def command_d():
    '''
    After the user inputs "D", it goes here and asks the
    user for a file that they would like to delete.
    '''
    print("Entered D mode!")
    path = input("What is the full name (path included)"
                 " of the file you would like to load?\r\n")
    directory = Path(path)
    ui.file_handler("D", directory)


def main():
    '''
    Prints a menu and asks the user for input to start.
    '''
    print("Welcome! ", end="")
    while True:
        command = print_options().upper()
        if len(command) > 1 and (command != "ADMIN"):
            print("Please input a singular letter in the " +
                  "given commands or 'admin'.\r")
            continue
        if command == "Q":
            print("Goodbye!")
            return
        if command == "ADMIN":
            print("Succesfully entered admin mode.\r")
            ui.run()
        elif command == "L":
            command_l()
            continue
        elif command == "C":
            command_c()
            continue
        elif command == "R":
            command_r()
        elif command == "D":
            command_d()
        elif command == "O":
            command_o()
        elif command == "E":
            command_e()
        elif command == "P":
            command_p()
        else:
            print("Invalid command. Please try again.\r")
            continue


if __name__ == "__main__":
    main()

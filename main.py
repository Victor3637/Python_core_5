import logging
import re

from fuzzywuzzy import fuzz, process
import readline

import classes
from handlers import commands


def completer(text, state):
    if not text.isalpha():
        return None
    options = [cmd for cmd in commands.keys() if cmd.startswith(text.lower())]
    if not options:
        return None
    if state < len(options):
        return options[state]
    return None


def parse_command(user_input: str):
    match = re.search(
        r"^show\s|^good\s|^del\s", user_input.lower())
    try:
        if match:
            user_command = " ".join(user_input.split()[:2]).lower()
            command_arguments = user_input.split()[2:]
        else:
            user_command = user_input.split()[0].lower()
            command_arguments = user_input.split()[1:]
    except IndexError:
        return "Please enter a command name."

    if user_command not in commands.keys():
        logging.basicConfig(level=logging.ERROR)
        best_match, match_ratio = process.extractOne(user_command,
                                                     commands.keys(),
                                                     scorer=fuzz.ratio)
        if match_ratio >= 60:
            return f"Command not found.\nPerhaps you meant '{best_match}'."
        else:
            return "Command not found.\nTo view all available commands, enter 'help'."
    else:
        return commands[user_command](*command_arguments)


def main():
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    while True:
        user_input = input("Enter command: ")
        result = parse_command(user_input)

        if result:
            if isinstance(result, classes.AddressBook):
                for page in result:
                    commands["clear"]()
                    print("\n".join([str(i) for i in page]))
                    user_input = input("Press 'q' to quit. Press any key to see the next page: ")
                    if user_input.lower() == "q":
                        break
            else:
                print(result)


if __name__ == "__main__":
    main()

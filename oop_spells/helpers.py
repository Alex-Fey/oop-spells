import os
import random
import sys
from pathlib import Path
from typing import List, Optional


def format_column_line(strings: List[str], column_size: int) -> str:
    """
    Formats a list of strings into a columnized row separated by "|" characters.
    :param strings: List of strings to separate into columns.
    :param column_size: Maximum number of characters each column will display
    :return: "| {string 1}     | {string 2}     | ..." where each "|" is separated by column_size characters plus two spaces.
    """
    output = "|"
    for string in strings:
        if len(string) >= column_size:
            output += " " + string[:column_size] + " |"
        else:
            output += " " + string + " "*(column_size - len(string)) + " |"
    return output

def can_be_int(s: str) -> bool:
    """
    :param s: A string.
    :return: True if the string can be converted to an integer, otherwise False.
    """
    try:
        int(s)
        return True
    except ValueError:
        return False

def can_be_float(s: str) -> bool:
    """
    :param s: A string.
    :return: True if the string can be converted to a float, otherwise False.
    """
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_valid_file_name(name: str) -> bool:
    """
    Checks if a given file name is valid on Windows.
    :param name: Name for a file without the extension (e.g. "foo" rather than "foo.txt").
    :return: True if that file name is valid, otherwise False.
    """
    stripped_name = name.strip()
    if stripped_name == "" or len(stripped_name) > 255:
        return False

    if stripped_name.endswith(".") or name.endswith(" "):
        return False

    illegal_chars = {"<", ">", ":", "\"", "/", "\\", "|", "?", "*"}
    for char in illegal_chars:
        if char in stripped_name:
            return False

    illegal_names = {"CON", "PRN", "AUX", "NUL",
                     *(f"COM{i+1}" for i in range(9)),
                     *(f"LPT{i+1}" for i in range(9))}
    if stripped_name in illegal_names:
        return False

    return True

def input_valid_int(lower_bound: Optional[float] = None,
                    upper_bound: Optional[float] = None,
                    lower_inclusive: bool = True,
                    upper_inclusive: bool = True,
                    input_str: str = "") -> int:
    """
    Gets user input for an integer. If the user inputs an invalid string, prints an error message and
    requests another input until the user enters a valid number.
    :param lower_bound: Lower bound of valid number range.
    :param lower_inclusive: True if a valid number must be >= the lower bound, False if is must be >.
    :param upper_bound: Upper bound of valid number range.
    :param upper_inclusive: True if a valid number must be <= the upper bound, False if is must be <.
    :param input_str: String printed to the left of the input query.
    :return: The first valid user-inputted integer.
    """
    valid = False
    num = 0

    while not valid:
        try:
            num = int(input(input_str))

            if ((lower_bound is None or lower_bound < num or (lower_inclusive and lower_bound == num))
                     and (upper_bound is None or upper_bound > num or (upper_inclusive and upper_bound == num))):
                valid = True
            else:
                print("That's out of range.")
        except ValueError:
            print("That's not an integer.")

    return num

def input_valid_float(lower_bound: Optional[float] = None,
                      upper_bound: Optional[float] = None,
                      lower_inclusive: bool = True,
                      upper_inclusive: bool = True,
                      input_str: str = "") -> float:
    """
    Gets user input for a float. If the user inputs an invalid string, prints an error message and
    requests another input until the user enters a valid number.
    :param lower_bound: Lower bound of valid number range.
    :param lower_inclusive: True if a valid number must be >= the lower bound, False if is must be >.
    :param upper_bound: Upper bound of valid number range.
    :param upper_inclusive: True if a valid number must be <= the upper bound, False if is must be <.
    :param input_str: String printed to the left of the input query.
    :return: The first valid user-inputted float.
    """
    valid = False
    num = 0

    while not valid:
        try:
            num = float(input(input_str))

            if ((lower_bound is None or lower_bound < num or (lower_inclusive and lower_bound == num))
                     and (upper_bound is None or upper_bound > num or (upper_inclusive and upper_bound == num))):
                valid = True
            else:
                print("That's out of range.")
        except ValueError:
            print("That's not a number.")

    return num

def written_list(l: list) -> str:
    """
    Converts a list into a string formatted as a written comma and "and" separated list. For example:
    [a] -> "a". [a, b] -> "a and b". [a, b, c] -> "a, b, and c".
    :param l: List to be converted.
    :return: Written list as a string.
    """
    if len(l) == 0:
        return ""
    elif len(l) == 1:
        return f"{l[0]}"
    elif len(l) == 2:
        return f"{l[0]} and {l[1]}"
    else:
        wl = ""
        for i in range(len(l)-1):
            wl += f"{l[i]}, "
        wl += f"and {l[-1]}"
        return wl

def random_win_message(winner: int, loser: int) -> str:
    """
    Generates a random win message from a list, given a winning team and a losing team.
    :param winner: Number of the winning team.
    :param loser: Number of the losing team.
    :return: A win message.
    """
    choices = [f"Team {winner} defeated Team {loser}!",
               f"Team {winner} has slain Team {loser}!",
               f"Team {winner} prevailed against Team {loser}!",
               f"Team {winner} triumphed against Team {loser}!",
               f"Team {winner} dominated Team {loser}!",
               f"Team {winner} destroyed Team {loser}!",
               f"Team {winner} crushed Team {loser}!",
               f"Team {winner} vanquished Team {loser}!",
               f"Team {winner} fended off Team {loser}!",
               f"Team {winner} checkmated Team {loser}!",
               f"Team {winner} revealed Team {loser}'s skill issue!",
               f"Team {winner} dunked on Team {loser}!",
               f"Team {winner} took that dub!"]
    return random.choice(choices)

def random_tie_message(first: int, second: int) -> str:
    """
    Generates a random tie (neither team won or lost) message from a list, given a first team and second team.
    :param first: Number of the first team.
    :param second: Number of the second team.
    :return: A tie message.
    """
    choices = [f"Teams {first} and {second} both folded!",
               f"Teams {first} and {second} had mutually assured destruction!",
               f"Teams {first} and {second} couldn't decide on a winner!",
               f"There's nobody left!",
               f"Teams {first} and {second} both no longer exist!",
               f"Teams {first} and {second} ended in a stalemate!",
               f"Teams {first} and {second} were equal opportunity unemployers!"]
    return random.choice(choices)

def create_or_get_appdata_path(path: Path) -> Path:
    """
    Gets the given path from AppData/Roaming, or creates it if it doesn't exist.
    :param path: The path starting from AppData/Roaming, such as "PolarisMagic/OOPSpells/storage" (do not start it with "/").
    :return: The entire target path, after creating it if it does not yet exist.
    :raises EnvironmentError: If not running on Windows.
    """
    if sys.platform != "win32":
        raise EnvironmentError("This program can only be run on Windows.")

    appdata_path = os.getenv("APPDATA")
    target_path = appdata_path / path

    os.makedirs(target_path, exist_ok=True)

    return target_path
import re
from enum import Enum

def yes_or_no_question(question):
    """
    Asks a question that requires a yes or no answer from the user.
    Yes, Y, No and N are accepted as valid responses (case insensitive).
    :param question: the question to ask
    :type question: string
    :return: user's answer
    :rtype: boolean
    """
    do_it = input(question + " (y/n) ").lower()
    while not re.match("^([yjn]|yes|no)$", do_it):
        do_it = input("Please answer with y(es) or n(o): ")
    if re.match("^([yj]|yes)$", do_it):
        return True
    return False


def choose_from_enum(enum):
    """
    Asks the user to choose from a given Enum.
    :param enum: the enum to choose from
    :type enum: Enum
    :return: the chosen enum element
    :rtype: enumeration member
    """
    i = 0
    items = []
    for item in enum:
        items.append(item.name)
        i += 1
        print(str(i) + "\t" + item.name)
    item_number = input_requires_int(input("Select an item: "))
    return enum[items[item_number-1]]


def input_requires_int(input_number):
    while True:
        try:
            if int(input_number) > 0:
                return int(input_number)
            else:
                raise ValueError
        except ValueError:
            input_number = input("Please enter a valid number: ")

def input_should_match_regex(regex, input_str):
    """
    Function that checks if a given input matchs a given regular expression.
    This will keep asking a user to enter an input until it matches the regular expression.
    :param regex: the required regular expression
    :type regex: string
    :param raw_input: the initial input to check
    :type raw_input: str
    :return: the user input matching the given expression
    :rtype: str
    """
    while not re.match(regex, input_str):
        input_str = input("Please try again, input should match regex=\"" + regex + "\"):\n")
    return input_str


class Entity(Enum):
    """
    Defines the different kinds of entities that can be configured during setup and configuration.
    """
    Component = "component"
    Sensor = "sensor"
    Actuator = "actuator"
import sys
import os
from os.path import join, dirname
from dotenv import load_dotenv


def get_token():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    return os.environ.get("GITSORT_TOKEN")


def pretty_prompt(left_text: str, right_text: str, width: int) -> str:
    """
    Creates a prompt with text both to the left and right of the cursor.

    :param left_text: str
        Text left of the cursor
    :param right_text: str
        Text right of the cursor
    :param width: int
        Width of the prompt
    :return: str
        User input
    """
    input_width = width - len(left_text) - len(right_text)
    print(left_text + " " * input_width + right_text)
    sys.stdout.write("\033[1A")
    sys.stdout.write(f"\033[{len(left_text)}C")
    sys.stdout.flush()
    return input("")

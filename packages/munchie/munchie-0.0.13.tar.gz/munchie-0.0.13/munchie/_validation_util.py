# import librares
import sys
from .pretty_print import console_log
from typing import Union


def _validate_confirmation_inputs(user_input: str) -> Union[bool, None]:
    """
    Validate user input for confirmation prompts.

    Args:
        user_input (str): the input as provided by the user

    Returns:
        (bool || None):
            'y' or 'yes' == True
            'n' or 'no' == True
            'q' or 'quit' == sys.exit()
            invalid input == None
    """

    user_input = user_input.lower()

    if user_input == 'y' or user_input == 'yes':
        return True

    elif user_input == 'n' or user_input == 'no':
        return False

    elif user_input == 'q' or user_input == 'quit':
        console_log('Exit received. Ending execution...', 'warning')
        sys.exit()

    else:
        console_log('Invalid input', 'warning')
        return None

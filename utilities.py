# Python
import sys
import pathlib

# Internal
from PlaceHolder import PlaceHolder

def err_print(*args, **kwargs) -> None:
    '''
    This function is a wrapper for writing to stderr.

	Params:
		The parameters are like usual parameters of print()

	Returns:
		None
	
	It works like print() but instead of writing to stdout, it writes to 
	stderr.
    '''

    print(*args, **kwargs, file=sys.stderr)

def input_file_opening(name: str):
    '''
    This function attempts to open the file as specified by the 
    name passed in through the argument for reading .

    Params:
        str: the name of the file to be opened.

    Returns:
        The file object if succesful, PlaceHolder object otherwise.
    '''
    has_problem = False

    try:
        file = open(name, "r")

    except PermissionError:
        err_print(f"Please give me sufficient permission to open file {name}")
        has_problem = True
    
    except FileNotFoundError:
        err_print(f"File {name} does not exist")
        has_problem = True

    except Exception:
        err_print("Something is wrong and I cannot figure out why, please submit a new issue so I can look into it :)")
        has_problem = True

    if (has_problem):
        return PlaceHolder.get_place_holder()

    return file

def output_file_opening(name: str):
    '''
    This function attempts to open the file as specified by the 
    name passed in through the argument for writing.

    Params:
        str: the name of the file to be opened.

    Returns:
        The file object if succesful, PlaceHolder object otherwise.
    '''
    has_problem = False

    try:
        file = open(name, "w")

    except PermissionError:
        err_print(f"Please give me sufficient permission to open file {name}")
        has_problem = True

    except Exception:
        err_print("Something is wrong and I cannot figure out why, please submit a new issue so I can look into it :)")
        has_problem = True

    if (has_problem):
        return PlaceHolder.get_place_holder()

    return file

def overwriting_file_warning(name: str) -> bool:
    '''
    This function warns the user of potentially overwriting an existing file 
    and ask whether it is intended.

    Params:
        str: Name of the file to be overwritten.

    Returns:
        bool: True if the overwriting is intended, False otherwise.
    '''

    while True:

        print(f"File with name {name} already exists, overwrite the file? (y/n)")

        intended = input().strip().lower()

        if (intended == "n"):
            return False
        
        elif (intended == "y"):
            return True
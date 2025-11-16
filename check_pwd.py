"""
# Name: Andrew Cochran
# OSU Email: cochandr@oregonstate.edu
# Course: CS 362
# Assignment: A2 TDD check_pwd.py
# Due Date: 10NOV2025
# Description: Creates check_pwd.py file to make implement a function that
checks if a password is of the correct length and complexity. Working it with
test.py.
"""

# imports
import sys


# function check_pwd
def check_pwd(pwd):
    # add minimum required symbols
    symbols = '~`!@#$%^&*()_+-='
    # if check for pwd parameter to have at least one symbol
    if not any(char in symbols for char in pwd):
        return False

    # if check for minimum password length requirements if met; test returned
    # true, which was correct, yet should have returned false
    # added length check to determine if pwd is greater than 20
    if len(pwd) < 12 or len(pwd) > 20:
        return False

    # add code to do a lowercase character check to ensure at least one lower
    # case letter is present in pwd parameter
    if not any(char.islower() for char in pwd):
        return False

    # add code to do an uppercase letter check to ensure pwd password has at
    # least one uppercase letter inside
    if not any(char.isupper() for char in pwd):
        return False

    # add code to check if there is at least one digit within the pwd parameter
    if not any(char.isdigit() for char in pwd):
        return False

    # 1st code change, return True
    # test3 passed, tests 1 & 2 did not
    # test3 passed, no errors with tests 1 and 2 commented out
    return True


if __name__ == "__main__":
    user_pwd = str(sys.argv[1])
    result = check_pwd(user_pwd)
    print(result)

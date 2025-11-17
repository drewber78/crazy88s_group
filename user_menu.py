"""
Placeholder file for use with video. Created 04NOV2025. Just shows the top menu for now.
"""
from datetime import datetime
from time import sleep
import os
import subprocess
import json



def print_menu_in_box(title, menu_items):
    """
    Prints a menu with a border around it.

    Args:
        title (str): The title of the menu.
        menu_items (list): A list of strings representing the menu options.
    """
    # Calculate the maximum width needed for the box, including padding
    max_length = len(title)
    for item in menu_items:
        max_length = max(max_length, len(item))

    width = max_length + 6  # 2 for vertical borders, 4 for padding
    border_line = "+" + "-" * width + "+"

    print(border_line)
    print(f"|  {title.center(width - 4)}  |")
    print(border_line)

    for item in menu_items:
        print(f"|  {item.ljust(width - 4)}  |")

    print(border_line)


def welcome_menu():
    """
    Welcome menu.
    :return: Nothing
    """

    # get current system time
    current_time = datetime.now().strftime("%H:%M")

    menu_title = "WELCOME TO MY ENCRYPTION PROGRAM"
    menu_list = [
        "Programmer: Drew Cochran",
        "Version: 0.2",
        "Date Time group",
        f"System Time: {current_time}",
        "Last updated: 16NOV2025"
    ]
    # call print_menu_in_box function
    print_menu_in_box(menu_title, menu_list)
    # sleep for 3 seconds
    sleep(2)

def main_menu():
    """
    Main menu. Prints after the welcome menu.
    :return: User choice input
    """

    title_main_menu = "Main Menu"
    menu_list = [
        "Introduction: This is the menu for the encryption and decrpytion program",
        "MENU OPTIONS",
        "1. Encrypt String or Numbers",
        "2. Encrypt a text file",
        "3. Decrypt a text file",
        "4. Encryption tracker",
        "5. Basic Instructions",
        "6. Exit program"
    ]
    # call print_menu_in_box function
    print_menu_in_box(title_main_menu, menu_list)
    # sleep for 1 seconds
    sleep(1)

    # print prompt for user choice
    user_choice = input("\nInput your choice: ")

    # if checks
    if user_choice == '1':
        print("Taking you to Encrypt a string or series of numbers service.")
        sleep(1)
    elif user_choice == '2':

        print("Taking you to encrypt a text file service.")
        sleep(1)
        menu_encrypt_file()

    elif user_choice == '3':
        print("Taking you to decrypt a text file service.")
        sleep(1)
        menu_decrypt_file()

    elif user_choice == '4':
        print("Taking you to the encryption tracker.")
        sleep(1)
    elif user_choice == '5':
        print("Taking you to the basic instructions menu.")
        sleep(1)
        basic_instructions()
    elif user_choice == '6':
        return False
    else:
        print("Invalid number choice. Please try again or press 5 to exit the program.")

def basic_instructions():
    """
    Menu for basic instructions on the program.
    :return:
    """
    instruct = "BASIC INSTRUCTIONS"
    menu_list = [
        "Welcome to my encryption program! Use this program to encrypt or decrypt a file anytime you like.",
        "If you forget what files you encrypted, make sure you choose the encryption tracking command on the main menu.",
        "You will be asked to provide a secure password of no less than 12 and no more the 20 characters.",
        "Make sure to remember your password, as it is required to decrypt your files later.",
        "You can choose to have a password randomly generated for you, or create your own.",
        "When encrypting a file, an encryption key file will be created. Keep this file safe, as it is needed to decrypt your file later.",
        "When decrypting a file, you will need to provide the name of the encrypted file and the password you used during encryption."
    ]
    # call print_menu_in_box function
    print_menu_in_box(instruct, menu_list)
    # sleep for 3 seconds
    sleep(3)
    # await user input to return
    input("Press Enter to go back to the main menu...")
    print("Taking you back to the main menu")
    sleep(1)
    return

def menu_encrypt_file():
    """
    Menu for encrypting a file. To be completed.
    :return:
    """

    menu_title = "Encrypt A File Options"
    menu_list = [
        "1. Encrypt a file",
        "2. Instructions",
        "3. Exit back to main menu"
    ]

    print("Welcome to the encrypting a file function of the program! Hope you like it.")

    user_input = None
    # while loop to ask for name of file or default choice
    while user_input != '3':
        print_menu_in_box(menu_title, menu_list)
        user_input = input("Enter your choice: ")

        # if checks
        if user_input == '1':
            # request name of file to be encrypted
            input_file = input("Enter the name of the file you wish to be encrypted. "
                               "Make sure the file is located in the current working directory.\n")
            # request name of output file from user
            output_file = input("Please specify the name for the file after it is encrypted. "
            "Press enter if you want the default as the encrypted_name_you_entered\n")
            # check if user enter a file name
            if output_file == '':
                output_file = None
            # build json payload
            json_arg = json.dumps(build_json_payload(operation="encrypt_file", input_file=input_file,
                            output_file=output_file))

            """
            USED TO BUILD THE FILE ENCRYPTION TRACKER. REMOVE THIS COMMENT LATER.
            """
            # call able.py to encrypt data
            try:
                encrypt_file = subprocess.run(['python', 'able.py', json_arg])
                print(f"Output: {encrypt_file}")

            except subprocess.CalledProcessError as e:
                print(f"Command failed with error: {e}")
                print(f"Standard Error: {e.stderr}")

        elif user_input == '2':
            instructions_encrypt_file()

        elif user_input == '3':
            break

        else:
            print("You entered an invalid choice. Please choose 1, 2, or 3.")

    return


def instructions_encrypt_file():
    """
    Instructions for how to encrypt a file. Returns nothing.
    :return:
    """
    menu_title = "INSTRUCTIONS FOR HOW TO ENCRYPT A FILE"
    menu_list = [
        "You must provide an input file to encrypt.",
        "An encryption key will be generated and saved, which will then be used "
        "to encrypt the file and identified for later use.",
        "You will be asked to provide a user password of length 12 to 20 characters, using certain"
        "allowed symbols, with at least one uppercase letter and one number\n. You can ask to have"
        "This password randomly generated. Make note of your password",
        "The file name will be outputed on screen. Take note of the name for when you wish it to "
        "be decrypted."
    ]
    print_menu_in_box(menu_title, menu_list)

    return


def menu_decrypt_file():
    """
    Menu for decrypting a file.
    :return:
    """

    title = "Decrypt A File Options"
    menu_list = [
        "1. Decrypt a file",
        "2. Instructions",
        "3. Exit back to main menu"
    ]

    print("Welcome to the decrypting a file function of the program! Lets get your data.")

    user_input = None
    # while loop to ask for name of file to be decrypted
    while user_input != '3':
        print_menu_in_box(title, menu_list)
        user_input = input("Enter your choice: ")

        # if checks
        if user_input == '1':
            # request name of file to be decrypted
            input_file = input("Enter the name of the file you want decrypted. "
                               "Make sure the file is in the current working directory.\n")

            # build json payload
            json_arg = json.dumps(build_json_payload(operation="decrypt_file", input_file=input_file))

            # call able.py to decrypt data
            try:
                decrypt_file = subprocess.run(["python", "able.py", json_arg])
                print(f"Output: {decrypt_file} was successfully decrypted.")

            except subprocess.CalledProcessError as e:
                print(f"Command failed with error: {e}")
                print(f"Standard Error: {e.stderr}")

        elif user_input == '2':
            instructions_decrypt_file()

        elif user_input == '3':
            break

        else:
            print("You entered an invalid choice. Please choos 1, 2, or 3.")

    return


def instructions_decrypt_file():
    """
    Instructions on how to decrypt a file.
    :return:
    """
    title = "INSTRUCTIONS ON HOW TO DECRYPT A FILE"
    menu_list = [
        "You will be asked to provide your password which you either randomly generated or "
        "created yourself",
        "The password will be used to first decrypt the key file, then the information in "
        "the key file will be used to decrypt the file itself.",
        "You need to remember the encrypted output file name, whether it was one"
        "you created or the default 'encrypted_(input_file_name)'."
    ]
    print_menu_in_box(title, menu_list)

    return


def build_json_payload(operation, input_file=None, output_file=None, message=None):
    """
    Takes the inputs for the JSON output payload, creates the JSON, and returns it.
    :return: JSON payload for use later
    """
    # build the json payload
    payload = {
        "input_file" : input_file,
        "output_file" : output_file,
        "operation" : operation,
        "message" : message
    }

    return payload


# main function
if __name__ == '__main__':
    # call welcome_menu function
    welcome_menu()

    # while loop to continue awaiting correct user choice
    menu_call = True
    while menu_call is not False:
        menu_call = main_menu()

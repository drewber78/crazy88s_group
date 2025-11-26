"""
Uses random_pw.py to generate a password or check_pwd.py to ensure a password
meets criteria.
For CS361 Software Engineering I project.
"""


import sys
import getpass
import subprocess


class GeneratePassword:
    """
    Class to generate a password using random_pw.py
    """

    def __init__(self, length):
        """
        Init for class.
        :param length: length of password to be generated
        """
        self.length = length

    def create_password(self):
        """
        Calls random_pw.py to generate a password of specified length.
        :return: generated password string
        """
        try:
            result = subprocess.run(
                ['python', 'random_pw.py', str(self.length), '-microservice'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error generating password: {e}")
            return None

    def check_password(self, user_password):
        """"
        Method which calls check_pwd.py to check if the user entered password
        meets complexity requirements.
        """
        try:
            result = subprocess.run(
                ['python', 'check_pwd.py', user_password],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error checking password: {e}")
            return None


class MenuMicroservice:
    def microservice_menu(self):
        """
        Creates a menu for the microservice password generation class.
        Uses method print_menu_in_box to print the menu.
        """
        symbols = '~`!@#$%^&*()_+-='
        title = "PASSWORD GENERATION MICROSERVICE"
        menu_list = [
            "This microservice generates a random password of user-defined"
            " length.",
            f"It will also check if a user-defined password meets complexity"
            f" requirements of length 12-20 characters, with at least one "
            f"upper, one lower, one digit, and one special character of "
            f"{symbols}.",
            "Please choose one of the following options:",
            "1. Generate a random password",
            "2. Check a password for complexity requirements",
            "3. Exit"
        ]

        print_menu_in_box(title, menu_list)


def json_builder(user_password=None, length=None, complexity_result=None):
    """
    Builds a json structure to return to a calling program.
    """
    # Return an empty JSON structure by default; modify as needed.
    payload = {
        "password": user_password,
        "length": length,
        "complexity_result": complexity_result}

    return payload


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


def main():
    """"
    Main function call and determination tree for microservice.
    """
    menu = MenuMicroservice()
    menu.microservice_menu()

    while True:
        user_choice = input("Enter your choice (1-3): ").strip()

        if user_choice == '1':
            length_input = input(
                "Enter desired password length (12-20): ").strip()
            try:
                length = int(length_input)
                if length < 8 or length > 20:
                    print("Length must be between 8 and 20.")
                    continue
            except ValueError:
                print("Please enter a valid integer for length.")
                continue

            generator = GeneratePassword(length)
            password = generator.create_password()
            if password:
                print(f"Save your new password: {password}\n"
                      "in a safe place!")

        elif user_choice == '2':
            user_password = getpass.getpass(
                "Enter the password to check: ").strip()
            checker = GeneratePassword(0)  # Length not needed for checking
            result = checker.check_password(user_password)
            if result == 'True':
                print("Password meets complexity requirements.")
            else:
                print("Password does NOT meet complexity requirements.")

        elif user_choice == '3':
            print("Exiting microservice.")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    # check sys.argv for microservice call
    if sys.argv[1] == "-microservice":
        # check if sys.argv[2] is present
        check_arg = sys.argv[2]

        if isinstance(check_arg, str):
            if check_arg.isdigit():
                try:
                    length = sys.argv[2]
                    generator = GeneratePassword(length)
                    password = generator.create_password()
                    print(password)
                except FileNotFoundError:
                    print("random_pw.py file not found.")
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                try:
                    user_password = sys.argv[2]
                    checker = GeneratePassword(0)
                    result = checker.check_password(user_password)
                    print(result)

                except ValueError:
                    print("Only integer lengths are acceptable for password"
                          " generation.")
                except IndexError:
                    print("Please provide a length for password generation or "
                          "a password to check.")
                    sys.exit(1)
                except Exception as e:
                    print(f"An error occurred: {e}")
                    sys.exit(1)

    else:
        main()

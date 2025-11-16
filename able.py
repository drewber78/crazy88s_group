"""
File which will do the actual encryption and decryption.
"""
import random
import time
import os
import subprocess
from time import sleep
from cryptography.fernet import Fernet
import sys
import json
import getpass


class EncryptDecrypt:
    """
    Class which encrypts and decrypts files and messages.
    """
    # init function
    def __init__(self):
        # init variables
        self.created_key = None
        self.input_file = None
        self.output_file = None
        self.message = None
        self.key_loaded = None
        self.directory_key = "stored_keys"
        self.file_key = "stored.key"
        self.key_file_path = None

    def get_created_key(self):
        """
        Get function to get the currently generated key.
        :return: self.created_key
        """
        return self.created_key

    def get_load_key(self):
        """
        Get function to return self.load_key
        :return: self.load_key
        """
        return self.load_key

    def generate_key(self):
        """
        Function to generate fernet key and return it to the calling function.
        :return:
        """
        self.created_key = Fernet.generate_key()

        # check if directory for keys is already present
        if not os.path.isdir(self.directory_key):
            os.mkdir(self.directory_key)
        # # create key file path
        # self.file_key = os.path.join()
        # self.key_file_path = os.path.join(self.directory_key, self.file_key)
        # try:
        #     # open the file to store key
        #     with open(os.getcwd() + '/' + self.key_file_path, "wb") as key_file:
        #         key_file.write(self.created_key)
        #     print(f"Created file '{self.key_file_path}' and wrote key to it.")
        #     sleep(3)
        # except OSError.filename as d:
        #     print(d)
        # except Exception as e:
        #     print(f"An error occurred: {e}")
        # finally:
        #     key_file.close()
        return

    def load_key(self, input_file):
        """
        Loads the key from the file where the key is stored. Raises error is file is not found. Stores the loaded
        key in self.load_key variable
        :return: Nothing
        """
        # ask user for password to use for decryption
        user_pwd = getpass.getpass("Enter the password used to encrypt the key file: ")

        # build json payload
        data = {
            "input_file" : input_file,
            "password" : user_pwd,
            "operation" : "decrypt_file",
            "directory" : self.directory_key
        }
        json_data = json.dumps(data)

        # try to run baker.py to decrypt key file
        try:
            result_json = subprocess.run(["python", "baker.py", json_data],
                                         capture_output=True, text=True)
            if result_json.stderr:
                print(f"Error: {result_json.stderr}")
        except TimeoutError:
            print("The file baker.py timed out.")
        except FileExistsError:
            print("The file baker.py does not exist. Please ensure it is in the current working directory.")

        stdout_result = result_json.stdout.strip()
        parsed = json.loads(stdout_result)
        return parsed

    def message_encrypt(self, message):
        """
        Accepts in a message that needs to be encrypted and encrypts for later decryption.
        :param message: Message user wishes to have encrypted. Can be a string or numbers
        :return: the encrypted message
        """
        # load the key into self.key_loaded variable
        self.load_key()
        # create fernet object using key_loaded
        fernet = Fernet(self.key_loaded)
        # encrypt the message
        encrypted = fernet.encrypt(message.encode())
        # display the encrypted message
        print("Encrypted message: ", encrypted)
        return encrypted, self.load_key()

    def message_decrypt(self, encrypted_message):
        """
        Decrypts a message using the key saved
        :param encrypted_message:
        :return: decrypted_message
        """
        # load the key into self.key_loaded variable
        self.load_key()
        # create fernet object
        fernet = Fernet(self.key_loaded)
        # create decrypted_message variable with the encrypted_message now decrypted
        decrypted_message = fernet.decrypt(encrypted_message).decode()
        # display encrypted message
        print("Decrypted message: ", decrypted_message)
        return decrypted_message

    def encrypt_file(self, input_file, output_file = None):
        """
        Reads and encrypts a file. Requests user provide a name for the decrypted file or, by default,
        adds .encrypted at the end. Stores name of output file in self.output_file for use later
        :param input_file: User specified name of file to encrypt WITH EXTENSION
        :param output_file: User specified name of the encrypted file. If no information passed, output_file is named
                        input_file.encrypted
        :return: self.output_file
        """

        print("Encrypting the key file.")
        # load the key
        # self.load_key()
        # create Fernet object
        fernet = Fernet(self.created_key)
        # create timestamp
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
        # try except finally
        try:
            with open(input_file, "rb") as f_read:
                # data variable
                data = f_read.read()
            # close the file
            f_read.close()
            # encrypt the data
            encrypted_data = fernet.encrypt(data)
            # check if output_file is None
            if output_file is None:
                output_file = 'encrypted_' + input_file
            # open output_file
            with open(output_file, "wb") as f_write:
                f_write.write(encrypted_data)

            print(f"File '{input_file}' encrypted as '{output_file}'")
        except FileExistsError:
            print(f"The file '{output_file}' already exists.")
        except FileNotFoundError:
            print(f"The file '{input_file}' was not found")
        except OSError as d:
            print(f"{d}")
        except Exception as e:
            print(f"{e}")
        finally:
            f_write.close()

        return output_file, timestamp, self.created_key

    def decrypt_file(self, parameters, output_file = None):
        """
        Decrypts a user provided file named encrypted_file and outputs to an optionally provided name by the user.
        If no output_file name is provided by the user, the name is encrypted_file.decrypted.
        :param parameters: JSON data provide from user_menu.py; contains file name to decrypt
        :param output_file: optionally provided by user. defaults to encrypted_file.decrypted
        :return: out_file, the name of it
        """

        print("Decrypting the key file.")

        # load the key
        result_json = self.load_key(parameters.get("input_file"))
        # result_json = json.loads(result)
        # pull Fernet key from result_json
        self.key_loaded = result_json["key"]
        # create Fernet object
        fernet = Fernet(self.key_loaded)
        # try except finally
        try:
            with open(parameters.get("input_file"), "rb") as f_read:
                encrypted_data = f_read.read()
            # close the file
            f_read.close()
            # decrypt the data
            decrypted_data = fernet.decrypt(encrypted_data)
            # check if output_file is None
            if output_file is None:
                output_file = input(f"Enter the name for the decrypted output file you want. Include the extension:\n" \
                f"Press Enter to use default name of {parameters.get('input_file') + '.decrypted'}\n")
                if output_file == '':
                    output_file = parameters.get("input_file") + ".decrypted"
            # open output file
            with open(output_file, "wb") as f_write:
                f_write.write(decrypted_data)
            print(f"The file '{parameters.get('input_file')}' was decrypted as '{output_file}'")
        except FileExistsError:
            print(f"The file '{output_file}' already exists")
        except FileNotFoundError:
            print(f"The file '{parameters.get('input_file')}' was not found")
        except OSError as d:
            print(f"{d}")
        except Exception as e:
            print(f"{e}")
        finally:
            f_write.close()

        return output_file

    def menu_user_password(self):
        """
        Requests user to enter a password of length 12 to 20 with special characters. If user wants a randomly
        generated password, calls on random_pw.py to generate a random password. Uses check_pwd.py to check for
        password complexity requirements.
        :return: user_password
        """
        symbols = '~`!@#$%^&*()_+-='
        # while menu loop
        while True:
            print("Now you need to enter a password to encrypt the key storage file with your file name and key"
                  " in it\n")
            user_input = getpass.getpass(f"Please enter a password 12 to 20 characters long.\n"
                               f"The password must contain at least one of the following symbols: {symbols}\n"
                               f"The password must contain at least one number and one uppercase letter.\n"
                               f"If you would like a random password generated, press Enter only.\n")

            # if checks
            if user_input == '':
                try:
                    random_num = random.randint(12, 20)
                    result = subprocess.check_output(["python", "random_pw.py", 
                                                      str(random_num)]).decode().strip()

                    user_pwd = result
                    print(f"The generated password is: {user_pwd}")
                    input("Remember your password and keep in a safe place. Press enter to continue.")
                    break
                except FileNotFoundError as e:
                    print(f"Error: {e}")
                    print("The file random_pw.py was not found.")
                except subprocess.TimeoutExpired:
                    print("Error: the script took too long to run and was terminated.")
                except Exception as e:
                    print(f"{e}")

            # user input their own password
            else:
                try:
                    result = subprocess.run(["python", "check_pwd.py", user_input],
                            capture_output=True,
                            text=True)
                    # if checks
                    if result.stdout.strip() == 'False':
                        print(f"Your password {user_input} was not complex enough. Try again or "
                              f"press Enter for a random password.\n")
                    else:
                        user_pwd = user_input
                        print(f"You entered the following pw: {user_pwd}")
                        input("Remember your password and keep in a safe place. Press enter to continue.")
                        break

                except FileNotFoundError as e:
                    print(f"Error: {e}")
                    print("The file random_pw.py was not found.")
                except subprocess.TimeoutExpired:
                    print("Error: the script took too long to run and was terminated.")
                except Exception as e:
                    print(f"{e}")

        return user_pwd


def json_payload_builder(timestamp = None, user_password = None, key = None, file_name = None, operation = None):
    """
    Builds a JSON payload to send to baker.py for encryption and to be used with the encryption tracker function.
    :param user_password: User provided password to encrypt the file
    :param key: self.created_key from EncryptDecrypt class
    :param timestamp: timestamp for when the file was encrypted
    :param file_name: user defined output file_name; default is encrypted_(input_file_name)
    :param operation: Operation to be performed.
    :return: JSON payload
    """

    payload = {
        "id" : timestamp,
        "password" : user_password,
        "key" : key,
        "file_name" : file_name,
        "operation" : operation
    }

    json_arg = json.dumps(payload)

    return json_arg


def main():
    if len(sys.argv) < 2:
        print("Usage: python able.py '<json_string>'")
        sys.exit(1)

    # establish result variable
    result = None

    # parse the json arg
    json_arg = sys.argv[1]
    try:
        parameters = json.loads(json_arg)
    except json.JSONDecodeError:
        print("Invalid JSON input")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"The type of error was: {type(e)}")

    # extract parameters
    operation = parameters.get("operation")

    # initiate class
    ed = EncryptDecrypt()

    # check which operation to perform
    if operation == "encrypt_file":
        try:
            ed.generate_key()
            output_file, timestamp, key = ed.encrypt_file(parameters.get("input_file"), parameters.get("output_file"))
            user_password = ed.menu_user_password()
            package_json = json_payload_builder(timestamp, user_password, key.decode(), output_file, operation)
            encrypt_key_file = subprocess.check_output(["python", "baker.py", package_json]).decode().strip()
            print(f"Encrypted {encrypt_key_file}")
            return encrypt_key_file
        except KeyError:
            print("Missing relevant key in JSON data.")
        except TimeoutError:
            print("The file baker.py timed out.")



    elif operation == "decrypt_file":
        result = ed.decrypt_file(parameters)
        return result


    # elif operation == "message_encrypt":
    #     message = parameters.get("message")
    #     ed.message_encrypt(message)
    # elif operation == "message_decrypt":
    #     decrypt_message = parameters.get("")

    # try:
    #     if os.path.exists(ed.key_file_path):
    #         os.remove(ed.key_file_path)
    # except FileNotFoundError as e:
    #     print(f"File '{ed.key_file_path}' does not exist.")
    #     print(f"Error found {e}")

    return result


def print_menu_in_box(self, title, menu_items):
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

# main function
if __name__ == '__main__':
    main()
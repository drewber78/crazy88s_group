"""
File which encrypts the Fernet key, output file name, and timestamp information.
"""

import time
import os
from time import sleep
import sys
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


# class KeySecurity:
#     """
#     Class which encrypts the key, file output name, and timestamp for the user's security. Returns the file name
#     under which this tracking info is created. Uses json packaging to find the main key, which is the output
#     file's name which the user wished to encrypt.
#     """
#     def __init__(self, output_file, timestamp=None, key=None, user_pwd=None):
#         """
#         Init for class.
#         :param output_file: User defined output file where the encrypted data is saved
#         :param timestamp: timestamp when the encryption occurred
#         :param key: Fernet key that was generated to encrypt the file
#         :param user_pwd: user defined password used to actually encrypt the file
#         """
#         self.output_file = output_file
#         self. timestamp = timestamp
#         self.key = key
#         self.user_pwd = user_pwd
#
#
#     def

def derive_key(password, salt):
    """
    Derives a secure key from the user_pwd parameter
    :param password:
    :param salt:
    :return: secure key to encrypt the Fernet key
    """
    kdf = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def save_encrypted_key(parameters, json_arg):
    """
    Encrypts the json_arg storing the key and output file name

    :param parameters: key encryption file name based on output file name. Adds "key_" to the front of the file
    :param json_arg: passed json structure when baker.py was opened
    :return: successful notification of encryption of key file.
    """

    # derive encryption from password
    salt = os.urandom(16)
    derived_key = derive_key(parameters.get("password"), salt)
    fernet = Fernet(derived_key)

    # encrypted key filename output
    key_output_filename = "key_" + parameters.get("file_name")

    parameters.update({"operation": None})
    json_arg = json.dumps(parameters)

    # encrypt the json data
    encrypted_data = fernet.encrypt(json_arg.encode())

    # open file and write encrypted json_arg data to it
    try:
        with open(key_output_filename, "wb") as file:
            file.write(salt + encrypted_data)
        print(f"Associated key file to output file {parameters.get("file_name")} saved as {key_output_filename}.")
    except FileExistsError as e:
        print(f"File Exists already.")
        print(f"{e}")
    finally:
        file.close()

    return key_output_filename

def load_encrypted_key(parameters):
    """
    Loads the encrypted key JSON data and returns it for decrypting a file.
    :param parameters: json parameters
    :return:
    """
    # attempt to create file name to open
    key_filename = "key_" + parameters.get("input_file")
    # current_working_directory = os.getcwd()
    # path = os.path.join(current_working_directory, parameters.get("directory"))
    try:
        # os.chdir(path)
        with open(key_filename, "rb") as file:
            data = file.read()

    except FileNotFoundError as e:
        print("File is not found.")
        print(f"{e}")
    except NotADirectoryError:
        print(f"Directory {parameters.get("directory")} does not exist.")

    finally:
        file.close()

    # extract data from read file
    salt = data[:16]
    encrypted_data = data[16:]

    # derive the key using password and salt
    derived_key = derive_key(parameters.get("password"), salt)
    fernet = Fernet(derived_key)

    # decrypt the JSON
    decrypted_json = fernet.decrypt(encrypted_data).decode()
    parsed = json.loads(decrypted_json)

    return parsed


def main():
    if len(sys.argv) < 2:
        print("Usage: python able.py '<json_string>'")
        sys.exit(1)

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

    # extract parameter operation
    operation = parameters.get("operation")

    if operation == "encrypt_file":
        
        sleep(1)
        result = save_encrypted_key(parameters, json_arg)
        return result

    if operation == "decrypt_file":
        
        sleep(1)
        result = load_encrypted_key(parameters)
        return result


# main function
if __name__ == '__main__':
    result = main()
    print(json.dumps(result))

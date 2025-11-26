"""
Generates a random password and returns it to the calling function.
"""

import random
import string
import sys


def generate_password(length):
    # if length < 8 or length > 20:
    #     raise ValueError("Password length must be between 8 and 20
    # characters.")

    # Character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = "~`!@#$%^&*()_+-=."

    # Ensure at least one of each required type
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special_chars)
    ]

    # Fill the rest with random choices from all sets combined
    all_chars = lowercase + uppercase + digits + special_chars
    password += random.choices(all_chars, k=length - 4)

    # Shuffle to avoid predictable positions
    random.shuffle(password)

    return ''.join(password)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        if sys.argv[2] == "-microservice":
            length = int(sys.argv[1])
            result = generate_password(length)
            cleaned_result = result.strip()
            print(cleaned_result)
            sys.exit(0)
        try:
            length = int(sys.argv[1])
            result = generate_password(length)
        except ValueError:
            print("Please provide a valid integer for password length.")
            sys.exit(1)
    else:
        length = int(sys.argv[1])
        result = generate_password(length)
        try:
            with open("generated_password.txt", "w") as f:
                f.write(result)
        except IOError as e:
            print(f"Error writing to file: {e}")
        finally:
            f.close()
            print(result)

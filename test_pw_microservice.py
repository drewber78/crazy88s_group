import unittest
import random
import subprocess
import time


class TestPWMicroservice(unittest.TestCase):
    def test_01_create_password_length_and_complexity(self):
        sequence_length = [12, 13, 14, 15, 16, 17, 18, 19, 20]
        loop_length = random.randint(1, 10)
        print(f"Loop length: {loop_length}")

        for i in range(loop_length):
            print(f"\nIteration: {i + 1}")
            length = str(random.choice(sequence_length))
            generate = subprocess.run(['python', 'pw_microservice.py',
                        '-microservice', length], 
                        capture_output=True, check=True)
            pwd = generate.stdout.decode().strip()
            self.assertIsInstance(pwd, str)
            self.assertEqual(len(pwd), int(length))
            # must contain at least one lowercase, uppercase, digit, and
            # special
            self.assertRegex(pwd, r"[a-z]")
            self.assertRegex(pwd, r"[A-Z]")
            self.assertRegex(pwd, r"[0-9]")
            self.assertRegex(pwd, r"[~`!@#$%^&*()_+\-=\.]")
            print(pwd)
            time.sleep(1)
        print("\n")
        time.sleep(1)

    def test_02_check_password_valid(self):
        # a known-good password (12 chars, has upper, lower, digit, special)
        good = "Abcdef1!2345"
        result = subprocess.run(['python', 'pw_microservice.py',
                                 '-microservice', good],
                                 capture_output=True, check=True)
        cleaned_result = result.stdout.decode().strip()
        print(f"Good password: {good} = {cleaned_result}")
        # pw_microservice returns subprocess stdout as 'True'/'False'
        # check_pwd prints True/False, so expect 'True'
        self.assertIn(cleaned_result, ("True", "False"))
        self.assertEqual(cleaned_result, "True")
        print("\n")
        time.sleep(2)

    def test_03_check_password_invalid(self):
        bad = "short1!A"  # too short
        result = subprocess.run(['python', 'pw_microservice.py',
                                 '-microservice', bad],
                                 capture_output=True, check=True)
        cleaned_result = result.stdout.decode().strip()
        print(f"Bad password: {bad} = {cleaned_result}")
        self.assertIn(cleaned_result, ("True", "False"))
        self.assertEqual(cleaned_result, "False")
        print("\n")
        time.sleep(2)

    def test_04_generate_length_11_and_check_fails(self):
        gen_pwd = subprocess.run(['python', 'pw_microservice.py',
                         '-microservice', '11'],
                         capture_output=True, check=True)
        pwd = gen_pwd.stdout.decode().strip()
        print(f"Generated pwd length {len(pwd)}: {pwd}")
        self.assertIsInstance(pwd, str)
        self.assertEqual(len(pwd), 11)
        # generated 11-char password should fail complexity (length < 12)
        result = subprocess.run(['python', 'pw_microservice.py',
                                 '-microservice', pwd],
                                 capture_output=True, check=True)
        clean_result = result.stdout.decode().strip()
        print(f"Result of check if generated password {pwd} "
              f"is valid: {clean_result}")
        self.assertIn(clean_result, ("True", "False"))
        self.assertEqual(clean_result, "False")
        print("\n")
        time.sleep(2)

    def test_05_generate_length_21_and_check_fails(self):
        gen_pwd = subprocess.run(['python', 'pw_microservice.py',
                         '-microservice', '21'],
                         capture_output=True, check=True)
        pwd = gen_pwd.stdout.decode().strip()
        print(f"Generated pwd length {len(pwd)}: {pwd}")
        self.assertIsInstance(pwd, str)
        self.assertEqual(len(pwd), 21)
        # generated 21-char password should fail complexity (length > 20)
        result = subprocess.run(['python', 'pw_microservice.py',
                                 '-microservice', pwd],
                                 capture_output=True, check=True)
        clean_result = result.stdout.decode().strip()
        print(f"Result of check if generated password {pwd} "
              f"is valid: {clean_result}")
        self.assertIn(clean_result, ("True", "False"))
        self.assertEqual(clean_result, "False")
        print("\n")
        time.sleep(2)

    def test_06_check_password_too_long(self):
        # construct a 21-char password that otherwise meets complexity
        too_long = "A" * 18 + "a1!"  # 21-char password
        print(f"Password length {len(too_long)} for pwd {too_long}")
        result = subprocess.run(['python', 'pw_microservice.py',
                                 '-microservice', too_long],
                                 capture_output=True, check=True)
        cleaned_result = result.stdout.decode().strip()
        print(f"Too_long password: {too_long} = {cleaned_result}")
        self.assertIn(cleaned_result, ("True", "False"))
        self.assertEqual(cleaned_result, "False")
        print("\n")
        # time.sleep(2)


if __name__ == "__main__":
    unittest.main()

import re
import unittest

class DataValidator:
    def email(self, data):
        # Checks weather the email is valid
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,}|(?:\d{1,3}\.){3}\d{1,3})$'
        return bool(re.fullmatch(pattern, data))


    def phone(self, data):
        # Checks weather the number is a valid UK phone number
        pattern = r'^(((\+44\s?\d{4}|\(?0\d{4}\)?)\s?\d{3}\s?\d{3})|((\+44\s?\d{3}|\(?0\d{3}\)?)\s?\d{3}\s?\d{4})|((\+44\s?\d{2}|\(?0\d{2}\)?)\s?\d{4}\s?\d{4}))(\s?\#(\d{4}|\d{3}))?$'
        return bool(re.fullmatch(pattern, data))


    def name(self, data):
        pattern = r'^[a-zA-Z]+(?:[ -][a-zA-Z]+)*$'
        return bool(re.fullmatch(pattern, data))


    def username(self, data):
        # 1 letter from first name
        # 4 letter from second name
        # 2 random numbers at end
        # length of name == 7
        pattern = r'^[a-zA-Z0-9]+$'
        return len(data) == 7 and bool(re.fullmatch(pattern, data))


    def birthdate(self, data):
        if re.match(r'^\d{4}-\d{2}-\d{2}$', data) and 1900 < int(data[:4]) < 2020 and 0 < int(data[5:7]) < 13 and 0 < int(data[8:10]) < 32:
            return True
        return False
    
    def date(self, data):
        if re.match(r'^\d{4}-\d{2}-\d{2}$', data) and 0 < int(data[5:7]) < 13 and 0 < int(data[8:10]) < 32:
            return True
        return False


    def age(self, data):
        if re.match(r'^[0-9]+$', data) and 0 < int(data) < 150:
            return True
        return False


    def length_check(self, data, length, option):
        if option == 'min':
            if len(data) >= length:
                return True
        elif option == 'max':
            if len(data) <= length:
                return True
        elif option == 'equal':
            if len(data) == length:
                return True
        return False

class TestValidator(unittest.TestCase):
    def setUp(self):
        # Create an instance of the DataValidator class to test data validation
        self.validator = DataValidator()

    def test_valid_email(self):
        # Valid emails
        valid_emails = [
        'user@example.com',
        'email@example.co.jp',
        'firstname-lastname@example.com',
        'email@example.museum',
        'email@example.name',
        '_______@example.com',
        '1234567890@example.com',
        'email@123.123.123.123'
        ]

        for email in valid_emails:
            # Tests valid emails
            self.assertTrue(self.validator.email(email))


    def test_invalid_email(self):
        # Invalid emails
        invalid_emails = [
        'plainaddress',
        '@example.com',
        'email@',
        'email@.com',
        'email@'
        ]

        for email in invalid_emails:
            # Tests invalid emails
            self.assertFalse(self.validator.email(email))


    def test_valid_phone(self):
        # Valid phone numbers
        valid_phones = [
        '+44 7975 556677',
        '07947674716',
        '020 7946 0716',
        '02079460716',
        '07975 556677'
]

        for phone in valid_phones:
            # Tests valid phone numbers
            self.assertTrue(self.validator.phone(phone))


    def test_invalid_phone(self):
        # Invalid phone numbers
        invalid_phones = [
        '1234567890',
        '1234',
        '12345678901234567890',
        '1234567890',
        '+1234567890',
        '+44 1234 56789'
]

        for phone in invalid_phones:
            # Tests invalid phone numbers
            self.assertFalse(self.validator.phone(phone))


    def test_valid_names(self):
        # Valid names
        valid_names = [
        'Preston',
        'Ahmed',
        'Elyas Chaal',
        'Hugh Janus',
        'John Smith',
        'Preston Leighton Tony Shaun Whiteman',
        'AJ',
        'BBG'
        ]

        for name in valid_names:
            self.assertTrue(self.validator.name(name))


    def test_invalid_names(self):
        # Invalid names
        invalid_names = [
        'Ely4s',
        'pestopasta74',
        'Mama-dan',
        '#Karim'
]

        for name in invalid_names:
            self.assertFalse(self.validator.name(name))


    def test_valid_usernames(self):
        valid_usernames = [
        'EChaa23',
        'AChaa23',
        'Utest54',
        'Uname69',
        'HOsbo65',
        'Ksoli96'
]
        for username in valid_usernames:
            self.assertTrue(self.validator.username(username))


    def test_invalid_usernames(self):
        # Invalid usernames
        invalid_usernames = [
        'username@',
        'user-name',
        'username',
        'user-name',
        'user_name',
        '123@abc'
]

        for username in invalid_usernames:
            self.assertFalse(self.validator.username(username))


    def test_valid_birthdate(self):
        # Valid birthdates
        valid_birthdates = [
        '2000-01-01',
        '1990-12-31',
        '1990-01-01',
        '2000-12-31',
        '2007-05-21'
        ]

        for birthdate in valid_birthdates:
            self.assertTrue(self.validator.birthdate(birthdate))


    def test_invalid_birthdate(self):
        # Invalid birthdates
        invalid_birthdates = [
        '2000-01-32',
        '1990-12-32',
        '1990-00-01',
        '2000-13-31',
        '2007-05-32'
        ]

        for birthdate in invalid_birthdates:
            self.assertFalse(self.validator.birthdate(birthdate))

if __name__ == '__main__':
    unittest.main()

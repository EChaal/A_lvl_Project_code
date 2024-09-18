import re
class DataValidator:

    def is_integer(self, data):
        return isinstance(data, int)

    def is_string(self, data):
        return isinstance(data, str)

    def is_float(self, data):
        return isinstance(data, float)

    def is_non_empty_string(self, data):
        return isinstance(data, str) and bool(data.strip())

    def is_positive_number(self, data):
        return isinstance(data, (int, float)) and data > 0

    def is_in_range(self, min_value, max_value, data):
        if isinstance(data, (int, float)):
            return min_value <= data <= max_value
        return False

    def email(self, data):
        # Checks weather the email is valid
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,}|(?:\d{1,3}\.){3}\d{1,3})$'
        return bool(re.fullmatch(pattern, data))

    def is_valid_username(self, data):
        pattern = r'^[a-zA-Z]{5}\d{2}$'
        return len(data) == 7 and bool(re.fullmatch(pattern, data))

    def birthdate(self, data):
        if re.match(r'^\d{4}-\d{2}-\d{2}$', data) and 1900 < int(data[:4]) < 2020 and 0 < int(data[5:7]) < 13 and 0 < int(data[8:10]) < 32:
            return True
        return False

    def date(self, data):
        if re.match(r'^\d{4}-\d{2}-\d{2}$', data) and 0 < int(data[5:7]) < 13 and 0 < int(data[8:10]) < 32:
            return True
        return False

    def birthdate(self, data):
        if re.match(r'^\d{4}-\d{2}-\d{2}$', data) and 1900 < int(data[:4]) < 2020 and 0 < int(data[5:7]) < 13 and 0 < int(data[8:10]) < 32:
            return True
        return False

    def date(self, data):
        if re.match(r'^\d{4}-\d{2}-\d{2}$', data) and 0 < int(data[5:7]) < 13 and 0 < int(data[8:10]) < 32:
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
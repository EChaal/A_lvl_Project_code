import re
from datetime import datetime

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
        return isinstance(data, (int, float)) and data >= 0  # Allow zero as well

    def is_in_range(self, min_value, max_value, data):
        return isinstance(data, (int, float)) and min_value <= data <= max_value

    def is_valid_email(self, data):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.fullmatch(pattern, data))

    def is_valid_username(self, data):
        pattern = r'^[a-zA-Z]{5}\d{2}$'
        return len(data) == 7 and bool(re.fullmatch(pattern, data))

    def birthdate(self, data):
        if re.match(r'^\d{4}-\d{2}-\d{2}$', data):
            year, month, day = map(int, data.split('-'))
            return 1900 < year < 2020 and 1 <= month <= 12 and 1 <= day <= 31
        return False

    def date(self, data):
        if re.match(r'^\d{4}-\d{2}-\d{2}$', data):
            year, month, day = map(int, data.split('-'))
            return 1 <= month <= 12 and 1 <= day <= 31
        return False

    def length_check(self, data, length, option):
        data_len = len(data)
        if option == 'min':
            return data_len >= length
        elif option == 'max':
            return data_len <= length
        elif option == 'equal':
            return data_len == length
        return False

    def is_valid_phone_number(self, data):
        pattern = r'^(?:\+44|07)\d{9,10}$'
        return bool(re.fullmatch(pattern, data))

    def in_future(self, data):
        # data is given as a string in the format YYYY-MM-DD
        month, day, year = map(int, data.split('-'))
        today = datetime.today()
        return datetime(year, month, day) > today
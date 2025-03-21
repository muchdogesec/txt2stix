import re

import phonenumbers
from ..base_extractor import BaseExtractor


class PhoneNumberExtractor(BaseExtractor):
    """
    A class for extracting phone numbers from text using a regular expression.

    Attributes:
        name (str): The name of the extractor, set to "phone_number".
        extraction_regex (str): The regular expression pattern used for extracting phone numbers from the text.
    """

    name = "pattern_phone_number"
    extraction_regex = r'((\+|00)\d{1,3}[ \-]?\d{1,5}[ \-]?\d{1,5}[ \-]?\d{1,5})'

    @staticmethod
    def validate_phone_number(regex, phone_number):
        match = re.fullmatch(regex, phone_number)
        return match

    @staticmethod
    def filter_function(input_string):
        input_string = input_string.replace(" ", "")
        if len(input_string) >= 15 or len(input_string) <= 7:
            return False
        return PhoneNumberExtractor.parse_phone_number(input_string)
    
    @staticmethod
    def parse_phone_number(phone_number: str):
        try:
            phone_number = '+' + phone_number.replace(' ', '').removeprefix('00').removeprefix('+')
            phone = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(phone):
                return None
            return phone
        except:
            return None


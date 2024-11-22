import re
from ..base_extractor import BaseExtractor


class PhoneNumberExtractor(BaseExtractor):
    """
    A class for extracting phone numbers from text using a regular expression.

    Attributes:
        name (str): The name of the extractor, set to "phone_number".
        extraction_regex (str): The regular expression pattern used for extracting phone numbers from the text.
    """

    name = "pattern_phone_number"
    extraction_regex = r'((\+|00)\d{1,3}\s?\d{1,4}\s?\d{1,4}\s?\d{1,4})'

    @staticmethod
    def validate_phone_number(regex, phone_number):
        match = re.fullmatch(regex, phone_number)
        return match

    @staticmethod
    def filter_function(input_string):
        input_string = input_string.replace(" ", "")
        pattern = re.compile(r"(\+\d{1,3})?\s?\(?\d{1,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{4}")
        if len(input_string) >= 15 or len(input_string) <= 7:
            return False
        return PhoneNumberExtractor.validate_phone_number(pattern, input_string)


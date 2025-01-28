from ..base_extractor import BaseExtractor
from ..helper import TLDs


class EmailAddressExtractor(BaseExtractor):
    """
    A class for extracting valid email addresses from text using a custom extraction function.

    Attributes:
        name (str): The name of the extractor, set to "email".
        extraction_regex (function): The custom extraction function to validate and extract email addresses.
    """
    name = "pattern_email_address"
    extraction_regex = r'[\w.+-]+@[\w-]+\.[\w.-]+'

    @staticmethod
    def filter_function(email):
        x = email.split("@")
        domain = x[-1].split(".")[-1]
        if domain in TLDs:
            return True

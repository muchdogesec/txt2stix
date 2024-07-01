from validators import iban
from ..base_extractor import BaseExtractor


class IBANExtractor(BaseExtractor):
    """
    A class for extracting International Bank Account Number (IBAN) codes from text using a custom extraction function.

    Attributes:
        name (str): The name of the extractor, set to "IBAN".
        extraction_function (function): The custom extraction function to validate and extract IBAN codes.
    """

    name = "pattern_iban_number"
    extraction_function = lambda x: iban(x)

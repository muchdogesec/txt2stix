from ..base_extractor import BaseExtractor

class MacAddressExtractor(BaseExtractor):
    """
    A class for extracting MAC addresses from text using a regular expression.

    Attributes:
        name (str): The name of the extractor, set to "mac_address".
        extraction_regex (str): The regular expression pattern used for extracting MAC addresses from the text.
    """

    name = "pattern_mac_address"
    extraction_regex = r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})'

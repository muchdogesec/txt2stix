from ..base_extractor import BaseExtractor


class CPEExtractor(BaseExtractor):
    """
    A class for extracting Common Platform Enumeration (CPE) strings from text using a custom extraction function.

    Attributes:
        name (str): The name of the extractor, set to "cpe".
        extraction_function (function): The custom extraction function to validate and extract CPE strings.
    """

    name = "pattern_cpe_uri"
    extraction_function = lambda x: CPEExtractor.is_valid_cpe(x)

    @staticmethod
    def is_valid_cpe(cpe_string):
        """
        Custom extraction function to validate if the provided string is a valid CPE string.

        Args:
            cpe_string (str): The string to be checked.

        Returns:
            bool: True if the CPE string is valid, False otherwise.
        """

        if cpe_string.startswith('cpe:') and cpe_string.count(':') == 12:
            return True

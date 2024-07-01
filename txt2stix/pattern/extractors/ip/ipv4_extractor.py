import re
from ..base_extractor import BaseExtractor
from ipaddress import IPv4Interface


class IPv4Extractor(BaseExtractor):
    """
    A class for extracting valid IPv4 addresses from text using a custom extraction function and a filter function.

    Attributes:
        name (str): The name of the extractor, set to "ipv4".
        extraction_function (function): The custom extraction function to validate and extract IPv4 addresses.
        filter_function (function): The custom filter function to further filter the extracted IPv4 addresses.
    """

    name = "pattern_ipv4_address_only"
    extraction_function = lambda x: IPv4Extractor.validate_ipv4(x)

    @staticmethod
    def validate_ipv4(ipaddress: str):
        """
        Custom extraction function to validate if the provided string is a valid IPv4 address.

        Args:
            ipaddress (str): The string to be checked.

        Returns:
            bool: True if the string is a valid IPv4 address, False otherwise.
        """
        try:
            if len(ipaddress) >= 7 and ':' not in ipaddress:
                # Validate the IPv4 address using the IPv4Interface class.
                IPv4Interface(ipaddress)
                if '/' in ipaddress or ':' in ipaddress:
                    return False
                return True
        except Exception as ex:
            return False

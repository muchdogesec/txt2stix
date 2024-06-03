from ..base_extractor import BaseExtractor
import ipaddress


class IPv6Extractor(BaseExtractor):
    """
    A class for extracting valid IPv6 addresses from text using a custom extraction function.

    Attributes:
        name (str): The name of the extractor, set to "ipv6".
        extraction_function (function): The custom extraction function to validate and extract IPv6 addresses.
    """

    name = "pattern_ipv6_address_only"
    extraction_function = lambda x: IPv6Extractor.validate_ipv6(x)

    @staticmethod
    def validate_ipv6(x):
        """
        Custom extraction function to validate if the provided string is a valid IPv6 address with a port.

        Args:
            x (str): The string to be checked.

        Returns:
            tuple: A tuple containing the extracted IPv6 address and port if valid, False otherwise.
        """
        if ":" in x and "/" not in x:
            try:
                ipaddress.ip_network(x, False)

                return True
            except ValueError:
                pass

        return False

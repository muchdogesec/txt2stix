from ..base_extractor import BaseExtractor
from ipaddress import IPv4Address


class IPv4WithPortExtractor(BaseExtractor):
    """
    A class for extracting valid IPv4 addresses with ports from text using a custom extraction function.

    Attributes:
        name (str): The name of the extractor, set to "ipv4_port".
        extraction_function (function): The custom extraction function to validate and extract IPv4 addresses with ports.
    """

    name = "pattern_ipv4_address_port"
    extraction_function = lambda x: IPv4WithPortExtractor.validate_ipv4_with_port(x)

    @staticmethod
    def validate_ipv4_with_port(x):
        """
        Custom extraction function to validate if the provided string is a valid IPv4 address with a port.

        Args:
            x (str): The string to be checked.

        Returns:
            tuple: A tuple containing the extracted IPv4 address and port if valid, False otherwise.
        """
        x = x.strip('"')
        if ":" in x and x.count(":") == 1:
            ip_address, port = x.split(":")

            try:
                # Validate the IPv4 address part.
                IPv4Address(ip_address)

                # Validate the port part.
                if 1 <= int(port) <= 65535:
                    return ip_address, port
            except ValueError:
                pass

        return False

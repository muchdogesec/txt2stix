import re
from ipaddress import IPv6Address
from ..base_extractor import BaseExtractor

class IPv6WithPortExtractor(BaseExtractor):
    """
    A class for extracting valid IPv6 addresses with ports from text using a custom extraction function.

    Attributes:
        name (str): The name of the extractor, set to "ipv6_port".
        extraction_function (function): The custom extraction function to validate and extract IPv6 addresses with ports.
    """

    name = "pattern_ipv6_address_port"
    extraction_function = lambda x: IPv6WithPortExtractor.validate_ipv6_with_port(x)

    @staticmethod
    def validate_ipv6_with_port(x):
        """
        Custom extraction function to validate if the provided string is a valid IPv6 address with a port.

        Args:
            x (str): The string to be checked.

        Returns:
            tuple: A tuple containing the extracted IPv6 address and port if valid, False otherwise.
        """
        if ":" in x:
            # Use regex to extract the IPv6 address and port.
            match = re.match(r"\[(.*)\]:(.*)", x)
            print([x, match])
            if match:
                ip_address, port = match.groups()

                try:
                    # Validate the IPv6 address part.
                    ip = IPv6Address(ip_address)
                    print("yes", ip.exploded)

                    # Validate the port part.
                    if 1 <= int(port) <= 65535:
                        return ip_address, port
                except ValueError:
                    pass

        return False

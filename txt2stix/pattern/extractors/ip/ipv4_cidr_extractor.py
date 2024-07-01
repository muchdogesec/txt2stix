from ..base_extractor import BaseExtractor
from ipaddress import IPv4Address


class IPv4WithCIDRExtractor(BaseExtractor):
    """
    A class for extracting valid IPv4 addresses with CIDR notation from text using a custom extraction function.

    Attributes:
        name (str): The name of the extractor, set to "ipv4-cidr".
        extraction_function (function): The custom extraction function to validate and extract IPv4 addresses with CIDR.
    """

    name = "pattern_ipv4_address_cidr"
    extraction_function = lambda x: IPv4WithCIDRExtractor.validate_ipv4_with_port(x)

    @staticmethod
    def validate_ipv4_with_port(x):
        """
        Custom extraction function to validate if the provided string is a valid IPv4 address with CIDR.

        Args:
            x (str): The string to be checked.

        Returns:
            tuple: A tuple containing the extracted IPv4 address and CIDR if valid, False otherwise.
        """
        x = x.strip('"')

        if "https://" in x:
            x = x.strip("https://")

        if "https://" in x:
            x = x.strip("http://")

        if "/" in x:
            ip_address, cidr = x.split("/")

            try:
                # Validate the IPv4 address part.
                IPv4Address(ip_address)

                # Validate the CIDR part.
                if 0 <= int(cidr) <= 32:
                    return ip_address, cidr
            except ValueError:
                pass

        return False

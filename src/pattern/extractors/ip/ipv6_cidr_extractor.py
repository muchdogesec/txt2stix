# import ipaddress
from ipaddress import IPv6Address
from ..base_extractor import BaseExtractor


class IPv6WithCIDRExtractor(BaseExtractor):
    """
    A class for extracting valid IPv6 addresses with ports from text using a custom extraction function.

    Attributes:
        name (str): The name of the extractor, set to "ipv6_port".
        extraction_function (function): The custom extraction function to validate and extract IPv6 addresses with ports.
    """

    name = "pattern_ipv6_address_cidr"
    extraction_function = lambda x: IPv6WithCIDRExtractor.validate_ipv6_with_cidr(x)

    @staticmethod
    def validate_ipv6_with_cidr(x):
        """
        Custom extraction function to validate if the provided string is a valid IPv6 address with a port.

        Args:
            x (str): The string to be checked.

        Returns:
            tuple: A tuple containing the extracted IPv6 address and port if valid, False otherwise.
        """
        # if ":" in x:
        #     try:
        #         ipaddress.ip_network(x, False)
        #
        #         return True
        #     except ValueError:
        #         pass
        #
        # return False
        x = x.strip('"')

        if "https://" in x:
            x = x.strip("https://")

        if "https://" in x:
            x = x.strip("http://")

        if "/" in x:
            ip_address, cidr = x.split("/")

            try:
                # Validate the IPv4 address part.
                IPv6Address(ip_address)
                # ipaddress.ip_network(ip_address, False)

                # Validate the CIDR part.
                if 0 <= int(cidr) <= 32:
                    return ip_address, cidr
            except ValueError:
                pass

        return False

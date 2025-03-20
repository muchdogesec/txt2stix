# import ipaddress
from ipaddress import IPv6Address

import validators
from ..base_extractor import BaseExtractor


class IPv6WithCIDRExtractor(BaseExtractor):
    """
    A class for extracting valid IPv6 addresses with ports from text using a custom extraction function.

    Attributes:
        name (str): The name of the extractor, set to "ipv6_port".
        extraction_function (function): The custom extraction function to validate and extract IPv6 addresses with ports.
    """

    name = "pattern_ipv6_address_cidr"
    extraction_function = lambda ipaddress: validators.ipv6(ipaddress, strict=True, cidr=True)

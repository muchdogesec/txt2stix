import validators
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
    extraction_function = lambda ipaddress: validators.ipv6(ipaddress, strict=True, cidr=False)
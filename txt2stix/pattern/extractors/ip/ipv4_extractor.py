import re
from ..base_extractor import BaseExtractor
from ipaddress import IPv4Interface
import validators


class IPv4Extractor(BaseExtractor):
    """
    A class for extracting valid IPv4 addresses from text using a custom extraction function and a filter function.

    Attributes:
        name (str): The name of the extractor, set to "ipv4".
        extraction_function (function): The custom extraction function to validate and extract IPv4 addresses.
        filter_function (function): The custom filter function to further filter the extracted IPv4 addresses.
    """

    name = "pattern_ipv4_address_only"
    extraction_function = lambda ipaddress: validators.ipv4(ipaddress, strict=True, cidr=False)
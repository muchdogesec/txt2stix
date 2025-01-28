from tld import get_tld

from txt2stix.utils import validate_file_mimetype
from ..helper import TLDs

from ..base_extractor import BaseExtractor


class HostnameBaseExtractor(BaseExtractor):
    """
    A class for extracting valid hostnames from text using a custom extraction function.

    Attributes:
        name (str): The name of the extractor, set to "hostname".
        extraction_regex (function): The custom extraction function to validate and extract hostnames.
    """

    name = "pattern_host_name"
    extraction_regex = r'(([\da-zA-Z])([_\w-]{,62})\.){,127}(([\da-zA-Z])[_\w-]{,61})?([\da-zA-Z]\.((xn\-\-[a-zA-Z\d]+)|([a-zA-Z\d]{2,})))'

    @staticmethod
    def filter_function(domain):
        """
        Checks if the given domain is valid based on the number of dots and the top-level domain.

        Args:
            domain (str): The domain to be checked.

        Returns:
            bool: True if the domain is valid (has at most 2 dots and a valid TLD), False otherwise.
        """
        if domain.count('.') <= 1:
            tld = get_tld(domain, fix_protocol=True, fail_silently=True)
            if not tld:
                return not validate_file_mimetype(domain)
        return False
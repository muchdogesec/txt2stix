from tld import get_tld

from txt2stix.utils import validate_file_mimetype
from ..helper import TLDs

from ..base_extractor import BaseExtractor


class SubDomainExtractor(BaseExtractor):
    """
    A class for extracting valid subdomains from text using a custom extraction function.

    This class inherits from BaseExtractor, which defines the basic structure and functionality for all extractors.

    Attributes:
        name (str): The name of the extractor, set to "sub-domain".
        extraction_regex (function): The custom extraction function to validate and extract subdomains.
    """

    name = "pattern_domain_name_subdomain"
    extraction_regex = r'(([\da-zA-Z])([_\w-]{,62})\.){,127}(([\da-zA-Z])[_\w-]{,61})?([\da-zA-Z]\.((xn\-\-[' \
                       r'a-zA-Z\d]+)|([a-zA-Z\d]{2,})))'

    @staticmethod
    def filter_function(domain):
        """
        Checks if the given domain is valid based on the number of dots and the top-level domain.

        Args:
            domain (str): The domain to be checked.

        Returns:
            bool: True if the domain is valid (has at most 2 dots and a valid TLD), False otherwise.
        """
        if domain.count('.') >= 2:
            tld = get_tld(domain, fix_protocol=True, fail_silently=True)
            if tld:
                domain_name = domain.strip(f".{tld}")
                if domain_name.count(".") > 0:
                    return True
        return False

class HostNameSubdomainExtractor(SubDomainExtractor):
    name = "pattern_host_name_subdomain"
    filter_function = lambda domain: domain.count('.') >= 2 and get_tld(domain, fail_silently=True) not in TLDs

    def filter_function(domain):
        tld =  get_tld(domain, fail_silently=True, fix_protocol=True)
        return domain.count('.') >= 2 and not tld and not validate_file_mimetype(domain)

from tld import get_tld

from ..base_extractor import BaseExtractor


class DomainNameExtractor(BaseExtractor):
    """
    A class for extracting valid domain names from text using a custom extraction function.

    Attributes:
        name (str): The name of the extractor, set to "domain".
        extraction_regex (function): The custom extraction function to validate and extract domain names.
    """
    name = "pattern_domain_name_only"
    extraction_regex =  r'(([\da-zA-Z])([_\w-]{,62})\.){,127}(([\da-zA-Z])[_\w-]{,61})?([\da-zA-Z]\.((xn\-\-[a-zA-Z\d]+)|([a-zA-Z\d]{2,})))'

    @staticmethod
    def filter_function(domain):
        """
        Checks if the given domain is valid based on the number of dots and the top-level domain.

        Args:
            domain (str): The domain to be checked.

        Returns:
            bool: True if the domain is valid (has at most 2 dots and a valid TLD), False otherwise.
        """
        if domain.count('.') <= 2:
            tld = get_tld(domain, fix_protocol=True, fail_silently=True)
            if tld:
                domain_name = domain.strip(f".{tld}")
                if domain_name.count(".") == 0:
                    return True
        return False


# class HostNameExtractor(DomainNameExtractor):
#     filter_function = None
#     name = "pattern_host_name"
import tldextract
import validators

from txt2stix import utils

from ..base_extractor import BaseExtractor
from ..helper import check_false_positive_domain, validate_file_extension
from urllib.parse import urlparse
from ipaddress import ip_address


class URLPathExtractor(BaseExtractor):
    """
    URLPathExtractor is a class that extracts URLs from input data using a simple validation mechanism.

    Attributes:
        name (str): The name of the extractor.
        extraction_function (function): The function to extract URLs.
    """
    name = "pattern_url_path"
    extraction_function = lambda url: URLPathExtractor.is_valid_url(url)
    filter_function = lambda url: URLPathExtractor.is_path(url) and URLPathExtractor.validate_host(url) and not validate_file_extension(url)

    @classmethod
    def is_path(cls, url):
        path = urlparse(url).path
        if path and path != "/":
            return True
        return False

    @classmethod
    def validate_host(cls, url, validate_tld=True):
        uri = urlparse(url)
        if not validators.hostname(uri.hostname):
            return False
        if validate_tld and not cls.is_ip_address(uri.hostname):
            return utils.validate_tld(uri.hostname)
        return True

    @staticmethod
    def is_ip_address(address):
        try:
            ip_address(address)
            return True
        except:
            return False
    @staticmethod
    def is_valid_url(url):
        """
        Checks if a given URL is valid and does not point to a file.

        Args:
            url (str): The URL to be validated.

        Returns:
            bool: True if the URL is valid and doesn't point to a file, False otherwise.
        """
        try:
            # Check if "http" or "www" is present in the URL
            if validators.url(url):
                extracted_domain = tldextract.extract(url)
                if check_false_positive_domain(extracted_domain.domain):
                        return True
        except Exception as e:
            # An exception occurred, consider the URL invalid
            return False

        # Default case: URL is not valid or doesn't meet the conditions
        return False


class HostnamePathExtractor(URLPathExtractor):
    name = "pattern_host_name_path"
    filter_function = lambda url: URLPathExtractor.is_path(url) and URLPathExtractor.validate_host(url, validate_tld=False) and not validate_file_extension(url)
import tldextract
from urllib.parse import urlparse

from .url_path_extractor import URLPathExtractor

from ..base_extractor import BaseExtractor
from ..helper import check_false_positive_domain, validate_tld, validate_file_extension


class URLExtractor(URLPathExtractor):
    """
    A class for extracting valid URLs from text using a combination of regular expressions and validation functions.

    Attributes:
        name (str): The name of the extractor, set to "url".
        extraction_function (function): The extraction function that validates and extracts URLs from the given text.
    """

    name = "pattern_url"
    filter_function = lambda url: not URLPathExtractor.is_path(url) and URLPathExtractor.validate_host(url)


class HostnameUrlExtractor(URLExtractor):
    name = "pattern_host_name_url"

    filter_function = lambda url: not URLPathExtractor.is_path(url) and URLPathExtractor.validate_host(url, validate_tld=False)
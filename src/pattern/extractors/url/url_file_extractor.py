import tldextract
from urllib.parse import urlparse

from ..base_extractor import BaseExtractor
from ..helper import check_false_positive_domain, validate_tld, validate_file_extension
from .url_path_extractor import URLPathExtractor


class URLFileExtractor(URLPathExtractor):
    """
    A class for extracting valid URLs from text using a combination of regular expressions and validation functions.

    Attributes:
        name (str): The name of the extractor, set to "url".
        extraction_function (function): The extraction function that validates and extracts URLs from the given text.
    """

    name = "pattern_url_file"
    filter_function = lambda url: URLFileExtractor.is_path(url) and URLPathExtractor.validate_host(url) and validate_file_extension(url)
    

class HostnameFileExtractor(URLFileExtractor):
    name = "pattern_host_name_file"
    filter_function = lambda url: URLFileExtractor.is_path(url) and validate_file_extension(url) and URLPathExtractor.validate_host(url, validate_tld=False)
import validators
from ..base_extractor import BaseExtractor

class FileHashSHA1Extractor(BaseExtractor):
    """
    A class for extracting SHA-1 file hash values from text using a custom extraction function.

    Attributes:
        name (str): The name of the extractor, set to "sha1".
        extraction_function (function): The custom extraction function to validate and extract SHA-1 file hash values.
    """

    name = "pattern_file_hash_sha_1"
    extraction_function = lambda x: validators.sha1(x)
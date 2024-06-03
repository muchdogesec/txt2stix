import validators
from ..base_extractor import BaseExtractor


class FileHashSHA224Extractor(BaseExtractor):
    """
    A class for extracting SHA-256 file hash values from text using a regular expression.

    Attributes:
        name (str): The name of the extractor, set to "sha2_256".
        extraction_regex (str): The regular expression pattern used for extracting SHA-256 file hash values from the text.
    """

    name = "pattern_file_hash_sha_224"
    extraction_regex = r'^[0-9a-fA-F]{56}$'
    extraction_function = lambda x: validators.sha224(x)

# not currently used as not supported by the STIX spec.
from ..base_extractor import BaseExtractor

class FileHashSHA2_512Extractor(BaseExtractor):
    """
    A class for extracting SHA-512 file hash values from text using a regular expression.

    Attributes:
        name (str): The name of the extractor, set to "sha2_512".
        extraction_regex (str): The regular expression pattern used for extracting SHA-512 file hash values from the text.
    """

    name = "pattern_file_hash_sha_512"
    extraction_regex = r'^[0-9a-fA-F]{128}$'

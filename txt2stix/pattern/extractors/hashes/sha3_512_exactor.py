from ..base_extractor import BaseExtractor


class FileHashSHA3_512Extractor(BaseExtractor):
    """
    A class for extracting SHA-3 (512-bit) file hash values from text using a regular expression.

    Attributes:
        name (str): The name of the extractor, set to "sha3_512".
        extraction_regex (str): The regular expression pattern used for extracting SHA-3 (512-bit) file hash values from the text.
    """

    name = "pattern_file_hash_sha3_512"
    extraction_regex = r'^[0-9a-fA-F]{128}$'



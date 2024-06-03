import validators
from ..base_extractor import BaseExtractor


class FileHashMD5Extractor(BaseExtractor):
    """
    A class for extracting MD5 file hash values from text using a custom extraction function.

    Attributes:
        name (str): The name of the extractor, set to "md5".
        extraction_function (function): The custom extraction function to validate and extract MD5 file hash values.
    """

    name = "pattern_file_hash_md5"
    extraction_function = lambda x: validators.md5(x)


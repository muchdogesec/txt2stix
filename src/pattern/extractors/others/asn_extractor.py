from ..base_extractor import BaseExtractor


class ASNExtractor(BaseExtractor):
    """
    A class for extracting Autonomous System Numbers (ASNs) from text using a regular expression.

    Attributes:
        name (str): The name of the extractor, set to "asn".
        extraction_regex (str): The regular expression pattern used for extracting ASNs from the text.
    """

    name = "pattern_autonomous_system_number"
    extraction_regex = r"(?:ASN?)(?: )?(\d+)"

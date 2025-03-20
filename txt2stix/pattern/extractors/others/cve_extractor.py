from ..base_extractor import BaseExtractor


class CVEExtractor(BaseExtractor):
    """
    A class for extracting Common Vulnerabilities and Exposures (CVE) identifiers from text using a regular expression.

    Attributes:
        name (str): The name of the extractor, set to "cve".
        extraction_regex (str): The regular expression pattern used for extracting CVE identifiers from the text.
    """

    name = "pattern_cve_id"
    extraction_regex = r'\bCVE-\d{4}-\d{4,5}\b'

from validators import card_number
from ..base_extractor import BaseExtractor


class JCBCardExtractor(BaseExtractor):
    """
    A class for extracting JCB credit card numbers from text using regular expressions.

    Attributes:
        name (str): The name of the extractor, set to "jcb-card".
        extraction_regex (str): The regular expression pattern used for extracting JCB credit card numbers.
    """

    name = "pattern_bank_card_jcb"

    # The following part is automatically generated from https://docs.trellix.com/bundle/data-loss-prevention-11.10.x-classification-definitions-reference-guide/page/GUID-D56393B2-2C27-4CAF-A7C3-AE83298BD96B.html
    description = """
    JCB CCN is a 16-digit number beginning with 3528 or 3589 and might have dashes
	(hyphens) or spaces as separators. For example, NNNN-NNNN-NNNN-NNNN or NNNN
	NNNN NNNNNNNN. This excludes common test card numbers.

    validator = Luhn 10 (remainder 0)
    """
    extraction_regex_list = [
        "\\b352[89]-\\d{4}-\\d{4}-\\d{4}\\b",
        "\\b352[89] \\d{4} \\d{4} \\d{4}\\b",
        "\\b352[89]\\d{12}\\b",
        "\\b35[3-8]\\d-\\d{4}-\\d{4}-\\d{4}\\b",
        "\\b35[3-8]\\d \\d{4} \\d{4} \\d{4}\\b",
        "\\b35[3-8]\\d{13}\\b"
    ]
    filter_regex_list = [
        "3528([ -]?)0007([ -]?)0000([ -]?)0000",
        "3528([ -]?)7237([ -]?)4002([ -]?)2896",
        "3530([ -]?)1113([ -]?)3330([ -]?)0000",
        "3556([ -]?)4000([ -]?)0055([ -]?)1234",
        "3566([ -]?)0020([ -]?)2036([ -]?)0505",
        "3569([ -]?)9900([ -]?)0000([ -]?)0009"
    ]
    extraction_regex = "|".join(extraction_regex_list)

    # end of generated code
    filter_function = card_number

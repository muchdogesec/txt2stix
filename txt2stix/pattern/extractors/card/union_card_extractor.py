from ..base_extractor import BaseExtractor


class UnionPayCardExtractor(BaseExtractor):
    """
    A class for extracting UnionPay credit card numbers from text using regular expressions.

    This class inherits from BaseExtractor, which defines the basic structure and functionality for all extractors.

    Attributes:
        name (str): The name of the extractor, set to "union-pay-card".
        extraction_regex (str): The regular expression pattern used for extracting UnionPay credit card numbers.
    """

    name = "pattern_bank_card_union_pay"

    # The following part is automatically generated from https://docs.trellix.com/bundle/data-loss-prevention-11.10.x-classification-definitions-reference-guide/page/GUID-B8D29ECE-E70A-401E-B18D-B773F4FF71ED.html
    description = """
    The China UnionPay credit card numbers begin with 62 or 60 and is a 16-19
	digit long number.

    validator = China Union Pay Card validator
    """
    extraction_regex_list = [
        "\\b622\\d{13,16}\\b",
        "\\b603601\\d{10}\\b",
        "\\b603265\\d{10}\\b",
        "\\b621977\\d{10}\\b",
        "\\b603708\\d{10}\\b",
        "\\b602969\\d{10}\\b",
        "\\b601428\\d{10}\\b",
        "\\b603367\\d{10}\\b",
        "\\b603694\\d{10}\\b"
    ]
    filter_regex_list = []
    extraction_regex = "|".join(extraction_regex_list)

    # end of generated code

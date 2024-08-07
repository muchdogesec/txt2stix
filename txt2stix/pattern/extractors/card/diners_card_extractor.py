from validators import card_number
from ..base_extractor import BaseExtractor


class DinersCardExtractor(BaseExtractor):
    """
    A class for extracting Diners Club credit card numbers from text using regular expressions.

    Attributes:
        pattern (str): The pattern to represent the extracted credit card number.
        extraction_regex (str): The regular expression pattern used for extracting Diners Club credit card numbers.
    """

    name = "pattern_bank_card_diners"

    # The following part is automatically generated from https://docs.trellix.com/bundle/data-loss-prevention-11.10.x-classification-definitions-reference-guide/page/GUID-2B5CF316-ED36-4CAB-92D7-AC46714E9882.html
    description = """
    Credit Card Number (Diner's Club) is a 14-digit number beginning with 300–305,
	36, 38, or 39 and might have dashes (hyphens) or spaces as separators. For
	example, NNNN-NNNNNN-NNNN or NNNN NNNNNN NNNN. Matches exclude common test
	card numbers.

    validator = Luhn 10 (remainder 0)
    """
    extraction_regex_list = [
        "\\b30[0-5]\\d-\\d{6}-\\d{4}\\b",
        "\\b30[0-5]\\d \\d{6} \\d{4}\\b",
        "\\b30[0-5]\\d{11}\\b",
        "\\b3[689]\\d{2}-\\d{6}-\\d{4}\\b",
        "\\b3[689]\\d{2} \\d{6} \\d{4}\\b",
        "\\b3[689]\\d{12}\\b"
    ]
    filter_regex_list = [
        "3020([ -]?)416932([ -]?)2643",
        "3021([ -]?)804719([ -]?)6557",
        "3022([ -]?)151156([ -]?)3252",
        "3046([ -]?)400000([ -]?)5512",
        "3600([ -]?)000000([ -]?)0008",
        "3614([ -]?)890064([ -]?)7913",
        "3670([ -]?)010200([ -]?)0000",
        "3852([ -]?)000002([ -]?)3237",
        "3912([ -]?)345678([ -]?)9019"
    ]
    extraction_regex = "|".join(extraction_regex_list)

    # end of generated code
    filter_function = card_number

from validators import card_number
from ..base_extractor import BaseExtractor


class BankCardDiscoverExtractor(BaseExtractor):
    """
    A class for extracting Discover credit card numbers from text using regular expressions.

    Attributes:
        name (str): The name of the extractor, set to "bank-card-discover".
        extraction_regex (str): The regular expression pattern used for extracting Discover credit card numbers.
    """

    name = "pattern_bank_card_discover"

    # The following part is automatically generated from https://docs.trellix.com/bundle/data-loss-prevention-11.10.x-classification-definitions-reference-guide/page/GUID-EF96B5CE-6C8E-49B2-BD19-82B0CE0E5091.html
    description = """
    Credit Card Number (Discover) is a 16-digit number beginning with 6011,
	644–649 or 65 and might have dashes (hyphens) or spaces as separators. For
	example, NNNN-NNNN-NNNN-NNNN or NNNN NNNN NNNN NNNN. This excludes common test
	card numbers.

    validator = Luhn 10 (remainder 0)
    """
    extraction_regex_list = [
        "\\b6011-\\d{4}-\\d{4}-\\d{4}\\b",
        "\\b6011 \\d{4} \\d{4} \\d{4}\\b",
        "\\b6011\\d{12}\\b",
        "\\b64[4-9]\\d-\\d{4}-\\d{4}-\\d{4}\\b",
        "\\b64[4-9]\\d \\d{4} \\d{4} \\d{4}\\b",
        "\\b64[4-9]\\d{13}\\b",
        "\\b65\\d{2}-\\d{4}-\\d{4}-\\d{4}\\b",
        "\\b65\\d{2} \\d{4} \\d{4} \\d{4}\\b",
        "\\b65\\d{14}\\b"
    ]
    filter_regex_list = [
        "6011([ -]?)0009([ -]?)9013([ -]?)9424",
        "6011([ -]?)1111([ -]?)1111([ -]?)1117",
        "6011([ -]?)1532([ -]?)1637([ -]?)1980",
        "6011([ -]?)6011([ -]?)6011([ -]?)6611",
        "6011([ -]?)6874([ -]?)8256([ -]?)4166",
        "6011([ -]?)8148([ -]?)3690([ -]?)5651",
        "6556([ -]?)4000([ -]?)0055([ -]?)1234"
    ]
    extraction_regex = "|".join(extraction_regex_list)

    # end of generated code
    filter_function = card_number

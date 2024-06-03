from ..base_extractor import BaseExtractor
from ..helper import extract_meta


class AmexCardExtractor(BaseExtractor):
    """
    A class for extracting American Express (Amex) credit card numbers from text using regular expressions.

    Attributes:
        name (str): The name of the extractor, set to "Amex-card".
        extraction_regex (str): The regular expression pattern used for extracting Amex credit card numbers.
    """

    name = "pattern_bank_card_amex"

    # The following part is automatically generated from https://docs.trellix.com/bundle/data-loss-prevention-11.10.x-classification-definitions-reference-guide/page/GUID-97839BB4-3077-4BB0-9974-CF8EEB0E2426.html
    description = """
    American Express Credit Card Number (CCN) is a 15-digit number starting with
	34 or 37 and might have dashes (hyphens) or spaces as separators. For example,
	NNNN-NNNNNN-NNNNN or NNNN NNNNNN NNNNN. Matches exclude common test card
	numbers.

    validator = Luhn 10 (remainder 0)
    """
    extraction_regex_list = [
        "\\b3[47]\\d{2} \\d{6} \\d{5}\\b",
        "\\b3[47]\\d{2}-\\d{6}-\\d{5}\\b",
        "\\b3[47]\\d{13}\\b"
    ]
    filter_regex_list = [
        "3400([- ]?)000000([- ]?)00009",
        "3411([- ]?)111111([- ]?)11111",
        "3434([- ]?)343434([- ]?)34343",
        "3456([- ]?)789012([- ]?)34564",
        "3456([- ]?)400000([- ]?)55123",
        "3468([- ]?)276304([- ]?)35344",
        "3700([- ]?)000000([ -]?)00002",
        "3700([- ]?)002000([ -]?)00000",
        "3704([- ]?)072699([ -]?)09809",
        "3705([- ]?)560193([ -]?)09221",
        "3714([- ]?)496353([ -]?)98431",
        "3742([- ]?)000000([ -]?)00004",
        "3756([- ]?)400000([ -]?)55123",
        "3764([- ]?)622809([ -]?)21451",
        "3777([- ]?)527498([ -]?)96404",
        "3782([- ]?)822463([ -]?)10005",
        "3787([- ]?)344936([ -]?)71000"
    ]
    extraction_regex = "|".join(extraction_regex_list)

    # end of generated code

from ..base_extractor import BaseExtractor


class MastercardCardExtractor(BaseExtractor):
    """
    A class for extracting Mastercard credit card numbers from text using regular expressions.

    Attributes:
        name (str): The name of the extractor, set to "master-card".
        extraction_regex (str): The regular expression pattern used for extracting Mastercard credit card numbers.
    """

    name = "pattern_bank_card_mastercard"

    # The following part is automatically generated from https://docs.trellix.com/bundle/data-loss-prevention-11.10.x-classification-definitions-reference-guide/page/GUID-8A0A2E8B-D740-476E-B10C-885919573022.html
    description = """
    Credit Card Number (Mastercard) is a 16-digit number beginning with 51–55 or
	2221– 2720 and might have dashes (hyphens) or spaces as separators. For
	example, NNNN-NNNN-NNNN-NNNN or NNNN NNNN NNNN NNNN. This excludes common test
	card numbers.

    validator = Luhn 10 (remainder 0)
    """
    extraction_regex_list = [
        "\\b5[1-5]\\d{2}-\\d{4}-\\d{4}-\\d{4}\\b",
        "\\b5[1-5]\\d{2} \\d{4} \\d{4} \\d{4}\\b",
        "\\b5[1-5]\\d{14}\\b",
        "\\b2[2-7]\\d{2}-\\d{4}-\\d{4}-\\d{4}\\b",
        "\\b2[2-7]\\d{2} \\d{4} \\d{4} \\d{4}\\b",
        "\\b2[2-7]\\d{14}\\b"
    ]
    filter_regex_list = [
        "5100([- ]?)0800([ -]?)0000([ -]?)0000",
        "5105([- ]?)1051([ -]?)0510([ -]?)5100",
        "5111([- ]?)1111([ -]?)1111([ -]?)1118",
        "5123([- ]?)4567([ -]?)8901([ -]?)2346",
        "5123([- ]?)6197([ -]?)4539([ -]?)5853",
        "5138([- ]?)4951([ -]?)2555([ -]?)0554",
        "5274([- ]?)5763([ -]?)9425([ -]?)9961",
        "5301([- ]?)7455([ -]?)2913([ -]?)8831",
        "5311([- ]?)5312([ -]?)8600([ -]?)0465",
        "5364([- ]?)5870([ -]?)1178([ -]?)5834",
        "5404([- ]?)0000([ -]?)0000([ -]?)0001",
        "5431([- ]?)1111([ -]?)1111([ -]?)1111",
        "5454([- ]?)5454([ -]?)5454([ -]?)5454",
        "5459([- ]?)8862([ -]?)6563([ -]?)1843",
        "5460([- ]?)5060([ -]?)4803([ -]?)9935",
        "5500([- ]?)9391([ -]?)7800([ -]?)4613",
        "5555([- ]?)5555([ -]?)5555([ -]?)4444",
        "5556([- ]?)4000([ -]?)0055([ -]?)1234",
        "5565([- ]?)5520([ -]?)6448([ -]?)1449",
        "5597([- ]?)5076([ -]?)4491([ -]?)0558",
        "220\\d([- ]?)\\d{4}([ -]?)\\d{4}([ -]?)\\d{4}",
        "221\\d([- ]?)\\d{4}([ -]?)\\d{4}([ -]?)\\d{4}",
        "2220([- ]?)\\d{4}([ -]?)\\d{4}([ -]?)\\d{4}",
        "272[1-9]([- ]?)\\d{4}([ -]?)\\d{4}([ -]?)\\d{4}",
        "27[3-9]\\d([- ]?)\\d{4}([ -]?)\\d{4}([ -]?)\\d{4}"
    ]
    extraction_regex = "|".join(extraction_regex_list)

    # end of generated code

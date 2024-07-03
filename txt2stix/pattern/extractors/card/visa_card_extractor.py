from ..base_extractor import BaseExtractor


class VisaCardBaseExtractor(BaseExtractor):
    """
    A class for extracting VISA credit card numbers from text using regular expressions.

    Attributes:
        name (str): The name of the extractor, set to "visa-card".
        extraction_regex (str): The regular expression pattern used for extracting VISA credit card numbers.
    """

    name = "pattern_bank_card_visa"

    # The following part is automatically generated from https://docs.trellix.com/bundle/data-loss-prevention-11.10.x-classification-definitions-reference-guide/page/GUID-66A52D16-CA41-4509-826D-8D29B1F968C2.html
    description = """
    Credit Card Number (Visa) is 16-digit number and might have dashes (hyphen) or
	spaces as separators. For example, NNNN-NNNN-NNNN-NNNN or NNNN NNNN NNNN NNNN.
	This excludes common test card numbers.

    validator = Luhn 10 (remainder 0)
    """
    extraction_regex_list = [
        "\\b4\\d{3}-\\d{4}-\\d{4}-\\d{4}\\b",
        "\\b4\\d{3} \\d{4} \\d{4} \\d{4}\\b",
        "\\b4\\d{15}\\b"
    ]
    filter_regex_list = [
        "4005([ -]?)5500([ -]?)0000([ -]?)0001",
        "4012([ -]?)8888([ -]?)8888([ -]?)1881",
        "4111([ -]?)1111([ -]?)1111([ -]?)1111",
        "4444([ -]?)3333([ -]?)2222([ -]?)1111",
        "4539([ -]?)1050([ -]?)1153([ -]?)9664",
        "4555([ -]?)4000([ -]?)0055([ -]?)5123",
        "4564([ -]?)4564([ -]?)4564([ -]?)4564",
        "4544([ -]?)1821([ -]?)7453([ -]?)7267",
        "4716([ -]?)9147([ -]?)0653([ -]?)4228",
        "4916([ -]?)5417([ -]?)1375([ -]?)7159",
        "4916([ -]?)6156([ -]?)3934([ -]?)6972",
        "4917([ -]?)6100([ -]?)0000([ -]?)0000"
    ]
    extraction_regex = "|".join(extraction_regex_list)

    # end of generated code

"""
`Extractor` class represents the properties of a given observable.
"""
import re
import logging

logger = logging.getLogger(__name__)

ALL_EXTRACTORS = {}

class BaseExtractor:
    name = None
    extraction_regex = None
    stripe_on_line = False
    extraction_function = None
    common_strip_elements = "\"'.,:"
    filter_function = None # further filter the extracted values
    meta_extractor = None
    version = None
    stix_mapping = None
    invalid_characters = ['.', ',', '!', '`', '(', ')', '{', '}', '"', '````', ' ']


    @classmethod
    def register_new_extractor(cls, name, extractor):
        ALL_EXTRACTORS[name] = extractor

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.register_new_extractor(cls.name, cls)

    @classmethod
    def extract_extraction_from_text(cls, text: str):
        """
        Extracts the required observables from text and returns the
        extracted observables and modified text.
        """
        extracted_observables = []
        start_index = 0
        if cls.extraction_regex is not None:
            if cls.extraction_regex.startswith("^") or cls.extraction_regex.endswith("$"):
                for word in text.split():
                    end_index = start_index + len(word) - 1
                    match = re.match(cls.extraction_regex, word)
                    if match:
                        extracted_observables.append((match.group(0), start_index))
                    else:
                        stripped_word = word.strip(cls.common_strip_elements)
                        match = re.match(cls.extraction_regex, stripped_word)
                        if match:
                            extracted_observables.append((match.group(0), start_index))
                    start_index = end_index + 2  # Adding 1 for the space and 1 for the next word's starting index
            else:
                # Find regex in the entire text (including whitespace)
                for match in re.finditer(cls.extraction_regex, text):
                    match = match.group().strip('\n')
                    end_index = start_index + len(match) - 1
                
                    extracted_observables.append((match, start_index))
                    start_index = end_index + 2  # Adding 1 for the space and 1 for the next word's starting index

        # If extraction_function is not None, then find matches that don't throw exception when
        elif cls.extraction_function is not None:

            start_index = 0
            if cls.stripe_on_line:
                words = text.splitlines()
            else:
                words = text.split()
            for word in words:
                end_index = start_index + len(word) - 1

                word = BaseExtractor.trim_invalid_characters(word, cls.invalid_characters)
                try:
                    if cls.extraction_function(word):
                        extracted_observables.append((word, start_index))
                except Exception as error:
                    pass

                start_index = end_index + 2  # Adding 1 for the space and 1 for the next word's starting index

        else:
            raise ValueError("Both extraction_regex and extraction_function can't be None.")

        string_positions = {}

        # Iterate through the input list to group positions for each string
        for position, (string, pos) in enumerate(extracted_observables, 1):
            if cls.filter_function and not cls.filter_function(string):
                continue
            if string not in string_positions:
                string_positions[string] = []
            string_positions[string].append(pos)

        response = []

        for extraction, positions in string_positions.items():
            response.append({
                "value": extraction,
                "type": cls.name,
                "version": cls.version,
                "stix_mapping": cls.stix_mapping,
                "start_index": positions,
            })

        return response

    @staticmethod
    def search_keyword_positions(input_string, keyword):
        keyword_positions = []
        start = 0
        while start < len(input_string):
            index = input_string.find(keyword, start)
            if index == -1:
                break
            keyword_positions.append((keyword, index))
            start = index + len(keyword)

        positions_only = [pos for kw, pos in keyword_positions]
        return keyword, positions_only

    @staticmethod
    def trim_invalid_characters(keyword, characters):
        if keyword[-1] in characters:
            keyword = keyword[:-1]

        if len(keyword) > 0:
            if keyword[0] in characters:
                keyword = keyword[1:]

        return keyword

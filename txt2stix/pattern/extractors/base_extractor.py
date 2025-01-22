"""
`Extractor` class represents the properties of a given observable.
"""
import re
import logging
from typing import Iterable

logger = logging.getLogger(__name__)

ALL_EXTRACTORS = {}

class BaseExtractor:
    name = None
    extraction_regex = None
    extraction_function = None
    common_strip_elements = "\"'.,:"
    filter_function = None # further filter the extracted values
    meta_extractor = None
    version = None
    stix_mapping = None
    invalid_characters = ['.', ',', '!', '`', '(', ')', '{', '}', '"', '````', ' ', '[', ']']
    SPLITS_FINDER = re.compile(r'[\'"<\(\{\[\s](?P<item>.*?)[\)\s\]\}\)>"\']') #split on boundary characters instead of ' ' only


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
                for matchsplit in cls.SPLITS_FINDER.finditer(text):
                    word = matchsplit.group('item')
                    start_index = matchsplit.start('item')
                    match = re.match(cls.extraction_regex, word)
                    if match:
                        extracted_observables.append((match.group(0), match.start()+start_index))
                    else:
                        stripped_word = word.strip(cls.common_strip_elements)
                        match = re.match(cls.extraction_regex, stripped_word)
                        if match:
                            extracted_observables.append((match.group(0), start_index + word.index(stripped_word)))
            else:
                # Find regex in the entire text (including whitespace)
                for match in re.finditer(cls.extraction_regex, text):
                    match_value = match.group().strip('\n')
                    start_index, end_index = match.span()
                
                    extracted_observables.append((match_value, start_index))

        # If extraction_function is not None, then find matches that don't throw exception when
        elif cls.extraction_function is not None:

            start_index = 0
            
            for match in cls.SPLITS_FINDER.finditer(text):
                word = match.group('item')
                end_index = start_index + len(word) - 1

                word = BaseExtractor.trim_invalid_characters(word, cls.invalid_characters)
                try:
                    if cls.extraction_function(word):
                        extracted_observables.append((word, match.start('item')))
                except Exception as error:
                    pass

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

        # for extraction, positions in string_positions.items():
        #     response.append({
        #         "value": extraction,
        #         "type": cls.name,
        #         "version": cls.version,
        #         "stix_mapping": cls.stix_mapping,
        #         "start_index": positions,
        #     })

        for position, (string, pos) in enumerate(extracted_observables, 1):
            if cls.filter_function and not cls.filter_function(string):
                continue
            response.append({
                "value": string,
                "type": cls.name,
                "version": cls.version,
                "stix_mapping": cls.stix_mapping,
                "start_index": pos,
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

    @classmethod
    def split_all(cls, text):
        for word in cls.SPLITS_FINDER.findall(text):
            yield cls.trim_invalid_characters(word, cls.invalid_characters)

    @classmethod
    def trim_invalid_characters(cls, keyword: str, characters: Iterable):
        return keyword.strip(''.join(characters))

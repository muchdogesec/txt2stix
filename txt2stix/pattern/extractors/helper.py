"""
Bunch of helper methods
"""
import csv
import logging
import sys

from .base_extractor import ALL_EXTRACTORS

from ...extractions import Extractor
from ...utils import read_included_file


def read_text_file(file_path):
    """
    Read the content of a text file line by line.

    Args:
        file_path (str): Path to the text file.

    Returns:
        list: List containing each line of the text file as stripped strings.
    """
    lines_list = []

    try:
        # Open the file in read mode
        with open(file_path, 'r') as file:
            # Read each line from the file and append it to the list
            for line in file:
                lines_list.append(line.strip())

    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except IOError as e:
        logging.error(f"Error reading the file: {file_path} - {e}")

    return lines_list

def check_false_positive_domain(domain):
    """
    Check if a domain is a false positive based on its file extension.

    Args:
        domain (str): The domain name to be checked.

    Returns:
        bool: True if the domain is not a false positive, False otherwise.
    """
    file_extension = domain.split(".")[-1]
    if file_extension in FILE_EXTENSION:
        return False
    else:
        return True

from txt2stix.utils import validate_file_mimetype as validate_file_extension, validate_tld

def load_extractor(extractor):
    if extractor.pattern_extractor:
        return
    extractor.pattern_extractor = ALL_EXTRACTORS.get(extractor.slug)
    if not extractor.pattern_extractor:
        raise TypeError(f"could not find associated python class for pattern extractor `{extractor.slug}`")
    extractor.pattern_extractor.version = extractor.version
    extractor.pattern_extractor.stix_mapping = extractor.stix_mapping


def extract_all(extractors :list[Extractor], input_text):
    logging.info("using pattern extractors")
    pattern_extracts = []
    for extractor in extractors:
        load_extractor(extractor)
        extracts = extractor.pattern_extractor().extract_extraction_from_text(input_text)
        pattern_extracts.extend(extracts)

    pattern_extracts.sort(key=lambda ex: (ex['start_index'], len(ex['value'])))
    retval = {}
    end = 0
    for raw_extract in pattern_extracts:
        start_index = raw_extract['start_index']
        key = (raw_extract['type'], raw_extract['value'])
        if start_index >= end:
            extraction = retval.setdefault(key, {**raw_extract, "start_index":[start_index]})
            if start_index not in extraction['start_index']:
                extraction['start_index'].append(start_index)
            end = start_index + len(raw_extract['value'])
    return list(retval.values())


FILE_EXTENSION = read_included_file('lookups/extensions.txt')
TLD = read_included_file('lookups/tld.txt')
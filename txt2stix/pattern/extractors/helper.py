"""
Bunch of helper methods
"""
import csv
import logging
import sys

from ...extractions import Extractor


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


def validate_file_extension(extension):
    """
    Validate if a file extension is in the list of valid extensions.

    Args:
        extension (str): The file extension to be validated.

    Returns:
        bool: True if the extension is valid, False otherwise.
    """

    extension = extension.split(".")[-1]

    return extension in FILE_EXTENSION


def validate_tld(tld):
    """
    Validate if a file tld is in the list of valid extensions.

    Args:
        tld (str): The file extension to be validated.

    Returns:
        bool: True if the extension is valid, False otherwise.
    """
    return tld in TLD


def extract_all(extractors :list[Extractor], input_text):
    logging.info("using pattern extractors")
    pattern_extracts = []
    for extractor in extractors:
        extracts = extractor.pattern_extractor().extract_extraction_from_text(input_text)
        pattern_extracts.extend(extracts)
    return pattern_extracts


FILE_EXTENSION = read_text_file('lookups/extensions.txt')
TLD = read_text_file('lookups/tld.txt')
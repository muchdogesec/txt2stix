"""
Bunch of helper methods
"""
import csv
import logging
import sys


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


def extract_meta(card):
    """
    Extract metadata based on a card identifier.

    Args:
        card (str): The card identifier to extract metadata for.

    Returns:
        dict or False: A dictionary containing metadata if a match is found, False otherwise.
    """
    for row in CARDS_META_DATA:
        if card.strip()[:6] == row[0]:
            meta = {'scheme': row[4] or '',
                    'type': row[6],
                    'country': row[8],
                    'bank_name': row[9],
                    'bank_url': row[11]
                    }
            if row[5]:
                meta['brand'] = row[5]
            if row[12]:
                meta['bank_phone'] = row[12]
            if row[13]:
                meta['bank_city'] = row[13]
            return meta

    return False


def validate_tld(tld):
    """
    Validate if a file tld is in the list of valid extensions.

    Args:
        tld (str): The file extension to be validated.

    Returns:
        bool: True if the extension is valid, False otherwise.
    """
    return tld in TLD


FILE_EXTENSION = read_text_file('lookups/extensions.txt')
TLD = read_text_file('lookups/tld.txt')
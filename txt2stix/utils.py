import os
import pkgutil
import re
from pathlib import Path

import tldextract


def remove_data_images(input_text):
    match_re = re.compile(r"(!\[([^\]]*)\]\((data:image/\w+;\w+),([^\^)]+)\))")
    def subber(match, *args):
        return "![{}]({},blank...)".format(match.group(2), match.group(3))
    return match_re.sub(subber, input_text)


def read_included_file(path):
    try:
        return pkgutil.get_data("txt2stix.includes", path).decode()
    except:
        return (Path("includes")/path).read_text()
    
def validate_tld(domain):
    extracted_domain = tldextract.extract(domain)
    return extracted_domain.suffix in TLDS

def validate_reg_key(reg_key):
    reg_key = reg_key.lower()
    for prefix in REGISTRY_PREFIXES:
        if reg_key.starts_with(prefix):
            return True
    return False

def validate_file_mimetype(file_name):
    _, ext = os.path.splitext(file_name)
    return FILE_EXTENSIONS.get(ext)

TLDS = [tld.lower() for tld in read_included_file('helpers/tlds.txt').splitlines()]
REGISTRY_PREFIXES = [key.lower() for key in read_included_file('helpers/windows_registry_key_prefix.txt').splitlines()]
FILE_EXTENSIONS = dict(line.lower().split(',') for line in read_included_file('helpers/mimetype_filename_extension_list.csv').splitlines())
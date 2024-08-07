import pkgutil
import re
from pathlib import Path


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

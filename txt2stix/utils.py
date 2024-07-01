import re
from pathlib import Path


def remove_data_images(input_text):
    match_re = re.compile(r"(!\[([^\]]*)\]\((data:image/\w+;\w+),([^\^)]+)\))")
    def subber(match, *args):
        return "![{}]({},blank...)".format(match.group(2), match.group(3))
    return match_re.sub(subber, input_text)

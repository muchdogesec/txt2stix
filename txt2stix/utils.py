import pkgutil
import re
from pathlib import Path
from typing import Dict

import mistune
from mistune.renderers.markdown import MarkdownRenderer
from mistune.util import unescape
class ImageLinkRemover(MarkdownRenderer):
    def __init__(self, remove_links: bool=False, remove_images: bool=False):
        self.remove_links = remove_links
        self.remove_images = remove_images
        super().__init__()

    def image(self, token: dict[str, dict], state: mistune.BlockState) -> str:
        if self.remove_images:
            return ''
        return super().image(token, state)

    def link(self, token: dict[str, dict], state: mistune.BlockState) -> str:
        if self.remove_links and token.get('type') != 'image':
            return self.render_children(token, state)
        return super().link(token, state)
    
    def codespan(self, token: dict[str, dict], state: mistune.BlockState) -> str:
        token['raw'] = unescape(token['raw'])
        return super().codespan(token, state)


def remove_links(input_text: str, remove_images: bool, remove_anchors: bool):
    modify_links = mistune.create_markdown(escape=False, renderer=ImageLinkRemover(remove_links=remove_anchors, remove_images=remove_images))
    return modify_links(input_text)

def read_included_file(path):
    try:
        return pkgutil.get_data("txt2stix.includes", path).decode()
    except:
        return (Path("includes")/path).read_text()

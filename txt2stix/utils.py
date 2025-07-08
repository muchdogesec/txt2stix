import os
import pkgutil
from pathlib import Path
from typing import Dict
from pydantic import BaseModel, Field
import bs4
import mistune
from mistune.renderers.markdown import MarkdownRenderer
from mistune.util import unescape

from txt2stix.ai_extractor.utils import AttackFlowList, DescribesIncident
class ImageLinkRemover(MarkdownRenderer):
    def __init__(self, remove_links: bool=False, remove_images: bool=False):
        self.remove_links = remove_links
        self.remove_images = remove_images
        super().__init__()

    def image(self, token: dict[str, dict], state: mistune.BlockState) -> str:
        if self.remove_images:
            token['attrs']['url'] = ''
        return super().image(token, state)

    def link(self, token: dict[str, dict], state: mistune.BlockState) -> str:
        if self.remove_links and token.get('type') != 'image':
            token['attrs']['url'] = ''
        return super().link(token, state)
    
    def codespan(self, token: dict[str, dict], state: mistune.BlockState) -> str:
        token['raw'] = unescape(token['raw'])
        return super().codespan(token, state)
    

    def block_html(self, token: Dict[str, dict], state: mistune.BlockState) -> str:
        return self.inline_html(token, state) + '\n\n'
    
    def inline_html(self, token: Dict[str, dict], state: mistune.BlockState) -> str:
        raw = token['raw']
        soup = bs4.BeautifulSoup(raw, 'html.parser')
        if self.remove_links:
            for a in soup.find_all('a'):
                del a['href']
        if self.remove_images:
            for img in soup.find_all('img'):
                del img['src']
        return soup.decode()



class Txt2StixData(BaseModel):
    content_check: DescribesIncident = Field(default=None)
    extractions: dict = Field(default=None)
    relationships: list[dict] = Field(default_factory=list)
    attack_flow: AttackFlowList = Field(default=None)


def remove_links(input_text: str, remove_images: bool, remove_anchors: bool):
    modify_links = mistune.create_markdown(escape=False, renderer=ImageLinkRemover(remove_links=remove_anchors, remove_images=remove_images))
    return modify_links(input_text)

def read_included_file(path):
    try:
        return pkgutil.get_data("txt2stix.includes", path).decode()
    except:
        return (Path("includes")/path).read_text()
    
def validate_tld(domain: str):
    _, _, suffix = domain.lower().rpartition('.')
    return suffix in TLDs

def validate_reg_key(reg_key: str):
    reg_key = reg_key.lower()
    for prefix in REGISTRY_PREFIXES:
        if reg_key.startswith(prefix):
            return True
    return False

def validate_file_mimetype(file_name):
    _, ext = os.path.splitext(file_name)
    return FILE_EXTENSIONS.get(ext)




TLDs = [tld.lower() for tld in read_included_file('helpers/tlds.txt').splitlines()]
REGISTRY_PREFIXES = [key.lower() for key in read_included_file('helpers/windows_registry_key_prefix.txt').splitlines()]
FILE_EXTENSIONS = dict(line.lower().split(',') for line in read_included_file('helpers/mimetype_filename_extension_list.csv').splitlines())
RELATIONSHIP_TYPES = [x for x in read_included_file('helpers/stix_relationship_types.txt').splitlines() if x and not x.startswith('#')]